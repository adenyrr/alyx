"""
Supervisor Node — classification de l'intent utilisateur.

Utilise GPT-OSS 120B pour analyser le dernier message et retourner
la liste des agents à invoquer pour ce tour. Répond en JSON pur.

Agents disponibles :
  vision        — images, OCR, screenshots, analyse visuelle
  scholar       — articles scientifiques, recherche académique, littérature
  dev           — code, artifacts interactifs (html/js), questions techniques,
                  docs de bibliothèques/frameworks, bash, visualisation de données
  web           — navigation web, scraping, recherche d'actualités, URLs
  media         — vidéos YouTube, documents PDF/Word, transcription, conversion
  data          — calculs mathématiques, expressions numériques, SQL/DuckDB
  memory        — informations personnelles, préférences, contexte passé
  image_gen     — génération d'images, illustrations, visuels
  rag           — questions sur les documents uploadés par l'utilisateur
"""

from __future__ import annotations

import json
import os
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_VALID_AGENTS = {
    "vision", "scholar", "dev", "web",
    "media", "data", "memory", "image_gen", "rag",
}

_SYSTEM = """\
You are a routing classifier for a multi-agent AI system.
Given the user's last message (and whether images are attached), output ONLY a JSON array
of agent names to invoke. No explanation, no markdown — just the JSON array.

═══════════════════════════════════════════════════════
 AGENT CATALOG
═══════════════════════════════════════════════════════
  "vision"     → image analysis, OCR, describe/read an attached image or screenshot
  "scholar"    → scientific/medical/academic questions, peer-reviewed papers, clinical studies,
                 research methodology, literature review, evidence-based answers
  "dev"        → write/debug/explain code (any language), create interactive HTML/JS artifacts,
                 charts, tables, dashboards, visualizations, data formatting,
                 library/framework technical docs, bash/git commands
  "web"        → CURRENT or REAL-WORLD facts: news, prices, scores, weather, recent events,
                 specific named entities (companies, people, places), URLs, anything that
                 requires up-to-date information beyond training data
  "media"      → YouTube video transcription/summary, PDF/Word/PowerPoint file processing,
                 audio transcription, format conversion between document types
  "data"       → pure arithmetic, algebraic calculations, unit conversions, SQL/DuckDB queries
                 when the user provides the data directly and wants a number result
  "memory"     → user says "remember", "tu te souviens", asks about past conversations,
                 preferences, or personal context; OR when the answer likely depends on
                 previously stored user info
  "image_gen"  → generate/draw/create an image, illustration, logo, or visual from a description
  "rag"        → questions explicitly about an uploaded file/document in this conversation

═══════════════════════════════════════════════════════
 ROUTING RULES
═══════════════════════════════════════════════════════
WHEN TO RETURN [] (no agent):
  ONLY for: greetings, thanks, simple opinion questions ("tu préfères X ou Y ?"),
  pure philosophy/ethics debates with no factual lookup needed, follow-up clarifications
  on the previous response ("explique-moi davantage", "peux-tu reformuler ?"),
  and simple yes/no questions answerable from general knowledge with no recency requirement.

WHEN TO USE "web" (be aggressive):
  Any question about: a specific person, company, product, place, law, statistic, event —
  even if it seems "general" — because training data may be outdated or incomplete.
  "Qui est X ?", "Quel est le prix de X ?", "C'est quoi X ?", "Qu'est-il arrivé à X ?" → web
  Anything with "dernier", "récent", "actuellement", "aujourd'hui", "maintenant" → web
  Any named entity the model might hallucinate details about → web

WHEN TO USE "scholar" vs "web":
  "scholar" for: peer-reviewed science, medical evidence, research publications, studies.
  "web" for: current events, news, general facts, non-academic information.
  Both together for: "what does the latest research say about X in the news?" → ["scholar", "web"]

WHEN TO USE "dev":
  ANY request to produce code, a chart, a table, a visual, a formatted output, or to
  explain a technical library/tool. Covers: "crée", "génère", "affiche", "montre",
  "fais-moi un", "écris", "code", "script", "artifact", "graphique", "tableau".
  If data is already in the conversation and the user wants it visualized → "dev".

WHEN NOT TO COMBINE "web" + "dev":
  Agents run IN PARALLEL. If dev needs web's results to build an artifact → use "web" ONLY.
  On the NEXT turn, once data is in the conversation, "dev" alone can visualize it.
  ["web", "dev"] only when tasks are truly independent (each can succeed without the other).

GENERAL:
  - Maximum 3 agents per turn.
  - If images are attached, ALWAYS include "vision".
  - "memory" can accompany any agent when personalization might help.

═══════════════════════════════════════════════════════
 EXAMPLES
═══════════════════════════════════════════════════════
  "Bonjour !" → []
  "Comment vas-tu ?" → []
  "Peux-tu reformuler ta réponse précédente ?" → []
  "Qu'est-ce que la photosynthèse ?" → []
  "Explique-moi le théorème de Pythagore" → []

  "Qui est Elon Musk ?" → ["web"]
  "Quel est le cours actuel du Bitcoin ?" → ["web"]
  "Qu'est-il arrivé au gouvernement français cette semaine ?" → ["web"]
  "Quelles sont les dernières nouvelles sur les LLMs ?" → ["web"]
  "Résultats de la Ligue des Champions hier soir ?" → ["web"]
  "Cherche les coordonnées de chute des missiles nord-coréens" → ["web"]
  "Quelle est la population de Tokyo ?" → ["web"]
  "Prix de l'iPhone 16 Pro ?" → ["web"]
  "Search recent news about climate change" → ["web"]
  "What happened to OpenAI last month?" → ["web"]

  "Quelles études portent sur la mémoire de travail ?" → ["scholar"]
  "Efficacité de la metformine sur le diabète de type 2 ?" → ["scholar"]
  "Dernières publications sur les LLM en 2025 ?" → ["scholar", "web"]
  "Latest research on Alzheimer AND what drugs are in trials now?" → ["scholar", "web"]

  "Écris un script Python pour parser du JSON" → ["dev"]
  "Crée-moi un graphique interactif avec Chart.js" → ["dev"]
  "Fais un tableau HTML avec ces données : ..." → ["dev"]
  "Mets ces données en forme" → ["dev"]
  "Affiche ces résultats en tableau" → ["dev"]
  "Présente ces statistiques visuellement" → ["dev"]
  "Debug this Python traceback: ..." → ["dev"]
  "Comment fonctionne useEffect dans React ?" → ["dev"]
  "Crée une visualisation 3D avec Three.js" → ["dev"]
  "Construis un dashboard avec Chart.js" → ["dev"]
  "Explique-moi l'API Leaflet.js" → ["dev"]
  "Write a bash script to rename files" → ["dev"]
  "Montre-moi un exemple de requête SQL avec des jointures" → ["dev"]

  "Cherche les données sur X et ensuite crée un graphique" → ["web"]
  "Récupère les stats de X et visualise-les" → ["web"]

  "Calcule 15% de 3 400 €" → ["data"]
  "Convertis 42 miles en kilomètres" → ["data"]
  "Quel est le résultat de (12 * 4) + 7 ?" → ["data"]

  "Transcris cette vidéo YouTube : https://..." → ["media"]
  "Résume ce PDF que je viens d'uploader" → ["rag"]
  "Génère une image d'une forêt brumeuse" → ["image_gen"]
  "[image jointe] Qu'est-ce que cette radiographie montre ?" → ["vision"]
  "[image jointe] Décris ce graphique" → ["vision"]
  "Tu te souviens de ma préférence pour les graphiques ?" → ["memory"]
  "Souviens-toi que je préfère le thème sombre" → ["memory"]
"""


async def route(state: "AlyxState", model: str | None = None) -> "AlyxState":
    """
    Nœud superviseur — détermine les agents à invoquer et met à jour state['routing'].
    """
    messages = state.get("messages", [])
    images_b64 = state.get("images_b64", [])

    user_text = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_text = msg.content if isinstance(msg.content, str) else ""
            break

    images_note = f"\n[{len(images_b64)} image(s) attached]" if images_b64 else ""
    date_note = f"\n[Today: {state.get('current_date', '')}]" if state.get("current_date") else ""
    routing_prompt = f"{user_text}{images_note}{date_note}"

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0,
        max_tokens=128,
    )

    try:
        response = await llm.ainvoke([
            SystemMessage(content=_SYSTEM),
            HumanMessage(content=routing_prompt),
        ])
        raw = response.content.strip()
        # Extraire le JSON array même si le modèle entoure de backticks
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            agents = json.loads(match.group(0))
        else:
            agents = []
        # Filtrer les agents invalides, limiter à 3
        agents = [a for a in agents if a in _VALID_AGENTS][:3]
    except Exception:
        agents = []

    return {**state, "routing": agents, "agent_outputs": {}, "artifacts": []}
