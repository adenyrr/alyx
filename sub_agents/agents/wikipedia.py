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
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

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


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    emitter = (config.get("configurable") or {}).get("event_emitter") if config else None

    async def _emit(desc: str) -> None:
        if emitter:
            try:
                await emitter({"type": "status", "data": {"description": desc, "done": False}})
            except Exception:
                pass

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
    keywords = re.sub(r"<think(?:ing)?[^>]*>.*?</think(?:ing)?>", "", kw_resp.content, flags=re.DOTALL | re.IGNORECASE).strip().replace("\n", " ")[:100]
    _prompt_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("input_tokens", 0) or 0
    _completion_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("output_tokens", 0) or 0

    # 2. Recherche Wikipedia via MCPO
    # wikipedia-mcp expose `search_wikipedia` (pas `search`) + `get_summary`.
    # On enchaîne : search → top 3 titres → résumés courts → synthèse.
    wiki_raw = ""
    try:
        await _emit(f"📖 Recherche Wikipédia : {keywords}")
        search_result = await call_tool("wikipedia", "search_wikipedia", {"query": keywords, "limit": 3})
        titles = _extract_titles(search_result)
        summaries: list[str] = []
        if titles:
            await _emit(f"📄 Résumés des {len(titles)} article(s)…")
            for title in titles:
                try:
                    summary = await call_tool("wikipedia", "get_summary", {"title": title})
                    summaries.append(f"### {title}\n{json.dumps(summary, ensure_ascii=False)[:1500]}")
                except Exception:
                    continue
        wiki_payload = {"search": search_result, "summaries": summaries}
        wiki_raw = json.dumps(wiki_payload, ensure_ascii=False, indent=2)[:6000]
    except Exception as exc:
        wiki_raw = f"Wikipedia indisponible : {exc}"

    # 3. Synthèse LLM
    prompt = (
        f"## Résultats Wikipedia (mots-clés : {keywords!r})\n{wiki_raw}"
        f"\n\nQuestion utilisateur : {user_text}"
    )

    await _emit("✍️ Synthèse Wikipédia…")
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


def _extract_titles(search_payload) -> list[str]:
    """Extrait les titres d'articles depuis la réponse `search_wikipedia`.

    Le format peut varier selon la version : dict avec `results: [{title, snippet, ...}]`,
    liste plate, ou enveloppe MCP `{content: [{text: "..."}]}`. On gère les cas
    courants et on s'arrête au premier qui marche."""
    if isinstance(search_payload, dict):
        # Enveloppe MCPO standard
        content = search_payload.get("content")
        if isinstance(content, list) and content:
            try:
                inner = json.loads(content[0].get("text", ""))
                return _extract_titles(inner)
            except Exception:
                pass
        for key in ("results", "items", "articles"):
            items = search_payload.get(key)
            if isinstance(items, list):
                return [str(it.get("title", "")).strip() for it in items if isinstance(it, dict) and it.get("title")][:3]
    if isinstance(search_payload, list):
        return [str(it.get("title", "")).strip() for it in search_payload if isinstance(it, dict) and it.get("title")][:3]
    return []


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
