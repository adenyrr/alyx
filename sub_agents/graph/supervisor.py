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
    "data", "geo", "memory", "image_gen", "rag", "reasoning", "writer", "presenter",
    "translator", "summarizer", "vision", "mindmap", "diagram",
    "spreadsheet", "code_exec", "fact_checker", "audio",
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
  "writer"    → LONG-FORM DOCUMENT AUTHORING in prose: business reports, technical RFCs,
                  academic papers, whitepapers, meeting minutes, blog posts, press releases,
                  cover letters, CVs, professional emails. Produces structured Markdown
                  (optionally converted to .docx/.tex/.epub via pandoc if explicitly requested).
                  Use writer when the user asks to "rédige", "compose", "write a report/letter/email",
                  "draft a document", "prepare a memo", or mentions a specific document type.
                  NOT for short conversational replies (Alyx handles those), NOT for code (use dev).
  "presenter" → SLIDE DECKS / PRESENTATIONS as reveal.js HTML: pitch decks, lecture
                  slides, slideshows, "présentation", "diaporama", "slides", "pitch deck".
                  Produces a self-contained reveal.js artifact. Use presenter (not dev) whenever
                  the deliverable is a multi-slide presentation. NOT for single charts/dashboards
                  (use dev), NOT for long-form prose documents (use writer).
  "translator" → translate a quoted text / code block / paragraph from/to a target language.
                  Triggers: "traduis", "translate", "traducción", "übersetze", "en anglais",
                  "to French", "in Spanish", etc. NOT for general multilingual answers
                  (Alyx already replies in the user's language).
  "summarizer" → summarize a URL, an inline long text, or an uploaded document.
                  Triggers: "résume", "summarize", "TL;DR", "fais-moi un résumé de…".
                  Use over web/doc when the goal is condensation, not retrieval.
  "vision"     → in-depth image analysis: OCR, chart reading (extract data),
                  diagram interpretation, object counting, document structure. Use when
                  an image is attached AND the user explicitly asks for analysis beyond
                  what Alyx's native vision can do (e.g. "extract the data from this chart").
  "mindmap"    → mind maps (markmap.js) — hierarchical tree of ideas/concepts.
                  Triggers: "carte mentale", "mindmap", "mind map", "arbre conceptuel".
  "diagram"    → diagrams: flowchart, sequence, class, ER, state machine, network topology,
                  whiteboard sketches. Auto-picks mermaid/jointjs/excalidraw based on type.
                  Triggers: "diagramme", "flowchart", "schéma", "UML", "BPMN", "topology".
  "spreadsheet" → produce a downloadable XLSX file (multi-sheet, headers, data).
                  Triggers: ".xlsx", "Excel", "tableur", "feuille de calcul", "spreadsheet".
                  Use spreadsheet (not data) when the user wants a FILE, not an inline table.
  "code_exec"  → ACTUAL Python execution (not just describing the algorithm).
                  Triggers: "exécute", "run this", "compute", "what's the result of",
                  any task requiring real computation. Sandbox via open-terminal.
                  Use over data when real computation is required, not just a description.
  "fact_checker" → adversarial verification of claims (web search + LLM critic). RARELY
                  invoked directly by the user — usually auto-wired via the critic loop
                  valve. User trigger: "vérifie ces affirmations", "fact-check".
  "audio"      → transcription of attached audio files (requires Whisper service).
                  Auto-invoked when audios_b64 is present in the state.

═══════════════════════════════════════════════════════
 ROUTING RULES
═══════════════════════════════════════════════════════
RULE 1 — WEB vs WIKIPEDIA : pick the right one based on the question's nature.
  Both can be used together when the user asks for COMPREHENSIVE coverage, but
  it's no longer mandatory. Pick by intent :

  USE "web" ALONE when :
    - The question is about CURRENT events, news, recent (≤ 2 years), prices,
      schedules, scores, releases, announcements, latest versions.
    - The question targets a specific URL or recent online resource.
    - The entity is too niche / too recent for Wikipedia coverage.
    Examples : "actualité X", "dernière version de Y", "prix de Z aujourd'hui",
    "que s'est-il passé cette semaine".

  USE "wikipedia" ALONE when :
    - The question is HISTORICAL, ENCYCLOPEDIC, biographical, conceptual.
    - The topic is stable and well-documented (≥ 5 ans d'histoire).
    - You need a definition, a concept overview, a person's biography.
    Examples : "qui était Marie Curie", "qu'est-ce que la photosynthèse",
    "histoire de Rome", "définition de la dialectique".

  USE BOTH (parallel) ONLY when :
    - The user explicitly demands a comprehensive answer combining historical
      context AND current news.
    - The topic spans both : "X aujourd'hui ET dans l'histoire", "actualité de
      cette personne célèbre".
    - The supervisor genuinely can't decide between historical and current —
      DEFAULT to both rather than risk missing context.

  Examples :
    "Bitcoin price now"                → ["web"]
    "What is the Higgs boson?"         → ["wikipedia"]
    "Who is Marie Curie?"              → ["wikipedia"]
    "Latest news about NASA"           → ["web"]
    "Compare ChatGPT and Claude"       → ["web", "wikipedia"]
    "History of OpenAI and recent funding" → ["web", "wikipedia"]

RULE 1bis — DATA RELIABILITY :
  When a single-agent web call answers a FACTUAL question with stakes
  (medical, legal, financial, scientific claims), the fact_checker MAY be
  auto-triggered by the pipeline (valve `enable_critic_loop` or auto-trigger
  on low confidence). You don't need to add it explicitly — just route to web
  and let the reliability layer kick in if needed.

RULE 2 — RETURN [] (no agent) ONLY for:
  Greetings, thanks, simple chat ("comment vas-tu ?", "merci"), pure opinions with no factual
  lookup needed, reformulation requests ("peux-tu reformuler ?"), simple yes/no answerable
  from general knowledge with no recency requirement.

RULE 3 — IMAGES ATTACHED:
  Alyx handles vision natively. Do NOT add any agent for image analysis.
  Still route other intents normally.

RULE 4 — MAX 4 agents per turn. Default to ≤ 3, but allow 4 for genuinely composed
  queries (e.g. "actualités + études + visualisation" → ["web","wikipedia","doc","dev"]).
  Use the 4th slot ONLY when each agent brings distinct value the others can't supply.

RULE 5 — SCIENTIFIC vs WEB:
  "doc" for peer-reviewed research, medical evidence, academic papers.
  "web"+"wikipedia" for current events, news, non-academic facts.
  Both when: latest published research AND recent news about a topic → ["doc", "wikipedia", "web"].

RULE 6 — FINANCIAL DATA:
  Stock prices, market data, quotes → "data" (uses Yahoo Finance).
  NOT "web" unless you also want general news about the company.

RULE 7 — WEATHER/GEO:
  Any weather, temperature, climate, map, location data → "geo".

RULE 8 — DEV depends on data sourced by another agent:
  Use the SEQUENTIAL workflow (routing + routing_next) — NEVER ask the user to split
  into two manual turns. Pattern:
    {"routing": ["web","wikipedia"], "routing_next": ["dev"]}
    {"routing": ["data"],            "routing_next": ["dev"]}
    {"routing": ["geo"],             "routing_next": ["dev"]}
  Only put dev in `routing` (parallel) when its work is independent of other agents
  in the same phase (e.g. "écris un script python" → ["dev"] alone).

RULE 9 — REASONING:
  Use "reasoning" ONLY for genuinely complex analytical questions requiring structured
  decomposition: pros/cons with multiple dimensions, strategic planning with constraints,
  risk matrices, differential diagnosis. NOT for factual lookups (use web+wiki instead).
  "reasoning" can combine with "doc" for academic evidence-backed analysis: ["reasoning", "doc"].
  NEVER combine "reasoning" with "image_gen", "geo", or "data".

RULE 10b — WRITER COMBINATIONS:
  "writer" is often the SECOND phase of a sequential workflow that collects facts first.
  Common patterns:
    "Rédige un rapport business sur X" (no prior research needed) → ["writer"]
    "Compose un mémo stratégique sur ce SWOT" → {"routing": ["reasoning"], "routing_next": ["writer"]}
    "Écris une revue de littérature sur Y" → {"routing": ["doc"], "routing_next": ["writer"]}
    "Prépare un rapport data avec les chiffres de ventes" → {"routing": ["data"], "routing_next": ["writer"]}
    "Press release sur l'actualité X" → {"routing": ["web", "wikipedia"], "routing_next": ["writer"]}
  Use writer ALONE when the user gives all the facts in the message.
  Use writer in phase 2 when facts must be fetched first (doc, web, data, reasoning).

RULE 10c — FILE FORMAT TRIGGERS WRITER (CRITICAL):
  ANY mention of a target file format in the user message MUST trigger writer (alone
  or as phase 2 of a sequential workflow). The writer agent is the ONLY component
  wired to the pandoc MCP server — without writer in the routing, no file conversion
  happens and the conversation degrades to "I can't generate DOCX/PPTX" excuses.
  File-format trigger keywords (any language): ".docx", ".pptx", ".odt", ".epub",
  ".tex", ".rtf", ".html" (when document, not page), "format Word/DOCX/PPTX/PowerPoint/EPUB/LaTeX",
  "fichier Word/PowerPoint", "as PDF/DOCX/PPTX/EPUB", "en DOCX/PPTX/LaTeX/EPUB/RTF/Word/PowerPoint",
  "document Word", "présentation PowerPoint".
  Routing pattern when factual research is also needed:
    "Synthèse Hantavirus en docx" → {"routing": ["doc"], "routing_next": ["writer"]}
    "Compile la météo des 5 capitales en .docx" → {"routing": ["geo"], "routing_next": ["writer"]}
    "Rapport sur Bitcoin en format Word" → {"routing": ["data"], "routing_next": ["writer"]}
    "Article LinkedIn sur l'IA en .epub" → {"routing": ["web", "wikipedia"], "routing_next": ["writer"]}
  Routing pattern when no research is needed:
    "Convertis ce CV en .docx" → ["writer"]
    "Génère-moi un .docx vide structuré pour un rapport business" → ["writer"]

  PPTX SPECIAL CASE — DUAL ROUTING (presenter + writer in PARALLEL):
  When the user asks for a presentation/slide deck AS .pptx (or "PowerPoint"),
  route to BOTH `presenter` AND `writer` IN THE SAME PHASE (flat array). Why:
    - `presenter` produces a reveal.js HTML deck rendered INLINE for instant preview.
    - `writer` produces a slide-mode Markdown that pandoc converts to a real,
      downloadable .pptx file. The two outputs are independent and complementary.
  Examples:
    "Fais-moi une présentation PowerPoint sur X" → ["presenter", "writer"]
    "Un deck pptx avec les chiffres fictifs DNS" → ["presenter", "writer"]
    "Slides pptx sur l'IA générative" → ["presenter", "writer"]
  If research is ALSO needed first → phase 1 fetches data, phase 2 = both:
    "Recherche les ventes Tesla 2024 et fais-en un pptx" → {"routing": ["data"], "routing_next": ["presenter", "writer"]}
    "Veille IA et présente-la en pptx" → {"routing": ["web", "wikipedia"], "routing_next": ["presenter", "writer"]}

  NEVER omit writer when a file format is mentioned. NEVER route only to a research
  agent (doc/data/web/wiki) when the user asks for a specific file format — the
  research output won't be wrapped in a downloadable document.

RULE 11b — AUTO-VISUALISATION (proposer un artifact SANS demande explicite) :
  Quand la réponse se prête NATURELLEMENT à un visuel interactif, ajoute `dev`
  en phase 2 (routing_next) MÊME si l'utilisateur·rice ne l'a pas demandé. Ne
  réclame jamais un second tour manuel. Déclenche sur ces SIGNAUX FORTS :
    • LIEUX / GÉOGRAPHIE → carte Leaflet : « lieux à visiter », « que voir à X »,
      « restaurants/musées/itinéraire à X », adresses, coordonnées, « sur une
      carte ». La phase 1 (web/wikipedia/geo) fournit les lieux ; dev en fait
      une carte interactive avec marqueurs.
    • COMPARATIF → tableau/chart : « compare X et Y », « versus », « différences
      entre », « X ou Y ? », classement, « top 5/10 », palmarès.
    • SÉRIES CHIFFRÉES → graphe : évolution, statistiques, parts de marché,
      données quantifiées multiples, « répartition de ».
    • CHRONOLOGIE → frise (vis-timeline) : « chronologie de X », « frise »,
      « les grandes dates de », histoire datée d'événements successifs.
    • PLANNING / DATES À VENIR → calendrier : « planning », « agenda »,
      « programme de la semaine », « emploi du temps ».
  Patterns :
    "Lieux à visiter à Tournai" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
    "Que voir à Kyoto + restos renommés" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
    "Compare l'iPhone 16 et le Pixel 9" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
    "Top 10 des pays par PIB" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
  N'ajoute PAS dev pour : définitions simples, biographies, questions oui/non,
  opinions, explications conceptuelles, ou quand la phase 1 est elle-même un
  livrable visuel (presenter/mindmap/diagram). En cas de doute → ne PAS ajouter
  dev (Alyx proposera l'artifact en fin de réponse, l'utilisateur·rice validera).

RULE 11 — SEQUENTIAL WORKFLOWS (phase 1 → phase 2):
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
  "Qu'est-ce que la photosynthèse ?" → ["wikipedia"]
  "Qui est Marie Curie ?" → ["wikipedia"]
  "Histoire de Rome" → ["wikipedia"]
  "Définition de la dialectique" → ["wikipedia"]
  "Quel est le cours actuel du Bitcoin ?" → ["data"]
  "Quelle est la météo à Paris demain ?" → ["geo"]
  "Qu'est-il arrivé au gouvernement cette semaine ?" → ["web"]
  "Actualité de la mission Artemis" → ["web"]
  "Dernière version de Python" → ["web"]
  "Compare ChatGPT et Claude (positionnement et derniers tarifs)" → ["wikipedia", "web"]
  "Bitcoin : son histoire ET son cours actuel" → ["wikipedia", "web", "data"]
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
  "[image jointe + question factuelle] Qui a peint ça ?" → ["wikipedia"]
  "Cours de l'action Apple en ce moment" → ["data"]
  "Carte de la région Bretagne" → ["geo"]
  "Analyse les risques d'un LBO" → ["reasoning"]
  "Quels sont les avantages et inconvénients de chaque approche d'IA ?" → ["reasoning"]
  "Plan stratégique pour une startup SaaS B2B" → ["reasoning"]
  "Analyse médicale approfondie des traitements anti-TNF" → ["reasoning", "doc"]
  "Donne-moi la population de Tokyo" → ["wikipedia"]
  "Population de Tokyo et croissance récente" → ["wikipedia", "web"]
  "Lieux à visiter à Tournai, incontournables et restos renommés" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
  "Que voir à Kyoto en 3 jours ?" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
  "Compare l'iPhone 16 et le Pixel 9" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
  "Top 10 des pays par PIB" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
  "Recherche les études sur le microbiome intestinal" → ["doc"]
  "Find the GDP of the top 10 countries and create an interactive bar chart" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
  "Recherche les coordonnées GPS de Paris, Lyon, Marseille et affiche les sur une carte Leaflet" → {"routing": ["geo"], "routing_next": ["dev"]}
  "Get the latest stock price of LVMH and Tesla, and build a comparison chart" → {"routing": ["data"], "routing_next": ["dev"]}
  "Trouve les 5 volcans les plus actifs et leurs coordonnées, puis affiche-les sur une carte" → {"routing": ["web", "wikipedia"], "routing_next": ["dev"]}
  "Rédige-moi une lettre de motivation pour ce poste" → ["writer"]
  "Compose un email professionnel pour décliner une réunion" → ["writer"]
  "Écris un CV de développeur senior en Markdown" → ["writer"]
  "Prépare un compte-rendu de réunion structuré" → ["writer"]
  "Rédige un rapport business sur le marché des EV en .docx" → ["writer"]
  "Synthétise une revue de littérature sur Alzheimer en rapport académique" → {"routing": ["doc"], "routing_next": ["writer"]}
  "SWOT du marché du SaaS B2B puis transforme-le en mémo stratégique" → {"routing": ["reasoning"], "routing_next": ["writer"]}
  "Récupère les chiffres de vente Tesla 2024 et fais un rapport investisseur" → {"routing": ["data"], "routing_next": ["writer"]}
  "Press release sur la nouvelle réglementation européenne sur l'IA" → {"routing": ["web", "wikipedia"], "routing_next": ["writer"]}
  "Crée une présentation sur l'histoire de Rome" → ["presenter"]
  "Fais-moi un pitch deck pour ma startup SaaS" → ["presenter"]
  "Prépare un diaporama de cours sur la photosynthèse" → ["presenter"]
  "Recherche les chiffres du marché EV 2024 et fais-en une présentation" → {"routing": ["web", "wikipedia"], "routing_next": ["presenter"]}
  "Récupère les ventes Tesla et présente-les en slides" → {"routing": ["data"], "routing_next": ["presenter"]}
  "Fais-moi une présentation pptx avec des données fictives" → ["presenter", "writer"]
  "Pitch deck pptx sur ma startup SaaS" → ["presenter", "writer"]
  "Recherche les chiffres du marché EV 2024 et fais-en un pptx" → {"routing": ["web", "wikipedia"], "routing_next": ["presenter", "writer"]}
  "Traduis ce texte en anglais : « ... »" → ["translator"]
  "Résume cet article : https://example.com/long-post" → ["summarizer"]
  "Résume mon PDF importé" → ["summarizer"]
  "Extrais les données de ce graphique [image jointe]" → ["vision"]
  "OCR ce document [image jointe]" → ["vision"]
  "Carte mentale de la révolution française" → ["mindmap"]
  "Flowchart du process de commande" → ["diagram"]
  "Diagramme de séquence login OAuth" → ["diagram"]
  "Topologie réseau d'un Kubernetes cluster" → ["diagram"]
  "Génère un .xlsx avec 3 feuilles : ventes, marges, prévisions" → ["spreadsheet"]
  "Calcule la moyenne de [1, 2, 3, ..., 100] et exécute le code" → ["code_exec"]
  "Combien font 234 * 567 ? Calcule réellement" → ["code_exec"]
  "Vérifie les affirmations de mon dernier message" → ["fact_checker"]
  "Transcris cet audio [audio joint]" → ["audio"]
  "Récupère les données du marché EV et fais-en un tableau Excel" → {"routing": ["web", "wikipedia"], "routing_next": ["spreadsheet"]}
  "Compile une mindmap des concepts de ce papier scientifique" → {"routing": ["doc"], "routing_next": ["mindmap"]}
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

        # Cap aligné avec RULE 4 (max 4 agents par phase). routing_next plafonné à 3
        # car les workflows composés (e.g. presenter+writer+fact_checker) en bénéficient.
        agents = [a for a in agents if a in _VALID_AGENTS][:4]
        routing_next = [a for a in routing_next if a in _VALID_AGENTS and a not in agents][:3]
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
