"""
Scholar Agent — recherche académique et scientifique.
Outils : paper-search (MCPO), wikipedia (MCPO), sequential-thinking (MCPO).
Modèle : GPT-OSS 120B.
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM_TEMPLATE = """\
You are an academic research specialist. Use the provided tool results to answer scientific questions.
Always cite DOIs, authors, and publication years when available.
Today's date: {current_date}. Prioritize the most recent publications; clearly note when articles are older than 2 years.
Prioritize peer-reviewed sources. Reply in English with structured markdown.
"""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)
    current_date = state.get("current_date", "")

    # LLM créé en premier — utilisé pour l'extraction de mots-clés ET la synthèse
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.2,
    )

    # Extraire 3-5 mots-clés anglophones pour les recherches MCPO
    keywords = await _extract_keywords(user_text, llm)

    # 1. Recherche académique — 3 outils en parallèle
    async def _safe(server: str, tool: str, params: dict):
        try:
            return await call_tool(server, tool, params)
        except Exception as exc:
            return {"error": str(exc)}

    papers_raw, wiki_raw, seq_raw = await asyncio.gather(
        _safe("paper-search", "search_papers", {"query": keywords, "limit": 5}),
        _safe("wikipedia", "search", {"query": keywords, "limit": 3}),
        _safe("sequential-thinking", "sequentialthinking", {"thought": keywords}),
    )

    def _to_str(v) -> str:
        if isinstance(v, (dict, list)):
            return json.dumps(v, ensure_ascii=False, indent=2)
        return str(v)

    paper_results = _to_str(papers_raw)
    wiki_results  = _to_str(wiki_raw)
    reasoning     = _to_str(seq_raw) if not isinstance(seq_raw, dict) or "error" not in seq_raw else ""

    # 2. Synthèse LLM
    context = (
        f"## Paper search results\n{paper_results}\n\n"
        f"## Wikipedia results\n{wiki_results}\n\n"
        f"## Sequential reasoning\n{reasoning}".strip()
    )

    system_prompt = _SYSTEM_TEMPLATE.format(current_date=current_date or "unknown")
    response = await llm.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"{context}\n\nUser question: {user_text}"),
    ])

    return {"agent_outputs": {"scholar": response.content}}


async def _extract_keywords(user_text: str, llm: ChatOpenAI) -> str:
    """Extrait 3-5 mots-clés anglophones pour les recherches MCPO."""
    resp = await llm.ainvoke(
        [
            SystemMessage(content=(
                "Extract 3-5 concise English search keywords from the user's message. "
                "Output ONLY the keywords, space-separated, lowercase, no punctuation, no explanation."
            )),
            HumanMessage(content=user_text),
        ],
        config={"max_tokens": 20},
    )
    return resp.content.strip().replace("\n", " ")


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
