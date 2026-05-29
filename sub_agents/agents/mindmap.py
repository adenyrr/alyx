"""
Mindmap Agent — génère une carte mentale interactive via markmap.js.

Modèle : openrouter/qwen3.5-flash (suffit pour structurer une mindmap).
Outils : skills/markmap.md (template auto-contenu).

Produit un artifact ```html auto-contenu, rendu inline via le mécanisme embeds
de la pipeline (cf. _extract_html_embeds).
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Callable

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.skills_loader import find_relevant as find_relevant_skills, get_skill
from tools.text_utils import last_user_message

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are a mindmap designer. Generate a self-contained ```html artifact using
markmap.js (see the skill in context for the EXACT CDN, init pattern, dark
theme tokens).

═══════════════════════════════════════════════════════
 OUTPUT CONTRACT
═══════════════════════════════════════════════════════
• Emit EXACTLY one ```html block. No prose around it.
• Use the markmap skill structure verbatim, replacing only the data.
• Mindmap content : 1 root → 4 to 6 branches → 2-5 leaves each.
• Max depth 4 (root → branch → sub-branch → leaf).
• Keep labels short (≤ 6 words).
• Dark theme by default. Descriptive <title>.

After the artifact, 2-3 sentences explaining the structure choices and citing
sources for the data shown.
"""


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = last_user_message(messages)

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

    # Phase 1 results (workflow séquentiel)
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
            "## Data from previous agents (USE THIS as primary content)\n" + prior_text
        )

    # Design system (tokens partagés)
    design_skill = get_skill("design-system")
    if design_skill:
        context_parts.append(
            f"## Design system (tokens couleurs/typo à utiliser sur le shell)\n{design_skill}"
        )

    # Skill markmap (obligatoire — sans ça, l'agent invente du HTML qui peut ne pas marcher)
    await _emit("📚 Skill markmap…")
    skill_hits = find_relevant_skills(user_text, agent="mindmap")
    if not skill_hits:
        # Fallback : chercher le skill `markmap` via le canal `dev`
        skill_hits = find_relevant_skills("markmap mindmap", agent="dev")
    if skill_hits:
        skill_block = "\n\n".join(f"### Skill: {n}\n{c[:7000]}" for _, n, c in skill_hits)
        context_parts.append(
            f"## Markmap skill (USE AS TEMPLATE — adapt content to user's request)\n{skill_block}"
        )

    await _emit("🗺️ Génération de la mindmap…")
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.2,
    )
    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nUser request: {user_text}" if context else user_text
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    return {
        "agent_outputs": {"mindmap": response.content},
        "agent_confidence": {"mindmap": 0.85},
        "agent_metrics": {"mindmap": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
    }
