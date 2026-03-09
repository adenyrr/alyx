"""
ImageGen Agent — génération d'images via pollinations.ai (flux / klein-large).
Utilise le endpoint LiteLLM /v1/images/generations qui route vers pollinations/flux.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import httpx

if TYPE_CHECKING:
    from graph.state import AlyxState

_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_MODEL = "pollinations/flux"  # pointe vers klein-large dans litellm_config.yaml
_TIMEOUT = 120.0


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    # Extraire le prompt image du message utilisateur
    prompt = _extract_image_prompt(user_text)

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(
                f"{_LITELLM_URL}/images/generations",
                headers={"Authorization": f"Bearer {_LITELLM_API_KEY}"},
                json={"model": model or _MODEL, "prompt": prompt, "n": 1, "size": "1024x1024"},
            )
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()

        # Récupérer l'URL de l'image générée
        images = data.get("data", [])
        if images:
            image_url = images[0].get("url", "")
            if image_url:
                # Retourner en markdown image pour rendu inline OpenWebUI
                output = f"![Generated image]({image_url})"
                return {
                    "agent_outputs": {"image_gen": output},
                    "artifacts": [{"type": "image", "url": image_url, "prompt": prompt}],
                }

        return {"agent_outputs": {"image_gen": "Image generation returned no result."}}

    except Exception as exc:
        return {"agent_outputs": {"image_gen": f"Image generation failed: {exc}"}}


def _extract_image_prompt(text: str) -> str:
    """Nettoie et retourne le prompt image depuis la demande utilisateur."""
    # Retirer les formulations communes de demande
    for prefix in [
        "génère une image", "générer une image", "crée une image", "créer une image",
        "dessine", "illustre", "generate an image", "create an image", "draw", "imagine",
        "une image de", "an image of",
    ]:
        lower = text.lower()
        if prefix in lower:
            idx = lower.index(prefix) + len(prefix)
            return text[idx:].strip().strip(":").strip()
    return text.strip()


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
