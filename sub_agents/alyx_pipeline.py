"""
title: Alyx
author: adenyrr
version: 0.4.0
requirements: langgraph>=0.2, langchain-core>=0.3, langchain-openai>=0.2, langgraph-checkpoint-postgres, psycopg[pool], httpx>=0.27, mcp, openai>=1.0, pydantic>=2.0
"""

"""
Alyx Pipeline — point d'entrée OpenWebUI Pipelines.

Alyx est un agent conversationnel en français orchestrant 10 sous-agents spécialisés
via un graphe LangGraph. Elle n'a accès à aucun outil directement (contexte allégé).
Les sous-agents travaillent en anglais et lui remontent leurs conclusions.

Flux d'un message :
  1. Extraction des images base64 du body OpenWebUI
  2. Exécution du graphe LangGraph (supervisor → agents sélectionnés)
  3. Synthèse finale streamée par Alyx en français
  4. Condensation mémoire en arrière-plan (fire-and-forget)
"""

import asyncio
import logging
import os
import queue
import sys
import threading
from datetime import datetime
from typing import Generator

# Garantit que graph/, agents/, tools/ sont importables depuis /app/pipelines/
_PIPELINES_DIR = os.path.dirname(os.path.abspath(__file__))
if _PIPELINES_DIR not in sys.path:
    sys.path.insert(0, _PIPELINES_DIR)

# Pydantic est nécessaire à la définition de Valves (module level).
# On l'importe avec un fallback pour garantir que le module charge
# même avant que les requirements soient installés.
try:
    from pydantic import BaseModel, Field
except ImportError:  # premier chargement, avant install des deps
    BaseModel = object  # type: ignore[assignment,misc]
    def Field(default=None, **_kwargs):  # type: ignore[misc]
        return default

# Valeurs d'environnement — servent de défauts pour les Valves
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_DB_URL = os.environ.get("DATABASE_URL", "")

# Icônes et libellés de statut par agent
_AGENT_ICONS = {
    "wikipedia": "📖 Wikipédia",
    "web":       "🌐 Recherche",
    "doc":       "🔬 Documentaliste",
    "dev":       "⚙️ Dev",
    "media":     "🎬 Média",
    "data":      "📊 Données",
    "memory":    "🧠 Mémoire",
    "image_gen": "🎨 ImageGen",
    "rag":       "📚 Documents",
    "geo":       "🗺️ Géographie",
}

_LOGGER = logging.getLogger(__name__)

# Sentinel signalant la fin du stream dans le queue bridge
_DONE = object()

_ALYX_SYSTEM_TEMPLATE = """\
Tu es Alyx, une intelligence artificielle conversationnelle multi-agents développé.e par adenyrr.
Tu n'es ni masculin·e ni féminin·e — toujours neutre (point médian : "développé·e", "conçu·e", "basé·e").
Tu t'exprimes EXCLUSIVEMENT en {language}, quelle que soit la langue de l'utilisateur·ice.

Date du jour : {current_date}

═══════════════ COMPORTEMENT ════════════════
Tu utilises TOUJOURS des balises <think>…</think> pour raisonner AVANT de répondre.
Dans ces balises, inclus :
  - Ton analyse de la demande
  - Les résultats bruts des agents invoqués (tels quels)
  - Ton plan de synthèse
La réponse finale arrive APRÈS la fermeture </think>, hors des balises.

RÈGLE ABSOLUE — Réponses directes et complètes :
  - Les agents ont DÉJÀ terminé. Leurs résultats sont dans ce prompt.
  - Si des résultats agents sont fournis → synthétise-les IMMÉDIATEMENT.
  - Si les résultats sont vides ou insuffisants → réponds sur tes connaissances
    en précisant que les données fraîches peuvent nécessiter une vérification en ligne.
  - INTERDIT : "Je vais chercher", "Je sollicite un agent", "Je reviens dès que",
    "en cours de récupération", "je lance une recherche", ou tout texte promettant
    un résultat futur. Tout est déjà là.

═════════════ ARTIFACTS ═════════════
L'agent DEV est le SEUL producteur d'artifacts (blocs ```html, ```javascript, ```python).
Alyx synthétise et présente ; elle ne code PAS.
Si un agent a fourni un bloc de code, REPRODUIS-LE INTÉGRALEMENT, sans le modifier.
Ne paraphrase jamais un artifact.
Si une image a été générée (lien markdown ![...](url)), inclus le lien tel quel.

═════════════ VISION ═════════════
Tu as des capacités natives de vision. Si des images t'ont été transmises,
analyse-les directement sans mentionner d'agent ou de processus interne.

══════════════ SOURCES (OBLIGATOIRE) ═══════════════
À la fin de chaque réponse (hors balises <think>) :
  - Cite toutes les sources avec des liens Markdown : [Titre](url)
  - Pour les articles académiques : auteurs, titre, journal, année, DOI
  - Format : > 📖 [Auteurs (année) — *Titre*](url)
  - Reprends fidèlement les sources fournies par les agents.

══════════════ SIGNATURE (OBLIGATOIRE) ═════════════
Termine TOUJOURS par une ligne de signature :
  ---
  *🤖 Alyx `{alyx_model}` · [Agent Nomᵢ `modèle_i`] · ...*
"""


def _convert_messages(messages: list[dict]) -> list:
    """Convertit le format OpenWebUI en messages LangChain."""
    from langchain_core.messages import HumanMessage, AIMessage  # lazy
    lc_messages = []
    for m in messages:
        role = m.get("role", "")
        content = m.get("content", "")
        if isinstance(content, list):
            # Garder uniquement le texte pour l'historique (les images sont dans images_b64)
            content = " ".join(
                part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text"
            )
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
    return lc_messages


def _extract_images_b64(messages: list[dict]) -> list[str]:
    """Extrait les images base64 du dernier message utilisateur."""
    images: list[str] = []
    for m in reversed(messages):
        if m.get("role") != "user":
            continue
        content = m.get("content", "")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:"):
                        # Extraire la partie base64 après la virgule
                        b64 = url.split(",", 1)[-1]
                        images.append(b64)
        break
    return images


class Pipeline:
    class Valves(BaseModel):
        # --- Connexion ---
        litellm_url: str = Field(default=_LITELLM_URL, description="LiteLLM API URL")
        litellm_api_key: str = Field(default=_LITELLM_API_KEY, description="LiteLLM API key")
        db_url: str = Field(default=_DB_URL, description="PostgreSQL connection string (LangGraph checkpoint)")

        # --- Alyx (synthèse finale) ---
        alyx_model: str = Field(default="openrouter/qwen3.5-flash", description="Modèle de synthèse finale d'Alyx")
        alyx_temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Température de synthèse Alyx")
        language: str = Field(default="français", description="Langue des réponses d'Alyx (ex: français, english, español)")
        history_messages: int = Field(default=12, ge=2, le=40, description="Nombre de messages d'historique envoyés à Alyx")

        # --- Comportement ---
        stream_agent_status: bool = Field(default=True, description="Streamer une ligne de statut avant la réponse (agents invoqués)")
        show_model_footer: bool = Field(default=True, description="Afficher un pied de page (modèle + agents) en fin de réponse")
        show_reasoning: bool = Field(default=True, description="Afficher le raisonnement interne (balises <think> ou champ reasoning_content)")
        realtime_status: bool = Field(default=True, description="Émettre des statuts OpenWebUI en temps réel (quel agent travaille)")
        enable_memory_bg: bool = Field(default=True, description="Activer la condensation mémoire en arrière-plan")

        # --- Superviseur ---
        supervisor_model: str = Field(default="openrouter/qwen3.5-flash", description="Modèle du superviseur (routage)")

        # --- Modèles agents ---
        model_wikipedia: str = Field(default="openrouter/qwen3.5-flash", description="Modèle agent Wikipédia")
        model_web: str = Field(default="openrouter/qwen3.5-flash", description="Modèle agent Recherche web (DuckDuckGo + Playwright fallback)")
        model_doc: str = Field(default="openrouter/deepseek", description="Modèle agent Documentaliste (publications scientifiques + Sci-hub)")
        model_dev: str = Field(default="openrouter/kimi-k2.5", description="Modèle agent Dev (code + artifacts)")
        model_media: str = Field(default="openrouter/gpt-oss", description="Modèle agent Média (YouTube, documents)")
        model_data: str = Field(default="openrouter/deepseek", description="Modèle agent Données (calculs, SQL, Yahoo Finance)")
        model_geo: str = Field(default="openrouter/qwen3.5-flash", description="Modèle agent Géographie (météo OpenMeteo, OSM)")
        model_memory: str = Field(default="openrouter/gpt-oss", description="Modèle agent Mémoire (knowledge graph)")
        model_rag: str = Field(default="openrouter/gpt-oss", description="Modèle agent Documents (RAG Qdrant)")

        # --- Génération d'images (Pollinations.ai — appel direct GET, sans passer par LiteLLM) ---
        enable_image_gen: bool = Field(default=True, description="Activer la génération d'images via Pollinations.ai")
        pollinations_api_key: str = Field(default="", description="Clé API Pollinations.ai (optionnelle — gratuit sans clé pour les modèles de base)")
        pollinations_model: str = Field(default="flux", description="Modèle Pollinations : flux, zimage, gptimage, klein-large, imagen-4, seedream5, nanobanana, grok-imagine…")
        pollinations_width: int = Field(default=1024, ge=64, le=4096, description="Largeur de l'image générée (pixels)")
        pollinations_height: int = Field(default=1024, ge=64, le=4096, description="Hauteur de l'image générée (pixels)")
        pollinations_enhance: bool = Field(default=True, description="Amélioration IA du prompt par Pollinations avant génération")

    def __init__(self):
        self.name = "Alyx"
        self.valves = self.Valves()
        self._graph = None
        self._pool = None
        self._models: dict = {}
        # Loop persistant dans un thread dédié — toutes les ops async partagent le même loop
        # pour que les connexions psycopg (liées à leur loop) restent valides.
        self._loop = asyncio.new_event_loop()
        threading.Thread(
            target=self._loop.run_forever,
            daemon=True,
            name="alyx-async",
        ).start()

    async def on_valves_updated(self):
        """Invalide le graphe pour forcer un rebuild avec les nouveaux paramètres.

        Déclarée async car OpenWebUI appelle cette méthode avec await.
        La fermeture du pool postgres est déléguée au loop persistant.
        """
        old_pool = self._pool
        self._graph = None
        self._pool = None
        self._models = {}
        if old_pool is not None:
            asyncio.run_coroutine_threadsafe(old_pool.close(), self._loop)

    def _run_sync(self, coro, timeout: int = 300):
        """Exécute une coroutine dans le loop persistant depuis un thread synchrone."""
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout=timeout)

    def _ensure_graph(self):
        """Initialise le graphe LangGraph une fois (lazy).

        On purge graph.builder (et les agents/tools) du cache sys.modules avant
        chaque (re-)build, pour que les modifications sur disque soient toujours
        prises en compte sans redémarrer le container.
        """
        if self._graph is not None:
            return self._graph

        # Invalider le cache des sous-modules Alyx pour forcer une relecture disque
        _submodule_prefixes = ("graph.", "agents.", "tools.")
        for key in list(sys.modules):
            if any(key == p.rstrip(".") or key.startswith(p) for p in _submodule_prefixes):
                del sys.modules[key]

        from graph.builder import build_graph
        models = {
            "supervisor": self.valves.supervisor_model,
            "wikipedia":  self.valves.model_wikipedia,
            "web":        self.valves.model_web,
            "doc":        self.valves.model_doc,
            "dev":        self.valves.model_dev,
            "media":      self.valves.model_media,
            "data":       self.valves.model_data,
            "geo":        self.valves.model_geo,
            "memory":     self.valves.model_memory,
            "image_gen":  "pollinations.ai",
            "rag":        self.valves.model_rag,
            # Paramètres Pollinations transmis aux agents via le dict models
            "_pollinations": {
                "enable":  self.valves.enable_image_gen,
                "api_key": self.valves.pollinations_api_key,
                "model":   self.valves.pollinations_model,
                "width":   self.valves.pollinations_width,
                "height":  self.valves.pollinations_height,
                "enhance": self.valves.pollinations_enhance,
            },
        }
        self._graph, self._pool = self._run_sync(build_graph(self.valves.db_url, models))
        self._models = models
        return self._graph

    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: list[dict],
        body: dict,
        __event_emitter__=None,
    ) -> Generator[str, None, None]:
        """
        Point d'entrée synchrone (Generator) exigé par le framework Pipelines.
        Toutes les opérations async s'exécutent dans le loop persistant de l'instance
        via run_coroutine_threadsafe, garantissant que les connexions psycopg restent valides.
        """
        # Helper : émet un statut OpenWebUI natif depuis le contexte synchrone.
        # done=True efface le spinner ; done=False affiche le spinner.
        def _emit(description: str, done: bool = False) -> None:
            if __event_emitter__ and self.valves.realtime_status:
                asyncio.run_coroutine_threadsafe(
                    __event_emitter__({"type": "status", "data": {"description": description, "done": done}}),
                    self._loop,
                )

        _emit("🔍 Analyse du message…")

        # 1. Préparer l'état initial
        lc_messages = _convert_messages(messages)
        images_b64 = _extract_images_b64(messages)

        # Date courante injectée dans l'état — lisible par tous les agents
        current_date = datetime.now().strftime("%A %d %B %Y").lower()

        chat_id = body.get("chat_id", body.get("session_id", "default"))
        config = {"configurable": {
            "thread_id": chat_id,
            "event_emitter": __event_emitter__ if self.valves.realtime_status else None,
        }}

        initial_state = {
            "messages": lc_messages,
            "images_b64": images_b64,
            "current_date": current_date,
            "routing": [],
            "agent_outputs": {},
            "artifacts": [],
            "_pollinations": {
                "enable":  self.valves.enable_image_gen,
                "api_key": self.valves.pollinations_api_key,
                "model":   self.valves.pollinations_model,
                "width":   self.valves.pollinations_width,
                "height":  self.valves.pollinations_height,
                "enhance": self.valves.pollinations_enhance,
            },
        }

        # 2. Lancer la coroutine graphe+synthèse et lire les tokens depuis la queue
        try:
            graph = self._ensure_graph()
        except Exception as exc:
            _emit("Erreur d'initialisation", done=True)
            yield f"[Erreur d'initialisation du graphe : {exc}]"
            return

        q: queue.Queue = queue.Queue()
        asyncio.run_coroutine_threadsafe(
            self._run_and_synthesize_async(
                q, graph, initial_state, config,
                __event_emitter__, self._models,
                messages, lc_messages, images_b64, user_message,
            ),
            self._loop,
        )

        while True:
            token = q.get()
            if token is _DONE:
                break
            yield token

    async def _run_and_synthesize_async(
        self,
        q: "queue.Queue",
        graph,
        initial_state: dict,
        config: dict,
        event_emitter,
        models: dict,
        messages: list[dict],
        lc_messages: list,
        images_b64: list[str],
        user_message: str,
    ) -> None:
        """Coroutine unique : graphe → synthèse → tokens dans la queue."""
        from openai import AsyncOpenAI  # lazy

        async def _emit(description: str, done: bool = False) -> None:
            if event_emitter and self.valves.realtime_status:
                try:
                    await event_emitter({"type": "status", "data": {"description": description, "done": done}})
                except Exception:
                    pass

        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []
        try:
            # Exécuter le graphe
            agent_outputs, artifacts = await self._run_graph(
                graph, initial_state, config, event_emitter, models=models
            )

            # Court-circuit : aucun agent invoqué → Alyx répond directement
            if not agent_outputs and not artifacts:
                await _emit("✍️ Réponse directe…")
                alyx_system = _ALYX_SYSTEM_TEMPLATE.format(
                    current_date=datetime.now().strftime("%A %d %B %Y"),
                    language=self.valves.language,
                    alyx_model=self.valves.alyx_model,
                )
                direct_messages = [{"role": "system", "content": alyx_system}]
                for m in messages[-self.valves.history_messages:]:
                    r = m.get("role", "user")
                    c = m.get("content", "")
                    # Dernier message utilisateur : attacher les images pour vision native
                    if r == "user" and images_b64 and m is messages[-1]:
                        content_parts = [{"type": "text", "text": c if isinstance(c, str) else ""}]
                        for b64 in images_b64[:4]:
                            content_parts.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
                        direct_messages.append({"role": r, "content": content_parts})
                    else:
                        direct_messages.append({"role": r, "content": c if isinstance(c, str) else ""})
                client = AsyncOpenAI(base_url=self.valves.litellm_url, api_key=self.valves.litellm_api_key)
                stream = await client.chat.completions.create(
                    model=self.valves.alyx_model,
                    messages=direct_messages,
                    temperature=self.valves.alyx_temperature,
                    stream=True,
                )
                async for token in self._astream_response(stream, self.valves.show_reasoning):
                    q.put(token)
                await _emit("", done=True)
                if self.valves.show_model_footer:
                    q.put(f"\n\n---\n*🤖 Alyx `{self.valves.alyx_model}`*")
                return

            # Ligne de statut agents (optionnelle)
            if self.valves.stream_agent_status and agent_outputs:
                labels = " · ".join(
                    _AGENT_ICONS.get(name, name)
                    for name in agent_outputs
                    if agent_outputs[name] and agent_outputs[name].strip()
                )
                if labels:
                    q.put(f"> *Agents invoqués : {labels}*\n\n")

            # Synthèse finale
            await _emit("✍️ Rédaction de la réponse…")
            synthesis_context = _build_synthesis_context(agent_outputs, artifacts)
            synth_messages = [{"role": "system", "content": _ALYX_SYSTEM_TEMPLATE.format(
                current_date=datetime.now().strftime("%A %d %B %Y"),
                language=self.valves.language,
                alyx_model=self.valves.alyx_model,
            )}]
            for m in messages[-self.valves.history_messages:]:
                r = m.get("role", "user")
                c = m.get("content", "")
                synth_messages.append({"role": r, "content": c if isinstance(c, str) else ""})

            # Message de synthèse avec résultats agents + vision native si images présentes
            agent_context_msg = (
                f"[Résultats des agents spécialisés]\n{synthesis_context}\n\n"
                f"[Message original de l'utilisateur·rice]\n{user_message}"
            )
            if images_b64:
                img_parts: list = [{"type": "text", "text": agent_context_msg}]
                for b64 in images_b64[:4]:
                    img_parts.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
                synth_messages.append({"role": "user", "content": img_parts})
            else:
                synth_messages.append({"role": "user", "content": agent_context_msg})

            client = AsyncOpenAI(base_url=self.valves.litellm_url, api_key=self.valves.litellm_api_key)
            stream = await client.chat.completions.create(
                model=self.valves.alyx_model,
                messages=synth_messages,
                temperature=self.valves.alyx_temperature,
                stream=True,
            )
            async for token in self._astream_response(stream, self.valves.show_reasoning):
                q.put(token)
            await _emit("", done=True)

            # Pied de page
            if self.valves.show_model_footer:
                _agent_models = {
                    "wikipedia": self.valves.model_wikipedia,
                    "web":       self.valves.model_web,
                    "doc":       self.valves.model_doc,
                    "dev":       self.valves.model_dev,
                    "media":     self.valves.model_media,
                    "data":      self.valves.model_data,
                    "geo":       self.valves.model_geo,
                    "memory":    self.valves.model_memory,
                    "image_gen": "pollinations.ai",
                    "rag":       self.valves.model_rag,
                }
                agent_parts = [
                    f"{_AGENT_ICONS.get(name, name)} `{_agent_models.get(name, '?')}`"
                    for name in agent_outputs
                    if agent_outputs[name] and agent_outputs[name].strip()
                ]
                synth_part = f"🤖 Alyx `{self.valves.alyx_model}`"
                if agent_parts:
                    footer = "\n\n---\n*" + "  ·  ".join(agent_parts) + "  ·  " + synth_part + "*"
                else:
                    footer = f"\n\n---\n*{synth_part}*"
                q.put(footer)

        except Exception as exc:
            await _emit("Erreur lors de l'exécution", done=True)
            q.put(f"[Erreur : {exc}]")
        finally:
            # Condensation mémoire en arrière-plan (fire-and-forget dans le même loop)
            if self.valves.enable_memory_bg:
                try:
                    import agents.memory_agent as memory_mod
                    from langchain_core.messages import HumanMessage
                    final_state = {
                        "messages": lc_messages + [HumanMessage(content=user_message)],
                        "images_b64": images_b64,
                        "routing": [],
                        "agent_outputs": agent_outputs,
                        "artifacts": artifacts,
                    }
                    asyncio.ensure_future(
                        memory_mod.run_bg(final_state, model=self.valves.model_memory)
                    )
                except Exception as exc:
                    _LOGGER.warning("Failed to schedule memory background task: %s", exc)
            q.put(_DONE)

    @staticmethod
    def _stream_response(stream, show_reasoning: bool) -> "Generator[str, None, None]":
        """
        Wrapper de stream OpenAI synchrone.
        - Balises <think>…</think> : passées TELLES QUELLES (rendu natif OpenWebUI).
        - Champ delta.reasoning_content : converti en blockquote si show_reasoning=True.
        """
        reasoning_parts: list[str] = []

        def _flush_reasoning() -> str:
            block = "".join(reasoning_parts).strip()
            reasoning_parts.clear()
            if not block or not show_reasoning:
                return ""
            lines = block.splitlines()
            out = "> 💭 **Raisonnement**\n>\n"
            out += "\n".join(f"> {ln}" for ln in lines)
            out += "\n\n"
            return out

        buf = ""
        in_think = False
        for chunk in stream:
            delta = chunk.choices[0].delta

            rc = getattr(delta, "reasoning_content", None)
            if rc is None and getattr(delta, "model_extra", None):
                rc = delta.model_extra.get("reasoning_content")
            if rc:
                reasoning_parts.append(rc)
                continue

            text = delta.content or ""
            if not text:
                continue

            buf += text
            out = ""
            while buf:
                if in_think:
                    end = buf.find("</think>")
                    if end >= 0:
                        out += buf[:end] + "</think>"
                        buf = buf[end + len("</think>"):]
                        in_think = False
                        reasoning_parts.clear()
                    else:
                        out += buf
                        buf = ""
                else:
                    start = buf.find("<think>")
                    if start >= 0:
                        out += buf[:start] + "<think>"
                        buf = buf[start + len("<think>"):]
                        in_think = True
                    else:
                        out += buf
                        buf = ""
            if out:
                yield out

        if buf:
            yield buf
        if reasoning_parts:
            flushed = _flush_reasoning()
            if flushed:
                yield flushed

    @staticmethod
    async def _astream_response(stream, show_reasoning: bool):
        """
        Stream OpenAI async.
        - Balises <think>…</think> passées TELLES QUELLES dans le stream
          (rendu natif OpenWebUI — affiche le raisonnement en temps réel).
        - Champ reasoning_content (delta, modèles o-series) : converti en blockquote
          si show_reasoning=True, supprimé sinon.
        """
        reasoning_parts: list[str] = []

        def _flush_reasoning() -> str:
            block = "".join(reasoning_parts).strip()
            reasoning_parts.clear()
            if not block or not show_reasoning:
                return ""
            lines = block.splitlines()
            out = "> 💭 **Raisonnement**\n>\n"
            out += "\n".join(f"> {ln}" for ln in lines)
            out += "\n\n"
            return out

        buf = ""
        in_think = False
        async for chunk in stream:
            delta = chunk.choices[0].delta

            rc = getattr(delta, "reasoning_content", None)
            if rc is None and getattr(delta, "model_extra", None):
                rc = delta.model_extra.get("reasoning_content")
            if rc:
                reasoning_parts.append(rc)
                continue

            text = delta.content or ""
            if not text:
                continue

            buf += text
            out = ""
            while buf:
                if in_think:
                    end = buf.find("</think>")
                    if end >= 0:
                        out += buf[:end] + "</think>"
                        buf = buf[end + len("</think>"):]
                        in_think = False
                        reasoning_parts.clear()
                    else:
                        out += buf
                        buf = ""
                else:
                    start = buf.find("<think>")
                    if start >= 0:
                        out += buf[:start] + "<think>"
                        buf = buf[start + len("<think>"):]
                        in_think = True
                    else:
                        out += buf
                        buf = ""
            if out:
                yield out

        if buf:
            yield buf
        if reasoning_parts:
            flushed = _flush_reasoning()
            if flushed:
                yield flushed

    @staticmethod
    async def _run_graph(graph, initial_state: dict, config: dict, event_emitter=None, models: dict | None = None):
        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []
        pending: set[str] = set()

        async def _emit(description: str, done: bool = False) -> None:
            if event_emitter:
                try:
                    await event_emitter({"type": "status", "data": {"description": description, "done": done}})
                except Exception:
                    pass

        async for event in graph.astream(initial_state, config=config, stream_mode="updates"):
            for node_name, node_output in event.items():
                if node_name == "supervisor":
                    routing = node_output.get("routing", [])
                    if routing:
                        pending = set(routing)
                        labels = "  ·  ".join(_AGENT_ICONS.get(a, a) for a in routing)
                        await _emit(f"Invocation des agents : {labels}")
                    continue

                icon = _AGENT_ICONS.get(node_name, node_name)
                model_name = (models or {}).get(node_name, "?")
                pending.discard(node_name)
                if pending:
                    remaining_labels = "  ·  ".join(_AGENT_ICONS.get(a, a) for a in pending)
                    await _emit(f"✅ {icon} — en cours : {remaining_labels}")
                else:
                    await _emit(f"✅ {icon} ({model_name})")

                agent_outputs.update(node_output.get("agent_outputs", {}))
                artifacts.extend(node_output.get("artifacts", []))

        return agent_outputs, artifacts


def _build_synthesis_context(agent_outputs: dict[str, str], artifacts: list[dict]) -> str:
    parts: list[str] = []
    for agent_name, output in agent_outputs.items():
        if output and output.strip():
            label = _AGENT_ICONS.get(agent_name, agent_name)
            parts.append(f"## {label}\n{output}")
    for artifact in artifacts:
        if artifact.get("type") == "image" and artifact.get("url"):
            parts.append(f"## Image générée\n![Image]({artifact['url']})")
    return "\n\n".join(parts)
