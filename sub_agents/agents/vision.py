"""
Vision Agent — analyse les images avec qwen/qwen3.5-flash (multimodal).
Reçoit les images base64 de l'état et retourne une description détaillée.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are a vision analysis expert. Analyze the provided image(s) thoroughly.
Describe content, text (OCR), objects, colors, layout, charts, diagrams, or any relevant detail.
Return a structured, factual description in English for the main agent to use.
"""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    images_b64 = state.get("images_b64", [])
    messages = state.get("messages", [])

    if not images_b64:
        return {"agent_outputs": {"vision": "No images provided."}}

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )

    # Dernier message humain comme contexte
    user_text = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_text = msg.content if isinstance(msg.content, str) else ""
            break

    content: list = []
    if user_text:
        content.append({"type": "text", "text": user_text})
    for b64 in images_b64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
        })

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=content),
    ])

    return {"agent_outputs": {"vision": response.content}}
