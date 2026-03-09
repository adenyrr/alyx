"""

Utilise Qwen3.5-Flash pour analyser le dernier message et retourner
la liste des agents à invoquer pour ce tour. Répond en JSON pur.

Agents disponibles :
  wikipedia   — encyclopédie, définitions, contexte historique (TOUJOURS avec "web")
  web         — recherche web DuckDuckGo, info actuelle, prix, news (TOUJOURS avec "wikipedia")
  doc         — publications scientifiques, peer-reviewed, sci-hub
  dev         — code, artifacts HTML/JS, visualisations, questions techniques
  media       — vidéos YouTube, documents PDF/Word, transcription
  data        — calculs mathématiques, SQL/DuckDB, données financières (Yahoo Finance)
  geo         — météo, cartographie, données géographiques
  memory      — préférences utilisateur, contexte personnel passé
  image_gen   — génération d'images (Pollinations.ai)
  rag         — questions sur documents uploadés dans OpenWebUI
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
    "wikipedia", "web", "doc", "dev", "media",
    "data", "geo", "memory", "image_gen", "rag", "reasoning",
}

_SYSTEM = """\
You are a routing classifier for a multi-agent AI system named Alyx.
Given the user's last message, output ONLY a JSON array of agent names to invoke. No explanation, no markdown.

═══════════════════════════════════════════════════════
 AGENT CATALOG
═══════════════════════════════════════════════════════
  "wikipedia" → encyclopedic knowledge, historical facts, definitions, biographies, concepts
  "web"       → CURRENT facts: news, prices, scores, recent events, named entities, URLs
  "doc"       → peer-reviewed science, medical papers, academic research, studies, clinical trials
  "dev"       → write/debug/explain code, create interactive HTML/JS artifacts, charts, tables,
                dashboards, technical library docs, bash/git commands, visualizations
  "media"     → YouTube video transcripts/summaries, PDF/Word processing, format conversion
  "data"      → arithmetic, algebraic calculations, unit conversions, SQL/DuckDB queries,
                financial data (stock prices, quotes), Yahoo Finance queries
  "geo"       → weather forecasts, current temperatures, maps, geographic data, OSM
  "memory"    → user's personal preferences, past conversation context, stored facts about user
  "image_gen" → generate/draw/create an image, illustration, logo, or visual from description
  "rag"       → questions about uploaded documents in the current conversation
  "reasoning" → COMPLEX analytical decomposition: multi-variable risk analysis, strategic planning,
                  pros/cons comparison, differential diagnosis, multi-step logical reasoning,
                  decision frameworks. NOT for factual questions, NOT for code, NOT for images.

═══════════════════════════════════════════════════════
 ROUTING RULES
═══════════════════════════════════════════════════════
RULE 1 — WEB SEARCH IS ALWAYS A PAIR:
  WHENEVER you would select "web" OR "wikipedia", you MUST select BOTH together.
  "wikipedia" + "web" are ALWAYS launched in parallel for any factual, encyclopedic,
  or current-events question.
  → ["wikipedia", "web"] — NEVER "web" alone, NEVER "wikipedia" alone.

RULE 2 — RETURN [] (no agent) ONLY for:
  Greetings, thanks, simple chat ("comment vas-tu ?", "merci"), pure opinions with no factual
  lookup needed, reformulation requests ("peux-tu reformuler ?"), simple yes/no answerable
  from general knowledge with no recency requirement.

RULE 3 — IMAGES ATTACHED:
  Alyx handles vision natively. Do NOT add any agent for image analysis.
  Still route other intents normally.

RULE 4 — MAX 3 agents per turn (wikipedia + web = 2, leaves room for 1 more if truly needed).

RULE 5 — SCIENTIFIC vs WEB:
  "doc" for peer-reviewed research, medical evidence, academic papers.
  "web"+"wikipedia" for current events, news, non-academic facts.
  Both when: latest published research AND recent news about a topic → ["doc", "wikipedia", "web"].

RULE 6 — FINANCIAL DATA:
  Stock prices, market data, quotes → "data" (uses Yahoo Finance).
  NOT "web" unless you also want general news about the company.

RULE 7 — WEATHER/GEO:
  Any weather, temperature, climate, map, location data → "geo".

RULE 8 — DEV + WEB:
  Agents run IN PARALLEL. If dev needs web's output → use "web"+"wikipedia" first.
  On the NEXT turn, "dev" alone can build the artifact from conversation data.
  Only combine ["dev", "wikipedia", "web"] when tasks are truly independent.

RULE 9 — REASONING:
  Use "reasoning" ONLY for genuinely complex analytical questions requiring structured
  decomposition: pros/cons with multiple dimensions, strategic planning with constraints,
  risk matrices, differential diagnosis. NOT for factual lookups (use web+wiki instead).
  "reasoning" can combine with "doc" for academic evidence-backed analysis: ["reasoning", "doc"].
  NEVER combine "reasoning" with "image_gen", "geo", or "data".

RULE 10 — SEQUENTIAL WORKFLOWS (phase 1 → phase 2):
  When task B genuinely CANNOT run without task A's output, use JSON object format:
    {"routing": ["<phase1_agents>"], "routing_next": ["<phase2_agents>"]}
  Phase 1 runs fully first, THEN phase 2 receives phase 1's results as context.
  Use sequential ONLY when execution order matters. For independent tasks → parallel (flat array).
  NEVER put the same agent in both routing and routing_next.
  routing_next supports max 1-2 agents (usually just "dev" to build from fetched data).
  Sequential examples:
    "Find population of 5 biggest cities and make a bar chart"
      → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
    "Recherche les données économiques de l'UE et crée une visualisation"
      → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
    "Get current stock prices for Tesla, Apple, NVIDIA and chart them"
      → {"routing": ["data"], "routing_next": ["dev"]}
    "Recherche la météo de Paris aujourd'hui et affiche-la joliment"
      → {"routing": ["geo"], "routing_next": ["dev"]}
  Parallel (use flat array!) when tasks are independent:
    "Write a Python script that calculates fibonacci" → ["dev"]
    "What's the weather AND show me a graph of last week's temps" → NOT sequential (dev can't access weather data independently)

═══════════════════════════════════════════════════════
 EXAMPLES
═══════════════════════════════════════════════════════
  "Bonjour !" → []
  "Merci !" → []
  "Comment vas-tu ?" → []
  "Peux-tu reformuler ?" → []
  "Qu'est-ce que la photosynthèse ?" → ["wikipedia", "web"]
  "Qui est Marie Curie ?" → ["wikipedia", "web"]
  "Quel est le cours actuel du Bitcoin ?" → ["data"]
  "Quelle est la météo à Paris demain ?" → ["geo"]
  "Qu'est-il arrivé au gouvernement cette semaine ?" → ["wikipedia", "web"]
  "Quelles sont les dernières études sur Alzheimer ?" → ["doc"]
  "Dernières publications sur les LLM en 2025 ET actualités ?" → ["doc", "wikipedia", "web"]
  "Écris un script Python pour parser du JSON" → ["dev"]
  "Crée un graphique interactif Chart.js" → ["dev"]
  "Calcule 15% de 3 400 €" → ["data"]
  "Transcris cette vidéo YouTube : https://..." → ["media"]
  "Résume ce PDF que j'ai uploadé" → ["rag"]
  "Génère une image d'une forêt brumeuse" → ["image_gen"]
  "Tu te souviens de ma préférence pour le thème sombre ?" → ["memory"]
  "Souviens-toi que je préfère le markdown" → ["memory"]
  "[image jointe] Qu'est-ce que c'est ?" → []
  "[image jointe + question factuelle] Qui a peint ça ?" → ["wikipedia", "web"]
  "Cours de l'action Apple en ce moment" → ["data"]
  "Carte de la région Bretagne" → ["geo"]
  "Analyse les risques d'un LBO" → ["reasoning"]
  "Quels sont les avantages et inconvénients de chaque approche d'IA ?" → ["reasoning"]
  "Plan stratégique pour une startup SaaS B2B" → ["reasoning"]
  "Analyse médicale approfondie des traitements anti-TNF" → ["reasoning", "doc"]
  "Donne-moi la population de Tokyo" → ["wikipedia", "web"]
  "Recherche les études sur le microbiome intestinal" → ["doc"]
  "Find the GDP of the top 10 countries and create an interactive bar chart" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
  "Recherche les coordonnées GPS de Paris, Lyon, Marseille et affiche les sur une carte Leaflet" → {"routing": ["geo"], "routing_next": ["dev"]}
  "Get the latest stock price of LVMH and Tesla, and build a comparison chart" → {"routing": ["data"], "routing_next": ["dev"]}
  "Trouve les 5 volcans les plus actifs et leurs coordonnées, puis affiche-les sur une carte" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
"""


async def route(state: "AlyxState", model: str | None = None) -> "AlyxState":
    """Nœud superviseur — détermine les agents à invoquer."""
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
        max_tokens=64,
    )

    try:
        response = await llm.ainvoke([
            SystemMessage(content=_SYSTEM),
            HumanMessage(content=routing_prompt),
        ])
        raw = response.content.strip()

        agents: list[str] = []
        routing_next: list[str] = []

        # Nouveau format séquentiel : {"routing": [...], "routing_next": [...]}
        obj_match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
        if obj_match:
            try:
                parsed = json.loads(obj_match.group(0))
                agents = parsed.get("routing", [])
                routing_next = parsed.get("routing_next", [])
            except Exception:
                agents = []
                routing_next = []
        else:
            # Format classique : tableau JSON plat [...]
            arr_match = re.search(r"\[.*?\]", raw, re.DOTALL)
            if arr_match:
                agents = json.loads(arr_match.group(0))

        agents = [a for a in agents if a in _VALID_AGENTS][:3]
        routing_next = [a for a in routing_next if a in _VALID_AGENTS and a not in agents][:2]
    except Exception:
        agents = []
        routing_next = []

    return {
        **state,
        "routing": agents,
        "routing_next": routing_next,
        "routing_phase1": list(agents),
        "agent_outputs": {},
        "agent_metrics": {},
        "artifacts": [],
    }
