"""
Vector memory conversation — indexation sémantique des tours de chat passés.

Complément du knowledge graph (memory_agent.py) : permet de retrouver des tours
de conversation pertinents par similarité sémantique plutôt que par exact-match
sur le knowledge graph.

Collection Qdrant dédiée par utilisateur·rice (tenant via filtre payload `user_id`).
Indexation à chaque tour via memory_agent.run_bg. Recall à chaque tour via
memory_agent.run (en complément du knowledge graph).

Échec silencieux : tout est best-effort, l'absence de Qdrant ne bloque jamais.
"""

from __future__ import annotations

import hashlib
import os
import time
from typing import Any

import httpx

_COLLECTION_DEFAULT = "alyx_conversation_memory"
_QDRANT_URI = os.environ.get("QDRANT_URI", "http://qdrant:6333")
_QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", "")
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_EMBEDDING_MODEL = os.environ.get("RAG_EMBEDDING_MODEL", "openrouter/embedding")


async def _embed(text: str) -> list[float] | None:
    """Calcule un embedding via LiteLLM (compat OpenAI). None en cas d'échec."""
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(base_url=_LITELLM_URL, api_key=_LITELLM_API_KEY)
        resp = await client.embeddings.create(model=_EMBEDDING_MODEL, input=text[:8000])
        return list(resp.data[0].embedding)
    except Exception:
        return None


async def _ensure_collection(client: "httpx.AsyncClient", vector_size: int,
                             collection: str) -> None:
    """Crée la collection si elle n'existe pas (idempotent)."""
    headers = {"api-key": _QDRANT_API_KEY} if _QDRANT_API_KEY else {}
    try:
        await client.put(
            f"{_QDRANT_URI.rstrip('/')}/collections/{collection}",
            headers=headers,
            json={"vectors": {"size": vector_size, "distance": "Cosine"}},
        )
    except Exception:
        pass


async def index_turn(user_id: str, chat_id: str, user_text: str, alyx_response: str,
                     collection: str = _COLLECTION_DEFAULT) -> None:
    """Indexe un tour de conversation dans Qdrant (best-effort).

    Le texte indexé est la concaténation user_text + alyx_response. Le payload
    contient les deux séparément + métadonnées (user_id, chat_id, timestamp).
    """
    if not user_id or not user_text:
        return
    combined = f"{user_text}\n\n{alyx_response}"[:8000]
    emb = await _embed(combined)
    if not emb:
        return

    headers = {"api-key": _QDRANT_API_KEY} if _QDRANT_API_KEY else {}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await _ensure_collection(client, len(emb), collection)
            # ID dérivé de user_id + chat_id + hash(text) → idempotent.
            seed = f"{user_id}|{chat_id}|{combined}".encode("utf-8", errors="ignore")
            pid = int(hashlib.sha256(seed).hexdigest()[:16], 16)
            await client.put(
                f"{_QDRANT_URI.rstrip('/')}/collections/{collection}/points",
                headers=headers,
                json={"points": [{
                    "id": pid,
                    "vector": emb,
                    "payload": {
                        "user_id": user_id,
                        "chat_id": chat_id,
                        "user_text": user_text[:2000],
                        "alyx_response": alyx_response[:4000],
                        "timestamp": int(time.time()),
                    },
                }]},
            )
    except Exception:
        pass


async def recall_similar(user_id: str, query: str, top_k: int = 3,
                         min_score: float = 0.75,
                         collection: str = _COLLECTION_DEFAULT) -> list[dict[str, Any]]:
    """Retourne jusqu'à `top_k` tours passés sémantiquement proches de `query`,
    filtrés par `user_id` (isolation). Liste vide si rien de pertinent ou échec.
    """
    if not user_id or not query:
        return []
    emb = await _embed(query)
    if not emb:
        return []
    headers = {"api-key": _QDRANT_API_KEY} if _QDRANT_API_KEY else {}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{_QDRANT_URI.rstrip('/')}/collections/{collection}/points/search",
                headers=headers,
                json={
                    "vector": emb,
                    "limit": top_k,
                    "with_payload": True,
                    "filter": {
                        "must": [{"key": "user_id", "match": {"value": user_id}}]
                    },
                },
            )
            if resp.status_code != 200:
                return []
            results = resp.json().get("result", [])
            return [
                {
                    "score": float(hit.get("score", 0.0)),
                    "user_text": (hit.get("payload") or {}).get("user_text", ""),
                    "alyx_response": (hit.get("payload") or {}).get("alyx_response", ""),
                    "timestamp": (hit.get("payload") or {}).get("timestamp", 0),
                }
                for hit in results
                if float(hit.get("score", 0.0)) >= min_score
            ]
    except Exception:
        return []
