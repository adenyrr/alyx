"""
Web Agent — recherche DuckDuckGo + extraction de contenu.

Modèle : openrouter/qwen3.5-flash.
Outils :
  1. duckduckgo (MCPO)  — 3-5 mots-clés, résultats avec URLs.
  2. fetch-web (MCPO)   — récupération rapide du contenu de chaque URL.
  3. playwright_client  — fallback si fetch-web échoue (navigateur réel).

Stratégie :
  a. LLM extrait 3-5 mots-clés de recherche.
  b. DuckDuckGo → liste de résultats avec URLs.
  c. Pour les 3 premières URLs : fetch-web → si erreur → playwright.
  d. LLM synthétise avec sources.
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
from tools.playwright_client import fetch_url as playwright_fetch

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
Tu es un·e assistant·e de recherche web. Utilise les résultats de recherche
fournis pour répondre avec précision. Cite systématiquement les URLs sources.
Indique la date des informations si disponible.
Réponds dans la même langue que la question.
"""

_KW_SYSTEM = """\
Extrais 3 à 5 mots-clés de recherche optimisés pour DuckDuckGo depuis le message
utilisateur. Si une URL est présente, retourne-la directement.
Retourne UNIQUEMENT les mots-clés séparés par des espaces, sans explication.
"""


async def _fetch_url_with_fallback(url: str) -> str:
    """Tente fetch-web (MCPO) puis playwright en fallback."""
    try:
        result = await call_tool("fetch-web", "fetch", {"url": url, "max_length": 4000})
        content = json.dumps(result, ensure_ascii=False) if isinstance(result, (dict, list)) else str(result)
        if content and content.strip() and content.strip() != "{}":
            return content[:4000]
        raise ValueError("empty fetch-web response")
    except Exception:
        # Fallback playwright
        try:
            return await playwright_fetch(url)
        except Exception as exc:
            return f"Inaccessible : {exc}"


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)
    current_date = state.get("current_date", "")

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
        max_tokens=2048,
    )

    # 1. Extraire les mots-clés / URL explicite
    kw_resp = await llm.ainvoke(
        [SystemMessage(content=_KW_SYSTEM), HumanMessage(content=user_text)],
        config={"max_tokens": 40},
    )
    keywords = kw_resp.content.strip().replace("\n", " ")[:120]
    _prompt_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("input_tokens", 0) or 0
    _completion_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("output_tokens", 0) or 0

    context_parts: list[str] = []

    # Cas URL explicite dans la question
    explicit_url = _extract_url(user_text)
    if explicit_url:
        await _emit(f"🌐 Lecture de {explicit_url[:100]}")
        content = await _fetch_url_with_fallback(explicit_url)
        context_parts.append(f"## Contenu de {explicit_url}\n{content}")
    else:
        # 2. Recherche DuckDuckGo
        ddg_raw = ""
        try:
            await _emit(f"🔎 Recherche web : {keywords}")
            ddg_result = await call_tool("duckduckgo", "search", {
                "query": keywords,
                "max_results": 5,
            })
            ddg_raw = json.dumps(ddg_result, ensure_ascii=False, indent=2)
            context_parts.append(f"## Résultats DuckDuckGo ({keywords!r})\n{ddg_raw[:3000]}")

            # 3. Visiter les 3 premières URLs
            urls = _extract_urls_from_ddg(ddg_result)[:3]
            for url in urls:
                await _emit(f"📄 Lecture source web : {url[:100]}")
                content = await _fetch_url_with_fallback(url)
                context_parts.append(f"## Contenu de {url}\n{content}")
        except Exception as exc:
            context_parts.append(f"## DuckDuckGo indisponible\n{exc}")

    if current_date:
        context_parts.insert(0, f"## Date actuelle : {current_date}")

    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nQuestion utilisateur : {user_text}"

    await _emit("✍️ Synthèse web…")
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    _prompt_tokens += _u.get("input_tokens", 0) or 0
    _completion_tokens += _u.get("output_tokens", 0) or 0
    return {
        "agent_outputs": {"web": response.content},
        "agent_metrics": {"web": {
            "prompt_tokens": _prompt_tokens,
            "completion_tokens": _completion_tokens,
            "model": model or _MODEL,
        }},
    }


def _extract_url(text: str) -> str:
    match = re.search(r"https?://[^\s]+", text)
    return match.group(0) if match else ""


def _extract_urls_from_ddg(data) -> list[str]:
    """Extrait les URLs depuis différents formats de réponse DuckDuckGo."""
    urls: list[str] = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                url = item.get("url") or item.get("href") or item.get("link", "")
                if url and url.startswith("http"):
                    urls.append(url)
    elif isinstance(data, dict):
        for key in ("results", "items", "organic"):
            items = data.get(key, [])
            for item in items:
                if isinstance(item, dict):
                    url = item.get("url") or item.get("href") or item.get("link", "")
                    if url and url.startswith("http"):
                        urls.append(url)
    return urls


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
