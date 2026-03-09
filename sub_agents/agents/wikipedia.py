"""
Wikipedia Agent — recherche encyclopédique via MCPO wikipedia-mcp.

Modèle : openrouter/qwen3.5-flash.
Outil  : wikipedia (MCPO) — serveur wikipedia-mcp en français.

Stratégie :
  1. LLM extrait 2-3 mots-clés français optimisés pour Wikipedia.
  2. Appel MCPO wikipedia/search avec ces mots-clés.
  3. LLM synthétise en incluant les sources Wikipedia.
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

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
Tu es un·e spécialiste de la connaissance encyclopédique. Utilise les résultats
Wikipedia fournis pour répondre avec précision. Cite les articles Wikipedia
consultés, les dates de publication et les sections pertinentes.
Structure ta réponse avec des titres markdown clairs.
Réponds dans la même langue que la question.
"""

_KW_SYSTEM = """\
Extrais 2 à 3 mots-clés courts en français, adaptés à une recherche Wikipedia.
Ne retourne QUE les mots-clés, séparés par des espaces, sans ponctuation,
sans explication.
"""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0,
        max_tokens=512,
    )

    # 1. Extraire 2-3 mots-clés français
    kw_resp = await llm.ainvoke(
        [
            SystemMessage(content=_KW_SYSTEM),
            HumanMessage(content=user_text),
        ],
        config={"max_tokens": 20},
    )
    keywords = kw_resp.content.strip().replace("\n", " ")[:100]
    _prompt_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("input_tokens", 0) or 0
    _completion_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("output_tokens", 0) or 0

    # 2. Recherche Wikipedia via MCPO
    wiki_raw = ""
    try:
        result = await call_tool("wikipedia", "search", {"query": keywords, "limit": 3})
        wiki_raw = json.dumps(result, ensure_ascii=False, indent=2)[:6000]
    except Exception as exc:
        wiki_raw = f"Wikipedia indisponible : {exc}"

    # 3. Synthèse LLM
    prompt = (
        f"## Résultats Wikipedia (mots-clés : {keywords!r})\n{wiki_raw}"
        f"\n\nQuestion utilisateur : {user_text}"
    )

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    _prompt_tokens += _u.get("input_tokens", 0) or 0
    _completion_tokens += _u.get("output_tokens", 0) or 0
    return {
        "agent_outputs": {"wikipedia": response.content},
        "agent_metrics": {"wikipedia": {
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
