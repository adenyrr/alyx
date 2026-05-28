"""
title: Alyx Actions
author: adenyrr
version: 0.1.0
description: >
  Bouton d'action ajouté à la barre d'outils des messages Alyx. Au clic, propose
  une opération de suivi (approfondir, exporter en document, régénérer en artifact
  ou en présentation) puis resoumet automatiquement une consigne à Alyx, qui
  réutilisera le message courant comme contexte de conversation.

  ⚠️ Ceci est une FONCTION NATIVE Open WebUI (type Action), à installer côté
  Open WebUI (Admin → Functions → +), distincte du pipeline Alyx hébergé dans le
  conteneur `pipelines`. Les types d'events interactifs (`input`, `confirmation`,
  `execute`) ne fonctionnent qu'en mode natif via WebSocket bidirectionnel — d'où
  ce fichier séparé.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# Opérations proposées au clic. Chaque entrée : (libellé affiché, gabarit de
# consigne resoumise à Alyx). Le `{n}` n'est pas utilisé — la consigne s'appuie
# sur le contexte de conversation déjà présent côté Alyx (le message précédent).
_OPERATIONS: dict[str, str] = {
    "approfondir": "Approfondis et détaille davantage ta réponse précédente, avec exemples et nuances.",
    "exporter":    "Reprends ta réponse précédente et produis-en un document téléchargeable au format .docx.",
    "artifact":    "Reprends ta réponse précédente et présente-la sous forme d'artifact HTML interactif.",
    "presentation": "Reprends ta réponse précédente et transforme-la en présentation (slides reveal.js).",
    "resumer":     "Résume ta réponse précédente en 5 points clés concis.",
}


class Action:
    class Valves(BaseModel):
        show_export: bool = Field(default=True, description="Proposer l'export en document (.docx)")
        show_artifact: bool = Field(default=True, description="Proposer la régénération en artifact HTML")
        show_presentation: bool = Field(default=True, description="Proposer la régénération en présentation reveal.js")

    def __init__(self):
        self.valves = self.Valves()

    async def action(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> Optional[dict]:
        if not __event_call__ or not __event_emitter__:
            return None

        # Liste des opérations disponibles selon les valves.
        choices = ["approfondir", "resumer"]
        if self.valves.show_export:
            choices.append("exporter")
        if self.valves.show_artifact:
            choices.append("artifact")
        if self.valves.show_presentation:
            choices.append("presentation")

        # Dialogue de saisie : l'utilisateur·rice choisit une opération (mot-clé)
        # ou tape une consigne libre.
        prompt_label = (
            "Que veut-on faire de cette réponse ?\n"
            f"Mots-clés : {', '.join(choices)}\n"
            "(ou tape une consigne libre)"
        )
        response = await __event_call__({
            "type": "input",
            "data": {
                "title": "✨ Alyx — action de suivi",
                "message": prompt_label,
                "placeholder": "approfondir",
            },
        })

        # __event_call__ peut renvoyer une chaîne ou un dict {"value": ...}.
        if isinstance(response, dict):
            answer = str(response.get("value", "")).strip()
        else:
            answer = str(response or "").strip()
        if not answer:
            return None

        # Mot-clé reconnu → gabarit ; sinon consigne libre transmise telle quelle.
        directive = _OPERATIONS.get(answer.lower(), answer)

        await __event_emitter__({
            "type": "status",
            "data": {"description": "Resoumission à Alyx…", "done": True},
        })

        # Resoumet la consigne comme nouveau prompt utilisateur. On utilise le pont
        # documenté par Open WebUI (les embeds/iframes postent `input:prompt:submit`
        # au parent) via l'event `execute` qui exécute du JS dans la page.
        safe = directive.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
        await __event_emitter__({
            "type": "execute",
            "data": {
                "code": (
                    "window.parent.postMessage("
                    f"{{ type: 'input:prompt:submit', text: `{safe}` }}, '*');"
                ),
            },
        })
        return None
