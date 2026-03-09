"""
Client Playwright — connexion MCP Streamable HTTP au service playwright.

Le service playwright (mcr.microsoft.com/playwright/mcp) expose un serveur MCP
via le transport Streamable HTTP (POST /) — transport par défaut depuis playwright-mcp v0.0.20.
L'ancien transport SSE (GET /sse) n'est plus utilisé.

Outils principaux :
  browser_navigate(url)     — navigue vers une URL
  browser_snapshot()        — retourne l'arbre d'accessibilité de la page courante
  browser_take_screenshot() — capture d'écran (base64)
"""

from __future__ import annotations

import os

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

_PLAYWRIGHT_BASE_URL = os.environ.get(
    "PLAYWRIGHT_URL", "http://playwright:8931/sse"
).removesuffix("/sse").removesuffix("/")  # normalise vers http://playwright:8931
_TIMEOUT = 30  # secondes


async def fetch_url(url: str) -> str:
    """
    Navigue vers une URL et retourne le contenu textuel (arbre d'accessibilité).

    Args:
        url: URL complète à charger (ex: 'https://example.com')

    Returns:
        Contenu textuel de la page (max 4000 caractères).
    """
    async with streamablehttp_client(_PLAYWRIGHT_BASE_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            await session.call_tool("browser_navigate", {"url": url})
            result = await session.call_tool("browser_snapshot", {})
            return _extract_text(result)


async def search_web(query: str) -> str:
    """
    Effectue une recherche DuckDuckGo et retourne les résultats.

    Args:
        query: termes de recherche

    Returns:
        Contenu textuel de la page de résultats DuckDuckGo.
    """
    search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&ia=web"
    return await fetch_url(search_url)


def _extract_text(result) -> str:
    """Extrait le texte brut d'un résultat de tool MCP."""
    text = ""
    if result and hasattr(result, "content") and result.content:
        for item in result.content:
            if hasattr(item, "text"):
                text += item.text
    return text[:4000] if text else "(empty page)"
