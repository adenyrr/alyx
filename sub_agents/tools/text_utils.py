"""
Utilitaires texte partagés entre agents.

Centralise les helpers récurrents (langue, strip reasoning tags, last user message)
pour éviter la duplication et garantir un comportement uniforme.
"""

from __future__ import annotations

import os
import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


_THINK_RE = re.compile(r"<think(?:ing)?[^>]*>.*?</think(?:ing)?>", re.DOTALL | re.IGNORECASE)


def strip_think_tags(text: str) -> str:
    """Retire les balises <think>…</think> et <thinking>…</thinking> émises par
    certains modèles à raisonnement. Évite que ces tags polluent les keywords
    extraits, les locations géocodées, etc.
    """
    return _THINK_RE.sub("", text or "")


def last_user_message(messages: list) -> str:
    """Dernier message de l'utilisateur·rice depuis une liste BaseMessage LangChain."""
    for msg in reversed(messages or []):
        if getattr(msg, "type", None) == "human":
            content = getattr(msg, "content", "")
            return content if isinstance(content, str) else ""
    return ""


_LANG_PATTERNS: dict[str, re.Pattern[str]] = {
    "fr": re.compile(r"[àâçéèêëîïôûùüÿœæ]|\b(le|la|les|un|une|des|et|est|qui|que|dans|pour|avec|sur|sans|sous|ont|sont|était|étaient|été|nous|vous|comment|pourquoi|quand)\b"),
    "es": re.compile(r"[áéíóúñ¿¡]|\b(el|la|los|las|que|para|con|sin|por|donde|cuando|cómo|qué)\b"),
    "de": re.compile(r"[äöüß]|\b(der|die|das|und|ist|sind|nicht|mit|für|von|was|wie|wann|warum|wo)\b"),
    "it": re.compile(r"[àèéìòù]|\b(il|lo|gli|le|che|come|quando|dove|perché|sono|è)\b"),
    "pt": re.compile(r"[ãõáâàçéêíóôú]|\b(o|os|as|que|para|com|sem|por|como|quando|onde)\b"),
}


def detect_language(text: str) -> str:
    """Heuristique simple de détection de langue (fr/en/es/de/it/pt).

    Retourne le code ISO le plus probable. Volontairement léger : pas de dep
    `langdetect`. Défaut : 'en' si rien ne matche (Wikipedia EN est la plus complète).
    """
    t = (text or "").lower()
    for lang, pattern in _LANG_PATTERNS.items():
        if pattern.search(t):
            return lang
    return "en"


_KEYWORDS_SYSTEM_TEMPLATE = """\
Extract search keywords from the user's question, optimized for {target}.
Output ONLY {n_min} to {n_max} keywords separated by spaces, in {lang}, no punctuation.
If a URL is present in the question, return that URL verbatim (no keyword extraction).
"""


async def extract_keywords(
    user_text: str,
    *,
    target: str = "web search",
    n_min: int = 3,
    n_max: int = 5,
    lang: str | None = None,
    model: str = "openrouter/qwen3.5-flash",
    max_tokens: int = 40,
) -> str:
    """Extraction de keywords mutualisée. Utilisée par web/wikipedia/doc pour éviter
    3 appels LLM redondants par tour (un seul appel cheap qwen-flash suffit).

    Args:
        user_text: question utilisateur.
        target: ce pour quoi optimiser ("web search", "Wikipedia", "academic papers").
        n_min/n_max: nombre de keywords visé.
        lang: langue cible (auto-détectée si None).
        model: modèle LLM (default qwen-flash, le moins cher).
        max_tokens: budget tokens.

    Returns:
        chaîne de keywords nettoyée (think tags retirés).
    """
    if lang is None:
        lang = detect_language(user_text)

    llm = ChatOpenAI(
        model=model,
        base_url=os.environ.get("LITELLM_URL", "http://litellm:4000/v1"),
        api_key=os.environ.get("LITELLM_API_KEY", ""),
        temperature=0,
        max_tokens=max_tokens,
    )
    sys_prompt = _KEYWORDS_SYSTEM_TEMPLATE.format(target=target, n_min=n_min, n_max=n_max, lang=lang)
    try:
        resp = await llm.ainvoke(
            [SystemMessage(content=sys_prompt), HumanMessage(content=user_text)]
        )
        return strip_think_tags(resp.content).strip().replace("\n", " ")[:160]
    except Exception:
        # Fallback brut : retourne les premiers tokens du user_text
        return " ".join(user_text.split()[:5])[:160]
