"""
Client Qdrant pour la recherche RAG.
Génère les embeddings via LiteLLM, puis interroge Qdrant directement.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

_QDRANT_URI = os.environ.get("QDRANT_URI", "http://qdrant:6333")
_QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", "")
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_EMBEDDING_MODEL = os.environ.get("RAG_EMBEDDING_MODEL", "text-embedding-3-small")
_TIMEOUT = 30.0


async def _embed(text: str) -> list[float]:
    """Génère un vecteur d'embedding pour un texte via LiteLLM."""
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.post(
                f"{_LITELLM_URL}/embeddings",
                headers={"Authorization": f"Bearer {_LITELLM_API_KEY}"},
                json={"model": _EMBEDDING_MODEL, "input": text},
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:500]
            raise RuntimeError(
                f"Embedding request failed for model '{_EMBEDDING_MODEL}'. "
                "Configure RAG_EMBEDDING_MODEL and ensure the model is declared in LiteLLM. "
                f"Response: {detail}"
            ) from exc
        return resp.json()["data"][0]["embedding"]


async def search(
    query_text: str,
    collection: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Recherche des passages similaires dans Qdrant.

    Args:
        query_text: question ou phrase de recherche
        collection: nom de la collection Qdrant (ex: "openwebui")
        top_k: nombre de résultats à retourner

    Returns:
        Liste de dicts avec 'id', 'score', 'payload' (contient le texte du chunk).
    """
    vector = await _embed(query_text)
    headers: dict[str, str] = {}
    if _QDRANT_API_KEY:
        headers["api-key"] = _QDRANT_API_KEY

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.post(
            f"{_QDRANT_URI}/collections/{collection}/points/search",
            headers=headers,
            json={"vector": vector, "limit": top_k, "with_payload": True},
        )
        resp.raise_for_status()
        return resp.json().get("result", [])
