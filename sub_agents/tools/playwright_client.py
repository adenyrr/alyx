"""
Client Playwright — passe par MCPO.

Le serveur MCP `playwright` (mcr.microsoft.com/playwright/mcp) est lancé par
MCPO via [mcpo_config.json](../../mcpo_config.json). Aucun service `playwright`
HTTP autonome n'existe dans compose.yaml : tout transite par MCPO sur
`http://mcpo:8000/playwright/*`.

Outils MCP utilisés :
  browser_navigate(url)  — charge l'URL
  browser_snapshot()     — arbre d'accessibilité textuel de la page courante
"""

from __future__ import annotations

from typing import Any

from tools.mcpo_client import call_tool


async def fetch_url(url: str, max_chars: int = 4000) -> str:
    """
    Navigue vers une URL via Playwright (MCPO) et retourne le texte de la page.

    Args:
        url: URL complète à charger.
        max_chars: tronque le résultat à cette longueur (défaut 4000).

    Returns:
        Texte extrait de l'arbre d'accessibilité, ou message d'erreur explicite.
    """
    try:
        await call_tool("playwright", "browser_navigate", {"url": url})
        snapshot = await call_tool("playwright", "browser_snapshot", {})
    except Exception as exc:
        return f"(playwright unavailable: {exc})"

    text = _extract_text(snapshot)
    return text[:max_chars] if text else "(empty page)"


def _extract_text(payload: Any) -> str:
    """Aplati la réponse MCPO d'un tool MCP en texte brut."""
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        # Format MCP standard : {"content": [{"type": "text", "text": "..."}, ...]}
        content = payload.get("content")
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    txt = item.get("text") or item.get("data") or ""
                    if isinstance(txt, str) and txt:
                        parts.append(txt)
            if parts:
                return "\n".join(parts)
        # Fallback : champs textuels usuels
        for key in ("text", "result", "snapshot", "body"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
    if isinstance(payload, list):
        parts = [_extract_text(item) for item in payload]
        return "\n".join(p for p in parts if p)
    return ""
