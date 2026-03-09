"""
Doc Agent — recherche académique et accès au texte intégral.

Modèle : openrouter/deepseek.
Outils :
  1. sequential-thinking (MCPO) — plan de recherche.
  2. paper-search (MCPO)        — 14 bases de données académiques.
  3. fetch-web (MCPO)           — accès sci-hub (fallback playwright).

Stratégie :
  a. Sequential-thinking décompose la question en plan de recherche.
  b. paper-search retourne les articles avec DOIs.
  c. Pour les articles sans résumé complet : sci-hub.se → fetch-web → playwright.
  d. LLM synthétise avec citations complètes (DOI, auteurs, année).
"""

from __future__ import annotations

import json
import os
import re
from typing import TYPE_CHECKING
from urllib.parse import quote_plus

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool
from tools.playwright_client import fetch_url as playwright_fetch

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/deepseek"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SCIHUB_MIRRORS = [
    "https://sci-hub.se",
    "https://sci-hub.st",
    "https://sci-hub.ru",
]

_SYSTEM = """\
Tu es un·e spécialiste de la littérature scientifique peer-reviewed.
Analyse les résultats de recherche académique fournis et synthétise les
résultats en cohérence avec la question posée.

RÈGLES DE CITATION (OBLIGATOIRES) :
- Cite chaque article avec : titre, auteur·es, année, journal, DOI.
- Format : > 📄 **Titre** — Auteur·es (Année) · *Journal* · doi:XXX
- Mentionne clairement si un article n'est disponible qu'en résumé.
- Classe les articles du plus récent au plus ancien.
- Quantifie les niveaux de preuve quand pertinent.
- Indique les limites et biais des études.

Réponds dans la même langue que la question.
"""

_KW_SYSTEM = """\
Transforme la question en 3-5 mots-clés de recherche académique en anglais.
Retourne UNIQUEMENT les mots-clés séparés par des espaces, sans explication.
"""


async def _fetch_scihub(doi: str) -> str:
    """Tente de récupérer le texte intégral depuis sci-hub (fetch-web → playwright)."""
    encoded_doi = quote_plus(doi)
    for mirror in _SCIHUB_MIRRORS:
        url = f"{mirror}/{encoded_doi}"
        # Essai 1 : fetch-web (MCPO)
        try:
            result = await call_tool("fetch-web", "fetch", {"url": url, "max_length": 6000})
            content = json.dumps(result, ensure_ascii=False) if isinstance(result, (dict, list)) else str(result)
            if content and len(content.strip()) > 200:
                return f"[sci-hub via fetch-web: {url}]\n{content[:5000]}"
        except Exception:
            pass
        # Essai 2 : playwright (fallback)
        try:
            content = await playwright_fetch(url)
            if content and len(content.strip()) > 200 and "captcha" not in content.lower():
                return f"[sci-hub via playwright: {url}]\n{content[:5000]}"
        except Exception:
            pass
    return ""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)
    current_date = state.get("current_date", "")

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
        max_tokens=4096,
    )

    # 1. Extraire les mots-clés académiques anglais
    kw_resp = await llm.ainvoke(
        [SystemMessage(content=_KW_SYSTEM), HumanMessage(content=user_text)],
        config={"max_tokens": 30},
    )
    keywords = kw_resp.content.strip().replace("\n", " ")[:120]
    _prompt_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("input_tokens", 0) or 0
    _completion_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("output_tokens", 0) or 0

    context_parts: list[str] = []

    # 2. Plan de recherche via sequential-thinking
    try:
        seq_result = await call_tool("sequential-thinking", "sequentialthinking", {
            "thought": f"Research plan for: {keywords}"
        })
        seq_str = json.dumps(seq_result, ensure_ascii=False, indent=2)
        context_parts.append(f"## Research plan\n{seq_str[:1500]}")
    except Exception as exc:
        context_parts.append(f"## Sequential-thinking unavailable: {exc}")

    # 3. Recherche académique
    try:
        papers_result = await call_tool("paper-search", "search_papers", {
            "query": keywords,
            "limit": 8,
        })
        papers_str = json.dumps(papers_result, ensure_ascii=False, indent=2)
        context_parts.append(f"## Paper search results ({keywords!r})\n{papers_str[:5000]}")

        # 4. Pour chaque article avec DOI mais sans résumé complet → sci-hub
        dois = _extract_dois(papers_result)
        for doi in dois[:3]:  # max 3 articles via sci-hub
            fulltext = await _fetch_scihub(doi)
            if fulltext:
                context_parts.append(f"## Full text DOI:{doi}\n{fulltext}")
    except Exception as exc:
        context_parts.append(f"## Paper search failed: {exc}")

    if current_date:
        context_parts.insert(0, f"## Current date: {current_date}")

    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nQuestion : {user_text}"

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    _prompt_tokens += _u.get("input_tokens", 0) or 0
    _completion_tokens += _u.get("output_tokens", 0) or 0
    return {
        "agent_outputs": {"doc": response.content},
        "agent_metrics": {"doc": {
            "prompt_tokens": _prompt_tokens,
            "completion_tokens": _completion_tokens,
            "model": model or _MODEL,
        }},
    }


def _extract_dois(papers_data) -> list[str]:
    """Extrait les DOIs depuis la réponse paper-search."""
    dois: list[str] = []
    doi_pattern = re.compile(r"10\.\d{4,9}/[^\s\"',]+")

    text = json.dumps(papers_data, ensure_ascii=False)
    for match in doi_pattern.finditer(text):
        doi = match.group(0).rstrip(".,;)")
        if doi not in dois:
            dois.append(doi)
        if len(dois) >= 5:
            break
    return dois


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
