"""
Client Context7 — MCP cloud public (https://mcp.context7.com/mcp).
Expose les docs officielles de bibliothèques en temps réel.

Deux outils :
  - resolve_library_id(library_name) → library_id
  - get_library_docs(library_id, topic, tokens) → str (documentation Markdown)
"""

from __future__ import annotations

import os
from typing import Any

import httpx

_CONTEXT7_URL = "https://mcp.context7.com/mcp"
_CONTEXT7_API_KEY = os.environ.get("CONTEXT7_API_KEY", "")
_TIMEOUT = 8.0  # échoue vite si le service cloud est lent ou indisponible

# Client persistent — évite la négociation TLS à chaque appel
_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=_TIMEOUT)
    return _client


def _headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if _CONTEXT7_API_KEY:
        h["Authorization"] = f"Bearer {_CONTEXT7_API_KEY}"
    return h


async def _mcp_call(method: str, params: dict[str, Any]) -> Any:
    """Appelle un outil MCP via HTTP POST JSON-RPC."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": method, "arguments": params},
    }
    client = _get_client()
    resp = await client.post(_CONTEXT7_URL, headers=_headers(), json=payload)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"Context7 error: {data['error']}")
    # Le contenu est dans result.content[0].text
    content = data.get("result", {}).get("content", [])
    if content and isinstance(content, list):
        return content[0].get("text", "")
    return str(data.get("result", ""))


async def resolve_library_id(library_name: str) -> str:
    """
    Résout le nom d'une bibliothèque en son identifiant Context7.

    Args:
        library_name: ex. 'leaflet', 'react', 'pandas'

    Returns:
        library_id utilisable dans get_library_docs (ex. '/leafletjs/leaflet')
    """
    result = await _mcp_call("resolve-library-id", {"libraryName": library_name})
    return str(result)


async def get_library_docs(library_id: str, topic: str = "", tokens: int = 5000) -> str:
    """
    Récupère la documentation d'une bibliothèque sur un sujet précis.

    Args:
        library_id: identifiant résolu par resolve_library_id
        topic:      sujet ou feature spécifique (ex. 'markers', 'authentication')
        tokens:     nombre de tokens max à retourner (défaut 5000)

    Returns:
        Documentation Markdown de la bibliothèque.
    """
    params: dict[str, Any] = {"libraryId": library_id, "tokens": tokens}
    if topic:
        params["topic"] = topic
    result = await _mcp_call("get-library-docs", params)
    return str(result)
