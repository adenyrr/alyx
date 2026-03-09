"""
Memory Agent — persistance et condensation du contexte conversationnel.
Modèle : GPT-OSS 120B.
Outil : MCPO memory (knowledge graph JSON persistant).

Mode normal : consulte la mémoire pour enrichir la réponse d'Alyx.
Mode background (run_bg) : condense la conversation courante en bullet facts
                           et les stocke, sans bloquer le streaming.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_LOGGER = logging.getLogger(__name__)

_SYSTEM_RECALL = """\
You are a memory assistant. Search the knowledge graph for information relevant to the user's question.
Return a concise summary of relevant memories (max 200 words). If nothing is relevant, return empty string.
Reply in English.
"""

_SYSTEM_CONDENSE = """\
You are a knowledge distiller. Given a conversation excerpt, extract 3-7 atomic facts worth remembering.
Format: one fact per line, starting with "•".
Facts should be concise, specific, and useful for future conversations.
Examples:
  • User prefers dark-themed HTML artifacts
  • User is researching cardiovascular MRI studies (2024)
  • Project stack: PostgreSQL + LangGraph + OpenWebUI
Reply in English only.
"""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    """Consulte la mémoire et retourne les informations pertinentes."""
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    recall_result = ""
    try:
        memories = await call_tool("memory", "search_nodes", {"query": user_text})
        recall_result = json.dumps(memories, ensure_ascii=False)[:2000]
    except Exception:
        pass

    if not recall_result or recall_result in ("{}", "[]", "null"):
        return {"agent_outputs": {"memory": ""}}

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM_RECALL),
        HumanMessage(content=f"Knowledge graph results:\n{recall_result}\n\nUser question: {user_text}"),
    ])

    return {"agent_outputs": {"memory": response.content}}


async def run_bg(state: "AlyxState", model: str | None = None) -> None:
    """
    Condense la conversation courante en faits et les stocke dans le knowledge graph.
    Conçu pour être exécuté en fire-and-forget via asyncio.run_coroutine_threadsafe().
    """
    messages = state.get("messages", [])
    if len(messages) < 2:
        return

    # Prendre les 6 derniers messages (3 tours) pour la condensation
    recent = messages[-6:]
    conversation = "\n".join(
        f"{'User' if m.type == 'human' else 'Alyx'}: {m.content if isinstance(m.content, str) else '[media]'}"
        for m in recent
    )

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.1,
    )

    try:
        response = await llm.ainvoke([
            SystemMessage(content=_SYSTEM_CONDENSE),
            HumanMessage(content=f"Conversation to distill:\n{conversation}"),
        ])
        facts_text = response.content.strip()
        if not facts_text:
            return

        # S'assurer que l'entité racine existe (idempotent — ignoré si déjà créée)
        try:
            await call_tool("memory", "create_entities", {
                "entities": [{"name": "Alyx-Context", "entityType": "ConversationContext", "observations": []}]
            })
        except Exception:
            pass  # Entité déjà existante — pas un problème

        # Stocker tous les faits en un seul appel
        facts = [f.strip("• ").strip() for f in facts_text.split("\n") if f.strip()]
        if facts:
            await call_tool("memory", "add_observations", {
                "observations": [{"entityName": "Alyx-Context", "contents": facts}]
            })
    except Exception as exc:
        _LOGGER.warning("Memory background condensation failed: %s", exc)


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
