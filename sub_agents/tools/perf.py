"""
Utilitaires de performance partagés par la pipeline.

  - compress_agent_outputs : compression LLM (cheap) des outputs longs avant
    synthèse, pour réduire le coût du modèle Alyx (qui peut être expensive).
  - select_model_by_complexity : heuristique simple pour basculer sur un modèle
    cheap quand la requête est manifestement triviale.
  - warm_up_litellm : pré-chauffe les connexions LiteLLM à l'initialisation
    (réduit la latence du premier token).
"""

from __future__ import annotations

import asyncio
import os
import re
from typing import Iterable

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")


_COMPRESS_SYSTEM = """\
You compress agent outputs for downstream synthesis. Keep ALL facts, numbers,
names, sources, and citations. Remove ONLY filler prose, repetitions, and
chatty transitions. Output should be ≤ 40% the length of the input but lose
zero factual content. Preserve Markdown links (sources!).
"""


async def compress_agent_outputs(agent_outputs: dict[str, str], target_max_chars: int = 8000,
                                 model: str = "openrouter/qwen3.5-flash") -> dict[str, str]:
    """Compresse les outputs agents > 2000 chars via un appel LLM cheap.

    Court-circuite si tous les outputs cumulés font < target_max_chars (pas besoin).
    """
    total = sum(len(v) for v in agent_outputs.values() if isinstance(v, str))
    if total <= target_max_chars:
        return agent_outputs

    llm = ChatOpenAI(
        model=model,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0,
    )

    async def _compress_one(name: str, text: str) -> tuple[str, str]:
        if len(text) < 2000:
            return (name, text)
        try:
            resp = await llm.ainvoke([
                SystemMessage(content=_COMPRESS_SYSTEM),
                HumanMessage(content=f"Agent: {name}\n\n{text[:12000]}"),
            ])
            return (name, resp.content or text)
        except Exception:
            return (name, text)

    compressed = await asyncio.gather(*(_compress_one(n, v) for n, v in agent_outputs.items()))
    return dict(compressed)


# ─── Model auto-selection ─────────────────────────────────────────────────────
# Heuristique : pour les questions clairement triviales (≤ 12 mots, salutation,
# remerciement), bascule sur un modèle cheap. Sinon, garde le modèle configuré.
# Évite de payer le tarif Opus pour répondre "bonjour".

_TRIVIAL_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^\s*(bonjour|salut|hello|hi|coucou|hey|bonsoir|merci|thanks|ok|d'accord|cool|super|génial|parfait)[\s!.,?]*$", re.IGNORECASE),
    re.compile(r"^\s*(comment vas[\s-]tu|how are you|ça va|how's it going)[\s?!.,]*$", re.IGNORECASE),
]


def select_model_by_complexity(user_text: str, default_model: str,
                               cheap_model: str = "openrouter/qwen3.5-flash") -> str:
    """Retourne `cheap_model` pour les requêtes triviales, sinon `default_model`."""
    t = (user_text or "").strip()
    if len(t) <= 60 and len(t.split()) <= 12:
        for pat in _TRIVIAL_PATTERNS:
            if pat.match(t):
                return cheap_model
    return default_model


# ─── Pré-chauffe LiteLLM ──────────────────────────────────────────────────────

async def warm_up_litellm(model: str, base_url: str | None = None, api_key: str | None = None) -> None:
    """Émet une requête minimale (1 token) pour ouvrir la connexion HTTP keep-alive
    et faire monter en cache le routing LiteLLM. Échec silencieux.
    """
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url=base_url or _LITELLM_URL,
            api_key=api_key or _LITELLM_API_KEY,
        )
        await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ok"}],
            max_tokens=1,
            stream=False,
        )
    except Exception:
        pass


async def warm_up_all(models: Iterable[str]) -> None:
    """Pré-chauffe en parallèle tous les modèles passés (dédupliqués)."""
    unique = list({m for m in models if m and isinstance(m, str)})
    await asyncio.gather(*(warm_up_litellm(m) for m in unique), return_exceptions=True)
