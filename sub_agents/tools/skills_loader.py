"""
Loader partagé pour les fichiers `skills/*.md`.

Chaque skill est un fichier Markdown avec un frontmatter YAML minimal :

    ---
    name: chartjs
    description: <phrase courte qui aide le scoring>
    agents: [dev]              # optionnel — défaut [dev]
    ---

    # Contenu Markdown…

Plusieurs agents peuvent partager un skill en listant plusieurs valeurs :
`agents: [dev, doc]`. Si le champ est absent, le skill est attribué à `dev`
(rétro-compatibilité avec l'existant).

Le loader est instancié comme un singleton paresseux : tout le filesystem
est lu une seule fois par process pipelines, indexé par `agents`. Les
modifications sur disque sont prises en compte au prochain rebuild du graphe
(cf. _ensure_graph dans alyx_pipeline.py qui purge sys.modules).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

_SKILLS_DIR = Path("/app/pipelines/skills")

# Mots-clés très fréquents — exclus du scoring sémantique pour ne pas
# polluer les correspondances.
_STOPWORDS: frozenset[str] = frozenset({
    "a", "an", "the", "is", "in", "to", "how", "do", "can", "me", "i", "for", "of",
    "with", "this", "my", "any", "and", "or", "it", "that", "on", "what", "use",
    "get", "have", "be", "are", "was", "will", "by", "at", "as", "from", "make",
    "build", "show", "give", "let", "want", "need", "please", "help", "write", "create",
    "de", "du", "le", "la", "les", "un", "une", "des", "je", "tu", "il", "nous",
    "vous", "ils", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
    "que", "qui", "quoi", "quel", "quelle", "faire", "fait", "fais", "avec",
    "sans", "mais", "ou", "et", "si", "car", "est", "sur", "par", "pour", "dans",
    "ce", "cet", "ces", "moi", "toi", "lui", "suis", "veux", "peux", "dois",
    "crée", "crée-moi", "génère", "fais-moi", "affiche", "montre", "présente",
})

_FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_FIELD_RE = re.compile(r"^\s*([a-zA-Z_]+)\s*:\s*(.+?)\s*$")


class _Skill:
    __slots__ = ("name", "description", "agents", "content")

    def __init__(self, name: str, description: str, agents: tuple[str, ...], content: str) -> None:
        self.name = name
        self.description = description
        self.agents = agents
        self.content = content


_cache_by_agent: dict[str, list[_Skill]] | None = None


def _parse_list(raw: str) -> tuple[str, ...]:
    """Parse une valeur YAML qui peut être `[a, b]` ou `a` simple."""
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return tuple(x.strip().strip("\"'") for x in raw[1:-1].split(",") if x.strip())
    return (raw.strip("\"'"),)


def _parse_frontmatter(text: str) -> tuple[dict[str, str], dict[str, tuple[str, ...]]]:
    """Retourne (scalars, lists). Champs scalaires : name, description. Listes : agents."""
    scalars: dict[str, str] = {}
    lists: dict[str, tuple[str, ...]] = {}
    m = _FRONT_RE.match(text)
    if not m:
        return scalars, lists
    for line in m.group(1).splitlines():
        fm = _FIELD_RE.match(line)
        if not fm:
            continue
        key, value = fm.group(1), fm.group(2)
        if value.startswith("[") and value.endswith("]"):
            lists[key] = _parse_list(value)
        else:
            scalars[key] = value.strip("\"'")
    return scalars, lists


def _load() -> dict[str, list[_Skill]]:
    """Charge tous les skills disponibles, indexés par agent."""
    by_agent: dict[str, list[_Skill]] = {}
    if not _SKILLS_DIR.exists():
        return by_agent

    for skill_file in _SKILLS_DIR.glob("*.md"):
        try:
            text = skill_file.read_text(encoding="utf-8")
        except Exception:
            continue
        scalars, lists = _parse_frontmatter(text)
        name = scalars.get("name") or skill_file.stem
        description = scalars.get("description", "")
        agents = lists.get("agents") or ("dev",)
        skill = _Skill(name=name, description=description, agents=agents, content=text)
        for agent in agents:
            by_agent.setdefault(agent, []).append(skill)
    return by_agent


def _ensure_loaded() -> dict[str, list[_Skill]]:
    global _cache_by_agent
    if _cache_by_agent is None:
        _cache_by_agent = _load()
    return _cache_by_agent


def _query_tokens(query: str) -> set[str]:
    return {w for w in re.split(r"\W+", query.lower()) if len(w) > 3 and w not in _STOPWORDS}


def _normalize(s: str) -> str:
    """Retire les séparateurs courants (-_.) pour matcher `pre-mortem` / `premortem`
    ou `markdown-it` / `markdownit` de façon symétrique."""
    return re.sub(r"[-_. ]+", "", s.lower())


def find_relevant(query: str, agent: str, max_results: int = 2) -> list[tuple[int, str, str]]:
    """
    Retourne les skills les plus pertinents pour un agent donné.

    Scoring (poids dégressifs) :
      - nom du skill présent verbatim ou avec séparateurs ignorés dans la query → +10
      - chacun des sous-tokens du nom (split sur -/_/. > 3 lettres) présent → +5
      - mots utiles de la query présents dans la description → +1 par hit, plafonné à 5

    Args:
        query: texte de la requête utilisateur·rice.
        agent: nom de l'agent appelant (`dev`, `doc`, `reasoning`, `data`…).
        max_results: nombre maximum de skills à renvoyer.

    Returns:
        Liste de tuples (score, name, content), triée par score décroissant.
        Seuls les skills avec score > 0 sont renvoyés.
    """
    skills = _ensure_loaded().get(agent) or []
    if not skills:
        return []

    query_lower = query.lower()
    query_norm = _normalize(query)
    query_words = _query_tokens(query)
    scored: list[tuple[int, str, str]] = []

    for skill in skills:
        score = 0
        name_lower = skill.name.lower()
        name_norm = _normalize(name_lower)
        # Match verbatim OU avec séparateurs ignorés des deux côtés
        if name_lower in query_lower or (name_norm and name_norm in query_norm):
            score += 10
        else:
            # Sous-tokens du nom : le seuil `>1` permet à `cv`, `ux`, `ia`, `ml`…
            # de matcher. On exige un match par limite de mot pour éviter qu'un
            # token de 2 lettres ne matche au hasard à l'intérieur d'un autre mot.
            for part in re.split(r"[-_.]", name_lower):
                if len(part) <= 1:
                    continue
                if re.search(rf"\b{re.escape(part)}\b", query_lower):
                    score += 5
        desc_lower = skill.description.lower()
        if desc_lower and query_words:
            score += min(sum(1 for w in query_words if w in desc_lower), 5)
        if score > 0:
            scored.append((score, skill.name, skill.content))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:max_results]


def list_names(agent: str | None = None) -> list[str]:
    """Liste les noms de skills (utile pour les listings de debug / supervisor)."""
    cache = _ensure_loaded()
    if agent:
        return [s.name for s in cache.get(agent, [])]
    seen: set[str] = set()
    out: list[str] = []
    for skills in cache.values():
        for s in skills:
            if s.name not in seen:
                seen.add(s.name)
                out.append(s.name)
    return out


def invalidate() -> None:
    """Force un rechargement au prochain appel (utile en dev)."""
    global _cache_by_agent
    _cache_by_agent = None


def iter_agents() -> Iterable[str]:
    return _ensure_loaded().keys()
