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
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.mcpo_client import call_tool
from tools.context7_client import get_library_docs, resolve_library_id
from tools.terminal_client import execute

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/kimi-k2.5"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

# ------- Skills -------
_skills_cache: dict[str, str] = {}
_skills_meta: dict[str, str] = {}
_SKILLS_DIR = Path("/app/pipelines/skills")

_STOPWORDS = {
    "a", "an", "the", "is", "in", "to", "how", "do", "can", "me", "i", "for", "of",
    "with", "this", "my", "any", "and", "or", "it", "that", "on", "what", "use",
    "get", "have", "be", "are", "was", "will", "by", "at", "as", "from", "make",
    "build", "show", "give", "let", "want", "need", "please", "help", "write", "create",
    "de", "du", "le", "la", "les", "un", "une", "des", "je", "tu", "il", "nous",
    "vous", "ils", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
    "que", "qui", "quoi", "quel", "quelle", "faire", "fait", "fais", "avec",
    "sans", "mais", "ou", "et", "si", "car", "est", "sur", "par", "pour", "dans",
    "ce", "cet", "ces", "moi", "toi", "lui", "suis", "veux", "peux", "dois",
    "crée", "crée-moi", "génère", "fais-moi", "affiche", "montre", "présente",
}

_KNOWN_LIBS = [
    "leaflet", "react", "vue", "angular", "svelte", "tailwind", "bulma",
    "chartjs", "chart.js", "d3", "plotly", "three.js", "threejs", "p5js", "p5",
    "langchain", "langgraph", "fastapi", "django", "flask", "sqlalchemy",
    "pandas", "numpy", "scipy", "sklearn", "tensorflow", "pytorch",
    "docker", "kubernetes", "terraform", "ansible",
    "shadcn", "gsap", "anime.js", "animejs", "konva", "jointjs",
    "mermaid", "vis-network", "vis-timeline", "tabulator",
    "recharts", "reveal.js", "mathjax", "prism", "tone.js",
    "fullcalendar", "vis",
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
  • Dark theme: #0f1117 background, #1a1d27 card backgrounds, unless told otherwise.
  • Descriptive <title> tag matching the user's actual request (not the skill example title).
  • No explanatory text inside the artifact — clean code only.
  • After the artifact block: a 2-4 sentence explanation in plain English.

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


def _load_skills() -> None:
    if _skills_cache or not _SKILLS_DIR.exists():
        return
    for skill_file in _SKILLS_DIR.glob("*.md"):
        try:
            content = skill_file.read_text(encoding="utf-8")
            name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
            key = name_match.group(1).strip() if name_match else skill_file.stem
            desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
            _skills_cache[key] = content
            _skills_meta[key] = desc_match.group(1).strip() if desc_match else ""
        except Exception:
            pass


def _find_relevant_skills(query: str) -> list[tuple[int, str, str]]:
    """Retourne les skills scorés (score, name, content) triés par pertinence."""
    _load_skills()
    query_lower = query.lower()
    query_words = {w for w in re.split(r"\W+", query_lower) if len(w) > 3 and w not in _STOPWORDS}
    scored: list[tuple[int, str, str]] = []
    for name, content in _skills_cache.items():
        score = 0
        name_lower = name.lower()
        if name_lower in query_lower:
            score += 10
        else:
            for part in re.split(r"[-_.]", name_lower):
                if len(part) > 3 and part in query_lower:
                    score += 5
        desc = _skills_meta.get(name, "").lower()
        if desc and query_words:
            score += min(sum(1 for w in query_words if w in desc), 5)
        if score > 0:
            scored.append((score, name, content))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:2]


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


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    _load_skills()
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

    # 1. Skills locaux pertinents
    await _emit("📚 Recherche dans les skills…")
    skill_hits = _find_relevant_skills(user_text)
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

    return {"agent_outputs": {"dev": response.content}}
