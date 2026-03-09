"""
ImageGen Agent — génération d'images via Pollinations.ai (direct HTTP).

N'utilise PAS LiteLLM. Appelle directement l'API Pollinations :
  GET https://gen.pollinations.ai/image/{prompt}?model=...&width=...&height=...&enhance=...

Paramètres lus depuis state["_pollinations"] (injecté par alyx_pipeline.py).
La valve enable_image_gen peut désactiver complètement l'agent.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING
from urllib.parse import quote

import httpx

if TYPE_CHECKING:
    from graph.state import AlyxState

_POLLINATIONS_BASE = "https://gen.pollinations.ai/image"
_TIMEOUT = 120.0


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    # Lire la config Pollinations depuis l'état (injectée par _ensure_graph)
    cfg: dict = state.get("_pollinations", {})

    # Valve disable
    if not cfg.get("enable", True):
        return {"agent_outputs": {"image_gen": "🚫 Génération d'images désactivée."}}

    pol_model = cfg.get("model", "flux")
    width = int(cfg.get("width", 1024))
    height = int(cfg.get("height", 1024))
    enhance = cfg.get("enhance", True)
    api_key = cfg.get("api_key", "")

    prompt = _extract_image_prompt(user_text)
    encoded_prompt = quote(prompt, safe="")

    params: dict[str, str] = {
        "model": pol_model,
        "width": str(width),
        "height": str(height),
        "enhance": "true" if enhance else "false",
        "nologo": "true",
    }

    headers: dict[str, str] = {"Accept": "image/*"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    url = f"{_POLLINATIONS_BASE}/{encoded_prompt}"

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()

            # Pollinations renvoie l'image directement OU une URL finale après redirect
            final_url = str(resp.url)

            # Si on reçoit une image binaire, construire un data URI (rare en pratique)
            content_type = resp.headers.get("content-type", "")
            if content_type.startswith("image/"):
                import base64
                img_b64 = base64.b64encode(resp.content).decode()
                mime = content_type.split(";")[0].strip()
                img_md = f"![Image générée](data:{mime};base64,{img_b64})"
            else:
                # Généralement Pollinations redirige vers une URL image CDN
                img_md = f"![Image générée : {prompt}]({final_url})"

            return {
                "agent_outputs": {"image_gen": img_md},
                "artifacts": [{"type": "image", "url": final_url, "prompt": prompt}],
            }

    except Exception as exc:
        return {"agent_outputs": {"image_gen": f"⚠️ Génération d'image échouée : {exc}"}}


def _extract_image_prompt(text: str) -> str:
    """Nettoie le texte utilisateur pour garder uniquement la description à générer."""
    prefixes = [
        "génère une image de", "génère une image d'", "génère une image",
        "générer une image de", "générer une image d'", "générer une image",
        "crée une image de", "crée une image d'", "crée une image",
        "créer une image de", "créer une image d'", "créer une image",
        "dessine", "illustre", "imagine",
        "generate an image of", "generate an image", "create an image of",
        "create an image", "draw", "a picture of", "an image of",
        "une illustration de", "une illustration d'", "une illustration",
    ]
    lower = text.lower().strip()
    for prefix in sorted(prefixes, key=len, reverse=True):
        if lower.startswith(prefix):
            return text[len(prefix):].strip().strip(":").strip()
    return text.strip()


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
