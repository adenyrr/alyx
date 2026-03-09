"""
AlyxState — état partagé du graphe LangGraph.
Tous les nœuds lisent et écrivent sur ce TypedDict.

Réducteurs :
  messages    : last-value-wins  — OpenWebUI est la source de vérité de l'historique ;
                add_messages provoquerait une double-accumulation dans le checkpoint car on
                passe TOUT l'historique à chaque tour.
  agent_outputs: merge reducer   — les agents s'exécutent en parallèle (fan-out) et écrivent
                 chacun leur clé. Sans merge, le dernier écrase les précédents.
  artifacts   : concat reducer   — même raison que agent_outputs.
"""

from __future__ import annotations

from typing import Annotated, Any
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage


def _merge_dicts(left: dict, right: dict) -> dict:
    """Fusionne deux dicts — utilisé pour agent_outputs en fan-out parallèle."""
    return {**left, **right}


def _concat_lists(left: list, right: list) -> list:
    """Concatène deux listes — utilisé pour artifacts en fan-out parallèle."""
    return left + right


class AlyxState(TypedDict):
    # Historique complet de la conversation (last-value-wins : OpenWebUI détient l'historique)
    messages: list[BaseMessage]

    # Images base64 extraites du message courant par la pipeline
    images_b64: list[str]

    # Date courante injectée par la pipeline (ex: "samedi 7 mars 2026")
    current_date: str

    # Liste des agents sélectionnés par le superviseur pour ce tour
    routing: list[str]

    # Sorties brutes de chaque agent invoqué — merge reducer pour le fan-out parallèle
    agent_outputs: Annotated[dict[str, str], _merge_dicts]

    # Artifacts générés (blocs html/js/py, images url…) — concat reducer
    artifacts: Annotated[list[dict[str, Any]], _concat_lists]
