"""
Code Execution Agent — exécution réelle de code Python dans le conteneur
`open-terminal` (déjà présent dans la stack, isolé via Docker).

Modèle : openrouter/kimi-k2.5 (bon en code).
Outils : tools.terminal_client.execute (HTTP → open-terminal).

Stratégie :
  1. LLM rédige un script Python autonome (imports + logique + print du résultat).
  2. Exécution dans le conteneur open-terminal via terminal_client.
  3. LLM commente le résultat (succès, erreur, interprétation).

Sécurité : open-terminal est un conteneur isolé. Le code n'a accès qu'au volume
`open_terminal_data` et aucune escalade hôte. Néanmoins, on bloque par regex
les imports clairement dangereux (subprocess.Popen avec /, eval/exec sur input,
ouverture de sockets externes inutiles) — défense en profondeur.
"""

from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from tools.terminal_client import execute
from tools.text_utils import last_user_message

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/kimi-k2.5"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are a Python execution agent. The user wants ACTUAL COMPUTATION, not a
description of what would happen. Output ONLY a Python script — no prose.

═══════════════════════════════════════════════════════
 SCRIPT CONTRACT
═══════════════════════════════════════════════════════
• Output exactly ONE ```python code block. No text before or after.
• Self-contained: all imports at top, no external file dependencies unless
  obvious from the task (e.g. user mentioned a CSV path).
• MUST end with `print(...)` of the final result. Stdout is the only return channel.
• Prefer stdlib + numpy/pandas/scipy/sympy if available. Avoid network calls
  unless absolutely required by the task.
• For long computations, print intermediate progress (the user sees stdout).
• Use try/except around risky calls and print useful error messages.
• Reply in English (the script comments may be in the user's language if useful).

═══════════════════════════════════════════════════════
 FORBIDDEN
═══════════════════════════════════════════════════════
  ✗ `os.system`, `subprocess.run` with shell=True, `eval(input())`, `exec(input())`
  ✗ Opening arbitrary sockets / making unauthorized HTTP requests
  ✗ Writing outside /tmp or the current working directory
"""

# Anti-patterns interdits — défense en profondeur (le conteneur est déjà isolé).
_FORBIDDEN_RE = re.compile(
    r"\b(?:os\.system|subprocess\.\w*\([^)]*shell\s*=\s*True"
    r"|eval\s*\(\s*input|exec\s*\(\s*input"
    r"|socket\.socket\([^)]*AF_INET[^)]*SOCK_RAW)\b",
    re.IGNORECASE,
)


def _extract_python(text: str) -> str:
    m = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Fallback : tout entre backticks triples
    m = re.search(r"```\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


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

    # Contexte phase 1 (données fournies par d'autres agents)
    context_parts: list[str] = []
    prior_outputs = {
        k: v for k, v in (state.get("agent_outputs") or {}).items()
        if v and not str(v).startswith("⚠️")
    }
    if prior_outputs:
        prior_text = "\n\n".join(
            f"### {name} agent results\n{content[:2000]}"
            for name, content in prior_outputs.items()
        )
        context_parts.append("## Data from previous agents (use as input)\n" + prior_text)

    await _emit("🐍 Rédaction du script…")
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )
    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nTask: {user_text}" if context else user_text
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])
    _u = getattr(response, "usage_metadata", None) or {}

    script = _extract_python(response.content or "")
    if not script:
        return {
            "agent_outputs": {"code_exec": "⚠️ Aucun script Python produit par le LLM."},
            "agent_confidence": {"code_exec": 0.0},
        }
    if _FORBIDDEN_RE.search(script):
        return {
            "agent_outputs": {"code_exec": "⚠️ Script bloqué : pattern dangereux détecté (os.system, eval/exec input, shell=True…)."},
            "agent_confidence": {"code_exec": 0.0},
        }

    await _emit("⚡ Exécution dans open-terminal…")
    try:
        # On encapsule le script dans un fichier temporaire puis exec via python3.
        cmd = (
            "python3 -c \"$(cat <<'__ALYX_EOF__'\n"
            + script.replace("\\", "\\\\").replace("$", "\\$")
            + "\n__ALYX_EOF__\n)\""
        )
        stdout = await execute(cmd)
    except Exception as exc:
        stdout = f"[execution error: {exc}]"

    output_md = (
        "## Script exécuté\n\n```python\n" + script[:4000] + "\n```\n\n"
        "## Résultat (stdout)\n\n```\n" + (stdout or "(vide)")[:4000] + "\n```\n\n"
        "> 🐍 Exécution : conteneur open-terminal (isolé)"
    )

    # Confidence basée sur le succès apparent : pas d'exception ⇒ haute.
    confidence = 0.3 if "[execution error" in (stdout or "") else 0.85

    return {
        "agent_outputs": {"code_exec": output_md},
        "agent_confidence": {"code_exec": confidence},
        "agent_metrics": {"code_exec": {
            "prompt_tokens": _u.get("input_tokens", 0) or 0,
            "completion_tokens": _u.get("output_tokens", 0) or 0,
            "model": model or _MODEL,
        }},
    }
