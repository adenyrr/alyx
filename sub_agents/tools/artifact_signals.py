"""
Registre central des SIGNAUX d'artifact — source unique de vérité.

Deux usages, une seule table :
  • SIGNAL FORT  → le superviseur chaîne `dev` automatiquement (RÈGLE 11b du
    prompt superviseur). Géré côté prompt LLM, pas ici (ce module documente les
    familles pour cohérence ; le superviseur reste le décideur).
  • SIGNAL FAIBLE → quand AUCUN artifact n'a été produit ce tour, le pipeline
    propose un artifact via un « follow-up chip » cliquable (event OpenWebUI
    `chat:message:follow_ups`). C'est ce que `detect_weak_signals` calcule.

Le détecteur scanne la REQUÊTE utilisateur + la RÉPONSE de synthèse (les deux,
car un signal peut n'apparaître que dans la réponse — ex. des dates → frise).
Les regex sont volontairement CONSERVATRICES : un faux négatif (pas de chip) est
préférable à un chip parasite. Insensible à la casse et aux accents partiels.

Aucune dépendance externe — pure logique + regex, donc testable en isolation.
"""

from __future__ import annotations

import re


class _Signal:
    __slots__ = ("key", "weak_re", "chip", "prompt")

    def __init__(self, key: str, weak: str, chip: str, prompt: str) -> None:
        self.key = key
        self.weak_re = re.compile(weak, re.IGNORECASE)
        self.chip = chip       # libellé du bouton (court, avec emoji)
        self.prompt = prompt   # consigne renvoyée au chat si l'utilisateur clique


# Ordre = priorité : le 1er match gagne sa place ; on plafonne à 3 chips.
# `weak` matche la requête OU la réponse de synthèse. `prompt` est rédigé pour
# RE-DÉCLENCHER le bon routage (mots-clés que le superviseur reconnaît : carte,
# tableau comparatif, graphique, frise chronologique, calendrier…).
_SIGNALS: tuple[_Signal, ...] = (
    _Signal(
        "map",
        r"\b(lieu|visiter|visite|itin[ée]raire|incontournable|restaurant|resto|"
        r"mus[ée]e|monument|attraction|touris|quartier|adresse|"
        r"coordonn[ée]e|latitude|longitude|(?:que|où|à) (?:voir|aller|visiter|manger|faire))",
        "🗺️ Voir sur une carte",
        "Affiche les lieux de ta réponse précédente sur une carte interactive (Leaflet).",
    ),
    _Signal(
        "compare",
        r"\b(compar|versus|\bvs\b|diff[ée]rence|avantages? et inconv|"
        r"pour et contre|meilleur|top\s*\d|palmar[èe]s|classement)",
        "📊 Tableau comparatif",
        "Reprends ta réponse précédente et présente la comparaison sous forme de "
        "tableau comparatif interactif (artifact HTML).",
    ),
    _Signal(
        "chart",
        r"\b([ée]volution|tendance|r[ée]partition|statistiq|pourcentage|part de march|"
        r"croissance|progression|chiffres? cl[ée]|donn[ée]es chiffr)",
        "📈 Graphique",
        "Reprends les données chiffrées de ta réponse précédente et fais-en un "
        "graphique interactif (artifact HTML, Chart.js).",
    ),
    _Signal(
        "timeline",
        r"\b(chronologie|frise|timeline|histori(?:que|ographie)|"
        r"\b(?:1[5-9]\d{2}|20\d{2})\b.{0,40}\b(?:1[5-9]\d{2}|20\d{2})\b)",
        "📅 Frise chronologique",
        "Reprends les événements datés de ta réponse précédente et présente-les "
        "sur une frise chronologique interactive (artifact HTML, vis-timeline).",
    ),
    _Signal(
        "calendar",
        r"\b(planning|agenda|calendrier|emploi du temps|programme de la (?:semaine|journ[ée]e)|"
        r"horaires?)",
        "🗓️ Calendrier",
        "Reprends le planning de ta réponse précédente et affiche-le dans un "
        "calendrier interactif (artifact HTML, FullCalendar).",
    ),
    _Signal(
        "document",
        r"\b(rapport|synth[èe]se compl[èe]te|dossier|m[ée]mo|note de synth)",
        "📄 Exporter en document",
        "Reprends ta réponse précédente et produis-en un document structuré "
        "téléchargeable au format .docx.",
    ),
)


def detect_weak_signals(user_text: str, response_text: str, max_chips: int = 3) -> list[dict]:
    """Retourne les suggestions d'artifact pertinentes (signaux faibles).

    Chaque suggestion = {"key", "chip", "prompt"}. À n'utiliser QUE si aucun
    artifact n'a été produit ce tour (sinon la proposition fait doublon).

    Args:
        user_text: dernier message de l'utilisateur·rice.
        response_text: réponse de synthèse d'Alyx (texte final).
        max_chips: nombre maximum de chips (défaut 3 — au-delà ça encombre).

    Returns:
        Liste de dicts, max `max_chips`, dans l'ordre de priorité du registre.
    """
    haystack = f"{user_text}\n{response_text}"
    out: list[dict] = []
    for sig in _SIGNALS:
        if sig.weak_re.search(haystack):
            out.append({"key": sig.key, "chip": sig.chip, "prompt": sig.prompt})
            if len(out) >= max_chips:
                break
    return out
