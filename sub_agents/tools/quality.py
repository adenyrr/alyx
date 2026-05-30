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
    ".gouv.fr": 0.92, ".gc.ca": 0.90, ".belgium.be": 0.88, ".admin.ch": 0.90,
    ".europa.eu": 0.92, ".int": 0.90, ".un.org": 0.90,
    ".edu": 0.85, ".ac.uk": 0.85, ".ac.jp": 0.85, ".edu.au": 0.85,
    ".ac.be": 0.85, ".univ-paris.fr": 0.85,
    # Domaines associatifs scientifiques / pro
    ".org.uk": 0.65,
}

# Domaines explicitement listés. La clé est un suffixe matché par endswith().
_TIER_DOMAINS: dict[str, float] = {
    # ─── Peer-reviewed / publications scientifiques ───
    "nature.com": 0.95, "science.org": 0.95, "thelancet.com": 0.95,
    "nejm.org": 0.95, "cell.com": 0.95, "bmj.com": 0.95, "jamanetwork.com": 0.95,
    "pnas.org": 0.92, "plos.org": 0.90, "elifesciences.org": 0.90,
    "frontiersin.org": 0.85, "mdpi.com": 0.65,  # éditeur variable
    "springer.com": 0.85, "sciencedirect.com": 0.85, "wiley.com": 0.85,
    "tandfonline.com": 0.82, "sage.com": 0.80, "sagepub.com": 0.80,
    "ieee.org": 0.90, "acm.org": 0.90,
    "pubmed.ncbi.nlm.nih.gov": 0.95, "ncbi.nlm.nih.gov": 0.92,
    "cochrane.org": 0.95, "cochranelibrary.com": 0.95,
    "arxiv.org": 0.85, "biorxiv.org": 0.78, "medrxiv.org": 0.78,
    "semanticscholar.org": 0.85, "scholar.google.com": 0.80,
    "crossref.org": 0.92, "doi.org": 0.90, "europepmc.org": 0.92,
    "researchgate.net": 0.70, "ssrn.com": 0.75,

    # ─── Médical & santé — international ───
    "who.int": 0.95, "cdc.gov": 0.95, "nih.gov": 0.95, "fda.gov": 0.93,
    "ema.europa.eu": 0.95, "ecdc.europa.eu": 0.95,
    "fda.europa.eu": 0.92, "eudravigilance.org": 0.90,
    "mayoclinic.org": 0.88, "clevelandclinic.org": 0.85,
    "hopkinsmedicine.org": 0.88, "uptodate.com": 0.92,
    "medscape.com": 0.82,  # référence pro — était à 0.50 par défaut, FIX
    "merckmanuals.com": 0.85, "msdmanuals.com": 0.85,
    "drugs.com": 0.78, "rxlist.com": 0.75,
    "kdigo.org": 0.90, "esmo.org": 0.90, "escardio.org": 0.90, "easl.eu": 0.90,
    "esmo.org": 0.90, "uspreventiveservicestaskforce.org": 0.92,

    # ─── Médical & santé — France/Belgique/Suisse francophone ───
    "ansm.sante.fr": 0.93, "has-sante.fr": 0.95, "santepubliquefrance.fr": 0.93,
    "sante.gouv.fr": 0.93, "solidarites-sante.gouv.fr": 0.92,
    "ameli.fr": 0.90, "amelipro.fr": 0.90,
    "vidal.fr": 0.90, "vidal.com": 0.90,
    "inserm.fr": 0.93, "inrs.fr": 0.88, "inra.fr": 0.88, "inrae.fr": 0.88,
    "anses.fr": 0.93, "pasteur.fr": 0.93, "institutpasteur.fr": 0.93,
    "mesvaccins.net": 0.85,  # référence vaccins FR — FIX
    "cbip.be": 0.92,  # Centre Belge d'Information Pharmacothérapeutique — FIX
    "afmps.be": 0.90,  # Agence fédérale des médicaments BE
    "swissmedic.ch": 0.92, "bag.admin.ch": 0.92,  # Suisse santé
    "infovac.fr": 0.85, "infovac.ch": 0.85,
    "snfmi.org": 0.85, "sf2h.net": 0.85,  # sociétés savantes FR
    "spilf.fr": 0.85, "splf.fr": 0.85, "sfmu.org": 0.85,
    "revmed.ch": 0.85,  # Revue Médicale Suisse
    "quechoisir.org": 0.75,  # consumer org FR — FIX
    "60millions-mag.com": 0.70,
    "ufc-quechoisir.org": 0.75,

    # ─── Cochrane / evidence-based ───
    "cochrane.fr": 0.95, "cochrane.org": 0.95,
    "evidencebasedhealth.org": 0.85,

    # ─── Légal & juridique ───
    "legifrance.gouv.fr": 0.95, "service-public.fr": 0.92,
    "eur-lex.europa.eu": 0.95, "echr.coe.int": 0.92,
    "courdecassation.fr": 0.95, "conseil-etat.fr": 0.95, "conseil-constitutionnel.fr": 0.95,
    "supremecourt.gov": 0.95, "supremecourt.uk": 0.95,
    "justice.belgium.be": 0.92, "moniteur.be": 0.92,
    "dalloz.fr": 0.85, "lexisnexis.com": 0.85,

    # ─── Organisations internationales / économique ───
    "un.org": 0.90, "worldbank.org": 0.90, "imf.org": 0.90, "oecd.org": 0.90,
    "ilo.org": 0.88, "wto.org": 0.88, "unesco.org": 0.88,
    "council.europa.eu": 0.92, "consilium.europa.eu": 0.92,
    "ecb.europa.eu": 0.92, "banque-france.fr": 0.90, "bis.org": 0.90,

    # ─── Médias internationaux référence ───
    "reuters.com": 0.82, "apnews.com": 0.82,
    "bbc.com": 0.80, "bbc.co.uk": 0.80,
    "ft.com": 0.80, "economist.com": 0.80, "wsj.com": 0.78,
    "nytimes.com": 0.78, "washingtonpost.com": 0.75, "theguardian.com": 0.75,
    "npr.org": 0.82, "pbs.org": 0.82,
    "afp.com": 0.85, "afp.fr": 0.85,
    "deutsche-welle.com": 0.78, "dw.com": 0.78,
    "elpais.com": 0.75, "lavanguardia.com": 0.72,
    "sueddeutsche.de": 0.75, "zeit.de": 0.78, "spiegel.de": 0.75, "faz.net": 0.75,

    # ─── Médias FR ───
    "lemonde.fr": 0.78, "lefigaro.fr": 0.72, "liberation.fr": 0.72,
    "lesechos.fr": 0.78, "latribune.fr": 0.72, "lopinion.fr": 0.70,
    "francetvinfo.fr": 0.75, "francetv.fr": 0.75, "franceinter.fr": 0.78,
    "radiofrance.fr": 0.78, "rfi.fr": 0.78, "france24.com": 0.75,
    "lalibre.be": 0.70, "lesoir.be": 0.70, "rtbf.be": 0.78,
    "letemps.ch": 0.78, "rts.ch": 0.78,
    "mediapart.fr": 0.78, "alternatives-economiques.fr": 0.75,
    "challenges.fr": 0.65, "capital.fr": 0.62,

    # ─── Fact-checking ───
    "factcheck.org": 0.88, "snopes.com": 0.80, "politifact.com": 0.85,
    "afp.com/factuel": 0.88, "factuel.afp.com": 0.88,
    "lemonde.fr/les-decodeurs": 0.85, "liberation.fr/checknews": 0.82,

    # ─── Encyclopédie ───
    "wikipedia.org": 0.65, "fr.wikipedia.org": 0.65, "en.wikipedia.org": 0.65,
    "britannica.com": 0.80, "universalis.fr": 0.85, "larousse.fr": 0.78,

    # ─── Tech — docs officielles ───
    "github.com": 0.70,  # le projet réel, pas un random repo
    "stackoverflow.com": 0.65,
    "mdn.mozilla.org": 0.92, "developer.mozilla.org": 0.92,
    "developer.apple.com": 0.92, "docs.microsoft.com": 0.90, "learn.microsoft.com": 0.92,
    "developer.android.com": 0.90, "developer.google.com": 0.85,
    "kubernetes.io": 0.92, "docker.com": 0.85, "docs.docker.com": 0.92,
    "python.org": 0.95, "docs.python.org": 0.95,
    "rust-lang.org": 0.92, "doc.rust-lang.org": 0.95,
    "golang.org": 0.92, "pkg.go.dev": 0.90, "go.dev": 0.92,
    "nodejs.org": 0.90, "npmjs.com": 0.75, "deno.com": 0.85,
    "postgresql.org": 0.92, "sqlite.org": 0.92, "redis.io": 0.90, "mongodb.com": 0.85,
    "nginx.com": 0.85, "nginx.org": 0.88, "apache.org": 0.85, "httpd.apache.org": 0.88,
    "linuxfoundation.org": 0.88, "kernel.org": 0.95, "gnu.org": 0.85,
    "ietf.org": 0.92, "rfc-editor.org": 0.95, "w3.org": 0.92, "tools.ietf.org": 0.92,
    "iana.org": 0.92, "iso.org": 0.92,
    "owasp.org": 0.92, "cve.mitre.org": 0.95, "nvd.nist.gov": 0.95,
    "nist.gov": 0.92, "cisa.gov": 0.92,
    "anssi.gouv.fr": 0.92,
    "react.dev": 0.90, "reactjs.org": 0.88,
    "vuejs.org": 0.90, "angular.io": 0.88, "svelte.dev": 0.88,
    "tailwindcss.com": 0.88, "nextjs.org": 0.88,
    "pytorch.org": 0.92, "tensorflow.org": 0.90, "huggingface.co": 0.78,
    "openai.com": 0.78, "anthropic.com": 0.78,
    "arxiv-sanity.com": 0.72, "paperswithcode.com": 0.80,

    # ─── Données économiques / finance ───
    "bloomberg.com": 0.80, "marketwatch.com": 0.72, "morningstar.com": 0.78,
    "sec.gov": 0.95, "amf-france.org": 0.92,  # régulateurs
    "finance.yahoo.com": 0.70, "investing.com": 0.55,
    "tradingview.com": 0.60, "stockanalysis.com": 0.55,

    # ─── Énergie & climat ───
    "ipcc.ch": 0.95, "iea.org": 0.92, "irena.org": 0.90,
    "ademe.fr": 0.92, "rte-france.com": 0.92, "edf.fr": 0.78,
    "energy.gov": 0.92, "epa.gov": 0.92, "eea.europa.eu": 0.92,
    "carbonbrief.org": 0.85, "climate.gov": 0.92,

    # ─── Géographie & cartographie ───
    "openstreetmap.org": 0.85, "nominatim.openstreetmap.org": 0.85,
    "open-meteo.com": 0.85, "meteofrance.com": 0.88, "noaa.gov": 0.92,

    # ─── Faible fiabilité — explicitement scoré bas ───
    "medium.com": 0.35, "substack.com": 0.40,
    "quora.com": 0.25, "reddit.com": 0.30,
    "facebook.com": 0.15, "twitter.com": 0.25, "x.com": 0.25,
    "tiktok.com": 0.10, "instagram.com": 0.15,
    "youtube.com": 0.50,  # variable — créateur de référence > vidéo random
    "pinterest.com": 0.20, "linkedin.com": 0.55,
    "discord.com": 0.15, "telegram.org": 0.15,
}

# Patterns d'URLs à FILTRER de la bibliographie : CDN de libs JS/CSS, fichiers
# d'asset, etc. — ce ne sont pas des "sources" mais des dépendances d'artifacts.
_NOT_A_SOURCE_PATTERNS: list[str] = [
    "cdn.jsdelivr.net",
    "unpkg.com",
    "cdnjs.cloudflare.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "ajax.googleapis.com",
    "code.jquery.com",
    "googletagmanager.com",
    "google-analytics.com",
]

# Domaines blacklistés : content farms / sites SEO-spam / contenus très douteux.
# Force le score à 0.10 indépendamment des autres règles.
_BLACKLIST_DOMAINS: set[str] = {
    "answers.com", "ehow.com", "wikihow.com",  # contenus généralistes très faibles
    "wikiwand.com",  # miroir wikipedia non-officiel
    "examine.com",  # nutrition controversée
}

# Score appliqué à un domaine INCONNU (pas dans _TIER_*). Volontairement bas
# (skepticisme par défaut) — un domaine non identifié ne mérite PAS une note
# neutre 0.5. Pour une vraie source il faut au moins être whitelisté.
_UNKNOWN_DOMAIN_SCORE: float = 0.30


def is_cdn_or_asset(url: str) -> bool:
    """Vrai si l'URL est un CDN de lib (jsdelivr, unpkg…) ou un asset (fonts,
    analytics). Ces URLs ne sont PAS des sources et doivent être filtrées de
    la bibliographie même si extract_citations les a remontées.
    """
    if not url or not isinstance(url, str):
        return False
    u = url.lower()
    return any(p in u for p in _NOT_A_SOURCE_PATTERNS)


def score_url_authority(url: str) -> float:
    """Retourne un score [0,1] d'autorité du domaine.

    Hiérarchie de matching :
      1. Domaine blacklisté → 0.10 (priorité absolue, override les autres)
      2. CDN/asset (jsdelivr, unpkg, fonts.google…) → 0.10 (ce n'est pas une source)
      3. Match exact dans _TIER_DOMAINS (suffix)
      4. Match TLD dans _TIER_TLDS
      5. Inconnu → _UNKNOWN_DOMAIN_SCORE (0.30) — skepticisme par défaut
    """
    if not url or not isinstance(url, str):
        return _UNKNOWN_DOMAIN_SCORE
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return _UNKNOWN_DOMAIN_SCORE
    if not host:
        return _UNKNOWN_DOMAIN_SCORE

    # 1. Blacklist explicite (override tout)
    root = _root_domain(host)
    for bl in _BLACKLIST_DOMAINS:
        if host == bl or host.endswith("." + bl) or root == bl:
            return 0.10

    # 2. CDN / asset (pas une vraie source — sera filtré de la biblio)
    if is_cdn_or_asset(url):
        return 0.10

    # 3. Match exact domain (suffix)
    for domain, score in _TIER_DOMAINS.items():
        if host == domain or host.endswith("." + domain):
            return score

    # 4. Match TLD (couvre `host.endswith(".gov.uk")` ET le cas host nu == "gov.uk")
    for tld, score in _TIER_TLDS.items():
        if host.endswith(tld) or host == tld.lstrip("."):
            return score

    # 5. Inconnu → skepticisme par défaut
    return _UNKNOWN_DOMAIN_SCORE


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


def build_bibliography(citations: list[dict], agent_confidence: dict | None = None) -> str:
    """Construit un bloc Markdown de bibliographie enrichie pour l'utilisateur·rice.

    Format pour chaque entrée :
      [^N]: 🟢 [Titre](url) — autorité 0.92 · agent web (confiance 0.78)

    Le préfixe `[^N]:` correspond à la convention footnote Markdown — si la
    synthèse Alyx utilise les marqueurs `[^N]` inline, OWUI les lie automatiquement
    aux entrées de cette bibliographie. Sinon, le bloc reste lisible comme un
    plain « ## Sources » numéroté.

    Args:
        citations: liste de dicts {url, title, snippet} (cf. _extract_citations)
        agent_confidence: dict optionnel agent → confidence pour afficher la
                          confiance de l'agent ayant fourni chaque source

    Returns: chaîne Markdown commençant par `\n\n---\n\n## 📚 Sources\n...`, ou ""
    """
    if not citations:
        return ""

    # Heuristique simple pour deviner quel agent a fourni quelle source : on
    # cherche le nom du domaine dans les sorties agents (déjà fait en amont
    # via _extract_citations qui itère sur web/wikipedia/doc/rag/geo/media).
    # Pour l'instant on n'a pas l'info exacte ; on affiche juste le score
    # d'autorité du domaine, et on laisse la confiance globale en footer si fournie.

    # Filtre : on retire les CDN / assets / fonts qui ne sont PAS des sources
    # documentaires (cf. _NOT_A_SOURCE_PATTERNS). Évite que cdn.jsdelivr.net
    # (chargé par un artifact) pollue la bibliographie.
    real_sources = [c for c in citations if not is_cdn_or_asset(c.get("url", ""))]
    if not real_sources:
        return ""

    lines = ["", "---", "", "## 📚 Sources", ""]
    for i, c in enumerate(real_sources, 1):
        url = c.get("url", "")
        title = c.get("title", "")[:100] or url
        score = score_url_authority(url)
        emoji = authority_emoji(score)
        lines.append(
            f"[^{i}]: {emoji} [{title}]({url}) — autorité {score:.2f}"
        )

    if agent_confidence:
        avg_c = avg_confidence(agent_confidence)
        if avg_c is not None:
            lines.append("")
            lines.append(
                f"> *Confiance moyenne des agents ayant collecté ces sources : "
                f"{authority_emoji(avg_c)} {avg_c:.2f}*"
            )

    return "\n".join(lines) + "\n"


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
