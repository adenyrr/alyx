"""
ImageGen Agent — génération d'images multi-provider local-friendly.

Providers supportés (par ordre de fallback) :
  1. Pollinations.ai (direct HTTP, gratuit, sans clé) — défaut, local-friendly.
  2. LiteLLM (DALL-E / Stable Diffusion / autres modèles vision déclarés dans
     litellm_config.yaml). Permet à un utilisateur·rice ayant configuré son
     propre fournisseur de l'utiliser sans changer le code.

Sélection via state["_pollinations"]["provider"] (défaut "pollinations") :
  - "pollinations" : appel HTTP direct
  - "litellm" : utilise le client OpenAI compatible vers LiteLLM
                (modèle dans state["_pollinations"]["model"], ex. "openai/dall-e-3")

La valve enable_image_gen peut désactiver complètement l'agent.
"""

from __future__ import annotations

import base64
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
        return {"agent_outputs": {"image_gen": "🚫 Génération d'images désactivée."},
                "agent_confidence": {"image_gen": 0.0}}

    pol_model = cfg.get("model", "flux")
    provider = cfg.get("provider", "pollinations")
    width = int(cfg.get("width", 1024))
    height = int(cfg.get("height", 1024))
    enhance = cfg.get("enhance", True)
    api_key = cfg.get("api_key", "")

    prompt = _extract_image_prompt(user_text)

    # Provider 2 : LiteLLM (DALL-E ou autre modèle image déclaré dans litellm_config.yaml)
    if provider == "litellm":
        return await _generate_via_litellm(prompt, pol_model, width, height)

    # Provider 1 : Pollinations (défaut, gratuit, sans clé)
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

            # Alt-text descriptif (accessibilité + indexation) construit depuis le
            # prompt utilisateur, tronqué pour rester lisible. Inclut le modèle pour
            # transparence (« quelle IA a généré ça ? »).
            alt_text = f"{prompt[:140]} — {pol_model} via Pollinations.ai"
            content_type = resp.headers.get("content-type", "")
            if content_type.startswith("image/"):
                import base64
                img_b64 = base64.b64encode(resp.content).decode()
                mime = content_type.split(";")[0].strip()
                img_md = f"![{alt_text}](data:{mime};base64,{img_b64})"
            else:
                # Généralement Pollinations redirige vers une URL image CDN
                img_md = f"![{alt_text}]({final_url})"
            # Citation source en ligne (cohérent avec les > 📊 / > 📖 des autres agents)
            img_md += f"\n\n> 🎨 Source : [Pollinations.ai · modèle {pol_model}]({final_url})"

            return {
                "agent_outputs": {"image_gen": img_md},
                "agent_confidence": {"image_gen": 0.85},
                "agent_metrics": {},
                "artifacts": [{"type": "image", "url": final_url, "prompt": prompt}],
            }

    except Exception as exc:
        return {"agent_outputs": {"image_gen": f"⚠️ Génération d'image échouée : {exc}"},
                "agent_confidence": {"image_gen": 0.0}}


async def _generate_via_litellm(prompt: str, model: str, width: int, height: int) -> dict:
    """Génère une image via LiteLLM (DALL-E 3, etc.) — utile si un fournisseur
    image est déclaré dans litellm_config.yaml. Retourne le même contrat que
    le provider Pollinations (markdown + artifact).
    """
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url=os.environ.get("LITELLM_URL", "http://litellm:4000/v1"),
            api_key=os.environ.get("LITELLM_API_KEY", ""),
        )
        # Taille la plus proche dans le set supporté par DALL-E 3 (1024x1024, 1792x1024, 1024x1792)
        size = "1024x1024"
        if width > height:
            size = "1792x1024"
        elif height > width:
            size = "1024x1792"
        resp = await client.images.generate(
            model=model if model not in ("flux", "zimage") else "dall-e-3",
            prompt=prompt,
            n=1,
            size=size,
            response_format="b64_json",
        )
        b64 = resp.data[0].b64_json
        alt_text = f"{prompt[:140]} — {model} via LiteLLM"
        img_md = f"![{alt_text}](data:image/png;base64,{b64})\n\n> 🎨 Source : modèle `{model}` via LiteLLM"
        return {
            "agent_outputs": {"image_gen": img_md},
            "agent_confidence": {"image_gen": 0.90},
            "agent_metrics": {},
            "artifacts": [{
                "type": "image",
                "url": f"data:image/png;base64,{b64}",
                "prompt": prompt,
            }],
        }
    except Exception as exc:
        return {"agent_outputs": {"image_gen": f"⚠️ Génération LiteLLM échouée : {exc}"},
                "agent_confidence": {"image_gen": 0.0}}


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
