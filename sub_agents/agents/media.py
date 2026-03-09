"""
Media Agent — traitement de médias : vidéos YouTube, documents, conversions.
Modèle : GPT-OSS 120B.
Outils : youtube-transcript, markitdown, pandoc (MCPO).
"""

from __future__ import annotations

import json
import os
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are a media content specialist. You process YouTube videos (transcripts), documents (PDF, Word, etc.),
and perform format conversions. Summarize, extract key points, or convert as requested.
Reply in English with clear, structured output.
"""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    context_parts: list[str] = []

    # YouTube
    yt_url = _extract_youtube_url(user_text)
    if yt_url:
        try:
            transcript = await call_tool("youtube-transcript", "get_transcript", {"url": yt_url})
            context_parts.append(f"## YouTube transcript ({yt_url})\n{json.dumps(transcript, ensure_ascii=False)[:4000]}")
        except Exception as exc:
            context_parts.append(f"## YouTube transcript failed\n{exc}")

    # URL de document non-YouTube
    doc_url = _extract_doc_url(user_text)
    if doc_url and not yt_url:
        try:
            converted = await call_tool("markitdown", "convert_url", {"url": doc_url})
            context_parts.append(f"## Document content ({doc_url})\n{json.dumps(converted, ensure_ascii=False)[:4000]}")
        except Exception as exc:
            context_parts.append(f"## Markitdown failed\n{exc}")

    context = "\n\n".join(context_parts)
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.2,
    )

    prompt = f"{context}\n\nUser request: {user_text}" if context else user_text
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])

    return {"agent_outputs": {"media": response.content}}


def _extract_youtube_url(text: str) -> str:
    match = re.search(r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w\-]+)", text)
    return match.group(1) if match else ""


def _extract_doc_url(text: str) -> str:
    match = re.search(r"https?://[^\s]+\.(?:pdf|docx?|xlsx?|pptx?|html?)", text, re.IGNORECASE)
    return match.group(0) if match else ""


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
