"""
title: Alyx
author: adenyrr
version: 0.8.0
requirements: langgraph>=0.2, langchain-core>=0.3, langchain-openai>=0.2, langgraph-checkpoint-postgres, psycopg[pool], httpx>=0.27, mcp, redis>=5.0, pypandoc-binary>=1.13, openpyxl>=3.1, openai>=1.0, pydantic>=2.0
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
import base64
import importlib
import inspect
import json
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
_WEBUI_URL = os.environ.get("WEBUI_URL", "http://open-webui:8080")
_WEBUI_API_KEY = os.environ.get("WEBUI_API_KEY", "")
_REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/2")

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
    "reasoning":    "🧩 Raisonnement",
    "writer":       "✍️ Rédaction",
    "presenter":    "🎞️ Présentation",
    "translator":   "🌍 Traduction",
    "summarizer":   "📰 Résumé",
    "vision":       "👁️ Vision",
    "mindmap":      "🗺️ Mindmap",
    "diagram":      "📐 Diagramme",
    "spreadsheet":  "📊 Tableur",
    "code_exec":    "🐍 Exécution code",
    "fact_checker": "🔬 Fact-checker",
    "audio":        "🎙️ Audio",
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
    "reasoning":    "Raisonnement",
    "writer":       "Rédaction",
    "presenter":    "Présentation",
    "translator":   "Traduction",
    "summarizer":   "Résumé",
    "vision":       "Vision",
    "mindmap":      "Mindmap",
    "diagram":      "Diagramme",
    "spreadsheet":  "Tableur",
    "code_exec":    "Exécution code",
    "fact_checker": "Fact-checker",
    "audio":        "Audio",
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
    "rag":          "agents.rag_agent",
    "reasoning":    "agents.reasoning",
    "writer":       "agents.writer",
    "presenter":    "agents.presenter",
    "translator":   "agents.translator",
    "summarizer":   "agents.summarizer",
    "vision":       "agents.vision",
    "mindmap":      "agents.mindmap",
    "diagram":      "agents.diagram",
    "spreadsheet":  "agents.spreadsheet",
    "code_exec":    "agents.code_exec",
    "fact_checker": "agents.fact_checker",
    "audio":        "agents.audio",
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

═════════════ ARTIFACTS & DOCUMENTS ═════════════
L'agent DEV est le SEUL producteur d'artifacts (blocs ```html, ```javascript, ```python).
L'agent WRITER est le SEUL producteur de documents structurés longue forme (rapports,
CV, lettres, emails, presse, etc.) — il peut joindre un lien data-URI pour téléchargement
au format demandé (DOCX/EPUB/TEX/HTML/RTF/ODT).

Règles strictes de pass-through :
  - Si un agent a fourni un bloc de code, REPRODUIS-LE INTÉGRALEMENT.
  - Si l'agent writer a fourni un document, REPRODUIS son contenu structuré
    (titres, sections, tableaux). Conserve sa note finale du type « 📎 Document
    xxx.docx généré … lien de téléchargement ci-dessous » : le lien réel est ajouté
    AUTOMATIQUEMENT par le système après ta réponse. Tu n'as RIEN à faire pour le lien.
  - Si une image a été générée (lien markdown ![...](url)), inclus le lien tel quel.
  - Si un agent a fourni des données factuelles (résumés doc, web, wikipedia…), tu peux
    les synthétiser librement — sauf si l'utilisateur·rice demandait un DOCUMENT
    (rapport/lettre/email/CV/…), auquel cas restitue la sortie writer.

INTERDICTION ABSOLUE de générer ces phrases (ou leurs paraphrases) :
  ✗ "Je ne peux pas générer directement un fichier DOCX/PPTX/PDF/EPUB/..."
  ✗ "I cannot create binary files like Microsoft Word/PowerPoint..."
  ✗ "Voici un modèle/du texte que tu pourras copier dans Word/PowerPoint..."
  ✗ "Utilise un convertisseur en ligne / Pandoc pour transformer..."
  ✗ "Je t'envoie le texte brut optimisé pour Word/PowerPoint"
  ✗ "Voici un format reveal.js (HTML) à la place du PPTX demandé"
     (si presenter ET writer ont tourné, les DEUX livrables sont là — décris-les
     ensemble, ne te justifie pas de l'un par rapport à l'autre).

INTERDICTION ABSOLUE de FABRIQUER un lien `data:` (data-URI) :
  ✗ Ne JAMAIS inventer une chaîne base64 ni écrire `data:...;base64,...` toi-même.
  ✗ Le lien de téléchargement réel est généré par le SYSTÈME à partir du fichier
    produit par l'agent writer, et ajouté après ta réponse. Tu ne dois jamais
    produire de data-URI : ce serait un faux fichier corrompu.
  ✗ Si l'utilisateur·rice a demandé un fichier mais qu'aucun document n'a été produit
    (writer non déclenché), indique honnêtement : « Le format demandé n'a pas été
    produit cette fois — relance en précisant explicitement le format (.docx, .epub,
    .tex…) pour activer l'agent rédaction. »

La conversion vers DOCX/PPTX/EPUB/TEX/ODT/RTF/HTML est gérée EXCLUSIVEMENT par
l'agent WRITER en aval via le serveur pandoc, et le lien est injecté par le système.
PDF n'est pas géré (LaTeX non installé) — si demandé, suggère un autre format.

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


def _extract_owui_context(body: dict) -> dict[str, Any]:
    """
    Extrait du body OpenWebUI le contexte d'autorisation nécessaire à l'isolation
    multi-tenant du RAG (Qdrant multitenancy).

    Le serveur OpenWebUI a déjà validé que l'utilisateur·rice a accès aux
    ressources listées dans `body["files"]` — la pipeline s'appuie sur cette
    liste pour restreindre les recherches Qdrant aux seules bases attachées
    à la conversation. Cf. open-webui/backend/retrieval/vector/dbs/qdrant_multitenancy.py.

    Returns:
        {"user_id": str, "chat_id": str, "knowledge_ids": list[str], "file_ids": list[str]}
    """
    user = body.get("user") if isinstance(body, dict) else None
    user_id = ""
    if isinstance(user, dict):
        user_id = str(user.get("id") or "")

    chat_id = ""
    if isinstance(body, dict):
        chat_id = str(body.get("chat_id") or body.get("session_id") or "")

    raw = body.get("files") if isinstance(body, dict) else None
    if not raw:
        meta = body.get("metadata") if isinstance(body, dict) else None
        if isinstance(meta, dict):
            raw = meta.get("files")
    if not isinstance(raw, list):
        raw = []

    knowledge_ids: list[str] = []
    file_ids: list[str] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        t = str(item.get("type") or "").lower()
        ident = item.get("id") or item.get("collection_id") or item.get("file_id")
        if not ident:
            inner = item.get("collection") or item.get("file")
            if isinstance(inner, dict):
                ident = inner.get("id")
        if not ident:
            continue
        ident = str(ident)
        if t in ("collection", "knowledge"):
            knowledge_ids.append(ident)
        elif t == "file":
            file_ids.append(ident)

    return {
        "user_id": user_id,
        "chat_id": chat_id,
        "knowledge_ids": knowledge_ids,
        "file_ids": file_ids,
    }


def _coalesce(override, default):
    """Retourne `override` s'il est défini (non None et non chaîne vide), sinon `default`."""
    if override is None:
        return default
    if isinstance(override, str) and override == "":
        return default
    return override


def _extract_user_valves(body: dict) -> dict[str, Any]:
    """Extrait les surcharges UserValves transmises par Open WebUI dans le body.

    Open WebUI place les valves utilisateur dans body["user"]["valves"] (mode
    natif). En mode Pipelines externe ce champ peut être absent → dict vide,
    auquel cas les valves globales prévalent intégralement.
    """
    if not isinstance(body, dict):
        return {}
    user = body.get("user")
    if not isinstance(user, dict):
        return {}
    valves = user.get("valves")
    if not isinstance(valves, dict):
        return {}
    return valves


def _extract_audios_b64(messages: list[dict]) -> list[str]:
    """Extrait les fichiers audio base64 du dernier message utilisateur.

    Open WebUI peut transmettre des audio sous deux formes :
      - dans un block `audio_url` (similaire à image_url) → data:audio/*;base64,…
      - dans `files` (uploaded file) — non géré ici, à transiter via le RAG / media
    On capte uniquement le premier format (audio inline).
    """
    audios: list[str] = []
    for m in reversed(messages or []):
        if m.get("role") != "user":
            continue
        content = m.get("content", "")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    # audio_url ou input_audio (variations de schéma)
                    url = ""
                    if part.get("type") == "audio_url":
                        url = part.get("audio_url", {}).get("url", "")
                    elif part.get("type") == "input_audio":
                        data = part.get("input_audio", {}).get("data", "")
                        if data:
                            audios.append(data)
                            continue
                    if url.startswith("data:audio"):
                        b64 = url.split(",", 1)[-1]
                        audios.append(b64)
        break
    return audios


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


def _build_pipeline_reasoning_emitter(
    q: "queue.Queue",
    model_name: str,
) -> Callable[[str, bool], Awaitable[None]]:
    """Émet du raisonnement via des chunks de contenu encapsulés dans `<think>...</think>`."""

    is_open = False

    def _push_content(content: str) -> None:
        q.put({
            "id": f"alyx-reasoning-{time.time_ns()}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model_name,
            "choices": [{
                "index": 0,
                "delta": {"content": content},
                "finish_reason": None,
            }],
        })

    async def _queue_reasoning(text: str, final: bool = False) -> None:
        nonlocal is_open
        if text:
            if not is_open:
                _push_content("<think>")
                is_open = True
            _push_content(text)
        if final and is_open:
            _push_content("</think>")
            is_open = False

    return _queue_reasoning


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
        show_agent_reasoning: bool = Field(default=True, description="Afficher le raisonnement structuré des agents dans le flux de reasoning OpenWebUI")
        show_model_reasoning: bool = Field(default=False, description="Afficher le raisonnement du modèle de synthèse dans des blocs <think> OpenWebUI")
        show_perf_stats: bool = Field(default=False, description="Afficher les métriques de performance dans la signature (⏱ temps, tokens, coût estimé)")
        realtime_status: bool = Field(default=True, description="Émettre des statuts OpenWebUI en temps réel (quel agent travaille)")
        enable_memory_bg: bool = Field(default=True, description="Activer la condensation mémoire en arrière-plan")
        memory_always_on: bool = Field(default=True, description="Consulter l'agent memory automatiquement à chaque tour (en parallèle phase 1) pour enrichir le contexte sans surcoût UX")
        enable_critic_loop: bool = Field(default=False, description="Pass adversarial post-phase 1 : fact_checker vérifie les claims des autres agents avant synthèse. Coût ~3-5s mais gain qualité radical.")
        critic_confidence_threshold: float = Field(default=0.6, ge=0.0, le=1.0, description="Seuil de confiance fact_checker en dessous duquel un avertissement est ajouté à la synthèse")
        auto_factcheck_low_confidence: bool = Field(default=True, description="Auto-déclenche fact_checker si la confiance moyenne phase 1 < critic_confidence_threshold")
        auto_factcheck_high_stakes: bool = Field(default=True, description="Auto-déclenche fact_checker si la question contient des mots-clés à enjeux (santé / légal / financier / scientifique)")
        inject_confidence_in_synthesis: bool = Field(default=True, description="Passer le bloc de confiance par agent à la synthèse Alyx pour pondération des claims")
        enrich_citations_authority: bool = Field(default=True, description="Ajouter un badge d'autorité (🟢🟡🟠🔴) à chaque source citée selon la fiabilité du domaine")
        writer_reference_docx: str = Field(default="", description="Chemin (dans le conteneur) vers un template DOCX de référence (--reference-doc) pour brander les sorties writer")
        writer_reference_pptx: str = Field(default="", description="Chemin vers un template PPTX de référence pour brander les sorties writer/presenter pptx")
        embed_html_inline: bool = Field(default=True, description="Rendre les artifacts HTML de l'agent dev en iframe inline (event `embeds` OpenWebUI) au lieu de blocs de code markdown (panneau Artifacts)")
        persist_html_artifacts: bool = Field(default=True, description="Produire AUSSI un fichier .html téléchargeable pour chaque artifact HTML (dev/presenter/mindmap/diagram) en plus de l'iframe inline")
        emit_execution_graph: bool = Field(default=False, description="Émettre un diagramme mermaid post-turn récapitulant les agents exécutés (phases, durées). Utile pour le debug.")

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
        model_writer: str = Field(default="openrouter/deepseek", description="Modèle agent Rédaction (documents longue forme, prose structurée)")
        model_presenter: str = Field(default="openrouter/kimi-k2.5", description="Modèle agent Présentation (slides reveal.js)")
        model_translator: str = Field(default="openrouter/qwen3.5-flash", description="Modèle agent Traduction")
        model_summarizer: str = Field(default="openrouter/qwen3.5-flash", description="Modèle agent Résumé")
        model_vision: str = Field(default="openrouter/gpt-oss", description="Modèle agent Vision (LLM multimodal via LiteLLM)")
        model_mindmap: str = Field(default="openrouter/qwen3.5-flash", description="Modèle agent Mindmap (markmap.js)")
        model_diagram: str = Field(default="openrouter/qwen3.5-flash", description="Modèle agent Diagramme (mermaid/jointjs/excalidraw)")
        model_spreadsheet: str = Field(default="openrouter/deepseek", description="Modèle agent Tableur (XLSX via openpyxl)")
        model_code_exec: str = Field(default="openrouter/kimi-k2.5", description="Modèle agent Exécution code Python (sandbox open-terminal)")
        model_fact_checker: str = Field(default="openrouter/deepseek", description="Modèle agent Fact-checker (vérification adversariale)")
        model_audio: str = Field(default="openrouter/gpt-oss", description="Modèle agent Audio (post-transcription Whisper)")

        # --- Workflows multi-phases ---
        max_phases: int = Field(default=2, ge=1, le=5, description="Nombre max de phases séquentielles (1 = parallèle seul, 2 = comportement actuel, >2 = replanification dynamique)")

        # --- Cache Redis des sorties agents (exact match) ---
        enable_agent_cache: bool = Field(default=False, description="Cache exact-match (Redis) des sorties d'agents déterministes")
        agent_cache_ttl: int = Field(default=3600, ge=60, le=86400, description="Durée de vie du cache agents en secondes")
        redis_url: str = Field(default=_REDIS_URL, description="URL Redis pour le cache agents")

        # --- Cache sémantique (Qdrant) — complémentaire ---
        enable_semantic_cache: bool = Field(default=False, description="Cache sémantique : si une question proche a été traitée (similarité cosinus ≥ seuil), réutilise la réponse")
        semantic_cache_threshold: float = Field(default=0.92, ge=0.7, le=0.99, description="Seuil de similarité pour le cache sémantique")
        semantic_cache_collection: str = Field(default="alyx_semantic_cache", description="Collection Qdrant dédiée au cache sémantique")

        # --- Optimisations LLM ---
        enable_context_compression: bool = Field(default=False, description="Compresser les outputs agents > 2000 chars avant la synthèse (1 appel LLM cheap, gain coût synthèse 20-40%)")
        context_compression_target: int = Field(default=8000, ge=2000, le=30000, description="Seuil cumulé en chars au-dessus duquel la compression s'active")
        enable_model_autoselect: bool = Field(default=True, description="Basculer sur un modèle cheap pour les requêtes triviales (salutations, accusés de réception)")
        enable_prewarming: bool = Field(default=True, description="Pré-chauffer les connexions LiteLLM au démarrage (réduit la latence du premier tour)")

        # --- Pièces jointes natives (writer) ---
        enable_native_file_attachments: bool = Field(default=False, description="Uploader les documents writer vers Open WebUI et les attacher en pièce jointe native (event `files`) au lieu d'un lien data-URI. Nécessite webui_url + webui_api_key")
        webui_url: str = Field(default=_WEBUI_URL, description="URL interne d'Open WebUI (pour l'upload de fichiers natifs)")
        webui_api_key: str = Field(default=_WEBUI_API_KEY, description="Clé API Open WebUI (Bearer) pour l'upload de fichiers natifs")

        # --- Limites de sources par agent (injectées via state._sources) ---
        sources_web_ddg_max:         int = Field(default=5, ge=1, le=10, description="Web — nombre max de résultats DuckDuckGo bruts")
        sources_web_fetch:           int = Field(default=3, ge=1, le=10, description="Web — nombre de pages visitées en parallèle après DDG")
        sources_wikipedia_articles:  int = Field(default=3, ge=1, le=10, description="Wikipedia — nombre d'articles cherchés + résumés")
        sources_doc_papers:          int = Field(default=8, ge=3, le=30, description="Doc — nombre de papiers académiques retournés par paper-search")
        sources_doc_scihub:          int = Field(default=3, ge=0, le=10, description="Doc — nombre de textes intégraux sci-hub à tenter (0 = désactivé)")
        sources_rag_top_k:           int = Field(default=5, ge=1, le=20, description="RAG — nombre de chunks Qdrant retournés par requête")
        sources_geo_limit:           int = Field(default=3, ge=1, le=5,  description="Geo — nombre de candidats OSM pour le géocodage (>1 = désambiguïsation)")
        sources_reasoning_steps:     int = Field(default=5, ge=2, le=8,  description="Reasoning — nombre max d'étapes analytiques sequential-thinking")

        # --- Feature toggles ---
        enable_scihub:               bool = Field(default=True, description="Doc — autoriser l'accès sci-hub (vérifier la légalité dans ta juridiction)")
        enable_playwright_fallback:  bool = Field(default=True, description="Web/Doc — activer le fallback Playwright (navigateur réel) si fetch-web échoue")
        enable_writer_conversion:    bool = Field(default=True, description="Writer — activer la conversion pandoc (DOCX/EPUB/ODT/TEX/HTML/RTF)")

        # --- Limite de troncature des contenus externes injectés dans les prompts ---
        truncate_external_content:   int = Field(default=4000, ge=500, le=20000, description="Caractères max par contenu externe (page web, transcript, chunk RAG, full-text…) avant injection prompt")

        # --- Génération d'images (Pollinations.ai — appel direct GET, sans passer par LiteLLM) ---
        enable_image_gen: bool = Field(default=True, description="Activer la génération d'images")
        image_gen_provider: str = Field(default="pollinations", description="Fournisseur image : `pollinations` (gratuit, sans clé) ou `litellm` (DALL-E ou autre modèle image déclaré dans litellm_config.yaml)")
        pollinations_api_key: str = Field(default="", description="Clé API Pollinations.ai (optionnelle — gratuit sans clé pour les modèles de base)")
        pollinations_model: str = Field(default="flux", description="Modèle Pollinations : flux, zimage, gptimage, klein-large, imagen-4, seedream5, nanobanana, grok-imagine…")
        pollinations_width: int = Field(default=1024, ge=64, le=4096, description="Largeur de l'image générée (pixels)")
        pollinations_height: int = Field(default=1024, ge=64, le=4096, description="Hauteur de l'image générée (pixels)")
        pollinations_enhance: bool = Field(default=True, description="Amélioration IA du prompt par Pollinations avant génération")

    class UserValves(BaseModel):
        """Surcharges par utilisateur·rice (exposées dans Open WebUI en mode natif).

        Chaque champ vide/None laisse la valve globale correspondante prévaloir.
        Appliquées par requête (concurrence-safe : aucune mutation de self.valves).
        """
        language: str = Field(default="", description="Forcer la langue de réponse d'Alyx (vide = valeur globale)")
        alyx_model: str = Field(default="", description="Forcer le modèle de synthèse d'Alyx (vide = valeur globale)")
        show_model_footer: bool | None = Field(default=None, description="Afficher le pied de page modèles/coût (None = valeur globale)")
        show_perf_stats: bool | None = Field(default=None, description="Afficher les métriques de performance (None = valeur globale)")
        enable_scihub: bool | None = Field(default=None, description="Autoriser l'accès sci-hub pour mes requêtes (None = valeur globale)")

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
            "writer":     self.valves.model_writer,
            "presenter":    self.valves.model_presenter,
            "translator":   self.valves.model_translator,
            "summarizer":   self.valves.model_summarizer,
            "vision":       self.valves.model_vision,
            "mindmap":      self.valves.model_mindmap,
            "diagram":      self.valves.model_diagram,
            "spreadsheet":  self.valves.model_spreadsheet,
            "code_exec":    self.valves.model_code_exec,
            "fact_checker": self.valves.model_fact_checker,
            "audio":        self.valves.model_audio,
            # Paramètres Pollinations transmis aux agents via le dict models
            "_pollinations": {
                "enable":   self.valves.enable_image_gen,
                "provider": self.valves.image_gen_provider,
                "api_key":  self.valves.pollinations_api_key,
                "model":    self.valves.pollinations_model,
                "width":    self.valves.pollinations_width,
                "height":   self.valves.pollinations_height,
                "enhance":  self.valves.pollinations_enhance,
            },
        }
        self._graph, self._pool = self._run_sync(build_graph(self.valves.db_url, models))
        self._models = models

        # Pré-chauffe les modèles utilisés (best-effort, non bloquant).
        if self.valves.enable_prewarming:
            try:
                from tools.perf import warm_up_all
                # On ne pré-chauffe que les modèles textuels (skip _pollinations / image_gen)
                model_set = {v for k, v in models.items() if isinstance(v, str) and not k.startswith("_")}
                asyncio.run_coroutine_threadsafe(warm_up_all(model_set), self._loop)
            except Exception:
                pass
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
        runtime_reasoning_stream_emitter = _build_pipeline_reasoning_emitter(q, self.valves.alyx_model)

        async def _emit_reasoning(text: str, final: bool = False) -> None:
            await runtime_reasoning_stream_emitter(text, final)

        # Helper : émet un statut OpenWebUI natif depuis le contexte synchrone.
        # En mode pipelines, l'event est injecté dans le flux streamé.
        async def _emit_status_sync(description: str, done: bool = False) -> None:
            if runtime_event_emitter:
                await runtime_event_emitter({"type": "status", "data": {"description": description, "done": done}})

        def _emit(description: str, done: bool = False) -> None:
            if runtime_event_emitter and self.valves.realtime_status:
                asyncio.run_coroutine_threadsafe(
                    _emit_status_sync(description, done),
                    self._loop,
                )

        _emit("🔍 Analyse du message…")

        # 1. Préparer l'état initial
        lc_messages = _convert_messages(messages)
        images_b64 = _extract_images_b64(messages)
        audios_b64 = _extract_audios_b64(messages)
        user_valves = _extract_user_valves(body)

        # Propager les valves writer_reference_* aux env vars que writer.py lit.
        # Process-wide mais sans race (le chemin est constant, juste lu par pypandoc).
        if self.valves.writer_reference_docx:
            os.environ["ALYX_WRITER_REFERENCE_DOCX"] = self.valves.writer_reference_docx
        if self.valves.writer_reference_pptx:
            os.environ["ALYX_WRITER_REFERENCE_PPTX"] = self.valves.writer_reference_pptx

        # Date courante injectée dans l'état — lisible par tous les agents
        current_date = datetime.now().strftime("%A %d %B %Y").lower()

        chat_id = body.get("chat_id", body.get("session_id", "default"))
        config = {"configurable": {
            "thread_id": chat_id,
            "event_emitter": runtime_event_emitter if self.valves.realtime_status else None,
            "reasoning_emitter": _emit_reasoning if self.valves.show_reasoning else None,
            "show_reasoning": self.valves.show_reasoning,
            "show_agent_reasoning": self.valves.show_agent_reasoning,
            "show_model_reasoning": self.valves.show_model_reasoning,
        }}

        initial_state = {
            "messages": lc_messages,
            "images_b64": images_b64,
            "audios_b64": audios_b64,
            "current_date": current_date,
            "routing": [],
            "routing_next": [],
            "routing_phase1": [],
            "agent_outputs": {},
            "agent_confidence": {},
            "agent_metrics": {},
            "artifacts": [],
            "_pollinations": {
                "enable":   self.valves.enable_image_gen,
                "provider": self.valves.image_gen_provider,
                "api_key":  self.valves.pollinations_api_key,
                "model":    self.valves.pollinations_model,
                "width":    self.valves.pollinations_width,
                "height":   self.valves.pollinations_height,
                "enhance":  self.valves.pollinations_enhance,
            },
            # Isolation multi-tenant du RAG : on transmet l'identité + les
            # ressources autorisées par OpenWebUI pour ce chat. L'agent rag s'en
            # sert pour filtrer Qdrant (cf. tools/rag_client.search).
            "_owui": _extract_owui_context(body),
            # Limites de sources + feature toggles, lus par les agents qui en
            # ont besoin via state.get("_sources"). Sert de dictionnaire partagé
            # pour découpler les valves de chaque agent.
            "_sources": {
                "web_ddg_max":        self.valves.sources_web_ddg_max,
                "web_fetch":          self.valves.sources_web_fetch,
                "wikipedia_articles": self.valves.sources_wikipedia_articles,
                "doc_papers":         self.valves.sources_doc_papers,
                "doc_scihub":         self.valves.sources_doc_scihub,
                "rag_top_k":          self.valves.sources_rag_top_k,
                "geo_limit":          self.valves.sources_geo_limit,
                "reasoning_steps":    self.valves.sources_reasoning_steps,
                "enable_scihub":              _coalesce(user_valves.get("enable_scihub"), self.valves.enable_scihub),
                "enable_playwright_fallback": self.valves.enable_playwright_fallback,
                "enable_writer_conversion":   self.valves.enable_writer_conversion,
                "truncate_chars":     self.valves.truncate_external_content,
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
                runtime_event_emitter, runtime_reasoning_stream_emitter, self._models,
                messages, lc_messages, images_b64, user_message, user_valves,
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
        reasoning_emitter,
        models: dict,
        messages: list[dict],
        lc_messages: list,
        images_b64: list[str],
        user_message: str,
        user_valves: dict | None = None,
    ) -> None:
        """Coroutine unique : graphe → synthèse → tokens dans la queue."""
        from openai import AsyncOpenAI  # lazy

        # Valeurs effectives = surcharges UserValves (par requête) sinon valves globales.
        uv = user_valves or {}
        eff_language = _coalesce(uv.get("language"), self.valves.language)
        eff_alyx_model = _coalesce(uv.get("alyx_model"), self.valves.alyx_model)
        eff_show_footer = _coalesce(uv.get("show_model_footer"), self.valves.show_model_footer)
        eff_show_perf = _coalesce(uv.get("show_perf_stats"), self.valves.show_perf_stats)

        async def _emit(description: str, done: bool = False, hidden: bool = False) -> None:
            if event_emitter and self.valves.realtime_status:
                await _emit_status(event_emitter, description, done=done, hidden=hidden)

        model_reasoning_enabled = self.valves.show_reasoning and self.valves.show_model_reasoning
        reasoning_stream_emitter = (config.get("configurable") or {}).get("reasoning_emitter")
        model_reasoning_buffer = ""

        async def _emit_model_reasoning(piece: str = "", final: bool = False) -> None:
            nonlocal model_reasoning_buffer
            if not (reasoning_stream_emitter and model_reasoning_enabled):
                return
            if piece:
                model_reasoning_buffer += piece

            should_flush = final or len(model_reasoning_buffer) >= 220 or "\n" in model_reasoning_buffer
            if not should_flush:
                return

            chunk = _compact_reasoning_text(model_reasoning_buffer)
            model_reasoning_buffer = ""
            if chunk:
                await reasoning_stream_emitter(chunk, final)
            elif final:
                await reasoning_stream_emitter("", True)

        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []
        agent_metrics: dict[str, dict] = {}
        agent_confidence: dict[str, float] = {}
        t0 = time.perf_counter()
        # Mistral ne supporte pas le paramètre enable_thinking
        is_mistral = "mistral" in eff_alyx_model.lower()
        extra_body: dict = {} if (model_reasoning_enabled or is_mistral) else {"enable_thinking": False}
        try:
            # ── Cache exact (Redis) puis cache sémantique (Qdrant) ────────
            # MULTI-USER SAFE : toutes les clés et toutes les recherches sont
            # scoped par user_id pour empêcher la fuite croisée entre comptes.
            cache_hit = False
            cache_key = None
            embedding: list | None = None
            owui_ctx = initial_state.get("_owui") or {}
            cache_user_id = str(owui_ctx.get("user_id") or "").strip()
            from tools import cache as _agent_cache
            if self.valves.enable_agent_cache or self.valves.enable_semantic_cache:
                cache_key = _agent_cache.cache_key(user_message, user_id=cache_user_id)
                # 1. Exact match (Redis) — moins cher, à essayer en premier
                if self.valves.enable_agent_cache:
                    cached = await _agent_cache.get(self.valves.redis_url, cache_key)
                    if cached:
                        await _emit("⚡ Réponse depuis le cache (exact)")
                        agent_outputs, artifacts, agent_metrics, agent_confidence = cached, [], {}, {}
                        cache_hit = True
                # 2. Cache sémantique (Qdrant) si exact a miss
                if not cache_hit and self.valves.enable_semantic_cache:
                    embedding = await _agent_cache._embed(
                        user_message,
                        embed_url=os.environ.get("LITELLM_URL", "http://litellm:4000/v1"),
                        embed_model=os.environ.get("RAG_EMBEDDING_MODEL", "openrouter/embedding"),
                        api_key=os.environ.get("LITELLM_API_KEY", ""),
                    )
                    if embedding:
                        cached = await _agent_cache.semantic_get(
                            qdrant_url=os.environ.get("QDRANT_URI", "http://qdrant:6333"),
                            qdrant_api_key=os.environ.get("QDRANT_API_KEY", ""),
                            collection=self.valves.semantic_cache_collection,
                            embedding=embedding,
                            threshold=self.valves.semantic_cache_threshold,
                            user_id=cache_user_id,
                        )
                        if cached:
                            await _emit("⚡ Réponse depuis le cache (sémantique)")
                            agent_outputs, artifacts, agent_metrics = cached, [], {}
                            cache_hit = True

            if not cache_hit:
                await _emit("🧭 Routage de la demande…")
                # Exécuter le graphe
                agent_outputs, artifacts, agent_metrics, agent_confidence = await self._run_graph(
                    graph, initial_state, config, event_emitter, models=models,
                    max_phases=self.valves.max_phases,
                    memory_always_on=self.valves.memory_always_on,
                    enable_critic_loop=self.valves.enable_critic_loop,
                    auto_factcheck_low_confidence=self.valves.auto_factcheck_low_confidence,
                    auto_factcheck_high_stakes=self.valves.auto_factcheck_high_stakes,
                    critic_confidence_threshold=self.valves.critic_confidence_threshold,
                )
                # Mémoriser si le tour est sûr à cacher
                if cache_key and _agent_cache.is_cacheable(agent_outputs, artifacts):
                    if self.valves.enable_agent_cache:
                        await _agent_cache.store(
                            self.valves.redis_url, cache_key, agent_outputs, self.valves.agent_cache_ttl
                        )
                    if self.valves.enable_semantic_cache and embedding:
                        await _agent_cache.semantic_store(
                            qdrant_url=os.environ.get("QDRANT_URI", "http://qdrant:6333"),
                            qdrant_api_key=os.environ.get("QDRANT_API_KEY", ""),
                            collection=self.valves.semantic_cache_collection,
                            embedding=embedding,
                            agent_outputs=agent_outputs,
                            user_id=cache_user_id,
                        )
            if reasoning_emitter and self.valves.show_reasoning:
                await reasoning_emitter("", True)

            # ── FAST PATH image_gen seul ────────────────────────────────────────
            # Pas de synthèse LLM : on émet directement l'image Markdown.
            # Gain ~2-3 s par rapport au chemin de synthèse complet.
            if (
                set(agent_outputs.keys()) == {"image_gen"}
                and not agent_outputs.get("image_gen", "").startswith("⚠️")
            ):
                if event_emitter and len(messages) <= 2:
                    asyncio.ensure_future(_emit_chat_meta(event_emitter, user_message))
                q.put(agent_outputs["image_gen"])
                elapsed = time.perf_counter() - t0
                await _emit("✅ Terminé", done=True)
                if eff_show_footer:
                    q.put(f"\n\n---\n*{_build_footer(eff_alyx_model, agent_outputs, models, agent_metrics, elapsed, eff_show_perf)}*")
                return

            # Court-circuit : aucun agent invoqué → Alyx répond directement
            if not agent_outputs and not artifacts:
                # Titre automatique du chat à la première réponse
                if event_emitter and len(messages) <= 2:
                    asyncio.ensure_future(_emit_chat_meta(event_emitter, user_message))
                await _emit("✍️ Réponse directe…")
                alyx_system = _ALYX_SYSTEM_TEMPLATE.format(
                    current_date=datetime.now().strftime("%A %d %B %Y"),
                    language=eff_language,
                    alyx_model=eff_alyx_model,
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
                    model=eff_alyx_model,
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
                        "model": eff_alyx_model,
                    }
                await _emit("✅ Terminé", done=True)
                if eff_show_footer:
                    footer = _build_footer(
                        alyx_model=eff_alyx_model,
                        agent_outputs={},
                        models=models,
                        agent_metrics=agent_metrics,
                        elapsed=elapsed,
                        show_perf_stats=eff_show_perf,
                    )
                    q.put(f"\n\n---\n*{footer}*")
                return

            # Synthèse finale
            # Émettre les citations source (OpenWebUI cartes persistantes)
            # avec, si valve activée, un badge d'autorité du domaine (🟢🟡🟠🔴).
            if event_emitter:
                from tools.quality import score_url_authority, authority_emoji
                for citation in _extract_citations(agent_outputs):
                    title = citation["title"]
                    if self.valves.enrich_citations_authority:
                        score = score_url_authority(citation["url"])
                        title = f"{authority_emoji(score)} {title} · autorité {score:.2f}"
                    try:
                        await event_emitter({"type": "source", "data": {
                            "document": [citation["snippet"]],
                            "metadata": [{"source": citation["url"]}],
                            "source": {"name": title, "url": citation["url"]},
                        }})
                    except Exception:
                        pass

            # Titre automatique du chat à la première réponse (avec agents)
            if event_emitter and len(messages) <= 2:
                asyncio.ensure_future(_emit_chat_meta(event_emitter, user_message))

            # Artifacts HTML inline : extraire les blocs ```html de l'agent dev et
            # les rendre en iframe directement dans la conversation (event `embeds`),
            # au lieu de les laisser passer en bloc de code markdown (panneau Artifacts).
            # La sortie dev est nettoyée pour que la synthèse explique l'artifact sans
            # reproduire le code (évite le doublon inline + panneau).
            if self.valves.embed_html_inline:
                all_embeds: list[str] = []
                for _html_agent in ("dev", "presenter", "mindmap", "diagram"):
                    if agent_outputs.get(_html_agent):
                        embeds_found, cleaned = _extract_html_embeds(agent_outputs[_html_agent])
                        if embeds_found:
                            agent_outputs[_html_agent] = cleaned
                            all_embeds.extend(embeds_found)
                            # Persistance : on push chaque embed comme artifact
                            # document, pour qu'il apparaisse en lien de
                            # téléchargement (data-URI ou natif selon valves).
                            if self.valves.persist_html_artifacts:
                                import uuid as _uuid
                                for emb_html in embeds_found:
                                    title_match = re.search(r"<title>(.*?)</title>", emb_html, re.IGNORECASE | re.DOTALL)
                                    label = (title_match.group(1).strip() if title_match else _html_agent)[:40]
                                    safe_label = re.sub(r"[^\w-]", "_", label).strip("_") or _html_agent
                                    fname = f"{safe_label}-{_uuid.uuid4().hex[:8]}.html"
                                    artifacts.append({
                                        "type": "document",
                                        "format": "html",
                                        "filename": fname,
                                        "mime": "text/html",
                                        "base64": base64.b64encode(emb_html.encode("utf-8")).decode("ascii"),
                                        "size_label": f"{len(emb_html) // 1024} KB" if len(emb_html) >= 1024 else f"{len(emb_html)} B",
                                    })
                if all_embeds:
                    await _emit_html_embeds(event_emitter, all_embeds)

            # ── Context compression : si la somme des outputs dépasse le seuil,
            # on compresse via un LLM cheap pour réduire le coût de synthèse. ──
            if self.valves.enable_context_compression:
                from tools.perf import compress_agent_outputs
                agent_outputs = await compress_agent_outputs(
                    agent_outputs,
                    target_max_chars=self.valves.context_compression_target,
                )

            # ── Model autoselect : pour les requêtes triviales, bascule sur
            # le modèle cheap pour ne pas brûler du compute pour rien. ──
            if self.valves.enable_model_autoselect:
                from tools.perf import select_model_by_complexity
                eff_alyx_model = select_model_by_complexity(
                    user_message, eff_alyx_model,
                    cheap_model=self.valves.supervisor_model,
                )

            await _emit("✍️ Rédaction de la réponse…")
            synthesis_context = _build_synthesis_context(agent_outputs, artifacts)
            # Injection du bloc de confiance par agent : Alyx pondère ses claims.
            if self.valves.inject_confidence_in_synthesis and agent_confidence:
                from tools.quality import format_confidence_block
                conf_block = format_confidence_block(agent_confidence)
                if conf_block:
                    synthesis_context = synthesis_context + "\n\n" + conf_block
            synth_messages = [{"role": "system", "content": _ALYX_SYSTEM_TEMPLATE.format(
                current_date=datetime.now().strftime("%A %d %B %Y"),
                language=eff_language,
                alyx_model=eff_alyx_model,
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
                model=eff_alyx_model,
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

            # Liens de téléchargement des documents (agent writer) — émis
            # DIRECTEMENT depuis les artifacts, JAMAIS via le LLM de synthèse :
            # le base64 ne doit pas transiter par le modèle (reproduction
            # corrompue/tronquée d'un long base64).
            # Pièces jointes : on émet TOUJOURS le bloc data-URI (baseline fiable
            # qui marche partout). L'upload natif Open WebUI, si activé, s'ajoute
            # en bonus (puce de fichier dans la barre de message). Pas d'« exclusive
            # or » : si le natif marche, l'utilisateur a chip + lien ; si le natif
            # rate silencieusement, il a au moins le lien.
            doc_links = _build_document_links(artifacts)
            if doc_links:
                q.put(doc_links)
            await _emit_writer_attachments(event_emitter, self.valves, artifacts)

            elapsed = time.perf_counter() - t0
            if synth_usage_out:
                u = synth_usage_out[0]
                agent_metrics["_synthesis"] = {
                    "prompt_tokens": getattr(u, "prompt_tokens", 0) or 0,
                    "completion_tokens": getattr(u, "completion_tokens", 0) or 0,
                    "model": eff_alyx_model,
                }
            await _emit("✅ Terminé", done=True)

            # Pied de page
            if eff_show_footer:
                footer = _build_footer(
                    alyx_model=eff_alyx_model,
                    agent_outputs=agent_outputs,
                    models=models,
                    agent_metrics=agent_metrics,
                    elapsed=elapsed,
                    show_perf_stats=eff_show_perf,
                )
                q.put(f"\n\n---\n*{footer}*")

            # Diagramme d'exécution (debug / transparence) — caché par défaut.
            if self.valves.emit_execution_graph:
                graph_md = _build_execution_graph(agent_metrics, elapsed=elapsed)
                if graph_md:
                    q.put(graph_md)

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
        - Champ delta.reasoning_content : converti en sortie dédiée si show_reasoning=True.
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
        reasoning_open = False
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
                    reasoning_open = True
                continue

            text = delta.content or ""
            if not text:
                continue

            if reasoning_open and reasoning_handler:
                await reasoning_handler("", True)
                reasoning_open = False

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
                            reasoning_open = True
                        buf = buf[end + len(close_tag):]
                        in_think = False
                        current_think_tag = ""
                    else:
                        if show_model_reasoning and reasoning_handler and buf:
                            await reasoning_handler(buf, False)
                            reasoning_open = True
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
        if reasoning_handler and reasoning_open:
            await reasoning_handler("", True)

    @staticmethod
    async def _run_graph(graph, initial_state: dict, config: dict, event_emitter=None,
                         models: dict | None = None, max_phases: int = 2,
                         memory_always_on: bool = True,
                         enable_critic_loop: bool = False,
                         auto_factcheck_low_confidence: bool = True,
                         auto_factcheck_high_stakes: bool = True,
                         critic_confidence_threshold: float = 0.6):
        agent_outputs: dict[str, str] = {}
        agent_confidence: dict[str, float] = {}
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
            agent_confidence.update(node_output.get("agent_confidence", {}))

            if event_emitter:
                for _n, out_text in node_output.get("agent_outputs", {}).items():
                    if isinstance(out_text, str) and out_text.startswith(("⚠️", "⏱️")):
                        await _emit_notification(event_emitter, "warning", f"{icon} : {out_text[:120]}")

        # ── Memory always-on : lecture mémoire en parallèle de phase 1, sans
        # bloquer le supervisor. Si supervisor route déjà memory, on skippe pour
        # éviter le double appel. Coût : ~1s parallèle, gain UX significatif
        # (personnalisation transparente sans demander à l'utilisateur·rice). ──
        always_on_memory_task = None
        # Note : on lance APRÈS le premier event astream pour connaître routing
        # — fait via un setup différé ci-dessous.

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
                    # Memory always-on : lancer en parallèle de phase 1 si pas
                    # déjà routé par le supervisor (évite le double appel).
                    if memory_always_on and "memory" not in routing and "memory" not in (routing_next or []):
                        import agents.memory_agent as _memory_mod
                        always_on_memory_task = asyncio.create_task(
                            _memory_mod.run(initial_state, config=config,
                                            model=(models or {}).get("memory"))
                        )
                    continue
                await _handle_agent_output(node_name, node_output)

        # ── Critic loop : vérification adversariale post-phase 1 ──────────────
        # Trois portes d'entrée :
        #   1. Valve enable_critic_loop : toujours-on (coûteux mais maximal)
        #   2. auto_factcheck_low_confidence + confidence moyenne < seuil
        #   3. auto_factcheck_high_stakes + question à enjeux (santé/légal/finance/science)
        # Le résultat rejoint agent_outputs comme tout autre agent.
        from tools.quality import should_auto_factcheck
        user_text_for_check = _last_human_text(initial_state.get("messages", []))
        trigger_fc = enable_critic_loop and "fact_checker" not in agent_outputs and agent_outputs
        trigger_reason = "valve enable_critic_loop"
        if not trigger_fc and "fact_checker" not in agent_outputs:
            auto_trigger, reason = should_auto_factcheck(
                user_text_for_check, agent_outputs, agent_confidence,
                critic_threshold=critic_confidence_threshold,
                high_stakes_only=auto_factcheck_high_stakes and not auto_factcheck_low_confidence,
            )
            if auto_trigger and (auto_factcheck_low_confidence or auto_factcheck_high_stakes):
                trigger_fc = True
                trigger_reason = reason
        if trigger_fc:
            import agents.fact_checker as _fc_mod
            try:
                await _emit(f"🔬 Vérification adversariale ({trigger_reason})")
                fc_state = {**initial_state, "agent_outputs": dict(agent_outputs)}
                fc_result = await asyncio.wait_for(
                    _fc_mod.run(fc_state, config=config, model=(models or {}).get("fact_checker")),
                    timeout=45.0,
                )
                if isinstance(fc_result, dict):
                    agent_outputs.update(fc_result.get("agent_outputs", {}))
                    agent_metrics.update(fc_result.get("agent_metrics", {}))
                    agent_confidence.update(fc_result.get("agent_confidence", {}))
            except (asyncio.TimeoutError, Exception):
                pass  # best-effort

        # ── Récupération de la memory lue en parallèle (always-on) ────────────
        if always_on_memory_task is not None:
            try:
                mem_result = await asyncio.wait_for(always_on_memory_task, timeout=15.0)
                if isinstance(mem_result, dict):
                    mem_text = (mem_result.get("agent_outputs") or {}).get("memory", "")
                    if mem_text:
                        agent_outputs["memory"] = mem_text
                    if "agent_metrics" in mem_result:
                        agent_metrics.update(mem_result["agent_metrics"])
                    if "agent_confidence" in mem_result:
                        # On ne tracke pas encore agent_confidence dans _run_graph,
                        # mais on logue côté output pour usage futur
                        pass
            except (asyncio.TimeoutError, Exception):
                pass  # Memory always-on est best-effort : pas d'erreur bloquante

        # ── Phases séquentielles 2..max_phases ─────────────────────────────────
        # Chaque phase reçoit agent_outputs/artifacts des phases précédentes.
        # max_phases=2 ⇒ on exécute uniquement routing_next (comportement historique,
        # aucune replanification). max_phases>2 ⇒ après chaque phase, le superviseur
        # est resollicité pour décider d'une phase suivante (replanification dynamique).
        async def _run_phase(phase_idx: int, agents_to_run: list[str]) -> None:
            nonlocal pending
            labels = "  ·  ".join(_AGENT_ICONS.get(n, n) for n in agents_to_run)
            await _emit(f"Phase {phase_idx} · {labels}")
            pending = set(agents_to_run)
            phase_state = {
                **initial_state,
                "agent_outputs": dict(agent_outputs),
                "artifacts": list(artifacts),
                "routing": agents_to_run,
                "routing_next": [],
                "routing_phase1": [],
            }
            coros = []
            for name in agents_to_run:
                mod = importlib.import_module(_AGENT_MODULES[name])
                has_config = "config" in inspect.signature(mod.run).parameters
                m = (models or {}).get(name)
                if has_config:
                    coros.append((name, mod.run(phase_state, config=config, model=m)))
                else:
                    coros.append((name, mod.run(phase_state, model=m)))
            results = await asyncio.gather(*[c for _, c in coros], return_exceptions=True)
            for (name, _), result in zip(coros, results):
                if isinstance(result, dict):
                    await _handle_agent_output(name, result)
                else:
                    agent_outputs[name] = f"⚠️ [Erreur phase {phase_idx}] {result}"

        already_run: set[str] = set(agent_outputs.keys())
        current_next = [n for n in routing_next if n in _AGENT_MODULES and n not in already_run]
        phase_idx = 2
        while current_next and phase_idx <= max_phases:
            await _run_phase(phase_idx, current_next)
            already_run.update(current_next)
            if phase_idx < max_phases:
                user_text = _last_human_text(initial_state.get("messages", []))
                replanned = await _replan_next(
                    user_text, agent_outputs, (models or {}).get("supervisor"), already_run
                )
                current_next = [n for n in replanned if n in _AGENT_MODULES and n not in already_run][:2]
            else:
                current_next = []
            phase_idx += 1

        return agent_outputs, artifacts, agent_metrics, agent_confidence


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


def _last_human_text(messages: list) -> str:
    """Dernier message humain d'une liste de BaseMessage LangChain."""
    for msg in reversed(messages or []):
        if getattr(msg, "type", None) == "human":
            content = getattr(msg, "content", "")
            return content if isinstance(content, str) else ""
    return ""


async def _replan_next(user_text: str, agent_outputs: dict, model: str | None,
                       already_run: set[str]) -> list[str]:
    """Replanification dynamique : sollicite le superviseur pour décider d'une phase
    supplémentaire au vu des résultats déjà obtenus. Retourne une liste d'agents
    (max 2) ou [] si la réponse est jugée complète. Conservateur par défaut.
    """
    from openai import AsyncOpenAI
    available = sorted(set(_AGENT_MODULES) - set(already_run))
    if not available:
        return []
    summary = "\n".join(
        f"- {k}: {str(v)[:300]}"
        for k, v in agent_outputs.items()
        if v and not str(v).startswith(("⚠️", "⏱️"))
    )[:3000]
    sys = (
        "You orchestrate a sequential multi-agent system. Given the user's request and the "
        "results gathered so far, decide whether ANOTHER phase of agents is needed to fully "
        "satisfy the request (e.g. transform gathered data into an artifact, write a document, "
        "or fetch a clearly missing piece).\n"
        f"Agents still available: {available}.\n"
        "Return ONLY a JSON array of agent names for the NEXT phase, or [] if the answer is "
        "already complete. Be conservative: prefer [] unless a clearly missing step remains. "
        "Max 2 agents."
    )
    try:
        client = AsyncOpenAI(
            base_url=os.environ.get("LITELLM_URL", "http://litellm:4000/v1"),
            api_key=os.environ.get("LITELLM_API_KEY", ""),
        )
        resp = await client.chat.completions.create(
            model=model or "openrouter/qwen3.5-flash",
            messages=[
                {"role": "system", "content": sys},
                {"role": "user", "content": f"Request: {user_text[:500]}\n\nResults so far:\n{summary}"},
            ],
            max_tokens=40,
            temperature=0,
            stream=False,
            extra_body={"enable_thinking": False},
        )
        raw = (resp.choices[0].message.content or "").strip()
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if not match:
            return []
        agents = json.loads(match.group(0))
        return [a for a in agents if isinstance(a, str) and a in available][:2]
    except Exception:
        return []


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


def _build_document_links(artifacts: list[dict]) -> str:
    """
    Construit le bloc de téléchargement data-URI pour les documents produits par
    l'agent writer. Émis directement dans le flux (hors LLM) pour éviter toute
    corruption du base64.

    Header dédié (`## 📎 Pièces jointes`) + séparateur visuel pour que le bloc soit
    clairement détectable même après une longue prose de synthèse — évite la
    confusion « est-ce que le lien est là ? » quand le LLM paraphrase la note du
    writer sans inclure d'URL.
    """
    rows: list[str] = []
    for a in artifacts:
        if not isinstance(a, dict) or a.get("type") != "document":
            continue
        filename = a.get("filename", "document")
        fmt = str(a.get("format", "")).upper()
        size = a.get("size_label", "")
        b64 = a.get("base64")
        if not b64:
            # Artifact incomplet : on signale plutôt que de rester silencieux.
            rows.append(f"- ⚠️ **{filename}** ({fmt}) — base64 manquant, conversion probablement échouée")
            continue
        mime = a.get("mime", "application/octet-stream")
        data_uri = f"data:{mime};base64,{b64}"
        rows.append(f"- 📎 **[{filename}]({data_uri})** — {fmt}, {size}")
    if not rows:
        return ""
    return "\n\n---\n\n## 📎 Pièces jointes\n\n" + "\n".join(rows) + "\n"


async def _upload_file_to_webui(webui_url: str, api_key: str, filename: str,
                                raw_bytes: bytes, mime: str) -> dict | None:
    """Upload un fichier vers Open WebUI (POST /api/v1/files/) et retourne l'objet
    fichier renvoyé (avec son `id`), ou None en cas d'échec."""
    import httpx
    url = webui_url.rstrip("/") + "/api/v1/files/"
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"file": (filename, raw_bytes, mime)}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, headers=headers, files=files)
        resp.raise_for_status()
        return resp.json()


async def _emit_writer_attachments(event_emitter, valves, artifacts: list[dict]) -> bool:
    """Upload les documents writer vers Open WebUI et les attache en pièce jointe
    native via l'event `files`.

    Returns:
        True si au moins un fichier a été attaché nativement (→ l'appelant NE doit
        PAS émettre de lien data-URI), False sinon (→ fallback data-URI).
    """
    if not (event_emitter and getattr(valves, "enable_native_file_attachments", False)
            and getattr(valves, "webui_api_key", "")):
        return False

    file_objs: list[dict] = []
    for a in artifacts:
        if not isinstance(a, dict) or a.get("type") != "document":
            continue
        b64 = a.get("base64")
        if not b64:
            continue
        filename = a.get("filename", "document")
        try:
            raw = base64.b64decode(b64)
            obj = await _upload_file_to_webui(
                valves.webui_url, valves.webui_api_key, filename, raw,
                a.get("mime", "application/octet-stream"),
            )
        except Exception as exc:
            _LOGGER.warning("Upload natif du document %s échoué : %s", filename, exc)
            continue
        if not obj or not obj.get("id"):
            continue
        fid = obj["id"]
        file_objs.append({
            "type": "file",
            "id": fid,
            "name": filename,
            "url": f"/api/v1/files/{fid}",
            "file": obj,
        })

    if not file_objs:
        return False
    try:
        await event_emitter({"type": "files", "data": {"files": file_objs}})
        return True
    except Exception as exc:
        _LOGGER.warning("Émission de l'event files échouée : %s", exc)
        return False


_HTML_FENCE_RE = re.compile(r"```html[^\n]*\n(.*?)```", re.DOTALL | re.IGNORECASE)

# Petit script injecté dans chaque embed extrait : poste la hauteur effective au
# parent Open WebUI (cf. doc rich-ui, message `iframe:height`). Sans cela, l'iframe
# garde la hauteur par défaut très courte d'OWUI, ce qui rend les decks reveal.js
# et autres widgets pleins-écran illisibles. Pour reveal.js spécifiquement, on
# garantit un minimum de 900 px (sinon le scaling auto rend le contenu minuscule
# et les slides un peu denses débordent du viewport virtuel 960x700).
_HEIGHT_REPORTER_JS = (
    "<script>(function(){function r(){"
    "var d=document.querySelector('.reveal');"
    "var h=d?Math.max(900,(d.offsetHeight||900)):"
    "Math.max(document.documentElement.scrollHeight||400,400);"
    "try{parent.postMessage({type:'iframe:height',height:h},'*');}catch(e){}}"
    "window.addEventListener('load',r);"
    "window.addEventListener('resize',r);"
    "setTimeout(r,300);setTimeout(r,1200);"
    "})();</script>"
)


def _inject_height_reporter(html: str) -> str:
    """Injecte `_HEIGHT_REPORTER_JS` juste avant `</body>` (ou en fin) si absent."""
    if "iframe:height" in html:
        return html  # déjà présent — ne pas dupliquer
    idx = html.lower().rfind("</body>")
    if idx >= 0:
        return html[:idx] + _HEIGHT_REPORTER_JS + html[idx:]
    return html + _HEIGHT_REPORTER_JS


def _extract_html_embeds(text: str) -> tuple[list[str], str]:
    """
    Extrait les blocs ```html d'une sortie d'agent pour les rendre en iframe
    inline (event OpenWebUI `embeds`) plutôt qu'en bloc de code markdown
    (panneau Artifacts).

    Le bloc de code est retiré du texte et remplacé par un court placeholder
    qui indique à la synthèse d'expliquer l'artifact SANS reproduire le code
    (sinon il s'afficherait deux fois : inline + panneau Artifacts).

    Returns:
        (liste des contenus HTML extraits, texte nettoyé pour la synthèse)
    """
    embeds: list[str] = []

    def _replace(match: "re.Match") -> str:
        html = match.group(1).strip()
        if not html:
            return match.group(0)
        embeds.append(_inject_height_reporter(html))
        title_m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        label = title_m.group(1).strip() if title_m else "interactif"
        return (
            f"[Artifact HTML « {label} » affiché directement dans la conversation. "
            "NE PAS reproduire le code : présente-le et commente-le en 2-3 phrases.]"
        )

    stripped = _HTML_FENCE_RE.sub(_replace, text)
    return embeds, stripped


async def _emit_html_embeds(event_emitter, embeds: list[str], replace: bool = False) -> None:
    """Émet les artifacts HTML en iframes inline via l'event OpenWebUI `embeds`.

    Args:
        replace: si True, remplace les embeds précédents au lieu de les empiler.
                 Utile pour un widget « vivant » mis à jour en place (polling,
                 build progressif). Par défaut False → comportement additif.
    """
    if not event_emitter or not embeds:
        return
    try:
        data: dict[str, Any] = {"embeds": embeds}
        if replace:
            data["replace"] = True
        await event_emitter({"type": "embeds", "data": data})
    except Exception:
        pass


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


def _build_execution_graph(agent_metrics: dict, agent_confidence: dict | None = None,
                           elapsed: float | None = None) -> str:
    """Construit un mini-diagramme mermaid récapitulant les agents exécutés ce tour.

    Format : flowchart compact avec, pour chaque agent, modèle utilisé + tokens.
    Utile en debug / transparence — caché par défaut (valve `emit_execution_graph`).
    """
    if not agent_metrics:
        return ""
    confs = agent_confidence or {}
    lines = ["```mermaid", "flowchart LR", "    U([User]) --> S[Supervisor]"]
    edges = []
    for i, (agent, m) in enumerate(agent_metrics.items()):
        if agent.startswith("_"):  # _synthesis etc.
            continue
        node_id = f"A{i}"
        model = m.get("model", "?").split("/")[-1]
        toks = (m.get("prompt_tokens", 0) or 0) + (m.get("completion_tokens", 0) or 0)
        conf = confs.get(agent)
        conf_str = f" [{conf:.2f}]" if isinstance(conf, (int, float)) else ""
        label = f"{agent}<br/>{model}<br/>~{toks // 100 / 10}k tok{conf_str}"
        lines.append(f"    {node_id}[\"{label}\"]")
        edges.append(f"    S --> {node_id}")
    lines.extend(edges)
    lines.append("    A0 -.-> SY[Alyx Synthèse]")
    if elapsed:
        lines.append(f"    SY --> F([Final · {elapsed:.1f}s])")
    else:
        lines.append("    SY --> F([Final])")
    lines.append("```")
    return "\n\n<details><summary>📊 Graphe d'exécution du tour</summary>\n\n" + "\n".join(lines) + "\n\n</details>"


async def _emit_chat_meta(event_emitter, user_message: str) -> None:
    """Émet en parallèle le titre et les tags du chat (premier tour uniquement)."""
    await asyncio.gather(
        _emit_chat_title(event_emitter, user_message),
        _emit_chat_tags(event_emitter, user_message),
    )


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
            extra_body={},  # Mistral ne supporte pas enable_thinking
        )
        title = resp.choices[0].message.content.strip().strip('"\'')[:60]
        if title:
            await event_emitter({"type": "chat:title", "data": {"title": title}})
    except Exception:
        pass  # Non-bloquant — le titre n'est pas critique


async def _emit_chat_tags(event_emitter, user_message: str) -> None:
    """Génère et émet 2-4 tags thématiques pour le chat (premier tour uniquement).

    Émis via l'event `chat:tags`. Non-bloquant : les tags ne sont pas critiques.
    """
    from openai import AsyncOpenAI
    try:
        client = AsyncOpenAI(
            base_url=os.environ.get("LITELLM_URL", "http://litellm:4000/v1"),
            api_key=os.environ.get("LITELLM_API_KEY", ""),
        )
        resp = await client.chat.completions.create(
            model="openrouter/qwen3.5-flash",
            messages=[
                {"role": "system", "content": (
                    "Generate 2 to 4 short topical tags categorizing this conversation. "
                    "Lowercase, single or two words each, no '#'. "
                    "Return ONLY a JSON array of strings, e.g. [\"finance\",\"bitcoin\"]."
                )},
                {"role": "user", "content": user_message[:400]},
            ],
            max_tokens=40,
            stream=False,
            extra_body={},
        )
        raw = (resp.choices[0].message.content or "").strip()
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if not match:
            return
        tags = json.loads(match.group(0))
        tags = [str(t).strip().lstrip("#").lower()[:24] for t in tags if str(t).strip()][:4]
        if tags:
            await event_emitter({"type": "chat:tags", "data": {"tags": tags}})
    except Exception:
        pass  # Non-bloquant — les tags ne sont pas critiques


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
