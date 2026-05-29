"""
Utilitaires de fiabilité des données.

Trois fonctions principales :
  - score_url_authority(url) : score [0,1] d'autorité d'un domaine source
  - format_confidence_block(agent_confidence) : bloc Markdown à injecter dans
    le contexte de synthèse pour qu'Alyx pondère ses claims
  - should_auto_factcheck(agent_outputs, agent_confidence, valves) : heuristique
    qui décide si on doit déclencher fact_checker automatiquement post-phase 1

Pas de dépendances externes — pure logique + regex.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse


# ─── URL Authority Scoring ────────────────────────────────────────────────────
# Score [0,1] d'autorité d'une source web. Une source à 0.95 (peer-reviewed) doit
# peser plus en synthèse qu'une source à 0.30 (forum random). Ces tiers sont
# heuristiques et délibérément conservateurs — un .gov de gouvernement autoritaire
# n'est pas plus fiable qu'un blog d'expert, mais cette nuance dépasse une heuristique.

_TIER_TLDS: dict[str, float] = {
    # Institutionnel / officiel (très fiable pour leur domaine)
    ".gov": 0.90, ".gov.uk": 0.90, ".gov.au": 0.90, ".gov.ca": 0.90,
    ".gouv.fr": 0.90, ".gc.ca": 0.90,
    ".europa.eu": 0.90, ".int": 0.90,
    ".edu": 0.85, ".ac.uk": 0.85, ".ac.jp": 0.85, ".edu.au": 0.85,
}

# Domaines explicitement listés. La clé est un suffixe matché par endswith().
_TIER_DOMAINS: dict[str, float] = {
    # Peer-reviewed / publications scientifiques de référence
    "nature.com": 0.95, "science.org": 0.95, "thelancet.com": 0.95,
    "nejm.org": 0.95, "cell.com": 0.95, "bmj.com": 0.95, "jamanetwork.com": 0.95,
    "pubmed.ncbi.nlm.nih.gov": 0.95, "ncbi.nlm.nih.gov": 0.92,
    "arxiv.org": 0.85, "biorxiv.org": 0.78, "medrxiv.org": 0.78,
    "semanticscholar.org": 0.85, "scholar.google.com": 0.80,
    "crossref.org": 0.92, "doi.org": 0.90,
    # Organisations internationales / santé
    "who.int": 0.95, "cdc.gov": 0.93, "nih.gov": 0.93, "fda.gov": 0.93,
    "ema.europa.eu": 0.93, "ansm.sante.fr": 0.90,
    "un.org": 0.88, "worldbank.org": 0.88, "imf.org": 0.88, "oecd.org": 0.88,
    # Médias de référence
    "reuters.com": 0.80, "apnews.com": 0.80, "bbc.com": 0.78, "bbc.co.uk": 0.78,
    "lemonde.fr": 0.75, "lefigaro.fr": 0.70, "liberation.fr": 0.70,
    "nytimes.com": 0.78, "washingtonpost.com": 0.75, "ft.com": 0.78,
    "economist.com": 0.78, "wsj.com": 0.78, "theguardian.com": 0.75,
    "afp.com": 0.85, "afp.fr": 0.85,
    # Encyclopédie
    "wikipedia.org": 0.65, "fr.wikipedia.org": 0.65, "en.wikipedia.org": 0.65,
    "britannica.com": 0.80,
    # Tech (à utiliser avec prudence — la qualité varie)
    "github.com": 0.70, "stackoverflow.com": 0.65, "mdn.mozilla.org": 0.85,
    "developer.mozilla.org": 0.85, "kubernetes.io": 0.85, "docker.com": 0.80,
    "python.org": 0.90, "rust-lang.org": 0.90, "golang.org": 0.90,
    # Données économiques / finance
    "bloomberg.com": 0.78, "finance.yahoo.com": 0.70, "reuters.com": 0.80,
    "investing.com": 0.55,
    # Faible fiabilité par défaut
    "medium.com": 0.40, "quora.com": 0.30, "reddit.com": 0.35,
    "facebook.com": 0.20, "twitter.com": 0.30, "x.com": 0.30,
    "tiktok.com": 0.15, "youtube.com": 0.50,
}


def score_url_authority(url: str) -> float:
    """Retourne un score [0,1] d'autorité du domaine. 0.5 par défaut (neutre)
    pour les domaines inconnus. Implémentation pure — pas de net call.
    """
    if not url or not isinstance(url, str):
        return 0.5
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return 0.5
    if not host:
        return 0.5
    # Match exact domain (suffix)
    for domain, score in _TIER_DOMAINS.items():
        if host == domain or host.endswith("." + domain):
            return score
    # Match TLD (couvre `host.endswith(".gov.uk")` ET le cas host nu == "gov.uk")
    for tld, score in _TIER_TLDS.items():
        if host.endswith(tld) or host == tld.lstrip("."):
            return score
    return 0.5  # neutre par défaut


def authority_emoji(score: float) -> str:
    """Mini-badge visuel pour un score d'autorité."""
    if score >= 0.85:
        return "🟢"  # très fiable
    if score >= 0.65:
        return "🟡"  # plutôt fiable
    if score >= 0.45:
        return "🟠"  # variable
    return "🔴"  # à prendre avec recul


# ─── Confidence formatting ────────────────────────────────────────────────────

def format_confidence_block(agent_confidence: dict[str, float]) -> str:
    """Bloc Markdown à injecter dans le prompt de synthèse pour que le LLM
    pondère ses claims par la confiance déclarée des agents.

    Retourne "" si pas de scores fournis.
    """
    if not agent_confidence:
        return ""
    lines = ["## Confiance par agent (à pondérer en synthèse)"]
    for agent, conf in sorted(agent_confidence.items(), key=lambda kv: -kv[1]):
        if not isinstance(conf, (int, float)):
            continue
        emoji = authority_emoji(float(conf))
        lines.append(f"- {emoji} **{agent}** : {float(conf):.2f}")
    lines.append(
        "\n*Règle* : agents en 🟢 fiabilité haute → repose-toi sur leurs claims ; "
        "agents en 🟠/🔴 → présente leurs données avec prudence (« selon X… »), "
        "préfère les sources mieux notées en cas de contradiction."
    )
    return "\n".join(lines)


def avg_confidence(agent_confidence: dict[str, float]) -> float | None:
    """Moyenne des confidences déclarées (ignore les valeurs non-numériques).
    None si aucune valeur exploitable.
    """
    vals = [float(v) for v in (agent_confidence or {}).values()
            if isinstance(v, (int, float))]
    return sum(vals) / len(vals) if vals else None


# ─── Auto-trigger du fact_checker ─────────────────────────────────────────────
# Agents qui produisent des claims factuels à risque (médical, juridique,
# scientifique, économique). Si SEUL ces agents tournent en phase 1, le pipeline
# peut décider de lancer fact_checker automatiquement même sans valve explicite.

_FACTUAL_AGENTS = {"web", "wikipedia", "doc", "data", "geo"}

# Mots-clés signalant des questions à enjeux (stakes-sensitive) — on resserre
# l'auto-trigger sur ces requêtes pour éviter de payer le fact_check sur tout.
_HIGH_STAKES_RE = re.compile(
    r"\b(m[ée]dic|sant[ée]|maladie|traitement|posologie|diagnostic|sympt[ôo]me|"
    r"l[ée]gal|loi|juridiq|tribunal|contrat|fiscal|imp[ôo]t|"
    r"financ|investiss|action|crypto|risque|"
    r"scientifiq|recherche|[ée]tude clinique|essai|m[ée]ta[\s-]?analyse|"
    r"statistique|nombre de|combien de|pourcentage de|taux de)\b",
    re.IGNORECASE,
)


def should_auto_factcheck(user_text: str, agent_outputs: dict, agent_confidence: dict,
                          critic_threshold: float = 0.6,
                          high_stakes_only: bool = True) -> tuple[bool, str]:
    """Décide si fact_checker doit être lancé automatiquement après phase 1.

    Critères (ANY déclenche) :
      a) confidence moyenne en dessous du seuil ET au moins un agent factuel
         a tourné → vérifier l'évidence
      b) si high_stakes_only=True : la requête contient des mots-clés à enjeux
         (santé/légal/financier/scientifique) ET un agent factuel a tourné →
         déclencher par prudence même si confidence haute

    Returns: (trigger: bool, reason: str)
    """
    if not agent_outputs:
        return (False, "")
    if "fact_checker" in agent_outputs:
        return (False, "déjà exécuté")
    factual_present = any(a in agent_outputs for a in _FACTUAL_AGENTS)
    if not factual_present:
        return (False, "aucun agent factuel en phase 1")
    avg_c = avg_confidence(agent_confidence)
    if avg_c is not None and avg_c < critic_threshold:
        return (True, f"confidence moyenne {avg_c:.2f} < seuil {critic_threshold}")
    if high_stakes_only and _HIGH_STAKES_RE.search(user_text or ""):
        return (True, "question à enjeux (santé/légal/finance/science) — vérification par prudence")
    return (False, "")


# ─── Enrichissement des citations ─────────────────────────────────────────────

def enrich_citation_with_authority(title: str, url: str) -> str:
    """Format de citation enrichie d'un badge d'autorité.
    Format : `🟢 [Titre](url)` où l'emoji reflète le tier.
    """
    score = score_url_authority(url)
    emoji = authority_emoji(score)
    return f"{emoji} [{title}]({url})"


# ─── Diversité des sources ────────────────────────────────────────────────────
# Mesure si une réponse s'appuie sur des sources INDÉPENDANTES (plusieurs
# domaines / plusieurs tiers d'autorité) plutôt que sur un seul. Permet
# d'éviter les hallucinations causées par la sur-représentation d'une source.


def _root_domain(host: str) -> str:
    """Réduit un hostname à son domaine racine (ex. fr.wikipedia.org → wikipedia.org).
    Heuristique simple : garde les 2 derniers labels sauf pour les TLDs composés
    courants (.co.uk, .gov.uk, .com.au, .gouv.fr…).
    """
    if not host:
        return ""
    parts = host.lower().split(".")
    if len(parts) < 2:
        return host.lower()
    compound = {"co.uk", "gov.uk", "ac.uk", "com.au", "edu.au", "gov.au",
                "co.jp", "ac.jp", "gouv.fr", "gc.ca", "gov.ca"}
    last_two = ".".join(parts[-2:])
    if last_two in compound and len(parts) >= 3:
        return ".".join(parts[-3:])
    return last_two


def source_diversity_score(urls: list[str]) -> float:
    """Score [0,1] de diversité des sources à partir d'une liste d'URLs.

    Heuristique pondérée :
      - Compte les DOMAINES RACINE distincts (pas les sous-domaines)
      - Bonus si différents tiers d'autorité représentés (peer-reviewed + presse,
        ou .gov + wikipedia, etc.)
      - 0.0 = un seul domaine ou aucune URL
      - 1.0 = ≥ 4 domaines distincts dont ≥ 2 tiers d'autorité différents
    """
    if not urls:
        return 0.0
    from urllib.parse import urlparse
    domains: set[str] = set()
    auth_buckets: set[str] = set()
    for u in urls:
        if not isinstance(u, str):
            continue
        try:
            host = (urlparse(u).hostname or "").lower()
        except Exception:
            continue
        if not host:
            continue
        domains.add(_root_domain(host))
        score = score_url_authority(u)
        # Bucketize en 3 tiers grossiers
        if score >= 0.85:
            auth_buckets.add("high")
        elif score >= 0.55:
            auth_buckets.add("mid")
        else:
            auth_buckets.add("low")
    n_domains = len(domains)
    if n_domains == 0:
        return 0.0
    if n_domains == 1:
        return 0.15
    base = min(0.75, 0.30 + 0.15 * (n_domains - 1))  # 2→0.45, 3→0.60, 4+→0.75
    if len(auth_buckets) >= 2:
        base += 0.15
    return min(1.0, base)


def diversity_emoji(score: float) -> str:
    """Mini-badge visuel pour un score de diversité."""
    if score >= 0.75:
        return "🟢"
    if score >= 0.55:
        return "🟡"
    if score >= 0.30:
        return "🟠"
    return "🔴"


def extract_urls_from_text(text: str) -> list[str]:
    """Extrait les URLs http(s) d'un texte (déduplique en conservant l'ordre)."""
    import re
    if not text:
        return []
    found = re.findall(r"https?://[^\s\)\]\"'<>]+", text)
    seen: set[str] = set()
    result: list[str] = []
    for u in found:
        clean = u.rstrip(".,;:!?)")
        if clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result


# ─── Auto-corroboration : choisir l'agent complémentaire ──────────────────────

# Compléments pour le single-source : quand un seul agent factuel a tourné,
# spawn celui-ci pour avoir une seconde source indépendante.
_COMPLEMENT_MAP: dict[str, str] = {
    "web":       "wikipedia",  # actualité → vérifier par l'encyclopédie
    "wikipedia": "web",        # encyclopédie → vérifier par sources récentes
    "doc":       "web",        # papier scientifique → contextualiser via web
}


def pick_complement_agent(factual_agents_run: set[str], already_run: set[str]) -> str | None:
    """Pour un set d'agents factuels exécutés, propose un agent complémentaire
    à spawner pour augmenter la diversité de sources. Returns None si
    impossible (déjà ≥ 2 agents factuels, ou complément déjà tourné).
    """
    if len(factual_agents_run) != 1:
        return None  # déjà multi-source ou aucune source factuelle
    only = next(iter(factual_agents_run))
    comp = _COMPLEMENT_MAP.get(only)
    if not comp or comp in already_run:
        return None
    return comp
