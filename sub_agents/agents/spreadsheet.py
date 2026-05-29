"""
Spreadsheet Agent — production et lecture de fichiers XLSX (Excel).

Modèle : openrouter/deepseek.
Outils : openpyxl (Python local — pas de MCP, pas d'API externe).

Stratégie :
  1. LLM produit un schéma JSON décrivant les feuilles, colonnes, types, données.
  2. openpyxl construit le .xlsx à partir du schéma.
  3. Artifact document avec base64 + mime, consommé par le flow de pièces jointes
     existant (cf. _build_document_links / _emit_writer_attachments dans le pipeline).
"""

from __future__ import annotations

import asyncio
import base64
import io
import json
import os
import re
import uuid
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.text_utils import last_user_message

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/deepseek"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

_SYSTEM = """\
You are a spreadsheet designer. Given a user request, output ONLY a JSON object
describing the workbook to generate. Schema:

{
  "filename": "name-without-extension",
  "sheets": [
    {
      "name": "Sheet1",
      "headers": ["Col A", "Col B", "Col C"],
      "rows": [
        ["value", 42, "text"],
        [...]
      ],
      "column_widths": [15, 30, 12]  // optional, in characters
    },
    {...}  // additional sheets
  ]
}

Rules:
  - Sheet names ≤ 31 chars (Excel limit), no [ ] / \\ ? * : characters.
  - Cell values: strings, numbers, booleans. No formulas (use literal values).
  - Use the data from earlier agents (if present in context) as the source.
  - If the user gives no data, generate plausible fictitious examples and TAG them
    as "(données fictives)" in a comment row, or in the filename.
  - Multiple sheets if natural (e.g. summary + details).
  - Output ONLY valid JSON, no markdown wrapping, no commentary.
"""


def _safe_sheet_name(name: str, fallback: str = "Sheet1") -> str:
    cleaned = re.sub(r"[\[\]\\/?*:]", "", name or "").strip()
    return (cleaned or fallback)[:31]


def _build_xlsx(spec: dict) -> bytes:
    """Construit un workbook XLSX en mémoire à partir d'un spec JSON."""
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    wb.remove(wb.active)  # retire la feuille par défaut

    for sheet_spec in spec.get("sheets", []):
        ws = wb.create_sheet(_safe_sheet_name(sheet_spec.get("name", "Sheet1")))
        headers = sheet_spec.get("headers", [])
        if headers:
            ws.append(headers)
            # Bold header row
            from openpyxl.styles import Font
            for cell in ws[1]:
                cell.font = Font(bold=True)
        for row in sheet_spec.get("rows", []):
            ws.append(list(row))
        widths = sheet_spec.get("column_widths", [])
        for idx, width in enumerate(widths, 1):
            try:
                ws.column_dimensions[get_column_letter(idx)].width = float(width)
            except Exception:
                pass

    if not wb.sheetnames:
        wb.create_sheet("Sheet1")

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


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

    context_parts: list[str] = []
    prior_outputs = {
        k: v for k, v in (state.get("agent_outputs") or {}).items()
        if v and not str(v).startswith("⚠️")
    }
    if prior_outputs:
        prior_text = "\n\n".join(
            f"### {name} agent results\n{content[:3000]}"
            for name, content in prior_outputs.items()
        )
        context_parts.append("## Source data from previous agents\n" + prior_text)

    await _emit("📊 Composition du workbook…")
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.2,
    )
    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nUser request: {user_text}" if context else user_text
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}

    # Parse le spec JSON
    raw = (response.content or "").strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return {
            "agent_outputs": {"spreadsheet": "⚠️ Impossible de produire un schéma XLSX valide."},
            "agent_confidence": {"spreadsheet": 0.0},
        }
    try:
        spec = json.loads(match.group(0))
    except Exception as exc:
        return {
            "agent_outputs": {"spreadsheet": f"⚠️ Schéma JSON invalide : {exc}"},
            "agent_confidence": {"spreadsheet": 0.0},
        }

    fname_base = re.sub(r"[^\w-]", "_", str(spec.get("filename", "data")))[:40] or "data"
    filename = f"{fname_base}-{uuid.uuid4().hex[:8]}.xlsx"

    await _emit("💾 Construction openpyxl…")
    try:
        raw_bytes = await asyncio.to_thread(_build_xlsx, spec)
    except Exception as exc:
        return {
            "agent_outputs": {"spreadsheet": f"⚠️ Construction XLSX échouée : {exc}"},
            "agent_confidence": {"spreadsheet": 0.0},
        }

    n_sheets = len(spec.get("sheets", []))
    summary_md = (
        f"## Tableur généré\n\n"
        f"Fichier **{filename}** avec {n_sheets} feuille(s) : "
        + ", ".join(f"`{s.get('name', '?')}`" for s in spec.get("sheets", []))
        + ".\n\n"
        + f"📎 Document **{filename}** généré (XLSX, {len(raw_bytes) // 1024} KB) — lien de téléchargement ci-dessous."
    )

    return {
        "agent_outputs": {"spreadsheet": summary_md},
        "agent_confidence": {"spreadsheet": 0.85},
        "agent_metrics": {"spreadsheet": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
        "artifacts": [{
            "type": "document",
            "format": "xlsx",
            "filename": filename,
            "mime": _XLSX_MIME,
            "base64": base64.b64encode(raw_bytes).decode("ascii"),
            "size_label": f"{len(raw_bytes) // 1024} KB" if len(raw_bytes) >= 1024 else f"{len(raw_bytes)} B",
        }],
    }
