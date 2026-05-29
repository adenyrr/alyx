"""
Fact-Checker Agent — vérification adversariale des claims produits par
les autres agents (verify/refute via recherche web indépendante).

Modèle : openrouter/deepseek (raisonnement critique).
Outils : duckduckgo + fetch-web (MCPO).

Stratégie :
  1. Extraire 3-5 claims factuels vérifiables depuis agent_outputs (phase 1).
  2. Pour chaque claim, recherche web ciblée (DuckDuckGo) → fetch top 2 URLs.
  3. LLM critique évalue chaque claim sur l'évidence trouvée :
       SUPPORTED / REFUTED / INCONCLUSIVE + courte justification.
  4. Émet un rapport structuré + confidence score global pour la phase 1.

Si appelé sans agents préalables, devient un mini-vérificateur de la question
elle-même (vérifie si la question contient des prémisses fausses).
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
from tools.text_utils import last_user_message

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/deepseek"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_EXTRACT_SYSTEM = """\
You extract factual, verifiable claims from text. Given the answers of one or more
research agents, list 3 to 5 SPECIFIC factual claims worth checking. Avoid:
  - Opinions, predictions, or value judgments
  - Vague claims ("X is popular")
  - Trivially true claims ("water is wet")

Each claim should be a single declarative sentence with concrete entities and
numbers/dates if applicable. Output ONLY a JSON array of strings.
Example: ["The Eiffel Tower is 330m tall.", "PostgreSQL 16 was released in 2023."]
"""

_VERIFY_SYSTEM = """\
You are a rigorous fact-checker. Given a CLAIM and EVIDENCE (web search snippets),
return ONLY a JSON object:

{
  "verdict": "SUPPORTED" | "REFUTED" | "INCONCLUSIVE",
  "confidence": 0.0 to 1.0,
  "reason": "one short sentence citing the evidence"
}

Be conservative: if the evidence is weak or ambiguous, return INCONCLUSIVE
rather than SUPPORTED. Default to skepticism.
"""


async def _search_evidence(claim: str, max_results: int = 3) -> str:
    """Recherche DuckDuckGo + fetch des premiers résultats pour récolter de
    l'évidence concernant un claim."""
    try:
        ddg = await call_tool("duckduckgo", "search", {"query": claim[:160], "max_results": max_results})
    except Exception as exc:
        return f"[duckduckgo unavailable: {exc}]"
    # Extraire les URLs
    urls: list[str] = []
    if isinstance(ddg, list):
        for item in ddg:
            if isinstance(item, dict):
                u = item.get("url") or item.get("href") or item.get("link")
                if u and u.startswith("http"):
                    urls.append(u)
    if not urls:
        return json.dumps(ddg, ensure_ascii=False)[:2000]
    snippets: list[str] = []
    for u in urls[:2]:
        try:
            r = await call_tool("fetch-web", "fetch", {"url": u, "max_length": 800})
            snippets.append(f"[{u}]\n{json.dumps(r, ensure_ascii=False)[:800]}")
        except Exception:
            continue
    return "\n\n".join(snippets) if snippets else json.dumps(ddg, ensure_ascii=False)[:2000]


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

    # Agréger les sorties des autres agents (phase 1) pour en tirer des claims
    prior_outputs = {
        k: v for k, v in (state.get("agent_outputs") or {}).items()
        if v and not str(v).startswith("⚠️") and k not in ("fact_checker", "memory")
    }
    source_text = "\n\n".join(f"### {name}\n{content[:2500]}" for name, content in prior_outputs.items())
    if not source_text:
        # Fallback : vérifier la question elle-même
        source_text = f"### user_question\n{user_text}"

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0,
    )

    await _emit("🔬 Extraction des claims à vérifier…")
    extract_resp = await llm.ainvoke([
        SystemMessage(content=_EXTRACT_SYSTEM),
        HumanMessage(content=source_text[:6000]),
    ])
    _u1 = getattr(extract_resp, "usage_metadata", None) or {}
    prompt_tokens = _u1.get("input_tokens", 0) or 0
    completion_tokens = _u1.get("output_tokens", 0) or 0

    claims: list[str] = []
    match = re.search(r"\[.*?\]", (extract_resp.content or ""), re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            claims = [str(c) for c in parsed if isinstance(c, str)][:5]
        except Exception:
            pass
    if not claims:
        return {
            "agent_outputs": {"fact_checker": "ℹ️ Aucun claim factuel vérifiable détecté dans les sorties de phase 1."},
            "agent_confidence": {"fact_checker": 0.5},
        }

    # Recherche d'évidence + vérification en parallèle
    await _emit(f"🔬 Vérification de {len(claims)} claim(s) en parallèle…")
    evidences = await asyncio.gather(*(_search_evidence(c) for c in claims), return_exceptions=True)

    async def _verify(claim: str, evidence: str) -> dict:
        try:
            resp = await llm.ainvoke([
                SystemMessage(content=_VERIFY_SYSTEM),
                HumanMessage(content=f"CLAIM: {claim}\n\nEVIDENCE:\n{evidence[:3000]}"),
            ])
            m = re.search(r"\{.*\}", (resp.content or ""), re.DOTALL)
            if m:
                obj = json.loads(m.group(0))
                return {"claim": claim, **obj}
        except Exception:
            pass
        return {"claim": claim, "verdict": "INCONCLUSIVE", "confidence": 0.3, "reason": "verification call failed"}

    verdicts = await asyncio.gather(
        *(_verify(c, e if isinstance(e, str) else "") for c, e in zip(claims, evidences))
    )
    # Compter tokens des verify calls (approx)
    for v in verdicts:
        _u_v = v.get("_usage") or {}
        prompt_tokens += _u_v.get("input_tokens", 0) or 0
        completion_tokens += _u_v.get("output_tokens", 0) or 0

    # Synthèse du rapport
    n_supported = sum(1 for v in verdicts if v.get("verdict") == "SUPPORTED")
    n_refuted = sum(1 for v in verdicts if v.get("verdict") == "REFUTED")
    n_inconclusive = sum(1 for v in verdicts if v.get("verdict") == "INCONCLUSIVE")
    overall_confidence = (
        sum(float(v.get("confidence", 0.5)) for v in verdicts) / max(len(verdicts), 1)
        if n_refuted == 0
        else 0.2 + 0.6 * (n_supported / max(len(verdicts), 1))
    )

    lines = [
        f"## 🔬 Rapport de fact-checking",
        f"",
        f"**Synthèse** : {n_supported} supported · {n_refuted} refuted · {n_inconclusive} inconclusive · "
        f"confidence globale : {overall_confidence:.2f}",
        f"",
    ]
    for v in verdicts:
        icon = {"SUPPORTED": "✅", "REFUTED": "❌", "INCONCLUSIVE": "❓"}.get(v.get("verdict", ""), "❓")
        lines.append(
            f"- {icon} **{v['claim']}** — *{v.get('verdict', '?')}* "
            f"(conf {float(v.get('confidence', 0.0)):.2f}) — {v.get('reason', '')}"
        )

    return {
        "agent_outputs": {"fact_checker": "\n".join(lines)},
        "agent_confidence": {"fact_checker": overall_confidence},
        "agent_metrics": {"fact_checker": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "model": model or _MODEL,
        }},
    }
