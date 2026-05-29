"""
Diagram Agent — diagrammes mermaid / jointjs / excalidraw (skills correspondants).

Modèle : openrouter/qwen3.5-flash.
Outils : skills (mermaid, jointjs, excalidraw, vis-network).

Choisit le bon outil selon le type de diagramme demandé :
  - Flowchart / sequence / class / ER / state → mermaid
  - Graph network / topologie → vis-network
  - Diagram libre / sketchy → excalidraw
  - UML rich / BPMN → jointjs

Produit un artifact ```html auto-contenu rendu inline via embeds.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Callable

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.skills_loader import find_relevant as find_relevant_skills
from tools.text_utils import last_user_message

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are a diagram designer. Pick the BEST diagram library for the user's request,
then emit a self-contained ```html artifact following the corresponding skill in
context.

═══════════════════════════════════════════════════════
 LIBRARY CHOICE GUIDE
═══════════════════════════════════════════════════════
  Flowchart, sequence, class, ER, state machine, gantt, git graph
    → mermaid (simplest, terse syntax, dark theme baked in)
  Network topology, force-directed graph, dependency map
    → vis-network (interactive nodes/edges)
  Architecture sketches, whiteboard-style, hand-drawn feel
    → excalidraw
  Rich UML, BPMN, custom shapes, editable canvas
    → jointjs

If multiple libraries fit, prefer mermaid (smallest, most readable source).

═══════════════════════════════════════════════════════
 OUTPUT CONTRACT
═══════════════════════════════════════════════════════
• Emit EXACTLY one ```html block, self-contained.
• Follow the corresponding skill EXACTLY for CDN URLs, version, dark theme tokens.
• Descriptive <title>.
• After the artifact: 2-3 sentences explaining which library was chosen and why.
"""


def _detect_diagram_type(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ("sequence", "séquence", "flowchart", "flow chart", "organigramme", "uml class", "diagramme de classe", "etat", "state machine", "machine à états", "gantt", "git graph")):
        return "mermaid"
    if any(k in t for k in ("network", "réseau", "topology", "topologie", "force-directed", "dépendance", "dependency")):
        return "vis-network"
    if any(k in t for k in ("excalidraw", "whiteboard", "sketch", "tableau blanc", "main levée", "schéma à main levée")):
        return "excalidraw"
    if any(k in t for k in ("bpmn", "jointjs", "process flow")):
        return "jointjs"
    return "mermaid"  # défaut


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

    diagram_type = _detect_diagram_type(user_text)
    await _emit(f"📐 Type détecté : {diagram_type}")

    context_parts: list[str] = []

    # Phase 1 results
    prior_outputs = {
        k: v for k, v in (state.get("agent_outputs") or {}).items()
        if v and not str(v).startswith("⚠️")
    }
    if prior_outputs:
        prior_text = "\n\n".join(
            f"### {name} agent results\n{content[:3000]}"
            for name, content in prior_outputs.items()
        )
        context_parts.append("## Data from previous agents\n" + prior_text)

    # Skills : on demande le skill du type détecté (fallback dev pool)
    skill_hits = find_relevant_skills(diagram_type, agent="diagram") \
                 or find_relevant_skills(diagram_type, agent="dev")
    if skill_hits:
        skill_block = "\n\n".join(f"### Skill: {n}\n{c[:7000]}" for _, n, c in skill_hits)
        context_parts.append(
            f"## Diagram skill ({diagram_type}, USE AS TEMPLATE)\n{skill_block}"
        )

    context_parts.append(f"## Library decision\nUse `{diagram_type}` for this diagram.")

    await _emit(f"📐 Génération diagramme ({diagram_type})…")
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.15,
    )
    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nUser request: {user_text}"
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    return {
        "agent_outputs": {"diagram": response.content},
        "agent_confidence": {"diagram": 0.85},
        "agent_metrics": {"diagram": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
    }
