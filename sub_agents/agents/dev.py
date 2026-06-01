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

    if skill_hits:
        skill_names = ", ".join(n for _, n, _ in skill_hits)
        await _emit(f"📚 Skills : {skill_names}")
        skill_block = "\n\n".join(f"### Skill: {n}\n{c[:6000]}" for _, n, c in skill_hits)
        context_parts.append(
            f"## Relevant skill files (USE AS TEMPLATE — adapt all content to user's request)\n{skill_block}"
        )

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
