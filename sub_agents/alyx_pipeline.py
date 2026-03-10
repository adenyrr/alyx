"""
title: Alyx
author: adenyrr
version: 0.5.0
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
import importlib
import inspect
import logging
import os
import queue
import re
import sys
import threading
import time
from datetime import datetime
from typing import Any, Awaitable, Callable, Generator

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
    "image_gen": "🎨 Illustration",
    "rag":       "📚 Documents",
    "geo":       "🗺️ Géographie",
    "reasoning": "🧩 Raisonnement",
}

# Noms courts des modèles pour la signature
_MODEL_SHORT_NAMES: dict[str, str] = {
    "openrouter/qwen3.5-flash": "Qwen-flash",
    "openrouter/deepseek":      "DeepSeek",
    "openrouter/kimi-k2.5":     "Kimi",
    "openrouter/gpt-oss":       "GPT-oss",
    "pollinations.ai":          "Pollinations",
}

# Noms courts des agents pour la signature
_AGENT_SHORT_NAMES: dict[str, str] = {
    "wikipedia":  "Wikipédia",
    "web":        "Recherche",
    "doc":        "Documentaliste",
    "dev":        "Dev",
    "media":      "Média",
    "data":       "Données",
    "memory":     "Mémoire",
    "image_gen":  "Illustration",
    "rag":        "Documents",
    "geo":        "Géographie",
    "reasoning":  "Raisonnement",
}

# Prix modèles en $/1M tokens {input, output}
_MODEL_PRICING: dict[str, dict[str, float]] = {
    "openrouter/qwen3.5-flash": {"input": 0.15,  "output": 0.60},
    "openrouter/deepseek":      {"input": 0.27,  "output": 1.10},
    "openrouter/kimi-k2.5":     {"input": 1.00,  "output": 3.00},
    "openrouter/gpt-oss":       {"input": 0.15,  "output": 0.60},
}

_LOGGER = logging.getLogger(__name__)

# Sentinel signalant la fin du stream dans le queue bridge
_DONE = object()

# Modules d'agents pour l'exécution directe des workflows séquentiels (phase 2)
# N'importe pas les modules ici — importlib.import_module est utilisé à l'exécution
# pour profiter du rechargement dynamique de _ensure_graph.
_AGENT_MODULES: dict[str, str] = {
    "wikipedia": "agents.wikipedia",
    "web":       "agents.web",
    "doc":       "agents.doc",
    "geo":       "agents.geo",
    "dev":       "agents.dev",
    "media":     "agents.media",
    "data":      "agents.data",
    "image_gen": "agents.image_gen",
    "rag":       "agents.rag_agent",
    "reasoning": "agents.reasoning",
}

_ALYX_SYSTEM_TEMPLATE = """\
Tu es Alyx, une intelligence artificielle conversationnelle multi-agents développé·e par adenyrr.
Tu n'a pas de sexe ou de genre (tu parles de toi et de l'utilisateur·rice avec un point médian : "développé·e", "conçu·e", "basé·e").
Tu t'exprimes EXCLUSIVEMENT en {language}, quelle que soit la langue de l'utilisateur·ice.

Date du jour : {current_date}

═══════════════ COMPORTEMENT ════════════════
Réponds toujours directement dans le corps final du message.
N'affiche JAMAIS de balises de raisonnement, de réflexion interne ou de pseudo-XML
comme <think>, <thinking>, <analysis>, <plan>, <synchro> ou équivalent.
Si un raisonnement interne est produit par le modèle, il est géré séparément par
le système et NE DOIT PAS apparaître dans la réponse finale.

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

══════════════ SIGNATURE ═══════════════════
NE génère PAS de ligne de signature ni de séparateur `---` en fin de réponse.
La signature est gérée automatiquement par le système.
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


def _build_pipeline_event_emitter(
    q: "queue.Queue",
    native_emitter=None,
) -> Callable[[dict[str, Any]], Awaitable[None]] | None:
    """
    Adapte l'émission d'events au runtime réel.

    - En mode fonction native OpenWebUI, on réutilise __event_emitter__.
    - En mode conteneur open-webui/pipelines, les events doivent être renvoyés
      dans le flux du pipe sous la forme {"event": {...}}.
    """
    if native_emitter:
        return native_emitter

    async def _queue_event(event: dict[str, Any]) -> None:
        q.put({"event": event})

    return _queue_event


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
        show_reasoning: bool = Field(default=False, description="Afficher le raisonnement en temps réel dans l'interface (jamais dans la réponse finale)")
        show_agent_reasoning: bool = Field(default=True, description="Afficher le raisonnement structuré des agents via les statuts OpenWebUI")
        show_model_reasoning: bool = Field(default=False, description="Afficher le reasoning_content du modèle de synthèse via les statuts OpenWebUI")
        show_perf_stats: bool = Field(default=False, description="Afficher les métriques de performance dans la signature (⏱ temps, tokens, coût estimé)")
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
        model_reasoning: str = Field(default="openrouter/deepseek", description="Modèle agent Raisonnement (sequential-thinking, analyses complexes)")

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
            "reasoning":  self.valves.model_reasoning,
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
    ) -> Generator[Any, None, None]:
        """
        Point d'entrée synchrone (Generator) exigé par le framework Pipelines.
        Toutes les opérations async s'exécutent dans le loop persistant de l'instance
        via run_coroutine_threadsafe, garantissant que les connexions psycopg restent valides.
        """
        q: queue.Queue = queue.Queue()
        runtime_event_emitter = _build_pipeline_event_emitter(q, __event_emitter__)

        # Helper : émet un statut OpenWebUI natif depuis le contexte synchrone.
        # En mode pipelines, l'event est injecté dans le flux streamé.
        def _emit(description: str, done: bool = False) -> None:
            if runtime_event_emitter and self.valves.realtime_status:
                asyncio.run_coroutine_threadsafe(
                    runtime_event_emitter({"type": "status", "data": {"description": description, "done": done}}),
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
            "event_emitter": runtime_event_emitter if self.valves.realtime_status else None,
            "show_reasoning": self.valves.show_reasoning,
            "show_agent_reasoning": self.valves.show_agent_reasoning,
            "show_model_reasoning": self.valves.show_model_reasoning,
        }}

        initial_state = {
            "messages": lc_messages,
            "images_b64": images_b64,
            "current_date": current_date,
            "routing": [],
            "routing_next": [],
            "routing_phase1": [],
            "agent_outputs": {},
            "agent_metrics": {},
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

        asyncio.run_coroutine_threadsafe(
            self._run_and_synthesize_async(
                q, graph, initial_state, config,
                runtime_event_emitter, self._models,
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

        async def _emit(description: str, done: bool = False, hidden: bool = False) -> None:
            if event_emitter and self.valves.realtime_status:
                await _emit_status(event_emitter, description, done=done, hidden=hidden)

        model_reasoning_enabled = self.valves.show_reasoning and self.valves.show_model_reasoning
        model_reasoning_buffer = ""

        async def _emit_model_reasoning(piece: str = "", final: bool = False) -> None:
            nonlocal model_reasoning_buffer
            if not (event_emitter and model_reasoning_enabled):
                return
            if piece:
                model_reasoning_buffer += piece

            should_flush = final or len(model_reasoning_buffer) >= 220 or "\n" in model_reasoning_buffer
            if not should_flush:
                return

            chunk = _compact_reasoning_text(model_reasoning_buffer)
            model_reasoning_buffer = ""
            if chunk:
                await _emit_status(event_emitter, f"💭 {chunk}", done=False, hidden=False)

        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []
        agent_metrics: dict[str, dict] = {}
        t0 = time.perf_counter()
        extra_body: dict = {} if model_reasoning_enabled else {"enable_thinking": False}
        try:
            await _emit("🧭 Routage de la demande…")
            # Exécuter le graphe
            agent_outputs, artifacts, agent_metrics = await self._run_graph(
                graph, initial_state, config, event_emitter, models=models
            )

            # ── FAST PATH image_gen seul ────────────────────────────────────────
            # Pas de synthèse LLM : on émet directement l'image Markdown.
            # Gain ~2-3 s par rapport au chemin de synthèse complet.
            if (
                set(agent_outputs.keys()) == {"image_gen"}
                and not agent_outputs.get("image_gen", "").startswith("⚠️")
            ):
                if event_emitter and len(messages) <= 2:
                    asyncio.ensure_future(_emit_chat_title(event_emitter, user_message))
                q.put(agent_outputs["image_gen"])
                elapsed = time.perf_counter() - t0
                await _emit("✅ Terminé", done=True, hidden=True)
                if self.valves.show_model_footer:
                    q.put(f"\n\n---\n*{_build_footer(self.valves.alyx_model, agent_outputs, models, agent_metrics, elapsed, self.valves.show_perf_stats)}*")
                return

            # Court-circuit : aucun agent invoqué → Alyx répond directement
            if not agent_outputs and not artifacts:
                # Titre automatique du chat à la première réponse
                if event_emitter and len(messages) <= 2:
                    asyncio.ensure_future(_emit_chat_title(event_emitter, user_message))
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
                direct_usage_out: list = []
                stream = await client.chat.completions.create(
                    model=self.valves.alyx_model,
                    messages=direct_messages,
                    temperature=self.valves.alyx_temperature,
                    stream=True,
                    stream_options={"include_usage": True},
                    extra_body=extra_body,
                )
                async for token in self._astream_response(
                    stream,
                    show_model_reasoning=model_reasoning_enabled,
                    usage_out=direct_usage_out,
                    reasoning_handler=_emit_model_reasoning if model_reasoning_enabled else None,
                ):
                    q.put(token)
                await _emit_model_reasoning(final=True)
                elapsed = time.perf_counter() - t0
                if direct_usage_out:
                    u = direct_usage_out[0]
                    agent_metrics["_synthesis"] = {
                        "prompt_tokens": getattr(u, "prompt_tokens", 0) or 0,
                        "completion_tokens": getattr(u, "completion_tokens", 0) or 0,
                        "model": self.valves.alyx_model,
                    }
                await _emit("✅ Terminé", done=True, hidden=True)
                if self.valves.show_model_footer:
                    footer = _build_footer(
                        alyx_model=self.valves.alyx_model,
                        agent_outputs={},
                        models=models,
                        agent_metrics=agent_metrics,
                        elapsed=elapsed,
                        show_perf_stats=self.valves.show_perf_stats,
                    )
                    q.put(f"\n\n---\n*{footer}*")
                return

            # Synthèse finale
            # Émettre les citations source (OpenWebUI cartes persistantes)
            if event_emitter:
                for citation in _extract_citations(agent_outputs):
                    try:
                        await event_emitter({"type": "source", "data": {
                            "document": [citation["snippet"]],
                            "metadata": [{"source": citation["url"]}],
                            "source": {"name": citation["title"], "url": citation["url"]},
                        }})
                    except Exception:
                        pass

            # Titre automatique du chat à la première réponse (avec agents)
            if event_emitter and len(messages) <= 2:
                asyncio.ensure_future(_emit_chat_title(event_emitter, user_message))

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
            synth_usage_out: list = []
            stream = await client.chat.completions.create(
                model=self.valves.alyx_model,
                messages=synth_messages,
                temperature=self.valves.alyx_temperature,
                stream=True,
                stream_options={"include_usage": True},
                extra_body=extra_body,
            )
            async for token in self._astream_response(
                stream,
                show_model_reasoning=model_reasoning_enabled,
                usage_out=synth_usage_out,
                reasoning_handler=_emit_model_reasoning if model_reasoning_enabled else None,
            ):
                q.put(token)
            await _emit_model_reasoning(final=True)
            elapsed = time.perf_counter() - t0
            if synth_usage_out:
                u = synth_usage_out[0]
                agent_metrics["_synthesis"] = {
                    "prompt_tokens": getattr(u, "prompt_tokens", 0) or 0,
                    "completion_tokens": getattr(u, "completion_tokens", 0) or 0,
                    "model": self.valves.alyx_model,
                }
            await _emit("✅ Terminé", done=True, hidden=True)

            # Pied de page
            if self.valves.show_model_footer:
                footer = _build_footer(
                    alyx_model=self.valves.alyx_model,
                    agent_outputs=agent_outputs,
                    models=models,
                    agent_metrics=agent_metrics,
                    elapsed=elapsed,
                    show_perf_stats=self.valves.show_perf_stats,
                )
                q.put(f"\n\n---\n*{footer}*")

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
    async def _astream_response(
        stream,
        show_model_reasoning: bool,
        usage_out: list | None = None,
        reasoning_handler: Callable[[str, bool], Awaitable[None]] | None = None,
    ):
        """
        Stream OpenAI async.
        - Le raisonnement (`reasoning_content` ou balises <think>) est envoyé vers
          un handler d'interface dédié, jamais concaténé au message final.
        - Le contenu final streamé vers l'utilisateur·rice reste limité au texte
          de réponse visible et persistant du pipe.
        - usage_out : si fourni, reçoit le dernier objet usage (stream_options include_usage).
        """
        buf = ""
        in_think = False
        current_think_tag = ""  # nom du tag ouvrant en cours (ex: "synchro", "think")
        # Pattern : détecte l'ouverture d'une balise de réflexion interne connue
        _OPEN_RE = re.compile(
            r"<(think(?:ing)?|synchro|inner[_\s]monologue|plan(?:[_\s]de[_\s]synth[èe]se)?)[^>]*>",
            re.IGNORECASE,
        )
        async for chunk in stream:
            # Capturer les données d'usage du dernier chunk (stream_options include_usage)
            if usage_out is not None and getattr(chunk, "usage", None):
                usage_out.clear()
                usage_out.append(chunk.usage)

            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            rc = getattr(delta, "reasoning_content", None)
            if rc is None and getattr(delta, "model_extra", None):
                rc = delta.model_extra.get("reasoning_content")
            if rc:
                if show_model_reasoning and reasoning_handler:
                    await reasoning_handler(str(rc), False)
                continue

            text = delta.content or ""
            if not text:
                continue

            buf += text
            out = ""
            while buf:
                if in_think:
                    close_tag = f"</{current_think_tag}>"
                    end = buf.lower().find(close_tag.lower())
                    if end >= 0:
                        inner = buf[:end]
                        if show_model_reasoning and reasoning_handler and inner:
                            await reasoning_handler(inner, False)
                        buf = buf[end + len(close_tag):]
                        in_think = False
                        current_think_tag = ""
                    else:
                        if show_model_reasoning and reasoning_handler and buf:
                            await reasoning_handler(buf, False)
                        buf = ""
                else:
                    m = _OPEN_RE.search(buf)
                    if m:
                        out += buf[:m.start()]
                        current_think_tag = m.group(1).lower()
                        buf = buf[m.end():]
                        in_think = True
                    else:
                        # Garder un suffixe en buffer pour les tags fragmentés entre chunks
                        # (ex: "<think" reçu, ">" arrivera dans le prochain chunk)
                        safe_split = max(0, len(buf) - 30)
                        out += buf[:safe_split]
                        buf = buf[safe_split:]
                        break
            if out:
                yield out

        if buf:
            yield buf
        if reasoning_handler:
            await reasoning_handler("", True)

    @staticmethod
    async def _run_graph(graph, initial_state: dict, config: dict, event_emitter=None, models: dict | None = None):
        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []
        agent_metrics: dict[str, dict] = {}
        pending: set[str] = set()
        routing_next: list[str] = []

        async def _emit(description: str, done: bool = False) -> None:
            if event_emitter:
                await _emit_status(event_emitter, description, done=done)

        async def _handle_agent_output(node_name: str, node_output: dict) -> None:
            """Met à jour agent_outputs/artifacts/metrics et émet notifications d'erreur."""
            icon = _AGENT_ICONS.get(node_name, node_name)
            model_name = (models or {}).get(node_name, "?")
            pending.discard(node_name)
            if pending:
                remaining_labels = "  ·  ".join(_AGENT_ICONS.get(a, a) for a in pending)
                await _emit(f"✅ {icon} terminé · En attente : {remaining_labels}")
            else:
                await _emit(f"✅ {icon} terminé ({model_name})")

            agent_outputs.update(node_output.get("agent_outputs", {}))
            artifacts.extend(node_output.get("artifacts", []))
            agent_metrics.update(node_output.get("agent_metrics", {}))

            if event_emitter:
                for _n, out_text in node_output.get("agent_outputs", {}).items():
                    if isinstance(out_text, str) and out_text.startswith(("⚠️", "⏱️")):
                        await _emit_notification(event_emitter, "warning", f"{icon} : {out_text[:120]}")

        # ── Phase 1 : exécution du graphe LangGraph ────────────────────────────
        async for event in graph.astream(initial_state, config=config, stream_mode="updates"):
            for node_name, node_output in event.items():
                if node_name == "supervisor":
                    routing = node_output.get("routing", [])
                    routing_next = node_output.get("routing_next", [])
                    if routing:
                        pending = set(routing)
                        labels = "  ·  ".join(_AGENT_ICONS.get(a, a) for a in routing)
                        if routing_next:
                            await _emit(f"Phase 1 · {labels}")
                        else:
                            await _emit(f"Invocation des agents : {labels}")
                    continue
                await _handle_agent_output(node_name, node_output)

        # ── Phase 2 : workflow séquentiel (si routing_next défini) ─────────────
        # Les agents phase 2 reçoivent agent_outputs de la phase 1 dans leur état.
        valid_next = [n for n in routing_next if n in _AGENT_MODULES]
        if valid_next:
            labels2 = "  ·  ".join(_AGENT_ICONS.get(n, n) for n in valid_next)
            await _emit(f"Phase 2 · Transmission du contexte à {labels2}")
            pending = set(valid_next)

            # Construire l'état phase 2 avec le contexte phase 1 inclus
            phase2_state = {
                **initial_state,
                "agent_outputs": dict(agent_outputs),
                "artifacts": list(artifacts),
                "routing": valid_next,
                "routing_next": [],
                "routing_phase1": [],
            }

            coros = []
            for name in valid_next:
                mod = importlib.import_module(_AGENT_MODULES[name])
                has_config = "config" in inspect.signature(mod.run).parameters
                m = (models or {}).get(name)
                if has_config:
                    coros.append((name, mod.run(phase2_state, config=config, model=m)))
                else:
                    coros.append((name, mod.run(phase2_state, model=m)))

            results = await asyncio.gather(*[c for _, c in coros], return_exceptions=True)
            for (name, _), result in zip(coros, results):
                if isinstance(result, dict):
                    await _handle_agent_output(name, result)
                else:
                    agent_outputs[name] = f"⚠️ [Erreur phase 2] {result}"

        return agent_outputs, artifacts, agent_metrics


async def _emit_event(event_emitter, event_type: str, data: dict[str, Any]) -> None:
    if not event_emitter:
        return
    try:
        await event_emitter({"type": event_type, "data": data})
    except Exception:
        pass


async def _emit_status(event_emitter, description: str, done: bool = False, hidden: bool = False) -> None:
    data: dict[str, Any] = {"description": description, "done": done}
    if hidden:
        data["hidden"] = True
    await _emit_event(event_emitter, "status", data)


async def _emit_notification(event_emitter, level: str, content: str) -> None:
    await _emit_event(event_emitter, "notification", {"type": level, "content": content})


def _compact_reasoning_text(text: str, max_len: int = 280) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= max_len:
        return compact
    return compact[: max_len - 1].rstrip() + "…"


def _strip_think_tags(text: str) -> str:
    """Supprime les blocs de réflexion interne XML des sorties d'agents.
    Gère : <think>, <thinking>, <synchro>, <inner_monologue>, <plan de synthèse>, etc.
    """
    # Balises connues (insensible à la casse, attributs possibles, espaces dans le nom)
    _KNOWN_THINK_TAGS = r"think(?:ing)?|synchro|inner[_\s]monologue|plan(?:[_\s]de[_\s]synth[èe]se)?"
    return re.sub(
        rf"<({_KNOWN_THINK_TAGS})[^>]*>.*?</\1>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    ).strip()


def _build_synthesis_context(agent_outputs: dict[str, str], artifacts: list[dict]) -> str:
    parts: list[str] = []
    for agent_name, output in agent_outputs.items():
        clean = _strip_think_tags(output) if output else ""
        if clean:
            label = _AGENT_ICONS.get(agent_name, agent_name)
            parts.append(f"## {label}\n{clean}")
    for artifact in artifacts:
        if artifact.get("type") == "image" and artifact.get("url"):
            parts.append(f"## Image générée\n![Image]({artifact['url']})")
    return "\n\n".join(parts)


def _extract_citations(agent_outputs: dict[str, str]) -> list[dict]:
    """
    Extrait les URLs depuis les sorties des agents web, doc et wikipedia.
    Retourne une liste de {url, title, snippet}, dédupliquée, max 10.
    """
    _url_pattern = re.compile(r"\[([^\]]{1,120})\]\((https?://[^\)]+)\)")
    _bare_url_pattern = re.compile(r"(?<!\()(https?://[^\s\]\)\"',]{10,})")
    seen: set[str] = set()
    results: list[dict] = []

    # Agents qui produisent des sources utiles
    for name in ("web", "wikipedia", "doc", "rag", "geo", "media"):
        text = agent_outputs.get(name, "") or ""
        if not text:
            continue

        # Liens markdown [titre](url)
        for title, url in _url_pattern.findall(text):
            url = url.rstrip(")")
            if url not in seen:
                seen.add(url)
                # snippet = phrase autour du lien (heuristique)
                idx = text.find(url)
                start = max(0, idx - 80)
                snippet = text[start:idx + len(url) + 80].strip()
                results.append({"url": url, "title": title[:100], "snippet": snippet[:300]})
                if len(results) >= 10:
                    return results

        # URLs brutes (fallback)
        for url in _bare_url_pattern.findall(text):
            url = url.rstrip(".,;:)")
            if url not in seen:
                seen.add(url)
                results.append({"url": url, "title": url[:100], "snippet": ""})
                if len(results) >= 10:
                    return results

    return results


async def _emit_chat_title(event_emitter, user_message: str) -> None:
    """Génère et émet un titre court pour le chat (premier tour uniquement)."""
    from openai import AsyncOpenAI
    try:
        client = AsyncOpenAI(
            base_url=os.environ.get("LITELLM_URL", "http://litellm:4000/v1"),
            api_key=os.environ.get("LITELLM_API_KEY", ""),
        )
        resp = await client.chat.completions.create(
            model="openrouter/qwen3.5-flash",
            messages=[
                {"role": "system", "content": "Generate a concise chat title (5 words max, in the same language as the message). Return ONLY the title, no quotes, no punctuation at end."},
                {"role": "user", "content": user_message[:300]},
            ],
            max_tokens=16,
            stream=False,
            extra_body={"enable_thinking": False},
        )
        title = resp.choices[0].message.content.strip().strip('"\'')[:60]
        if title:
            await event_emitter({"type": "chat:title", "data": {"title": title}})
    except Exception:
        pass  # Non-bloquant — le titre n'est pas critique


def _estimate_cost(agent_metrics: dict[str, dict]) -> float:
    """Retourne le coût estimé en USD pour l'ensemble des appels LLM du tour."""
    total = 0.0
    for m in agent_metrics.values():
        model = m.get("model", "")
        pricing = _MODEL_PRICING.get(model, {})
        if pricing:
            inp = m.get("prompt_tokens", 0) or 0
            out = m.get("completion_tokens", 0) or 0
            total += (inp * pricing["input"] + out * pricing["output"]) / 1_000_000
    return total


def _build_footer(
    alyx_model: str,
    agent_outputs: dict,
    models: dict | None = None,
    agent_metrics: dict | None = None,
    elapsed: float | None = None,
    show_perf_stats: bool = False,
) -> str:
    """
    Construit la signature Alyx.
    Exemples :
      "Alyx (Qwen-flash)"
      "Alyx (Qwen-flash) avec Recherche (Qwen-flash) et Dev (Kimi)"
      "Alyx (Qwen-flash) avec Recherche, Wikipédia et Dev  ·  ⏱ 4.2s  ·  ~1.2k tok  ·  ~$0.001"
    """
    alyx_short = _MODEL_SHORT_NAMES.get(alyx_model, alyx_model.split("/")[-1])
    base = f"Alyx ({alyx_short})"

    active_agents = [
        name for name in agent_outputs
        if agent_outputs.get(name, "").strip()
    ]

    if not active_agents:
        footer = base
    else:
        agent_parts: list[str] = []
        for name in active_agents:
            label = _AGENT_SHORT_NAMES.get(name, name)
            agent_model = (models or {}).get(name, "")
            short_model = _MODEL_SHORT_NAMES.get(agent_model, "")
            if short_model and short_model != alyx_short:  # n'afficher le modèle que s'il est différent d'Alyx
                agent_parts.append(f"{label} ({short_model})")
            else:
                agent_parts.append(label)

        if len(agent_parts) == 1:
            footer = f"{base} avec {agent_parts[0]}"
        elif len(agent_parts) == 2:
            footer = f"{base} avec {agent_parts[0]} et {agent_parts[1]}"
        else:
            footer = f"{base} avec {', '.join(agent_parts[:-1])} et {agent_parts[-1]}"

    if show_perf_stats and agent_metrics:
        total_in = sum(m.get("prompt_tokens", 0) or 0 for m in agent_metrics.values())
        total_out = sum(m.get("completion_tokens", 0) or 0 for m in agent_metrics.values())
        total_tok = total_in + total_out
        cost = _estimate_cost(agent_metrics)

        perf_parts: list[str] = []
        if elapsed is not None:
            perf_parts.append(f"⏱ {elapsed:.1f}s")
        if total_tok > 0:
            if total_tok >= 1000:
                perf_parts.append(f"~{total_tok / 1000:.1f}k tok")
            else:
                perf_parts.append(f"~{total_tok} tok")
        if cost > 0.0:
            perf_parts.append(f"~${cost:.4f}")
        if perf_parts:
            footer += "  ·  " + "  ·  ".join(perf_parts)

    return footer
