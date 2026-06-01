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
# NB : plus de fallback `_anon` partagé — sans user_id fiable on ne cache pas
# (ni exact, ni sémantique), pour ne jamais agréger plusieurs comptes dans un
# bucket commun (fuite cross-user constatée : instruction générique « corrige ce
# document » resservant la réponse d'un·e autre utilisateur·rice).


def cache_key(user_text: str, user_id: str | None = None) -> str | None:
    """Clé déterministe scopée par utilisateur·rice, ou None si non cacheable.

    Format : `alyx:agentcache:{user_id}:{sha256(texte)}`. Le user_id en préfixe
    garantit l'isolation : deux utilisateur·rices posant la même question ont des
    clés différentes, pas de fuite de cache entre comptes.

    Retourne None si user_id est ABSENT : sans identité fiable (fréquent en mode
    Pipelines externe), un bucket `_anon` PARTAGÉ agrégerait plusieurs comptes —
    une instruction générique (« corrige ce document ») y collisionnerait entre
    utilisateur·rices. On préfère ne pas cacher plutôt que fuiter (cf. la même
    règle dans memory_agent : pas de user_id → pas de mémoire).
    """
    uid = (user_id or "").strip()
    if not uid:
        return None
    norm = re.sub(r"\s+", " ", (user_text or "").strip().lower())[:1000]
    digest = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:32]
    return f"{_KEY_PREFIX}{uid}:{digest}"


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


# ─── Cache sémantique (Qdrant) ───────────────────────────────────────────────
# Complémentaire au cache exact (Redis ci-dessus). Cherche par similarité
# cosinus dans Qdrant : si une question sémantiquement proche a déjà été
# traitée (au-delà d'un seuil de similarité), réutilise la réponse.

_SEMANTIC_COLLECTION_DEFAULT = "alyx_semantic_cache"


async def _embed(text: str, embed_url: str, embed_model: str, api_key: str) -> list[float] | None:
    """Calcule un embedding via LiteLLM (compat OpenAI)."""
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(base_url=embed_url, api_key=api_key)
        resp = await client.embeddings.create(model=embed_model, input=text[:8000])
        return list(resp.data[0].embedding)
    except Exception:
        return None


async def semantic_get(qdrant_url: str, qdrant_api_key: str, collection: str,
                       embedding: list[float], threshold: float = 0.92,
                       user_id: str | None = None) -> dict | None:
    """Cherche dans Qdrant le point le plus proche de `embedding`, FILTRÉ par
    `user_id`. Si score ≥ threshold (cosinus), retourne payload['agent_outputs'].

    Multi-user safe : le filtre garantit qu'un·e utilisateur·rice ne peut JAMAIS
    récupérer le cache sémantique d'un·e autre, même si les embeddings sont proches.

    Échec silencieux : indisponibilité Qdrant ⇒ None (pas d'erreur bloquante).
    """
    uid = (user_id or "").strip()
    if not embedding or not uid:
        return None  # pas d'identité fiable → pas de lecture cache (cf. cache_key)
    try:
        import httpx
        headers = {"api-key": qdrant_api_key} if qdrant_api_key else {}
        url = f"{qdrant_url.rstrip('/')}/collections/{collection}/points/search"
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(url, headers=headers, json={
                "vector": embedding,
                "limit": 1,
                "with_payload": True,
                "filter": {
                    "must": [{"key": "user_id", "match": {"value": uid}}]
                },
            })
            if resp.status_code != 200:
                return None
            results = resp.json().get("result", [])
            if not results:
                return None
            top = results[0]
            if float(top.get("score", 0.0)) < threshold:
                return None
            payload = top.get("payload", {})
            ao = payload.get("agent_outputs")
            return ao if isinstance(ao, dict) else None
    except Exception:
        return None


async def semantic_store(qdrant_url: str, qdrant_api_key: str, collection: str,
                         embedding: list[float], agent_outputs: dict,
                         user_id: str | None = None) -> None:
    """Stocke (embedding, agent_outputs, user_id) dans Qdrant. Échec silencieux.

    Le payload contient user_id pour permettre le filtre de lecture (cf.
    semantic_get). L'ID du point intègre user_id : un même texte stocké par
    plusieurs utilisateur·rices coexiste sans collision.

    Crée la collection idempotemment.
    """
    uid = (user_id or "").strip()
    if not embedding or not agent_outputs or not uid:
        return  # pas d'identité fiable → pas d'écriture cache (cf. cache_key)
    try:
        import httpx
        headers = {"api-key": qdrant_api_key} if qdrant_api_key else {}
        base = qdrant_url.rstrip("/")
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Crée la collection idempotemment + index sur user_id pour des
            # filtres rapides (sinon Qdrant linéaire sur le payload).
            await client.put(
                f"{base}/collections/{collection}",
                headers=headers,
                json={"vectors": {"size": len(embedding), "distance": "Cosine"}},
            )
            try:
                await client.put(
                    f"{base}/collections/{collection}/index",
                    headers=headers,
                    json={"field_name": "user_id", "field_schema": "keyword"},
                )
            except Exception:
                pass  # déjà créé
            # ID intègre user_id pour éviter collision multi-user sur même contenu
            first_out = next(iter(agent_outputs.values()), "")
            seed = f"{uid}|{first_out}".encode("utf-8", errors="ignore")
            pid = int(hashlib.sha256(seed).hexdigest()[:16], 16)
            await client.put(
                f"{base}/collections/{collection}/points",
                headers=headers,
                json={"points": [{
                    "id": pid,
                    "vector": embedding,
                    "payload": {"agent_outputs": agent_outputs, "user_id": uid},
                }]},
            )
    except Exception:
        pass
