"""
Client HTTP async pour MCPO (MCP-to-OpenAPI proxy).
Chaque serveur MCP est exposé sous http://mcpo:8000/{server}/{tool}.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

_MCPO_URL = os.environ.get("MCPO_URL", "http://mcpo:8000")
_TIMEOUT = 60.0

# Client persistent — pool de connexions réutilisées vers mcpo (même réseau Docker)
_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=_TIMEOUT)
    return _client


async def call_tool(server: str, tool: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Appelle un outil MCP via MCPO.

    Args:
        server: nom du serveur tel que défini dans mcpo_config.json
                (ex: 'paper-search', 'memory', 'calculator')
        tool:   nom de l'endpoint/outil (ex: 'search_papers', 'store', 'evaluate')
        payload: corps JSON de la requête (paramètres de l'outil)

    Returns:
        Réponse JSON de l'outil sous forme de dict.
    """
    url = f"{_MCPO_URL}/{server}/{tool}"
    client = _get_client()
    resp = await client.post(url, json=payload or {})
    resp.raise_for_status()
    return resp.json()
