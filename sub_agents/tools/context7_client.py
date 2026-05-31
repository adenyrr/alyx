"""
Client Context7 — passe par MCPO.

Context7 fournit les docs officielles de bibliothèques en temps réel. Le serveur
MCP `@upstash/context7-mcp` est lancé par MCPO en stdio (cf. mcpo_config.json →
context7, `npx … --api-key ${CONTEXT7_API_KEY}`). On l'atteint donc via MCPO sur
`http://mcpo:8000/context7/*`, comme tous les autres outils.

Historique : ce client faisait auparavant un POST HTTP JSON-RPC DIRECT vers
https://mcp.context7.com/mcp. Ça renvoyait systématiquement 400 Bad Request car
le transport streamable-HTTP MCP impose un handshake `initialize` (→ Mcp-Session-Id)
AVANT tout `tools/call` — handshake que ce client ne faisait pas. MCPO, lui, gère
le protocole MCP complet. On délègue donc tout à MCPO (cf. mémoire
mcpo-session-and-headers-limits).

Deux outils MCP exposés par context7 :
  resolve-library-id(libraryName)                         → texte listant les
                                                            bibliothèques candidates
  get-library-docs(context7CompatibleLibraryID, topic, tokens) → doc Markdown
"""

from __future__ import annotations

import re
from typing import Any

from tools.mcpo_client import call_tool

# ID Context7 de la forme `/org/projet` ou `/org/projet/version` dans le texte
# renvoyé par resolve-library-id (qui liste plusieurs candidates).
_LIB_ID_RE = re.compile(r"/[A-Za-z0-9._-]+/[A-Za-z0-9._/-]+")


def _flatten(payload: Any) -> str:
    """Aplati la réponse MCPO (str, liste, ou dict format MCP) en texte brut."""
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, list):
        return "\n".join(_flatten(item) for item in payload if item)
    if isinstance(payload, dict):
        content = payload.get("content")
        if isinstance(content, list):
            parts = [
                c.get("text", "") for c in content
                if isinstance(c, dict) and isinstance(c.get("text"), str)
            ]
            if any(parts):
                return "\n".join(p for p in parts if p)
        for key in ("text", "result", "data"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
    return str(payload)


async def resolve_library_id(library_name: str) -> str:
    """
    Résout un nom de bibliothèque en identifiant Context7 (`/org/projet`).

    resolve-library-id renvoie un TEXTE listant plusieurs candidates avec leur
    ID ; on extrait le premier ID `/org/projet` rencontré. Si aucun ID n'est
    trouvé (ou erreur), retourne "" pour que l'appelant abandonne proprement.

    Args:
        library_name: ex. 'leaflet', 'react', 'pandas'

    Returns:
        library_id utilisable par get_library_docs, ou "" si introuvable.
    """
    try:
        result = await call_tool("context7", "resolve-library-id", {"libraryName": library_name})
    except Exception:
        return ""
    text = _flatten(result)
    if not text or "error" in text.lower()[:200]:
        return ""
    match = _LIB_ID_RE.search(text)
    return match.group(0) if match else ""


async def get_library_docs(library_id: str, topic: str = "", tokens: int = 5000) -> str:
    """
    Récupère la documentation d'une bibliothèque sur un sujet précis.

    Args:
        library_id: identifiant `/org/projet` résolu par resolve_library_id
        topic:      sujet/feature spécifique (ex. 'markers', 'authentication')
        tokens:     nombre de tokens max à retourner (défaut 5000)

    Returns:
        Documentation Markdown, ou "" en cas d'échec.
    """
    if not library_id:
        return ""
    args: dict[str, Any] = {"context7CompatibleLibraryID": library_id, "tokens": tokens}
    if topic:
        args["topic"] = topic
    try:
        result = await call_tool("context7", "get-library-docs", args)
    except Exception:
        return ""
    return _flatten(result)
