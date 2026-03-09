"""
RAG Agent — recherche dans les documents uploadés par l'utilisateur (Qdrant).
Modèle : GPT-OSS 120B.
Outil : Qdrant HTTP direct (via rag_client).

Interroge la collection "openwebui" qui contient les documents traités par Tika + OpenWebUI RAG.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.rag_client import search

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_QDRANT_COLLECTION = "openwebui"

_SYSTEM = """\
You are a document retrieval specialist. Use the provided document excerpts to answer the user's question.
Always cite the source document name/ID when available in the metadata.
If the documents don't contain enough information, state this clearly.
Reply in English with structured, accurate output.
"""


async def run(state: "AlyxState", model: str | None = None) -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    rag_context = ""
    try:
        results = await search(query_text=user_text, collection=_QDRANT_COLLECTION, top_k=5)
        if results:
            chunks = []
            for hit in results:
                payload = hit.get("payload", {})
                text = payload.get("text", payload.get("content", ""))
                source = payload.get("metadata", {}).get("source", payload.get("source", "unknown"))
                score = hit.get("score", 0.0)
                if text:
                    chunks.append(f"[Source: {source} | score: {score:.3f}]\n{text[:800]}")
            rag_context = "\n\n---\n\n".join(chunks)
    except Exception as exc:
        return {"agent_outputs": {"rag": f"RAG search failed: {exc}"}}

    if not rag_context:
        return {"agent_outputs": {"rag": "No relevant documents found in the knowledge base."}}

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.15,
    )

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=f"## Document excerpts\n{rag_context}\n\nUser question: {user_text}"),
    ])

    return {"agent_outputs": {"rag": response.content}}


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
