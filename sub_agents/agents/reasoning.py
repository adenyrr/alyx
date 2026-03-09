"""
Reasoning Agent — décomposition analytique via sequential-thinking.

Modèle : openrouter/deepseek.
Outil  : sequential-thinking (MCPO) — décomposition multi-étapes guidée.

Stratégie :
  1. LLM décompose la question en plan d'analyse structuré.
  2. Appel sequential-thinking pour chaque étape principale.
  3. LLM synthétise les résultats en analyse structurée avec conclusions.

Usage : analyses complexes, plans stratégiques, diagnostics différentiels,
        pros/cons, décompositions de problèmes multi-variables.
"""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/deepseek"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_DECOMPOSE_SYSTEM = """\
You are a rigorous analytical thinker. Break down the user's question into
3-5 key analytical steps or sub-questions that together form a complete analysis.
Return ONLY a JSON array of strings (the steps), no explanation.
Example: ["What are the main stakeholders?", "What are the key risks?", "What are viable alternatives?"]
"""

_SYNTHESIS_SYSTEM = """\
You are an expert analyst. Using the structured thinking process provided,
synthesize a comprehensive, rigorous analysis.

Rules:
  - Structure your answer with clear markdown sections (##, ###).
  - For each claim, indicate the strength of the argument.
  - Distinguish facts from hypotheses from recommendations.
  - For pros/cons or risk analyses, use structured tables when appropriate.
  - Conclude with a short, actionable summary (≤ 5 bullet points).
  - Reply in the same language as the original question.
"""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.2,
    )

    _prompt_tokens = 0
    _completion_tokens = 0
    context_parts: list[str] = []

    # 1. Décomposer la question en étapes d'analyse
    decomp_resp = await llm.ainvoke([
        SystemMessage(content=_DECOMPOSE_SYSTEM),
        HumanMessage(content=user_text),
    ])
    _u = getattr(decomp_resp, "usage_metadata", None) or {}
    _prompt_tokens += _u.get("input_tokens", 0) or 0
    _completion_tokens += _u.get("output_tokens", 0) or 0

    steps: list[str] = []
    try:
        import re
        raw = decomp_resp.content.strip()
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            steps = json.loads(match.group(0))
            steps = [s for s in steps if isinstance(s, str)][:5]
    except Exception:
        steps = [user_text]

    # 2. Sequential-thinking pour chaque étape
    for i, step in enumerate(steps, 1):
        try:
            result = await call_tool("sequential-thinking", "sequentialthinking", {
                "thought": step,
                "thoughtNumber": i,
                "totalThoughts": len(steps),
                "nextThoughtNeeded": i < len(steps),
            })
            result_str = json.dumps(result, ensure_ascii=False, indent=2) if isinstance(result, (dict, list)) else str(result)
            context_parts.append(f"## Step {i}: {step}\n{result_str[:2000]}")
        except Exception as exc:
            context_parts.append(f"## Step {i}: {step}\n[Sequential-thinking unavailable: {exc}]")

    context = "\n\n".join(context_parts) if context_parts else "(no structured thinking available)"

    # 3. Synthèse finale
    synthesis_prompt = (
        f"## Original question\n{user_text}\n\n"
        f"## Structured thinking process\n{context}\n\n"
        f"Synthesize a complete, rigorous analysis."
    )
    synthesis_resp = await llm.ainvoke([
        SystemMessage(content=_SYNTHESIS_SYSTEM),
        HumanMessage(content=synthesis_prompt),
    ])
    _u2 = getattr(synthesis_resp, "usage_metadata", None) or {}
    _prompt_tokens += _u2.get("input_tokens", 0) or 0
    _completion_tokens += _u2.get("output_tokens", 0) or 0

    return {
        "agent_outputs": {"reasoning": synthesis_resp.content},
        "agent_metrics": {"reasoning": {
            "prompt_tokens": _prompt_tokens,
            "completion_tokens": _completion_tokens,
            "model": model or _MODEL,
        }},
    }


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
