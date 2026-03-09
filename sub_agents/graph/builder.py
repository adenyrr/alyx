"""
Graph Builder — assemble le StateGraph LangGraph.

Architecture :
  supervisor → (agents sélectionnés en parallèle) → END

La persistance est assurée par PostgresSaver (DB langgraph).
Le thread_id correspond au chat_id OpenWebUI pour l'historique multi-tours.
"""

from __future__ import annotations

import inspect
from typing import Callable, Optional

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.memory import MemorySaver
from psycopg_pool import AsyncConnectionPool

from graph.state import AlyxState
from graph.supervisor import route
import agents.vision as vision_agent
import agents.scholar as scholar_agent
import agents.dev as dev_agent
import agents.web as web_agent
import agents.media as media_agent
import agents.data as data_agent
import agents.memory_agent as memory_mod
import agents.image_gen as image_gen_agent
import agents.rag_agent as rag_agent

_AGENT_MAP: dict[str, Callable] = {
    "vision":    vision_agent.run,
    "scholar":   scholar_agent.run,
    "dev":       dev_agent.run,
    "web":       web_agent.run,
    "media":     media_agent.run,
    "data":      data_agent.run,
    "memory":    memory_mod.run,
    "image_gen": image_gen_agent.run,
    "rag":       rag_agent.run,
}


def _make_node(fn: Callable, model: str | None) -> Callable:
    """Crée un nœud LangGraph avec annotation RunnableConfig explicite.

    `functools.partial` perd les annotations de type, ce qui empêche LangGraph
    de détecter automatiquement le paramètre `config: RunnableConfig`. Ce wrapper
    corrige cela en déclarant explicitement la signature attendue par LangGraph.
    Le paramètre `config` n'est transmis à la fonction sous-jacente que si elle
    le déclare dans sa propre signature.
    """
    _pass_config = "config" in inspect.signature(fn).parameters

    async def _node(state: AlyxState, config: Optional[RunnableConfig] = None) -> dict:
        if _pass_config:
            return await fn(state, config=config, model=model)
        return await fn(state, model=model)

    return _node


def _routing_condition(state: AlyxState) -> list[str]:
    """Retourne les nœuds agents à invoquer (fan-out parallèle)."""
    routing = state.get("routing", [])
    return routing if routing else [END]


def _merge_agent_output(state: AlyxState, agent_name: str, output: dict) -> AlyxState:
    """Fusionne la sortie d'un agent dans l'état partagé."""
    current_outputs = dict(state.get("agent_outputs", {}))
    current_outputs.update(output.get("agent_outputs", {}))

    current_artifacts = list(state.get("artifacts", []))
    current_artifacts.extend(output.get("artifacts", []))

    return {**state, "agent_outputs": current_outputs, "artifacts": current_artifacts}


async def build_graph(db_url: str, models: dict | None = None):
    """
    Construit et compile le graphe LangGraph avec persistance PostgreSQL.

    Args:
        db_url: connection string PostgreSQL pour LangGraph (DB langgraph).
        models: dict optionnel de modèles par nom de nœud (supervisor, vision, …).

    Returns:
        Graphe compilé prêt à l'usage.
    """
    _models = models or {}
    builder = StateGraph(AlyxState)

    # Nœud superviseur
    builder.add_node("supervisor", _make_node(route, _models.get("supervisor")))
    builder.set_entry_point("supervisor")

    # Nœuds agents
    for name, fn in _AGENT_MAP.items():
        builder.add_node(name, _make_node(fn, _models.get(name)))

    # Edge conditionnel depuis le superviseur → agents ou END
    builder.add_conditional_edges(
        "supervisor",
        _routing_condition,
        {**{name: name for name in _AGENT_MAP}, END: END},
    )

    # Tous les agents terminent → END
    for name in _AGENT_MAP:
        builder.add_edge(name, END)

    # Checkpointer PostgreSQL via pool de connexions persistant
    # Timeout court (10s) pour échouer vite si la DB est inaccessible.
    # Fallback MemorySaver si db_url est vide ou la DB inexistante.
    pool = None
    if db_url:
        try:
            pool = AsyncConnectionPool(
                conninfo=db_url,
                min_size=2,
                max_size=20,
                open=False,
                # autocommit requis par LangGraph : CREATE INDEX CONCURRENTLY et
                # les opérations de checkpoint ne peuvent pas tourner dans une transaction.
                kwargs={"autocommit": True, "prepare_threshold": 0},
            )
            await pool.open(wait=True, timeout=10.0)
            checkpointer = AsyncPostgresSaver(pool)
            await checkpointer.setup()
        except Exception as exc:
            if pool is not None:
                await pool.close()
                pool = None
            raise RuntimeError(
                f"Impossible d'ouvrir la base PostgreSQL '{db_url}' : {exc}\n"
                "Vérifie que la base 'langgraph' existe : "
                "docker exec openwebui-postgres psql -U openwebui -c "
                "\"CREATE DATABASE langgraph; GRANT ALL PRIVILEGES ON DATABASE langgraph TO openwebui;\""
            ) from exc
    else:
        checkpointer = MemorySaver()

    graph = builder.compile(checkpointer=checkpointer)
    return graph, pool
