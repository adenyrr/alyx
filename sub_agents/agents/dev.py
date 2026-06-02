"""
Dev Agent — création d'artifacts interactifs et assistance technique.

Fusion de Coder + Tech. Modèle : kimi-k2.5.

Outils (dans l'ordre d'utilisation) :
  1. Skills locaux (skills/*.md) — base de référence OBLIGATOIRE pour les artifacts
  2. Context7 (docs officielles de bibliothèques en temps réel)
  3. Terminal bash (validation de commandes, vérification d'environnement)
  4. Git (MCPO — diff, log, status)

Émet des statuts OpenWebUI en temps réel via config["configurable"]["event_emitter"].
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from typing import TYPE_CHECKING, Callable

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.mcpo_client import call_tool
from tools.context7_client import get_library_docs, resolve_library_id
from tools.skills_loader import find_relevant as find_relevant_skills, get_skill
from tools.terminal_client import execute

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/kimi-k2.5"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_KNOWN_LIBS = [
    # Charts / data viz
    "leaflet", "maplibre", "chartjs", "chart.js", "d3", "plotly", "echarts",
    "recharts", "tabulator", "vis-network", "vis-timeline", "mermaid", "jointjs",
    "konva", "pixijs", "pixi.js", "excalidraw", "markmap", "wavesurfer",
    # Animation / 3D
    "three.js", "threejs", "p5js", "p5", "gsap", "anime.js", "animejs", "tone.js",
    # UI / frameworks
    "react", "vue", "angular", "svelte", "tailwind", "bulma", "shadcn",
    "htmx", "lit", "monaco", "monaco-editor", "tiptap", "prosemirror",
    "reveal.js", "reveal", "fullcalendar", "mathjax", "prism",
    # Backend / data
    "langchain", "langgraph", "fastapi", "django", "flask", "sqlalchemy",
    "pandas", "numpy", "scipy", "sklearn", "tensorflow", "pytorch",
    "docker", "kubernetes", "terraform", "ansible",
]

_SYSTEM = """\
You are an expert software engineer, creative front-end developer, and technical documentation specialist.

═══════════════════════════════════════════════════════
 ARTIFACT GENERATION — STRICT PRIORITY ORDER
═══════════════════════════════════════════════════════
1. ```html  ← THE DEFAULT for ANY visual output, data display, UI, chart, table, game, or animation.
             Always use a CDN-hosted library rather than writing raw logic.
2. ```javascript  ← Only if no HTML structure is needed (rare).
3. ```python  ← ABSOLUTE LAST RESORT.
               ONLY IF the user explicitly asks for a Python script, OR
               the task is purely algorithmic with zero visual/display component.
               DO NOT use Python to display tables, format data, render charts, or produce
               readable output — use ```html with an inline table or Chart.js instead.

═══════════════════════════════════════════════════════
 WHEN TO GENERATE AN ARTIFACT
═══════════════════════════════════════════════════════
Generate a ```html artifact for ANY of these:
  • Charts, graphs, plots of any kind
  • Tables, grids, dashboards, statistics
  • Interactive UIs, forms, visualizations
  • Data formatted for readability ("mettre en forme", "afficher", "présenter")
  • Animations, games, 3D scenes
  • Technical comparisons, feature matrices
If in doubt → generate the artifact. Always better than plain text.

═══════════════════════════════════════════════════════
 SKILL FILES — MANDATORY USAGE
═══════════════════════════════════════════════════════
When skill files are provided in context (## Relevant skill files):
  • Follow the skill's library choice, CDN URL and version, and HTML structure EXACTLY.
  • Replace ALL example data, labels, and titles with content from the user's request.
  • Preserve the visual theme and layout principles from the skill.
  • The final artifact must serve the user's request — NOT reproduce the example.
  • If the skill provides a code example, use it as a structural scaffold only.

═══════════════════════════════════════════════════════
 ARTIFACT TECHNICAL RULES
═══════════════════════════════════════════════════════
  • 100% self-contained: all CSS in <style>, all JS inline or via CDN <script>.
  • Descriptive <title> tag matching the user's actual request (not the skill example title).
  • No explanatory text inside the artifact — clean code only.
  • After the artifact block: a 2-4 sentence explanation in plain English.

═══════════════════════════════════════════════════════
 DESIGN SYSTEM (OBLIGATOIRE)
═══════════════════════════════════════════════════════
The `design-system` skill (in context) defines the SHARED visual language for
ALL Alyx artifacts: design tokens, base reset, font loading, card shell,
buttons, inputs, badges, animations.

You MUST :
  - Copy the token block (`:root, [data-theme="dark"]`) into your `<style>`.
  - Load Inter + JetBrains Mono via Google Fonts in `<head>`.
  - Apply the reset + ambient background gradient on `body`.
  - Use the `.card` shell as the default container UNLESS the artifact has its
    own native structure (reveal.js deck, markmap mindmap, etc.).
  - Use the tokens (`var(--accent)`, `var(--bg-elevated)`, etc.) for ALL colors —
    no hardcoded hex except inside the token block.
  - Apply `animation: card-in` for the entry, and the `.fade` / `.lift` utility
    classes where natural.
  - Keep the dark theme as the DEFAULT (data-theme="dark" on body).

The design-system makes artifacts look polished by default, instead of "bare HTML".
It's the difference between functional and produced. Apply it systematically.

═══════════════════════════════════════════════════════
 TECHNICAL DOCUMENTATION
═══════════════════════════════════════════════════════
  • For library-specific questions, rely on Context7 docs supplied in context.
  • Use the terminal to validate versions, run tests, or check the environment.

═══════════════════════════════════════════════════════
 SOURCES & CITATIONS (MANDATORY)
═══════════════════════════════════════════════════════
  • Cite every CDN library used: name + version in the post-artifact explanation.
  • For library docs: > 📖 [Library vX.Y](https://official-docs-url)
  • For data sources: cite origin ("Data: World Bank 2023").
  • For Stack Overflow / GitHub Issues: include the direct link.

Always reply in English.
"""


def _detect_library(query: str) -> str | None:
    q = query.lower()
    return next(
        (lib for lib in _KNOWN_LIBS
         if lib.replace(".", "").replace("-", "") in q.replace(".", "").replace("-", "")),
        None,
    )


async def _fetch_context7(detected: str, topic: str) -> str:
    try:
        lib_id = await resolve_library_id(detected)
        if not lib_id or "error" in lib_id.lower():
            return ""
        return await get_library_docs(lib_id, topic=topic[:80], tokens=5000)
    except Exception:
        return ""


def _infer_quick_command(query: str) -> str:
    q = query.lower()
    if "python" in q and "version" in q:
        return "python3 --version"
    if "node" in q and "version" in q:
        return "node --version"
    if "docker" in q:
        return "docker --version"
    return ""


# Indices d'une intention cartographique (requête OU données de phase 1).
# Pas de \b final : on veut matcher les pluriels (« restaurants », « lieux »…).
_MAP_INTENT_RE = re.compile(
    r"\b(carte|map\b|leaflet|itin[ée]raire|lieu|visiter|visite|incontournable|"
    r"restaurant|resto|mus[ée]e|monument|attraction|touris|adresse|quartier|"
    r"r[ée]gion|coordonn[ée]e|latitude|longitude|\bgps\b|"
    r"(?:que|où|a|à) (?:voir|aller|visiter|manger|faire))",
    re.IGNORECASE,
)
# Coordonnées explicites dans les données (lat/lon décimaux côte à côte).
_COORD_RE = re.compile(r"-?\d{1,3}\.\d{3,}\s*[,;]\s*-?\d{1,3}\.\d{3,}")


def _wants_map(user_text: str, prior_outputs: dict) -> bool:
    """Vrai si une carte est l'artifact pertinent : l'agent geo a tourné, OU des
    coordonnées sont présentes dans les données, OU l'intention cartographique
    est lisible dans la requête + des lieux ont été collectés en phase 1."""
    if prior_outputs.get("geo"):
        return True
    joined = " ".join(str(v) for v in prior_outputs.values())
    if _COORD_RE.search(joined):
        return True
    if prior_outputs and _MAP_INTENT_RE.search(user_text):
        return True
    return False


# Intention « tableau / comparatif / listing » : justifie un artifact tableau,
# en complément d'une carte (ex. lieux + restos). Conservateur — exige des
# données de phase 1 pour ne pas fabriquer un tableau sans contenu.
_TABLE_INTENT_RE = re.compile(
    r"\b(tableau|comparat(?:if|ive)|comparaison|comparer|versus|vs|diff[ée]rences?|"
    r"liste|classement|top\s*\d+|palmar[èe]s|restos?|restaurants?|adresses?|"
    r"incontournables?|s[ée]lection|menus?)\b",
    re.IGNORECASE,
)


def _wants_table(user_text: str, prior_outputs: dict) -> bool:
    """Vrai si un tableau récapitulatif/comparatif apporte de la valeur ce tour."""
    return bool(prior_outputs) and bool(_TABLE_INTENT_RE.search(user_text))


# Specs des artifacts auto-produits en PASSES SÉPARÉES (1 appel LLM chacun →
# budget de tokens complet par artifact, pas de troncature croisée). L'ordre de
# la liste = l'ordre d'affichage. `skill` = skill local chargé pour cette passe.
_DELIVERABLE_SPECS: dict[str, dict[str, str]] = {
    "table": {
        "skill": "tabulator",
        "status": "📊 Génération du tableau…",
        "focus": (
            "Produce EXACTLY ONE self-contained ```html artifact: an interactive, "
            "sortable/filterable TABLE summarizing the items from the data above "
            "(places, restaurants, options…), with clear columns (e.g. name, "
            "type/category, highlight, address/zone). Do NOT include a map in this "
            "artifact. End with 1-2 sentences of plain-English explanation."
        ),
    },
    "map": {
        "skill": "leaflet-maps",
        "status": "🗺️ Génération de la carte…",
        "focus": (
            "Produce EXACTLY ONE self-contained ```html artifact: an interactive "
            "Leaflet MAP with one marker per location from the data above. For each "
            "marker, use the EXACT lat/lon from the '## Verified coordinates' block "
            "when present; only for a place absent from that block, fall back to its "
            "best-known approximate coordinates. Each marker carries a popup (name + "
            "short note). Do NOT include a data table in this artifact. End with 1-2 "
            "sentences of explanation."
        ),
    },
}


def _plan_deliverables(user_text: str, prior_outputs: dict) -> list[str]:
    """Liste ORDONNÉE des artifacts à produire en passes séparées.

    Retourne [] (→ passe unique nominale) sauf si AU MOINS DEUX signaux forts
    distincts coexistent (ex. lieux à voir + restos/comparatif → tableau PUIS
    carte). Conservateur : un seul signal = un seul artifact via le chemin
    nominal existant.
    """
    deliverables: list[str] = []
    if _wants_table(user_text, prior_outputs):
        deliverables.append("table")
    if _wants_map(user_text, prior_outputs):
        deliverables.append("map")
    return deliverables if len(deliverables) >= 2 else []


_GEOCODE_EXTRACT_SYSTEM = """\
From the data below, list the specific MAPPABLE places (landmarks, monuments, museums,
restaurants, sites, addresses) that belong on a map. Output ONE place per line as
"Place name, City, Country" so each can be geocoded unambiguously. Max 15 lines.
No numbering, no commentary. If there is nothing mappable, output nothing.
"""


def _parse_latlon(osm_result) -> "tuple[float | None, float | None]":
    """Extrait (lat, lon) d'une réponse OSM `geocode`, en gérant l'enveloppe MCPO
    (`{content: [{text: "<json>"}]}`), la liste de résultats et le dict direct."""
    try:
        if isinstance(osm_result, dict):
            content = osm_result.get("content")
            if isinstance(content, list) and content:
                try:
                    return _parse_latlon(json.loads(content[0].get("text", "")))
                except Exception:
                    pass
            lat = float(osm_result.get("lat", osm_result.get("latitude", 0)) or 0) or None
            lon = float(osm_result.get("lon", osm_result.get("longitude", 0)) or 0) or None
            return lat, lon
        if isinstance(osm_result, list) and osm_result and isinstance(osm_result[0], dict):
            first = osm_result[0]
            lat = float(first.get("lat", first.get("latitude", 0)) or 0) or None
            lon = float(first.get("lon", first.get("longitude", 0)) or 0) or None
            return lat, lon
    except Exception:
        pass
    return None, None


async def _geocode_for_map(prior_outputs: dict, user_text: str, model: str | None) -> str:
    """Géocode (OSM) les lieux issus de la phase 1 → bloc de coordonnées EXACTES à
    injecter dans la passe carte.

    Corrige le cas où aucun agent `geo` n'a tourné (geo s'exécute en phase 1, avant
    que les POI ne soient découverts par web/wikipedia, et ne géocode qu'UN lieu) :
    sans ça, le modèle « devine » les coordonnées. On utilise le même outil OSM que
    l'agent geo. Best-effort : '' si rien d'exploitable (n'empêche jamais la carte).
    """
    if not prior_outputs:
        return ""
    data = "\n\n".join(str(v)[:3000] for v in prior_outputs.values()).strip()
    if not data:
        return ""
    llm = ChatOpenAI(
        model=model or _MODEL, base_url=_LITELLM_URL, api_key=_LITELLM_API_KEY,
        temperature=0, max_tokens=400,
    )
    try:
        resp = await llm.ainvoke([
            SystemMessage(content=_GEOCODE_EXTRACT_SYSTEM),
            HumanMessage(content=f"Map context / region: {user_text}\n\nData:\n{data}"),
        ])
    except Exception:
        return ""
    raw = re.sub(r"<think(?:ing)?[^>]*>.*?</think(?:ing)?>", "", resp.content,
                 flags=re.DOTALL | re.IGNORECASE)
    names = [ln.strip("-•*  \t").strip() for ln in raw.splitlines() if ln.strip()][:15]
    if not names:
        return ""

    async def _geo_one(name: str) -> str | None:
        try:
            r = await call_tool("osm-mcp-server", "geocode", {"q": name, "limit": 1})
            lat, lon = _parse_latlon(r)
            if lat is not None and lon is not None:
                return f"- {name} → {lat:.5f}, {lon:.5f}"
        except Exception:
            return None
        return None

    rows = [r for r in await asyncio.gather(*(_geo_one(n) for n in names)) if r]
    if not rows:
        return ""
    return (
        "## Verified coordinates (OSM geocoding) — USE THESE EXACT lat/lon for the markers\n"
        + "\n".join(rows)
        + "\nDo NOT invent coordinates. If a place you want to show is missing here, "
        "omit its marker or place it approximately and note the approximation."
    )


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    # Récupérer l'emitter depuis la config LangGraph pour les statuts en temps réel
    emitter: Callable | None = None
    if config:
        emitter = (config.get("configurable") or {}).get("event_emitter")

    async def _emit(desc: str) -> None:
        if emitter:
            try:
                await emitter({"type": "status", "data": {"description": desc, "done": False}})
            except Exception:
                pass

    context_parts: list[str] = []

    # 0. Résultats phase 1 (workflow séquentiel) — données récupérées par web/geo/data/etc.
    prior_outputs = {
        k: v for k, v in (state.get("agent_outputs") or {}).items()
        if v and not str(v).startswith("⚠️")
    }

    # ── Auto multi-artifacts (passes séparées) ───────────────────────────────
    # Si DEUX signaux forts distincts coexistent (ex. lieux à voir + restos /
    # comparatif), on produit chaque artifact dans sa PROPRE passe LLM. Chacun
    # dispose du budget de tokens complet (pas de troncature croisée) et ils
    # s'affichent à la suite, dans l'ordre planifié (tableau puis carte). Le
    # pipeline extrait les N blocs ```html de la sortie concaténée.
    deliverables = _plan_deliverables(user_text, prior_outputs)
    if deliverables:
        prior_block = ""
        if prior_outputs:
            prior_block = (
                "## Data retrieved by previous agents (USE THIS as your primary data source)\n"
                + "\n\n".join(
                    f"### {name} agent results\n{content[:3000]}"
                    for name, content in prior_outputs.items()
                )
            )
        design_block = ""
        design_skill = get_skill("design-system")
        if design_skill:
            design_block = (
                "## Design system (OBLIGATOIRE — appliquer tokens + shell exactement)\n"
                + design_skill
            )
        base_context = "\n\n".join(p for p in (prior_block, design_block) if p)

        llm = ChatOpenAI(
            model=model or _MODEL,
            base_url=_LITELLM_URL,
            api_key=_LITELLM_API_KEY,
            temperature=0.15,
        )
        await _emit(
            f"🧩 {len(deliverables)} artifacts à produire : "
            + ", ".join(_DELIVERABLE_SPECS[k]["status"].rstrip("… ") for k in deliverables)
        )

        async def _one_pass(kind: str) -> "tuple[str, int, int]":
            """Génère UN artifact (1 appel LLM). Renvoie (contenu, prompt_tk, completion_tk)."""
            spec = _DELIVERABLE_SPECS[kind]
            skill_content = get_skill(spec["skill"]) or ""
            parts = [base_context]
            # Carte : géocoder les lieux (OSM) → coordonnées exactes, pas devinées.
            if kind == "map":
                await _emit("🌍 Géocodage des lieux (OSM)…")
                coords = await _geocode_for_map(prior_outputs, user_text, model)
                if coords:
                    parts.append(coords)
            if skill_content:
                parts.append(
                    "## Relevant skill file (USE AS TEMPLATE — adapt all content to user's request)\n"
                    f"### Skill: {spec['skill']}\n{skill_content[:6000]}"
                )
            parts.append(f"## Your task for THIS artifact\n{spec['focus']}")
            context = "\n\n".join(p for p in parts if p)
            resp = await llm.ainvoke([
                SystemMessage(content=_SYSTEM),
                HumanMessage(content=f"{context}\n\nUser request: {user_text}"),
            ])
            _u = getattr(resp, "usage_metadata", None) or {}
            return resp.content, (_u.get("input_tokens", 0) or 0), (_u.get("output_tokens", 0) or 0)

        # Passes INDÉPENDANTES → concurrentes (wall-clock ≈ une seule passe, pas la
        # somme : sinon deux gros artifacts dépasseraient le timeout 60s du nœud dev).
        # gather préserve l'ordre → tableau puis carte, conformément au plan.
        results = await asyncio.gather(*(_one_pass(k) for k in deliverables))
        chunks = [r[0] for r in results]
        prompt_tokens = sum(r[1] for r in results)
        completion_tokens = sum(r[2] for r in results)

        return {
            "agent_outputs": {"dev": "\n\n".join(chunks)},
            "agent_metrics": {"dev": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "model": model or _MODEL,
            }},
        }

    if prior_outputs:
        prior_text = "\n\n".join(
            f"### {name} agent results\n{content[:3000]}"
            for name, content in prior_outputs.items()
        )
        context_parts.append(
            "## Data retrieved by previous agents (USE THIS as your primary data source)\n"
            + prior_text
        )

    # 1a. Design system : TOUJOURS chargé (tokens partagés tous artifacts)
    design_skill = get_skill("design-system")
    if design_skill:
        context_parts.append(
            f"## Design system (OBLIGATOIRE — appliquer tokens + shell exactement)\n{design_skill}"
        )

    # 1b. Skills locaux pertinents (charts, libs spécifiques…)
    await _emit("📚 Recherche dans les skills…")
    skill_hits = find_relevant_skills(user_text, agent="dev")
    skill_names_loaded = {n for _, n, _ in skill_hits}

    # 1c. Auto-carte : si la phase 1 a produit des données GÉOGRAPHIQUES (geo, ou
    # des lieux/coordonnées dans web/wikipedia), on FORCE le skill leaflet-maps.
    # Le matcher de skills score sur le texte utilisateur·rice (anglais) ; une
    # requête FR « lieux à visiter » ne le ferait pas surfacer alors que la carte
    # est précisément l'artifact attendu (cf. supervisor RULE 11b).
    if "leaflet-maps" not in skill_names_loaded and _wants_map(user_text, prior_outputs):
        leaflet = get_skill("leaflet-maps")
        if leaflet:
            skill_hits = [(99, "leaflet-maps", leaflet), *skill_hits]
            skill_names_loaded.add("leaflet-maps")

    # 1c-bis. Auto-tableau : symétrique de l'auto-carte. Une intention comparatif /
    # listing (« compare », « top 10 », « restos »…) avec des données de phase 1 ne
    # ferait pas surfacer le skill tabulator par le matcher anglais → on le force.
    if "tabulator" not in skill_names_loaded and _wants_table(user_text, prior_outputs):
        tabulator = get_skill("tabulator")
        if tabulator:
            skill_hits = [(98, "tabulator", tabulator), *skill_hits]
            skill_names_loaded.add("tabulator")

    if skill_hits:
        skill_names = ", ".join(n for _, n, _ in skill_hits)
        await _emit(f"📚 Skills : {skill_names}")
        skill_block = "\n\n".join(f"### Skill: {n}\n{c[:6000]}" for _, n, c in skill_hits)
        context_parts.append(
            f"## Relevant skill files (USE AS TEMPLATE — adapt all content to user's request)\n{skill_block}"
        )

    # 1d. Carte mono-artifact : géocoder les lieux (OSM) pour des coordonnées
    # exactes (cf. _geocode_for_map). Même correctif géo que la passe multi-artifacts.
    if _wants_map(user_text, prior_outputs):
        await _emit("🌍 Géocodage des lieux (OSM)…")
        coords_block = await _geocode_for_map(prior_outputs, user_text, model)
        if coords_block:
            context_parts.append(coords_block)

    # 2. Docs Context7 si une bibliothèque est détectée
    detected_lib = _detect_library(user_text)
    if detected_lib:
        await _emit(f"🔍 Context7 : {detected_lib}…")
        topic = user_text.lower().replace(detected_lib, "").strip()
        lib_docs = await _fetch_context7(detected_lib, topic)
        if lib_docs:
            context_parts.append(f"## Context7 live documentation ({detected_lib})\n{lib_docs}")
            await _emit(f"✅ Docs {detected_lib} récupérées")

    # 3. Terminal si pertinent
    if any(kw in user_text.lower() for kw in ["version", "install", "run", "execute", "check", "test", "terminal", "bash", "shell"]):
        cmd = _infer_quick_command(user_text)
        if cmd:
            await _emit(f"🖥️ Terminal : {cmd}")
            try:
                terminal_output = await execute(cmd)
                context_parts.append(f"## Terminal output (`{cmd}`)\n```\n{terminal_output}\n```")
            except Exception as exc:
                context_parts.append(f"## Terminal (unavailable)\n{exc}")

    # 4. Contexte git si pertinent
    if any(kw in user_text.lower() for kw in ["git", "commit", "diff", "branch", "repo"]):
        await _emit("🔀 Git status…")
        try:
            git_info = await call_tool("git", "git_status", {})
            context_parts.append(f"## Git status\n{git_info}")
        except Exception:
            pass

    await _emit("💻 Génération…")
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.15,
    )

    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nUser request: {user_text}" if context else user_text

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    return {
        "agent_outputs": {"dev": response.content},
        "agent_metrics": {"dev": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
    }
