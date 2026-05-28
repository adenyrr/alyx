"""
Cache Redis optionnel des sorties d'agents.

Sert à dédupliquer les requêtes répétées sans relancer le graphe multi-agents.
Conçu pour être conservateur sur la correction :

  - On ne met JAMAIS en cache les agents temps-réel (web, météo, finance, image,
    transcription, RAG, mémoire) : leurs réponses dépendent du moment ou d'un
    contexte mutable.
  - On ne met PAS en cache les tours produisant des artifacts (dev/writer/image) :
    le base64 gonflerait Redis et ces sorties sont peu réutilisables telles quelles.
  - On ne met PAS en cache les sorties en erreur (⚠️/⏱️).

Le client Redis est importé paresseusement : l'absence du paquet `redis` ou d'une
instance joignable n'empêche jamais le pipeline de fonctionner (échec silencieux).
"""

from __future__ import annotations

import hashlib
import json
import re

# Agents dont la sortie dépend du temps / d'un contexte mutable → jamais en cache.
_TIME_SENSITIVE = {"web", "geo", "data", "image_gen", "media", "rag", "memory"}

_KEY_PREFIX = "alyx:agentcache:"


def cache_key(user_text: str) -> str:
    """Clé déterministe normalisée à partir du message utilisateur."""
    norm = re.sub(r"\s+", " ", (user_text or "").strip().lower())[:1000]
    digest = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:32]
    return _KEY_PREFIX + digest


def is_cacheable(agent_outputs: dict, artifacts: list) -> bool:
    """Vrai si le tour est sûr à mettre en cache (déterministe, sans artifact/erreur)."""
    if artifacts or not agent_outputs:
        return False
    keys = set(agent_outputs.keys())
    if keys & _TIME_SENSITIVE:
        return False
    for v in agent_outputs.values():
        if isinstance(v, str) and v.startswith(("⚠️", "⏱️")):
            return False
    return True


async def get(redis_url: str, key: str) -> dict | None:
    """Récupère un dict agent_outputs en cache, ou None (échec silencieux)."""
    try:
        import redis.asyncio as aioredis
        client = aioredis.from_url(redis_url)
        try:
            raw = await client.get(key)
        finally:
            await client.aclose()
        if not raw:
            return None
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


async def store(redis_url: str, key: str, agent_outputs: dict, ttl: int) -> None:
    """Stocke agent_outputs en cache avec TTL (échec silencieux).

    Nommée `store` et non `set` pour ne pas shadowner le builtin `set` à l'intérieur
    du module (utilisé par `is_cacheable`).
    """
    try:
        import redis.asyncio as aioredis
        client = aioredis.from_url(redis_url)
        try:
            await client.set(key, json.dumps(agent_outputs), ex=ttl)
        finally:
            await client.aclose()
    except Exception:
        pass
