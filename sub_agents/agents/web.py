"""
Web Agent — navigation, scraping et recherche web.
Modèle : GPT-OSS 120B.
Outil : playwright MCP (service natif OpenWebUI, transport Streamable HTTP).

Playwright est fourni comme outil natif par le service playwright du compose.
La connexion se fait directement vers http://playwright:8931,
évité de passer par MCPO (playwright n'y est pas configuré).
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.playwright_client import fetch_url, search_web

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM_TEMPLATE = """\
You are a web research assistant. You have access to a real Chromium browser via Playwright.
Use the provided browser results to answer questions about web pages, news, current events, or online content.
Summarize findings accurately, quote relevant excerpts, and include source URLs.
Today's date: {current_date}. Prioritize the most recent content available.
Reply in English.
"""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)
    current_date = state.get("current_date", "")

    # Enrichir la requête avec la date complète pour favoriser des résultats récents cohérents.
    search_query = f"{user_text} {current_date}" if current_date else user_text

    # Navigation via playwright MCP Streamable HTTP
    browser_result = ""
    try:
        url = _extract_url(user_text)
        if url:
            browser_result = await fetch_url(url)
            browser_result = f"Page: {url}\n{browser_result}"
        else:
            browser_result = await search_web(search_query)
    except Exception as exc:
        browser_result = f"Browser navigation failed: {exc}"

    system_prompt = _SYSTEM_TEMPLATE.format(current_date=current_date or "unknown")

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.2,
    )

    prompt = f"## Browser result\n{browser_result}\n\nUser question: {user_text}"
    response = await llm.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt),
    ])

    return {"agent_outputs": {"web": response.content}}


def _extract_url(text: str) -> str:
    import re
    match = re.search(r"https?://[^\s]+", text)
    return match.group(0) if match else ""


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
