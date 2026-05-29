"""
Vision Agent — analyse poussée d'image (OCR, lecture de graphes, annotation,
extraction de données structurées depuis une image).

Modèle : openrouter/gpt-oss (vision-capable via LiteLLM ; à confirmer selon
provider config). Pour de meilleures perfs vision, brancher Claude Sonnet ou
GPT-4o côté LiteLLM. La pipeline passe les images via `images_b64` dans le state.

Note : Alyx synth a déjà des capacités vision « basiques » via le modèle de
synthèse. Cet agent est dédié à des tâches vision PRÉCISES (OCR, extraction de
tableau d'une image, lecture de schéma) qui demandent un modèle vision dédié
+ un system prompt vision-focused.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.text_utils import last_user_message

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are an expert visual analyst. Given image(s), perform the task requested by
the user with precision. Common tasks:

  - OCR : transcribe ALL visible text verbatim (preserve line breaks, lists,
    tabular structure with Markdown tables).
  - Chart reading : extract the data points / categories / axes / legend, then
    output a Markdown table with the values you read from the chart.
  - Diagram interpretation : describe nodes, edges, hierarchy, with labels.
  - Object identification : list visible objects, count them, note positions.
  - Document structure : identify headings, sections, footnotes.
  - Annotation : if asked to highlight or describe specific regions, be precise
    about location (top-left, lower-right, etc.).

Rules:
  - Be exhaustive but factual — never invent text or values not visible.
  - If text is partially illegible, write `[illegible]` rather than guessing.
  - Reply in the same language as the user's question.
  - When extracting tabular data, use Markdown tables, not prose.
"""


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = last_user_message(messages)
    images_b64 = state.get("images_b64") or []

    emitter = (config.get("configurable") or {}).get("event_emitter") if config else None

    async def _emit(desc: str) -> None:
        if emitter:
            try:
                await emitter({"type": "status", "data": {"description": desc, "done": False}})
            except Exception:
                pass

    if not images_b64:
        return {
            "agent_outputs": {"vision": "⚠️ Aucune image fournie pour analyse vision."},
            "agent_confidence": {"vision": 0.0},
        }

    await _emit(f"👁️ Analyse vision de {len(images_b64)} image(s)…")
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )

    # Composition du message multimodal : texte + images (jusqu'à 4 — la plupart
    # des modèles vision plafonnent là).
    content_parts: list = [{"type": "text", "text": user_text or "Décris cette image de façon exhaustive."}]
    for b64 in images_b64[:4]:
        content_parts.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
        })

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=content_parts),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    output = (response.content or "") + f"\n\n> 👁️ Source : analyse vision de {min(len(images_b64), 4)} image(s)"
    return {
        "agent_outputs": {"vision": output},
        "agent_confidence": {"vision": 0.80},
        "agent_metrics": {"vision": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
    }
