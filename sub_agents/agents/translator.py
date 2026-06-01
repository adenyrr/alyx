"""
Translator Agent — traduction de texte vers une langue cible.

Modèle : openrouter/qwen3.5-flash (suffit largement pour la traduction).
Pas d'outils : LLM seul.

Stratégie :
  1. Détecter la langue cible demandée (par regex ou par LLM si ambigu).
  2. Détecter le contenu à traduire :
       - texte cité entre guillemets / triple-backticks
       - sinon : tout le message moins l'instruction de traduction
  3. Traduire en préservant le formatage Markdown.

Renvoie une confidence haute (0.95) — la traduction est un acte déterministe.
"""

from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.text_utils import detect_language, last_user_message

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/qwen3.5-flash"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are a professional translator. Translate the provided text into the requested
target language and NOTHING ELSE.

═══════════════════════════════════════════════════════
 FIDELITY CONTRACT — translate, do not rewrite
═══════════════════════════════════════════════════════
• Render the SAME meaning, register and tone as the source — no more, no less.
• Do NOT add content, explanations, transitions or examples that aren't in the
  source. Do NOT remove or summarize anything. Do NOT "improve", clarify, or
  correct the source — even if it contains errors or awkward phrasing: translate
  it faithfully, errors and all.
• Preserve structure EXACTLY: paragraph breaks, sentence count, lists, headings,
  emphasis, links and Markdown formatting map 1:1 from source to translation.
• Adapt idioms so they read naturally in the target language (a faithful
  translation, not a word-for-word transliteration) — but never paraphrase
  beyond what the language change requires.
• Keep code blocks (```...```) untranslated; only translate inline comments if
  explicitly requested.

Output ONLY the translation. No commentary, no notes, no "Here is the translation:".
"""

# Cible explicite extraite du prompt utilisateur.
_LANG_TARGETS: dict[str, str] = {
    "anglais": "English", "english": "English", "en": "English",
    "français": "French", "francais": "French", "french": "French", "fr": "French",
    "espagnol": "Spanish", "spanish": "Spanish", "español": "Spanish", "es": "Spanish",
    "allemand": "German", "german": "German", "deutsch": "German", "de": "German",
    "italien": "Italian", "italian": "Italian", "italiano": "Italian", "it": "Italian",
    "portugais": "Portuguese", "portuguese": "Portuguese", "português": "Portuguese", "pt": "Portuguese",
    "néerlandais": "Dutch", "dutch": "Dutch", "nl": "Dutch",
    "russe": "Russian", "russian": "Russian", "ru": "Russian",
    "chinois": "Chinese", "chinese": "Chinese", "zh": "Chinese",
    "japonais": "Japanese", "japanese": "Japanese", "ja": "Japanese",
    "arabe": "Arabic", "arabic": "Arabic", "ar": "Arabic",
}


def _extract_target_language(text: str) -> str:
    """Cherche dans le prompt 'traduis en X', 'translate to X', 'in english'…"""
    t = text.lower()
    patterns = [
        r"(?:traduis|traduire|traduction|translate|translation)[^.,;!?\n]*?\b(en|to|into|vers|en)\s+([\wàâçéèêëîïôûùüÿ]+)",
        r"\b(?:in|en)\s+([\wàâçéèêëîïôûùüÿ]+)\s*\??\s*$",
    ]
    for pat in patterns:
        m = re.search(pat, t)
        if m:
            candidate = (m.group(m.lastindex) or "").strip()
            if candidate in _LANG_TARGETS:
                return _LANG_TARGETS[candidate]
    return "English"  # défaut raisonnable


def _extract_source_text(text: str) -> str:
    """Récupère le texte à traduire : prioritairement triple-backticks, sinon
    guillemets, sinon tout le message moins l'instruction."""
    m = re.search(r"```(?:\w+)?\n?(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"[«\"](.+?)[»\"]", text, re.DOTALL)
    if m and len(m.group(1)) > 20:
        return m.group(1).strip()
    # Sinon : tout sauf l'éventuel imperatif de tête
    stripped = re.sub(
        r"^(?:traduis|traduire|translate)[^\n.,:;]*[\n.,:;]\s*",
        "", text, count=1, flags=re.IGNORECASE,
    )
    return stripped.strip()


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = last_user_message(messages)

    emitter = (config.get("configurable") or {}).get("event_emitter") if config else None

    async def _emit(desc: str) -> None:
        if emitter:
            try:
                await emitter({"type": "status", "data": {"description": desc, "done": False}})
            except Exception:
                pass

    target = _extract_target_language(user_text)
    source = _extract_source_text(user_text)
    source_lang = detect_language(source)

    if not source:
        return {
            "agent_outputs": {"translator": "⚠️ Aucun texte à traduire détecté."},
            "agent_confidence": {"translator": 0.0},
        }

    await _emit(f"🌍 Traduction {source_lang} → {target}…")
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )
    prompt = (
        f"Target language: {target}\n"
        f"Source language (detected): {source_lang}\n\n"
        f"Source text:\n{source}"
    )
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    output = (
        f"## Traduction ({source_lang} → {target})\n\n"
        + (response.content or "")
        + f"\n\n> 🌍 Source : texte original en {source_lang} (longueur : {len(source)} car.)"
    )
    _u = getattr(response, "usage_metadata", None) or {}
    return {
        "agent_outputs": {"translator": output},
        "agent_confidence": {"translator": 0.95},
        "agent_metrics": {"translator": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
    }
