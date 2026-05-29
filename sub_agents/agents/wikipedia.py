"""
Wikipedia Agent — recherche encyclopédique via MCPO wikipedia-mcp.

Modèle : openrouter/qwen3.5-flash.
Outil  : wikipedia (MCPO) — serveur wikipedia-mcp en français.

Stratégie :
  1. LLM extrait 2-3 mots-clés français optimisés pour Wikipedia.
  2. Appel MCPO wikipedia/search avec ces mots-clés.
  3. LLM synthétise en incluant les sources Wikipedia.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.mcpo_client import call_tool
from tools.text_utils import extract_query_variants

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
Tu es un·e spécialiste de la connaissance encyclopédique. Utilise les résultats
Wikipedia fournis pour répondre avec précision. Cite les articles Wikipedia
consultés, les dates de publication et les sections pertinentes.
Structure ta réponse avec des titres markdown clairs.
Réponds dans la même langue que la question.
"""

_KW_SYSTEM_TEMPLATE = """\
Extract 2 to 3 short keywords for Wikipedia search, in {lang} (ISO code).
Return ONLY the keywords separated by spaces, no punctuation, no explanation.
"""


def _detect_language(text: str) -> str:
    """Heuristique simple de détection de langue (fr/en/es/de/it/pt).

    Retourne le code ISO le plus probable. Volontairement léger : pas de dep
    `langdetect` (~10 Mo). Pour les questions courtes, c'est largement suffisant.
    Défaut : 'en' (Wikipedia EN est la plus complète si on doute).
    """
    t = text.lower()
    fr_markers = re.compile(r"[àâçéèêëîïôûùüÿœæ]|\b(le|la|les|un|une|des|et|est|qui|que|dans|pour|avec|sur|sans|sous|ont|sont|était|étaient|été|été|nous|vous|comment|pourquoi|quand)\b")
    es_markers = re.compile(r"[áéíóúñ¿¡]|\b(el|la|los|las|que|para|con|sin|por|donde|cuando|cómo|qué)\b")
    de_markers = re.compile(r"[äöüß]|\b(der|die|das|und|ist|sind|nicht|mit|für|von|was|wie|wann|warum|wo)\b")
    it_markers = re.compile(r"\b(il|lo|la|gli|le|che|come|quando|dove|perché|sono|è|sono)\b|[àèéìòù]")
    pt_markers = re.compile(r"[ãõáâàçéêíóôú]|\b(o|a|os|as|que|para|com|sem|por|como|quando|onde|por que)\b")
    if fr_markers.search(t):
        return "fr"
    if es_markers.search(t):
        return "es"
    if de_markers.search(t):
        return "de"
    if pt_markers.search(t):
        return "pt"
    if it_markers.search(t):
        return "it"
    return "en"


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)
    current_date = state.get("current_date", "")

    emitter = (config.get("configurable") or {}).get("event_emitter") if config else None

    async def _emit(desc: str) -> None:
        if emitter:
            try:
                await emitter({"type": "status", "data": {"description": desc, "done": False}})
            except Exception:
                pass

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0,
        max_tokens=512,
    )

    # 1. Détection langue + extraction de 2-3 mots-clés DANS LA MÊME LANGUE.
    # Le MCP wikipedia-mcp est démarré avec --language fr (cf. mcpo_config.json),
    # mais beaucoup d'instances acceptent un paramètre `language` à l'appel —
    # on le passe défensivement (ignoré si non supporté). Le keyword-extractor,
    # lui, génère DÉJÀ dans la bonne langue, ce qui aide même si le MCP reste fr.
    lang = _detect_language(user_text)
    kw_resp = await llm.ainvoke(
        [
            SystemMessage(content=_KW_SYSTEM_TEMPLATE.format(lang=lang)),
            HumanMessage(content=user_text),
        ],
        config={"max_tokens": 20},
    )
    keywords = re.sub(r"<think(?:ing)?[^>]*>.*?</think(?:ing)?>", "", kw_resp.content, flags=re.DOTALL | re.IGNORECASE).strip().replace("\n", " ")[:100]
    _prompt_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("input_tokens", 0) or 0
    _completion_tokens = (getattr(kw_resp, "usage_metadata", None) or {}).get("output_tokens", 0) or 0

    # 2. Recherche Wikipedia via MCPO
    # wikipedia-mcp expose `search_wikipedia` (pas `search`) + `get_summary`.
    # On enchaîne : search → top N titres → résumés courts → synthèse.
    # N piloté par la valve sources_wikipedia_articles.
    limits = state.get("_sources") or {}
    articles_n = int(limits.get("wikipedia_articles", 3))
    truncate_chars = int(limits.get("truncate_chars", 4000))

    wiki_raw = ""
    summaries: list[str] = []  # alimenté dans le try, lu après pour la confidence
    try:
        # Query expansion : si la valve est on, lancer N variantes en parallèle
        # pour diversifier les articles trouvés (différents angles du sujet).
        use_qe = bool(limits.get("enable_query_expansion", False))
        if use_qe:
            variants = await extract_query_variants(user_text, n=2, lang=lang)
            await _emit(f"📖 Recherche Wikipédia (×{len(variants)} variantes)")
            search_results = await asyncio.gather(
                *(call_tool("wikipedia", "search_wikipedia",
                            {"query": v, "limit": articles_n, "language": lang})
                  for v in variants),
                return_exceptions=True,
            )
            # Merger les titres uniques
            all_titles: list[str] = []
            seen_t: set[str] = set()
            for r in search_results:
                if isinstance(r, BaseException):
                    continue
                for t in _extract_titles(r, max_n=articles_n):
                    if t not in seen_t:
                        seen_t.add(t)
                        all_titles.append(t)
            titles = all_titles[:articles_n]
            search_result = {"variants": variants, "merged_titles": titles}
        else:
            await _emit(f"📖 Recherche Wikipédia : {keywords}")
            search_result = await call_tool("wikipedia", "search_wikipedia",
                                            {"query": keywords, "limit": articles_n, "language": lang})
            titles = _extract_titles(search_result, max_n=articles_n)
        summaries: list[str] = []
        if titles:
            await _emit(f"📄 Résumés des {len(titles)} article(s)…")
            # Fetch parallèle des résumés (gain : ~ (N-1) * latence d'un appel).
            async def _fetch_one(t: str) -> tuple[str, str] | None:
                try:
                    summary = await call_tool("wikipedia", "get_summary", {"title": t, "language": lang})
                    return (t, json.dumps(summary, ensure_ascii=False)[:truncate_chars])
                except Exception:
                    return None
            fetched = await asyncio.gather(*(_fetch_one(t) for t in titles), return_exceptions=True)
            for item in fetched:
                if isinstance(item, tuple):
                    summaries.append(f"### {item[0]}\n{item[1]}")
        wiki_payload = {"search": search_result, "summaries": summaries}
        wiki_raw = json.dumps(wiki_payload, ensure_ascii=False, indent=2)[:max(truncate_chars * 2, 6000)]
    except Exception as exc:
        wiki_raw = f"Wikipedia indisponible : {exc}"

    # 3. Synthèse LLM
    date_prefix = f"## Date actuelle : {current_date}\n\n" if current_date else ""
    prompt = (
        f"{date_prefix}## Résultats Wikipedia (mots-clés : {keywords!r})\n{wiki_raw}"
        f"\n\nQuestion utilisateur : {user_text}"
    )

    await _emit("✍️ Synthèse Wikipédia…")
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    _prompt_tokens += _u.get("input_tokens", 0) or 0
    _completion_tokens += _u.get("output_tokens", 0) or 0
    # Confidence wikipedia : 0.70 si ≥ 2 articles consultés, 0.55 si 1 seul,
    # 0.30 si indisponible. Wikipedia est globalement fiable mais éditable —
    # on ne dépasse pas 0.75 sans corroboration.
    if "indisponible" in wiki_raw.lower():
        conf = 0.30
    elif len(summaries) >= 2:
        conf = 0.70
    else:
        conf = 0.55
    return {
        "agent_outputs": {"wikipedia": response.content},
        "agent_confidence": {"wikipedia": conf},
        "agent_metrics": {"wikipedia": {
            "prompt_tokens": _prompt_tokens,
            "completion_tokens": _completion_tokens,
            "model": model or _MODEL,
        }},
    }


def _extract_titles(search_payload, max_n: int = 3) -> list[str]:
    """Extrait les titres d'articles depuis la réponse `search_wikipedia`.

    Le format peut varier selon la version : dict avec `results: [{title, snippet, ...}]`,
    liste plate, ou enveloppe MCP `{content: [{text: "..."}]}`. On gère les cas
    courants et on s'arrête au premier qui marche."""
    if isinstance(search_payload, dict):
        # Enveloppe MCPO standard
        content = search_payload.get("content")
        if isinstance(content, list) and content:
            try:
                inner = json.loads(content[0].get("text", ""))
                return _extract_titles(inner, max_n=max_n)
            except Exception:
                pass
        for key in ("results", "items", "articles"):
            items = search_payload.get(key)
            if isinstance(items, list):
                return [str(it.get("title", "")).strip() for it in items if isinstance(it, dict) and it.get("title")][:max_n]
    if isinstance(search_payload, list):
        return [str(it.get("title", "")).strip() for it in search_payload if isinstance(it, dict) and it.get("title")][:max_n]
    return []


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
