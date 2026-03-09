"""
Data Agent — calcul mathématique, analyse de données, requêtes DuckDB.
Modèle : GPT-OSS 120B.
Outils : calculator, duckdb (MCPO).
"""

from __future__ import annotations

import json
import os
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
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


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    context_parts: list[str] = []

    # Calculatrice si expression mathématique détectée
    math_expr = _extract_math_expression(user_text)
    if math_expr:
        try:
            result = await call_tool("calculator", "evaluate", {"expression": math_expr})
            context_parts.append(f"## Calculator result\nExpression: `{math_expr}`\nResult: {json.dumps(result, ensure_ascii=False)}")
        except Exception as exc:
            context_parts.append(f"## Calculator failed\n{exc}")

    # DuckDB si requête SQL détectée
    sql_query = _extract_sql_query(user_text)
    if sql_query:
        try:
            result = await call_tool("duckdb", "query", {"sql": sql_query})
            context_parts.append(f"## DuckDB result\nQuery: `{sql_query}`\nResult: {json.dumps(result, ensure_ascii=False)[:2000]}")
        except Exception as exc:
            context_parts.append(f"## DuckDB failed\n{exc}")

    context = "\n\n".join(context_parts)
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )

    prompt = f"{context}\n\nUser question: {user_text}" if context else user_text
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])

    return {"agent_outputs": {"data": response.content}}


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
