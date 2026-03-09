# OpenWebUI — Stack LLM complète

Stack d'inférence LLM auto-hébergée construite autour d'OpenWebUI, LiteLLM, LangGraph et un ensemble de services d'outils. Le point central est **Alyx**, un agent conversationnel en français qui orchestre 10 sous-agents spécialisés de façon transparente.

---

## Sommaire

1. [Architecture](#architecture)
2. [Services](#services)
3. [Installation](#installation)
4. [Alyx — agent principal](#alyx--agent-principal)
5. [Sous-agents](#sous-agents)
6. [Skills](#skills)
7. [Personnalisation](#personnalisation)
8. [Vérification](#vérification)

---

## Architecture

```
Utilisateur → OpenWebUI :3721
                 │
                 ├── LiteLLM :4000/v1     ← tous les modèles LLM (OpenRouter, Pollinations…)
                 └── Pipelines :9099      ← "Alyx" (LangGraph multi-agent)
                          │
                            └── LangGraph Supervisor (Qwen 3.5 Flash)
                                ├─ vision      qwen/qwen3.5-flash     images, OCR
                                ├─ scholar     GPT-OSS 120B           papers, wikipedia
                              ├─ dev         kimi-k2.5              code, artifacts, Context7, bash, skills
                              ├─ web         GPT-OSS 120B           playwright MCP HTTP
                                ├─ media       GPT-OSS 120B           youtube, pdf, pandoc
                                ├─ data        GPT-OSS 120B           calcul, duckdb
                                ├─ memory      GPT-OSS 120B           knowledge graph MCPO
                                ├─ image_gen   pollinations/flux       génération images
                                └─ rag         GPT-OSS 120B           Qdrant (docs uploadées)

Outils (accès depuis Pipelines via clients internes) :
  MCPO :8000     → paper-search, wikipedia, sequential-thinking,
                   youtube-transcript, markitdown, pandoc,
                   calculator, duckdb, memory, git
  Playwright     → MCP HTTP :8931  (outil natif OpenWebUI, Streamable HTTP)
  Context7       → cloud public https://mcp.context7.com/mcp
  open-terminal  → bash REST :8000
  Qdrant         → vector DB :6333
  LiteLLM        → proxy LLM unifié :4000
```

---

## Services

| Service | Image | Port exposé | Rôle |
|---|---|---|---|
| `open-webui` | `ghcr.io/open-webui/open-webui:main` | 3721 | Interface utilisateur |
| `pipelines` | `ghcr.io/open-webui/pipelines:main` | — (interne 9099) | Alyx / LangGraph |
| `litellm` | `ghcr.io/berriai/litellm:main-latest` | 4000 | Proxy LLM (OpenRouter, Pollinations…) |
| `postgres` | `postgres:16-alpine` | — | BDD principale (openwebui, litellm, langgraph) |
| `redis` | `redis:7-alpine` | — | Cache (DB0: OpenWebUI, DB1: LiteLLM) |
| `qdrant` | `qdrant/qdrant:latest` | — | Vector store (RAG) |
| `mcpo` | `ghcr.io/open-webui/mcpo:main` | 3722 | Proxy MCP→REST pour les outils |
| `playwright` | `mcr.microsoft.com/playwright/mcp:latest` | — (interne 8931) | Navigateur Chromium (MCP Streamable HTTP) |
| `tika` | `apache/tika:latest-full` | — | Parsing documents (PDF, Word…) |
| `open-terminal` | `ghcr.io/open-webui/open-terminal` | — | Terminal bash sandboxé |

### Volumes

| Volume | Contenu |
|---|---|
| `open-webui` | Données OpenWebUI (chats, modèles, users) |
| `postgres_data` | Bases PostgreSQL (openwebui, litellm, langgraph) |
| `qdrant_storage` | Index vectoriels Qdrant |
| `redis_data` | Cache Redis persistant |
| `mcp_memory` | Knowledge graph (MCPO memory) |
| `mcp_duckdb` | Base DuckDB analytique |
| `mcp_uploads` | Fichiers uploadés via OpenWebUI |
| `mcp_exports` | Exports générés |
| `mcp_papers` | Cache recherche académique |
| `open_terminal_data` | Workspace terminal utilisateur |

---

## Installation

### Prérequis

- Docker + Docker Compose v2
- Réseau Docker externe `llm-network` : `docker network create llm-network`
- Clé API OpenRouter (obligatoire pour Alyx)

### 1. Copier et remplir les variables d'environnement

```bash
cp example.env .env
$EDITOR .env
```

Variables **obligatoires** :

| Variable | Description |
|---|---|
| `WEBUI_SECRET_KEY` | Clé secrète OpenWebUI (valeur aléatoire) |
| `PG_PASS` | Mot de passe PostgreSQL |
| `PG_USER` | Utilisateur PostgreSQL |
| `QDRANT_API_KEY` | Clé Qdrant (valeur aléatoire) |
| `LITELLM_MASTER_KEY` | Clé maître LiteLLM (format `sk-…`) |
| `LITELLM_SALT_KEY` | Sel LiteLLM (valeur aléatoire) |
| `OPENROUTER_API_KEY` | Clé OpenRouter (modèles Alyx) |
| `PIPELINES_API_KEY` | Clé d'authentification Pipelines (valeur aléatoire) |
| `OPEN_TERMINAL_API_KEY` | Clé terminal bash (valeur aléatoire) |

Variables **optionnelles** :

| Variable | Description |
|---|---|
| `POLLINATIONS_API_KEY` | Génération d'images (gratuit sans clé) |
| `CONTEXT7_API_KEY` | Améliore le rate-limit Context7 cloud |
| `PUBMED_API_KEY` | Rate-limit PubMed étendu (3→10 req/s) |
| `SEMANTIC_SCHOLAR_API_KEY` | Quotas Semantic Scholar étendus |
| `WOS_API_KEY` | Accès Web of Science (paper-search) |

### 2. Créer le réseau Docker et démarrer

```bash
docker network create llm-network
docker compose up -d
```

Au premier démarrage, PostgreSQL exécute automatiquement les scripts d'init :
- `postgres-init/01-create-litellm-db.sql` — crée la base `litellm`
- `postgres-init/02-create-langgraph-db.sql` — crée la base `langgraph` (checkpoints Alyx)

### 3. Connecter Pipelines à OpenWebUI

1. Ouvrir **OpenWebUI → Admin Panel → Settings → Connections**
2. Ajouter une connexion OpenAI :
   - URL : `http://pipelines:9099`
   - Clé : valeur de `PIPELINES_API_KEY`
3. Cliquer **Save** — le modèle **Alyx** apparaît dans le sélecteur

> **Note** : `OPENAI_API_BASE_URLS` dans le compose est déjà configuré avec les deux sources
> (`litellm:4000/v1` et `pipelines:9099`). Si OpenWebUI est configuré via cette variable
> d'environnement, l'étape manuelle ci-dessus peut ne pas être nécessaire selon la version.

### 4. Connecter les outils MCP natifs à OpenWebUI

OpenWebUI se connecte directement aux serveurs MCP via HTTP :

| Outil | URL |
|---|---|
| Playwright (navigation web) | `http://playwright:8931` |

**Admin Panel → Settings → Tools → MCP Servers** → ajouter l'URL du serveur MCP.

> MCPO expose les autres outils (paper-search, memory, duckdb…) via OpenAPI REST sur
> `http://mcpo:8000` — configuré automatiquement via `MCP_SERVER_BASE_URL`.

---

## Structure des fichiers

```
openwebui/
├── compose.yaml              Services Docker
├── example.env               Variables d'environnement (template)
├── litellm_config.yaml       Configuration LiteLLM (modèles)
├── mcpo_config.json          Configuration MCPO (serveurs MCP)
├── skills/                   Guides de bibliothèques pour l'agent Dev
│   ├── animejs.md
│   ├── bulma.md
│   └── … (24 fichiers)
├── sub_agents/               Code source pipeline Alyx (LangGraph)
│   ├── alyx_pipeline.py      Point d'entrée OpenWebUI Pipelines
│   ├── graph/
│   │   ├── state.py          AlyxState — état partagé du graphe
│   │   ├── supervisor.py     RouterNode — classification de l'intent
│   │   └── builder.py        Assemblage StateGraph + PostgresSaver
│   ├── agents/               10 sous-agents spécialisés
│   │   ├── vision.py
│   │   ├── scholar.py
│   │   ├── dev.py
│   │   ├── web.py
│   │   ├── media.py
│   │   ├── data.py
│   │   ├── memory_agent.py
│   │   ├── image_gen.py
│   │   └── rag_agent.py
│   └── tools/                Clients HTTP/MCP pour les services externes
│       ├── mcpo_client.py    Client MCPO (outils via REST)
│       ├── rag_client.py     Client Qdrant (RAG)
│       ├── context7_client.py Client Context7 (docs bibliothèques)
│       ├── playwright_client.py Client Playwright (MCP Streamable HTTP)
│       └── terminal_client.py  Client open-terminal (bash)
└── postgres-init/
    ├── 01-create-litellm-db.sql
    └── 02-create-langgraph-db.sql
```

---

## Alyx — agent principal

**Modèle** : `openrouter/openai/gpt-oss-120b`  
**Langue** : français exclusivement  
**Accès outils** : aucun (contexte allégé — délègue tout aux sous-agents)

Alyx reçoit le message de l'utilisateur, lance le **Superviseur LangGraph** qui identifie les sous-agents pertinents (max 3 par tour), attend leurs résultats, puis rédige une réponse synthétique en français.

Les status intermédiaires (`[📷 Vision en cours…]`) sont émis en streaming via `__event_emitter__` et apparaissent dans le chat OpenWebUI.

Après chaque réponse, une tâche de **condensation mémoire** tourne en arrière-plan (`asyncio.create_task`) : les 3 derniers tours sont résumés en bullet facts et stockés dans le knowledge graph MCPO.

La **persistance multi-tours** est assurée par LangGraph via la base `langgraph` dans PostgreSQL (table `checkpoints`, clé = `chat_id` OpenWebUI).

---

## Sous-agents

### 📷 Vision — `agents/vision.py`
**Modèle** : `openrouter/qwen/qwen3.5-flash`  
**Invoqué quand** : une image est jointe à la conversation  
**Capacités** : description détaillée, OCR, analyse de graphiques, lecture de screenshots, identification d'objets

### 🔬 Scholar — `agents/scholar.py`
**Modèle** : `openrouter/openai/gpt-oss-120b`  
**Invoqué quand** : question scientifique, littérature, études, citations  
**Outils MCPO** : `paper-search` (14 plateformes : arXiv, PubMed, Semantic Scholar…), `wikipedia`, `sequential-thinking`

### ⚙️ Dev — `agents/dev.py`
**Modèle** : `openrouter/moonshotai/kimi-k2.5`  
**Invoqué quand** : génération de code, création d'artifacts interactifs, documentation technique, commandes bash, visualisations  
**Sources** : skills locaux (`skills/*.md`), Context7 cloud, terminal bash (open-terminal), outil Git via MCPO  
**Fonctionnement** : fusion de l'ancien Coder et de l'ancien Tech. L'agent charge les skills correspondant à la bibliothèque mentionnée, interroge Context7 pour la doc officielle en temps réel, peut exécuter des commandes de vérification d'environnement et produire des artifacts HTML/JS/Python.

### 🌐 Web — `agents/web.py`
**Modèle** : `openrouter/openai/gpt-oss-120b`  
**Invoqué quand** : navigation vers une URL, recherche web, actualités  
**Outil** : Playwright (navigateur Chromium réel, connexion MCP directe sur `http://playwright:8931`)  
**Comportement** : si une URL est présente → navigue directement ; sinon → recherche DuckDuckGo

### 🎬 Media — `agents/media.py`
**Modèle** : `openrouter/openai/gpt-oss-120b`  
**Invoqué quand** : URL YouTube, document PDF/Word à analyser, conversion de format  
**Outils MCPO** : `youtube-transcript`, `markitdown` (PDF/Word/Excel→Markdown), `pandoc` (conversions)

### 📊 Data — `agents/data.py`
**Modèle** : `openrouter/openai/gpt-oss-120b`  
**Invoqué quand** : calcul mathématique, expression numérique, requête SQL  
**Outils MCPO** : `calculator` (évaluation Python complète), `duckdb` (base analytique CSV/Parquet)

### 🧠 Memory — `agents/memory_agent.py`
**Modèle** : `openrouter/openai/gpt-oss-120b`  
**Invoqué quand** : rappel de préférences, contexte passé, informations personnelles  
**Outil MCPO** : `memory` (knowledge graph JSON persistant dans `mcp_memory`)  
**Mode background** : `run_bg()` condense automatiquement chaque conversation en bullet facts sans bloquer la réponse

### 🎨 ImageGen — `agents/image_gen.py`
**Modèle** : `pollinations/flux` (klein-large) via LiteLLM  
**Invoqué quand** : génération d'image, illustration, visuel  
**Endpoint** : `POST /v1/images/generations` → LiteLLM → `https://gen.pollinations.ai/v1`  
**Sortie** : image inline dans le chat (`![Image](url)`)

### 📚 RAG — `agents/rag_agent.py`
**Modèle** : `openrouter/openai/gpt-oss-120b`  
**Invoqué quand** : question sur les documents uploadés dans OpenWebUI  
**Outil** : Qdrant HTTP direct (collection `openwebui`) + embeddings via LiteLLM  
**Fonctionnement** : génère un vecteur d'embedding pour la question, recherche les 5 chunks les plus proches, synthétise avec les sources

---

## Skills

Les skills sont des fichiers Markdown dans `skills/` chargés au démarrage par l'**agent Dev**. Ils contiennent des guides d'utilisation détaillés et des exemples de code pour des bibliothèques JavaScript et CSS spécifiques.

| Fichier | Nom | Cas d'usage |
|---|---|---|
| `animejs.md` | animejs-animation | Animations DOM/SVG chorégraphiées avec Anime.js v4 |
| `bulma.md` | bulma-css | Interfaces HTML responsives sans JS (Bulma v1) |
| `chartjs.md` | chartjs | Graphiques standards interactifs (bar, line, pie…) avec Chart.js v4 |
| `creative.md` | creative-artifacts | **Skill maître** — règles universelles d'artifacts, sélection de bibliothèque |
| `d3-charting.md` | d3-charting | Visualisations SVG sur mesure, force-directed, choropleths (D3.js v7) |
| `fullcalendar.md` | fullcalendar | Calendriers et plannings interactifs |
| `gsap.md` | gsap-animation | Animations scroll-driven, parallax, storytelling (GSAP + ScrollTrigger) |
| `jointjs.md` | jointjs-flowchart | Flowcharts et diagrammes éditables drag-and-drop |
| `konva.md` | konva-canvas | Éditeurs canvas 2D, annotation d'images, dessin interactif |
| `leaflet.md` | leaflet-maps | Cartes géographiques interactives (Leaflet.js v1.9) |
| `mathjax.md` | mathjax-latex | Rendu d'équations LaTeX dans le navigateur (MathJax 3) |
| `mermaid.md` | mermaid-diagrams | Diagrammes textuels (flowchart, sequence, ER, state, Gantt…) |
| `p5js.md` | p5js-creative-coding | Art génératif, simulations, sketches créatifs (p5.js v2) |
| `plotly.md` | plotly | Graphiques scientifiques avancés, 3D, statistiques (Plotly.js) |
| `prism.md` | prism-code | Coloration syntaxique de blocs de code (Prism.js) |
| `recharts.md` | recharts | Graphiques React (Recharts) pour artifacts React/shadcn |
| `reveal.md` | reveal-slides | Présentations HTML interactives avec transitions (Reveal.js) |
| `shadcn.md` | shadcn-ui | Interfaces React accessibles avec composants prêts (shadcn/ui) |
| `tabulator.md` | tabulator | Tables et grilles de données interactives (Tabulator.js v6) |
| `tailwind.md` | tailwind-css | Interfaces utility-first avec contrôle pixel (Tailwind CSS v4) |
| `threejs.md` | threejs-3d | Scènes 3D temps-réel, particules, WebGL (Three.js r183) |
| `tone.md` | tone-audio | Synthèse audio, séquenceurs, instruments navigateur (Tone.js) |
| `vis-network.md` | vis-network | Graphes de noeuds interactifs, topologies, org-charts |
| `vis-timeline.md` | vis-timeline | Timelines et Gantt interactifs (vis-timeline) |

---

## Personnalisation

### Changer le modèle d'un agent

Modifier la constante `_MODEL` en tête de fichier dans `sub_agents/agents/<agent>.py`.  
Le nom doit correspondre à un `model_name` défini dans `litellm_config.yaml`.

**Exemple** — passer l'agent Dev sur GPT-OSS :

```python
# sub_agents/agents/dev.py
_MODEL = "openrouter/gpt-oss"  # au lieu de "openrouter/kimi-k2.5"
```

Puis relancer : `docker compose restart pipelines`

### Ajouter un modèle dans LiteLLM

Éditer `litellm_config.yaml` :

```yaml
- model_name: openrouter/mon-modele
  litellm_params:
    model: openrouter/provider/model-name
    api_key: os.environ/OPENROUTER_API_KEY
```

Puis : `docker compose restart litellm`

### Modifier les instructions d'Alyx (system prompt)

Éditer la constante `_ALYX_SYSTEM` dans `sub_agents/alyx_pipeline.py`.  
Alyx doit rester en français et ne doit pas recevoir d'outils directs pour conserver un contexte allégé.

### Modifier les instructions d'un sous-agent

Chaque agent définit sa constante `_SYSTEM` en tête de fichier.  
Les sous-agents travaillent en anglais — cela améliore leur performance sur les appels d'outils.

**Exemple** — rendre le Scholar plus concis :

```python
# sub_agents/agents/scholar.py
_SYSTEM = """\
You are a concise academic research assistant. Return bullet-point summaries only.
Always cite DOI and year. Max 150 words. Reply in English.
"""
```

### Ajouter un nouveau sous-agent

1. Créer `sub_agents/agents/mon_agent.py` avec la fonction `async def run(state) -> dict`
2. L'enregistrer dans `sub_agents/graph/builder.py` dans `_AGENT_MAP`
3. L'ajouter dans le catalogue de `sub_agents/graph/supervisor.py` (constante `_SYSTEM`, section *Agent catalog*)
4. Optionnel : ajouter une icône dans `alyx_pipeline.py` → `_AGENT_ICONS`
5. Relancer : `docker compose restart pipelines`

### Ajouter un skill (bibliothèque supplémentaire)

Déposer un fichier `.md` dans `skills/` avec un frontmatter YAML minimal :

```markdown
---
name: mon-skill
description: Quand utiliser ce skill (déclencheurs, cas d'usage, exclusions).
---

# Titre du skill

Contenu, exemples de code, patterns recommandés…
```

Le skill est chargé automatiquement au prochain démarrage du service `pipelines` (ou au redémarrage). L'agent Dev l'indexera et l'injectera dans son contexte quand la bibliothèque est mentionnée dans la conversation.

### Ajouter un outil MCPO

1. Ajouter l'entrée dans `mcpo_config.json` sous `mcpServers`
2. Utiliser `call_tool("nom-serveur", "nom-outil", {...})` dans l'agent concerné
3. Relancer : `docker compose restart mcpo`

### Activer la génération d'images dans OpenWebUI

La génération d'images via Pollinations est désactivée pour le modèle général (`ENABLE_IMAGE_GENERATION: "false"`) car Alyx gère l'image_gen via son sous-agent. Pour l'activer globalement, changer cette variable à `"true"` dans le compose et définir le modèle d'image dans Admin Panel → Settings → Images.

---

## Variables d'état LangGraph

L'état `AlyxState` (défini dans `sub_agents/graph/state.py`) circule entre tous les nœuds du graphe :

| Champ | Type | Description |
|---|---|---|
| `messages` | `list[BaseMessage]` | Historique de la conversation (reducer append-only) |
| `images_b64` | `list[str]` | Images base64 extraites du message courant |
| `routing` | `list[str]` | Agents sélectionnés par le superviseur pour ce tour |
| `agent_outputs` | `dict[str, str]` | Sorties brutes de chaque agent invoqué |
| `artifacts` | `list[dict]` | Artifacts générés (images URL, métadonnées) |

---

## Vérification

```bash
# 1. Tous les services démarrent sans erreur
docker compose up -d
docker compose ps

# 2. Pipelines charge Alyx correctement
docker logs pipelines 2>&1 | grep -E "loaded|error|Error"
# Attendu : "1 pipeline(s) loaded"

# 3. LiteLLM accessible
curl http://localhost:4000/health/liveliness

# 4. MCPO accessible
curl http://localhost:3722/openapi.json | python3 -m json.tool | head -10

# 5. Checkpoints LangGraph présents après une conversation
docker exec openwebui-postgres psql -U openwebui -d langgraph \
  -c "SELECT count(*) FROM checkpoints;"
```

### Problèmes courants

| Symptôme | Cause probable | Solution |
|---|---|---|
| "Alyx" absent du sélecteur de modèle | Pipelines pas connecté | Admin Panel → Connections → ajouter `http://pipelines:9099` |
| Erreur d'import au démarrage de pipelines | Package manquant | Vérifier les requirements dans le frontmatter d'`alyx_pipeline.py` ; le service installe les deps au démarrage |
| Vision ne fonctionne pas | ID modèle Qwen incorrect | Vérifier `openrouter/qwen/qwen3.5-flash` sur `openrouter.ai/models` |
| DB langgraph non créée | Ancien volume postgres | Supprimer le volume et recréer : `docker volume rm openwebui_postgres_data` ⚠️ destructif |
| Context7 timeout | Rate-limit cloud | Définir `CONTEXT7_API_KEY` dans `.env` |
| Playwright `connection refused` | Service pas démarré | `docker compose up -d playwright` |
