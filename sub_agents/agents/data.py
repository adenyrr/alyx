"""
Data Agent — calcul mathématique, données financières, requêtes DuckDB.
Modèle : openrouter/deepseek.
Outils : calculator, duckdb, yahoo-finance (MCPO).
"""

from __future__ import annotations

import json
import os
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.mcpo_client import call_tool
from tools.skills_loader import find_relevant as find_relevant_skills

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/deepseek"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are a data analyst and mathematician. Use the provided tool results to perform calculations,
analyze datasets, and run SQL queries on DuckDB.
Show your work clearly: formulas, intermediate steps, final results.
For DuckDB/SQL queries, show the query and its results.

Presentation rules (STRICT):
  - NEVER use ```python to display, format, or present data.
  - For ANY table, chart, comparison, list of values, or multi-value result:
    generate a self-contained ```html artifact with inline CSS. Always use a CDN library
    (Chart.js, Tabulator, etc.) when a chart or styled table is appropriate.
  - "Mettre en forme", "afficher", "présenter", "visualiser" → ```html artifact MANDATORY.
  - Only use plain text for a single scalar result (one number or one-line formula answer).

Sources & citations (MANDATORY):
  - Always cite the dataset or formula source.
  - If using DuckDB results, state the table and query used.
  - Format: > 📊 Source: [name or description]

Reply in English with structured output.
"""


async def run(state: "AlyxState", config: RunnableConfig | None = None, model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    emitter = (config.get("configurable") or {}).get("event_emitter") if config else None

    async def _emit(desc: str) -> None:
        if emitter:
            try:
                await emitter({"type": "status", "data": {"description": desc, "done": False}})
            except Exception:
                pass

    context_parts: list[str] = []

    # Skills méthodologiques (recettes SQL, tests stats, patterns DuckDB…)
    skill_hits = find_relevant_skills(user_text, agent="data")
    if skill_hits:
        skill_block = "\n\n".join(f"### Skill: {n}\n{c[:5000]}" for _, n, c in skill_hits)
        context_parts.append(
            "## Data analysis recipes (apply when relevant to the question)\n" + skill_block
        )

    # Calculatrice si expression mathématique détectée
    math_expr = _extract_math_expression(user_text)
    if math_expr:
        try:
            await _emit(f"🧮 Calcul : {math_expr[:120]}")
            result = await call_tool("calculator", "evaluate", {"expression": math_expr})
            context_parts.append(f"## Calculator result\nExpression: `{math_expr}`\nResult: {json.dumps(result, ensure_ascii=False)}")
        except Exception as exc:
            context_parts.append(f"## Calculator failed\n{exc}")

    # DuckDB si requête SQL détectée
    sql_query = _extract_sql_query(user_text)
    if sql_query:
        try:
            await _emit("🗃️ Requête DuckDB…")
            result = await call_tool("duckdb", "query", {"sql": sql_query})
            context_parts.append(f"## DuckDB result\nQuery: `{sql_query}`\nResult: {json.dumps(result, ensure_ascii=False)[:2000]}")
        except Exception as exc:
            context_parts.append(f"## DuckDB failed\n{exc}")

    # Yahoo Finance si ticker/action détecté.
    # mcp-yahoo-finance expose : get_current_stock_price / get_news /
    # get_recommendations / get_historical_stock_prices / get_dividends / etc.
    # (pas de `get_stock_info`). On compose un mini-bundle pour le LLM.
    ticker = _extract_ticker(user_text)
    if ticker:
        await _emit(f"📈 Données financières : {ticker}")
        finance_blocks: list[str] = []
        for tool, label, args in (
            ("get_current_stock_price", "current price", {"symbol": ticker}),
            ("get_news",                "recent news",   {"symbol": ticker}),
            ("get_recommendations",     "analyst recs",  {"symbol": ticker}),
        ):
            try:
                result = await call_tool("yahoo-finance", tool, args)
                finance_blocks.append(
                    f"### {label}\n```\n{json.dumps(result, ensure_ascii=False, indent=2)[:1500]}\n```"
                )
            except Exception as exc:
                finance_blocks.append(f"### {label}\n(unavailable: {exc})")
        context_parts.append(f"## Yahoo Finance ({ticker})\n" + "\n\n".join(finance_blocks))

    context = "\n\n".join(context_parts)
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )

    prompt = f"{context}\n\nUser question: {user_text}" if context else user_text
    await _emit("✍️ Synthèse des données…")
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}
    return {
        "agent_outputs": {"data": response.content},
        "agent_metrics": {"data": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
    }


def _extract_math_expression(text: str) -> str:
    """Extrait une expression mathématique simple ou complexe du texte."""
    # Expression entre backticks
    m = re.search(r"`([^`]+)`", text)
    if m:
        return m.group(1)
    # Expression avec opérateurs
    m = re.search(r"([\d\s\.\+\-\*\/\^\(\)%e]+(?:\*\*[\d\.]+)?)", text)
    if m and any(op in m.group(1) for op in ["+", "-", "*", "/", "^", "**", "%"]):
        return m.group(1).strip()
    return ""


# Faux positifs à exclure : mots courants en MAJUSCULES, codes pays/devises,
# acronymes techniques. Les vrais tickers passent par un cue explicite (cf. _extract_ticker).
_TICKER_BLACKLIST: frozenset[str] = frozenset({
    "I", "A", "AI", "ML", "API", "CEO", "CFO", "CTO", "CV", "DNS", "DOI",
    "EUR", "USD", "GBP", "CHF", "JPY", "CNY",
    "FR", "US", "UK", "EU", "UN", "OK", "TV", "PC", "HTML", "JSON", "CSV",
    "PDF", "URL", "HTTP", "SQL", "GPS", "RAM", "CPU", "GPU", "OS", "IT",
    "SaaS", "B2B", "B2C", "LBO", "MBA", "PME", "TPE", "CDD", "CDI", "RTT",
})


def _extract_ticker(text: str) -> str:
    """
    Détecte un ticker boursier (ex: AAPL, BTC-USD, ^GSPC) dans le texte.

    Exige un cue contextuel (`$AAPL`, `ticker:`, "action/cours/stock/price"…)
    pour éviter les faux positifs sur des acronymes courants ("EUR", "PDF", "AI"…).
    """
    # Format $TICKER ou ^INDEX — non ambigu
    m = re.search(r"(?:\$|\^)([A-Z]{1,5}(?:-[A-Z]{2,4})?)\b", text)
    if m:
        return m.group(1)

    # Crypto explicite (BTC-USD, ETH-EUR…) — toujours avec un tiret
    m = re.search(r"\b([A-Z]{2,5}-[A-Z]{3,4})\b", text)
    if m:
        return m.group(1)

    # Sinon : exiger un mot-clé financier dans la phrase pour interpréter un
    # token MAJUSCULE comme un ticker
    cue_re = re.compile(
        r"\b(ticker|stock|action|cours|cotation|bourse|nasdaq|nyse|share|quote|price)\b",
        re.IGNORECASE,
    )
    if not cue_re.search(text):
        return ""

    for candidate in re.findall(r"\b([A-Z]{2,5})\b", text):
        if candidate not in _TICKER_BLACKLIST:
            return candidate
    return ""


def _extract_sql_query(text: str) -> str:
    """Extrait une requête SQL du texte."""
    m = re.search(r"```sql\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r"\b(SELECT|INSERT|UPDATE|DELETE|WITH)\b.+", text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0)[:500]
    return ""


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
