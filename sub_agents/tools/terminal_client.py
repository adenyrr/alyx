"""
Client open-terminal — service bash MCP intégré à OpenWebUI.
Exécute des commandes shell dans un environnement sandboxé persistant.
"""

from __future__ import annotations

import os

import httpx

_TERMINAL_URL = os.environ.get("OPEN_TERMINAL_URL", "http://open-terminal:8000")
_TERMINAL_API_KEY = os.environ.get("OPEN_TERMINAL_API_KEY", "")
_TIMEOUT = 120.0


async def execute(command: str) -> str:
    """
    Exécute une commande bash dans open-terminal.

    Args:
        command: commande shell à exécuter (ex. 'ls -la', 'python3 script.py')

    Returns:
        Sortie combinée stdout + stderr sous forme de str.
    """
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.post(
            f"{_TERMINAL_URL}/execute",
            headers={"Authorization": f"Bearer {_TERMINAL_API_KEY}"},
            json={"command": command},
        )
        resp.raise_for_status()
        data = resp.json()
        stdout = data.get("stdout", "")
        stderr = data.get("stderr", "")
        output = stdout
        if stderr:
            output += f"\n[stderr]\n{stderr}"
        return output.strip()
