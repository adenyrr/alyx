---
name: press-release
description: Apply this methodology when the user asks the writer agent to draft, rewrite, or audit a press release, news release, "communiqué de presse", media announcement, or any short-form document distributed to journalists or wire services to announce a newsworthy event. Trigger keywords include "press release", "communiqué de presse", "media announcement", "announce our launch", "we just raised", "we just hired", "press kit". Use this skill for documents intended for external pickup by journalists, trade press, or newsroom syndication. Do NOT use it for internal announcements (use email-pro.md), social-media posts, marketing copy, blog posts (use blog-post.md), investor updates, or earnings call scripts.
agents: [writer]
---

# Press Release / Communiqué de Presse — Methodology

A press release is a journalist-facing document. Its single goal is to give a busy reporter — who scans 50–200 releases a day — everything they need to write a story without picking up the phone, while signalling the news is real, attributable, and worth covering. This skill teaches the writer agent how to compose, structure, and adapt press releases in English and French across the six most common occasions: news announcement, product launch, partnership, funding round, executive hire, and award.

---

## When to Apply

Apply this skill when the user request implies:

- An external announcement of a fundraising round, M&A, partnership, product launch, executive hire, award, milestone, or research finding
- Drafting a French *communiqué de presse* respecting AFP/Reuters-style conventions
- Producing a bilingual EN/FR release for international wire distribution
- Building a press kit (release + boilerplate + media contact + assets references)
- Rewriting marketing copy *as* a press release (compression, removal of adjectives, addition of attribution)

Do NOT apply this skill for:

- Internal company announcements — `skills/email-pro.md` (status update template)
- Blog posts or thought-leadership articles — `skills/blog-post.md`
- Social-media posts (LinkedIn, X) — short-form, different cadence and tone
- Marketing landing-page copy — sales-driven, different structure
- Investor letters or earnings releases (8-K, listed-company filings) — these have regulatory templates
- Crisis communications — adjacent but requires legal and PR specialist input, not just this skill

---

## Document Structure

The canonical press release skeleton, top to bottom:

1. **Release status tag** — `FOR IMMEDIATE RELEASE` (English) or `SOUS EMBARGO JUSQU'AU…` if embargoed; in French, `POUR DIFFUSION IMMÉDIATE` or `SOUS EMBARGO JUSQU'AU…`.
2. **Media contact block** — named contact, role, phone, email. *Above* the headline so a journalist with one question can find it in two seconds.
3. **Headline** — 5–10 words, factual, no hype.
4. **Subheadline / deck** (optional, 1 line) — adds the most important context the headline could not carry.
5. **Dateline** — `City, COUNTRY — Month DD, YYYY` (EN) or `Ville, Pays — JJ mois AAAA` (FR).
6. **Lead paragraph** — the 5W1H (who, what, when, where, why, how) compressed into ≤ 35 words.
7. **Body** — inverted pyramid: most important fact first, then supporting evidence, then context, then color. 3–5 paragraphs.
8. **Quote 1** — from the senior internal spokesperson, named with full title.
9. **Quote 2** (optional, often present) — from an external endorser (customer, partner, investor, regulator).
10. **Supporting facts / data table** (optional) — for product launches with specs, funding with cap table, etc.
11. **Boilerplate** — `About {{Company}}` — 3–5 sentence standing description, kept identical across releases for that calendar year.
12. **End marker** — `###` (or `–30–`, both archaic but expected by wire desks) centered on its own line, signalling "this is the end of the release; what follows is not for publication".
13. **Notes to editors** (below ###, optional) — URL to press kit, asset library, embargo terms, interview availability.

Maximum length: **one to two pages, ≤ 600 words**, excluding boilerplate.

---

## Section-by-Section Writing Guide

### Release tag

`FOR IMMEDIATE RELEASE` is the default and is *always* in capitals. If embargoed, the format is:

> `EMBARGOED UNTIL 09:00 CET, TUESDAY 28 MAY 2026`

French equivalents:

> `POUR DIFFUSION IMMÉDIATE`
> `SOUS EMBARGO JUSQU'AU MARDI 28 MAI 2026 À 09H00 CET`

Embargoes are a contract with journalists; honor them or you damage future trust.

### Media contact block

Above the headline. Format:

> **Media contact:**
> Camille Martin, Head of Communications, {{Company}}
> +33 1 23 45 67 89 · press@company.com

For French releases:

> **Contact presse :**
> Camille Martin, Directrice de la Communication, {{Société}}
> +33 1 23 45 67 89 · presse@societe.com

Never use a generic `info@` — journalists want a human's name they can re-contact.

### Headline rules

A press-release headline is *not* an advertising tagline. Rules:

- **5–10 words.** Anything longer breaks wire-service templates.
- **Subject-verb-object** declarative sentence.
- **Concrete and factual.** "Acme raises $40M Series B" beats "Acme announces game-changing funding milestone".
- **No exclamation marks.** Ever.
- **No clickbait adjectives**: "revolutionary", "world-first", "unprecedented", "best-in-class", "cutting-edge", "groundbreaking", "next-gen", "leading", "innovative". Even if accurate, they signal marketing copy and reduce pickup.
- **Title-case for English; sentence-case for French**: `Acme Raises $40M Series B`; `Acme lève 40 M€ en série B`.
- **No questions, no puns, no rhetorical devices.** Journalists need to extract the news in one read.

Compare:

| Bad | Good |
|---|---|
| Helix Pay Unveils Revolutionary AI-Powered Payments Platform That Will Transform Commerce! | Helix Pay Launches Multi-Region Settlement Service in 7 EU Markets |
| Acme Welcomes Dynamic New CMO to Drive Next-Gen Growth | Acme Names Priya Shah Chief Marketing Officer |
| Big News from Verdant: Our Most Ambitious Partnership Yet | Verdant and Patagonia Open Joint Recycling Facility in Lyon |

### Subheadline / deck (optional)

One line, sentence-case, adding the most important fact the headline left out — typically the *so what* or the scale. Italic or normal weight, never bold.

> Headline: `Helix Pay Raises €40M Series B`
> Deck: `Funding led by Index Ventures; will be used to scale settlement infrastructure to LATAM and APAC.`

### Dateline

Format: **`CITY, COUNTRY — Month DD, YYYY`** for English; **`Ville, Pays — JJ mois AAAA`** for French.

- City is the company's announcement city (usually HQ), in ALL CAPS for the city, mixed-case country.
- Em dash (—), not hyphen.
- Date is the announcement date, written out.
- This format is parsed by wire-service software; do not innovate.

Examples:

> `PARIS, FRANCE — May 21, 2026 —`
> `LONDON, UK — May 21, 2026 —`
> `PARIS, FRANCE — 21 mai 2026 —`

### Lead paragraph (the lede)

The most important paragraph. A journalist who reads only the headline + lede must understand the entire story. Compress 5W1H (who, what, when, where, why, how) into ≤ 35 words.

Pattern:

> `{{Company}}, {{1-clause descriptor}}, today announced {{the news, with the key number}}, {{the so-what}}.`

Example:

> Helix Pay, a Paris-based payments infrastructure company, today announced it has raised €40 million in Series B funding led by Index Ventures, bringing total funding to €58 million and enabling expansion of its multi-region settlement service to Latin America in 2026.

That sentence is 39 words — at the edge of acceptable. Trim ruthlessly if needed.

### Body — inverted pyramid

Each subsequent paragraph adds less-important detail. A journalist must be able to *cut from the bottom* without losing meaning.

Paragraph 2: scale, traction, or proof point that validates the news.

Paragraph 3: context — why this matters now (market, competition, regulation, customer need).

Paragraph 4: how it works / what's planned (the *how*).

Paragraph 5: roadmap or next milestone (the *what's next*).

Each paragraph 2–4 sentences. No paragraph > 60 words.

### Quotes

A quote does three things: humanizes the news, adds an attributable opinion the journalist can use without paraphrase, and signals seniority of the source. Rules:

- **Always named**, with full title and company.
- **First quote** from the most senior internal spokesperson (CEO for company-level news; functional head for functional news).
- **Second quote** (optional, often present) from an external party — customer, partner, investor — adding third-party validation.
- **Sounds like a human spoke it**, not like a press release wrote it. Strip jargon and superlatives.
- **Carries an opinion or insight**, not a restatement of facts already in the body.
- **One sentence is fine**; never more than three.
- **Attribution after the first sentence** of a multi-sentence quote: `"...," said Alex Dupont, CEO of Helix Pay. "..."`

Compare:

- Weak: "We are thrilled and excited to announce this groundbreaking partnership that will revolutionize the industry," said the CEO.
- Strong: "This funding lets us do something we have wanted to do for two years: ship settlement in markets where the regulatory cost was previously prohibitive," said Alex Dupont, CEO of Helix Pay. "Latin America is first because the demand is loudest from our existing merchants."

### Boilerplate

A 3–5 sentence standing description of the company, used identically across every release in a given calendar year. Update once per year (typically January) with new headcount, customer count, and tenure.

Pattern:

> About {{Company}}
> {{Company}} is a {{descriptor}} headquartered in {{city}}, {{country}}. Founded in {{year}} by {{founders}}, the company {{what it does, one sentence}}. {{Company}} serves {{N}} customers in {{N}} countries, processes {{scale figure}}, and employs {{N}} people. Backed by {{key investors}}. More at {{URL}}.

French:

> À propos de {{Société}}
> {{Société}} est {{descripteur}} dont le siège est à {{ville}}, {{pays}}. Fondée en {{année}} par {{fondateurs}}, l'entreprise {{ce qu'elle fait, une phrase}}. {{Société}} sert {{N}} clients dans {{N}} pays, traite {{chiffre de volume}}, et emploie {{N}} personnes. Soutenue par {{investisseurs clés}}. En savoir plus sur {{URL}}.

### End marker

A line containing only `###` (or `–30–`), centered, marks the end of the publishable release. Anything below is for the editor only.

### Notes to editors

Below the end marker:

- Press kit URL with logos, headshots, product screenshots
- Embargo terms (re-stated)
- Interview availability windows
- B-roll or media availability

---

## Variant Rules by Occasion

### 1. News announcement (general)

- Lead with the news, the date, and the so-what.
- Body: scale, context, what's next.
- One internal quote sufficient.

### 2. Product launch

- Headline: `{{Company}} Launches {{Product Name}} for {{Market}}`.
- Body must include: what the product does in one sentence, who it's for, pricing or availability date, supported regions/languages, key differentiation in one sentence (without superlatives — use specifications).
- Include a specifications table if technical.
- One customer quote ("design partner", "early adopter") strengthens the release substantially.

### 3. Partnership

- Headline: `{{Company A}} and {{Company B}} Partner to {{Joint Outcome}}`.
- Both logos in the asset pack; both PR teams approve final copy.
- Two quotes: one from each company's senior spokesperson.
- Body must answer: what the partnership produces (joint product? integration? distribution?), where it's available, customer benefit.

### 4. Funding round

- Headline: `{{Company}} Raises {{$X}} Series {{Letter}} Led by {{Lead Investor}}`.
- Mandatory data: round size, lead investor, participating investors, post-money valuation if disclosed (often not), use of funds (3 bullets), prior funding total.
- Quotes: CEO + lead investor partner.
- Avoid disclosing valuation if the company has not chosen to — once published, it sticks.

### 5. Executive hire

- Headline: `{{Company}} Names {{Person}} {{Title}}`.
- Body: who, prior role, what they will do, who they replace (if relevant), team they'll lead.
- Quotes: CEO welcoming, the new hire on their priorities.
- Avoid hyperbole about the candidate ("legendary", "industry-shaping"); let the bio do the work.

### 6. Award / recognition

- Headline: `{{Company}} Wins {{Award}}`.
- Body: who issued the award, the category, the criteria, what was recognized.
- One quote from the company; ideally one quote or citation from the awarding body.
- Short release (≤ 350 words); awards rarely warrant the full body.

---

## Output Templates

### Template — English press release (funding round)

```markdown
**FOR IMMEDIATE RELEASE**

**Media contact:**
{{Communications lead full name}}, {{Title}}, {{Company}}
{{phone}} · press@{{company}}.com

# {{Company}} Raises {{$X}} Series {{Letter}} to {{One-Line Purpose}}

*{{Optional subhead: lead investor name and headline use of funds.}}*

**{{CITY, COUNTRY}} — {{Month DD, YYYY}} —** {{Company}}, {{one-clause descriptor}}, today announced it has raised {{$X million / €X million}} in Series {{Letter}} funding led by {{Lead Investor}}, with participation from {{Co-investors}}. The round brings total funding to {{$Y}} and will fund {{primary use of funds in one clause}}.

{{Paragraph 2: scale/traction proof — e.g., revenue, customers, growth rate, market share, that justifies the round.}}

{{Paragraph 3: context — what's happening in the market, why this funding is timely, who the customers are.}}

"{{Quote 1: from CEO, opinion-bearing, ≤ 3 sentences.}}" said {{CEO Full Name}}, {{Title}} of {{Company}}.

{{Paragraph 4: how the funds will be used — three concrete bullets or a tight paragraph.}}

"{{Quote 2: from Lead Investor partner, ≤ 3 sentences, articulates the investment thesis.}}" said {{Investor Full Name}}, {{Title}} at {{Investor Firm}}.

{{Paragraph 5: what's next — hiring plans, geographic expansion, roadmap milestone with timeline.}}

**About {{Company}}**
{{Company}} is a {{descriptor}} headquartered in {{city}}, {{country}}. Founded in {{year}} by {{founders}}, the company {{what it does, one sentence}}. {{Company}} serves {{N}} customers in {{N}} countries and employs {{N}} people. More at {{URL}}.

**About {{Lead Investor}}**
{{Investor Firm}} is a {{stage}} venture capital firm investing in {{thesis}}. Portfolio includes {{2–3 names}}. More at {{URL}}.

###

Notes to editors: Press kit (logos, founder headshots, product screenshots) available at {{URL}}. CEO {{Name}} available for interview {{date window, time zone}}.
```

### Template — Communiqué de presse français (lancement produit)

```markdown
**POUR DIFFUSION IMMÉDIATE**

**Contact presse :**
{{Nom de la responsable communication}}, {{Fonction}}, {{Société}}
{{téléphone}} · presse@{{societe}}.com

# {{Société}} lance {{Nom du produit}} pour {{marché}}

*{{Sous-titre facultatif : précision la plus importante absente du titre.}}*

**{{VILLE, PAYS}} — {{JJ mois AAAA}} —** {{Société}}, {{descripteur en une proposition}}, annonce aujourd'hui le lancement de {{Nom du produit}}, {{une phrase décrivant ce que fait le produit}}. La solution est disponible dès {{date}} en {{liste des marchés}}.

{{Paragraphe 2 : preuves de traction — partenaires de lancement, volumes, performance technique, certification.}}

{{Paragraphe 3 : contexte de marché — pourquoi maintenant, quel besoin client, quel changement réglementaire ou technologique le justifie.}}

« {{Citation 1 : du DG ou de la responsable produit, porteuse d'une opinion, ≤ 3 phrases.}} », déclare {{Nom complet}}, {{Fonction}} de {{Société}}.

{{Paragraphe 4 : caractéristiques principales du produit, en 3 points ou un paragraphe serré.}}

« {{Citation 2 : d'un client de design partner, ≤ 3 phrases, apportant une validation externe.}} », ajoute {{Nom complet}}, {{Fonction}} chez {{Société cliente}}.

{{Paragraphe 5 : feuille de route — prochaines fonctionnalités, prochains marchés, calendrier.}}

**À propos de {{Société}}**
{{Société}} est {{descripteur}} dont le siège est à {{ville}}, {{pays}}. Fondée en {{année}} par {{fondateurs}}, l'entreprise {{ce qu'elle fait, une phrase}}. {{Société}} sert {{N}} clients dans {{N}} pays et emploie {{N}} personnes. En savoir plus sur {{URL}}.

###

Notes à la rédaction : kit presse (logos, photos des fondateurs, captures produit) disponible sur {{URL}}. {{Nom du DG}} disponible pour interview {{créneau, fuseau horaire}}.
```

---

## Two Full Samples

### Sample 1 — English (Series B funding round)

```markdown
**FOR IMMEDIATE RELEASE**

**Media contact:**
Camille Martin, Head of Communications, Helix Pay
+33 1 84 60 12 34 · press@helixpay.com

# Helix Pay Raises €40M Series B to Expand Multi-Region Settlement to Latin America

*Round led by Index Ventures; existing investors Accel and Eurazeo participated. Funds will support a 25-engineer hiring plan in 2026.*

**PARIS, FRANCE — May 21, 2026 —** Helix Pay, a Paris-based payments infrastructure company providing settlement and reconciliation services to European merchants, today announced it has raised €40 million in Series B funding led by Index Ventures, with participation from existing investors Accel and Eurazeo. The round brings total funding to €58 million and will fund expansion of the company's settlement service into Latin America starting Q3 2026.

Helix Pay processes €1.4 billion in monthly merchant volume across seven European markets, with revenue growth of 4.2× year over year and gross margin above 70%. The company serves 320 merchants ranging from mid-market e-commerce to listed retailers, including Decathlon and Mango.

The round comes amid accelerating demand for European-built payments infrastructure following the EU's Instant Payments Regulation, which took effect in January 2026 and requires settlement of SEPA Instant transactions within ten seconds for all participating banks. Helix Pay's platform has supported the regulation since launch.

"This funding lets us do something we have wanted to do for two years: ship settlement in markets where the regulatory cost was previously prohibitive," said Alex Dupont, CEO and co-founder of Helix Pay. "Latin America is first because the demand is loudest from our existing merchants, and because we can build there on the same primitives we built for the EU."

The €40 million will fund three priorities: hiring 25 engineers in Paris and São Paulo, regulatory licensing in Brazil and Mexico, and a multi-region active-active architecture intended to absorb a 10× volume growth without re-architecture.

"Helix has built one of the cleanest settlement engines we've seen in Europe, and the team has shown unusual discipline about staying focused on infrastructure rather than chasing consumer-facing products," said Marta Cifuentes, Partner at Index Ventures. "Latin America is a natural extension, not a pivot — the same architecture, applied to a market that needs it."

Helix Pay plans to open a São Paulo office in Q4 2026 and to support its first Brazilian merchants in early 2027.

**About Helix Pay**
Helix Pay is a payments infrastructure company headquartered in Paris, France. Founded in 2021 by Alex Dupont and Léa Bernard, the company provides settlement and reconciliation services to European merchants under a licensed payment-institution status (ACPR). Helix Pay serves 320 merchants in 7 countries, processes €1.4 billion in monthly volume, and employs 62 people. More at helixpay.com.

**About Index Ventures**
Index Ventures is a global venture capital firm investing across seed to growth stages in technology companies. Portfolio includes Adyen, Revolut, Wise, and Datadog. More at indexventures.com.

###

Notes to editors: Press kit (logos, founder headshots, product screenshots, traction data) available at helixpay.com/press. CEO Alex Dupont and Lead Investor Marta Cifuentes (Index Ventures) available for interview 21–24 May, CET business hours. Embargo: none — for immediate publication.
```

### Sample 2 — Français (partenariat industriel)

```markdown
**POUR DIFFUSION IMMÉDIATE**

**Contact presse :**
Camille Martin, Directrice de la Communication, Verdant France
+33 1 42 50 67 89 · presse@verdant.fr

# Verdant et Patagonia ouvrent une usine commune de recyclage textile à Lyon

*L'usine traitera jusqu'à 4 000 tonnes de coton et polyester recyclés par an dès 2027 et alimentera les deux marques en fibres certifiées.*

**LYON, FRANCE — 21 mai 2026 —** Verdant, marque française d'habillement durable, et Patagonia, marque américaine de vêtements outdoor, annoncent aujourd'hui l'ouverture d'une usine commune de recyclage textile à Lyon-Vaise. Le site, d'une capacité de 4 000 tonnes par an, traitera coton et polyester en boucle fermée et alimentera en fibres recyclées les collections des deux marques à partir du second semestre 2027.

L'investissement initial s'élève à 28 millions d'euros, financé à parts égales par les deux entreprises. L'usine emploiera 84 personnes à sa pleine capacité et a obtenu la certification GRS (Global Recycled Standard) avant son ouverture.

Ce projet répond à l'entrée en vigueur du règlement européen sur l'éco-conception des textiles (ESPR), qui impose à partir de 2027 un seuil minimal de fibres recyclées dans les collections vendues dans l'Union européenne. Verdant et Patagonia avaient annoncé en 2024 leur engagement à atteindre 60 % de fibres recyclées dans leurs collections d'ici 2030, un objectif que cette infrastructure rend désormais atteignable sans recours à des importations.

« Nous avons cherché pendant trois ans un partenaire industriel capable de partager notre méthode d'audit fournisseur — la rigueur de Patagonia sur ce sujet est connue, et la combinaison avec notre savoir-faire de filature française nous permet de produire des fibres dont nous pouvons garantir l'origine ligne par ligne », déclare Sophie Lambert, Directrice Générale de Verdant France.

L'usine intégrera trois lignes de production distinctes : tri optique automatisé, défibrage mécanique pour le coton, et dépolymérisation chimique pour le polyester. La capacité sera ramenée à 6 000 tonnes par an d'ici 2028, sous réserve de l'obtention d'une seconde tranche d'autorisation environnementale.

« Patagonia construit depuis quarante ans des chaînes d'approvisionnement vérifiables. Ce partenariat avec Verdant est notre premier investissement industriel en Europe, et nous avons choisi Lyon pour la proximité avec le bassin textile français et pour la qualité du dialogue avec les autorités locales », ajoute Marc Reyes, Vice-Président Supply Chain Europe chez Patagonia.

L'usine ouvrira ses portes en juin 2027 et commencera à livrer les premières fibres aux deux marques au troisième trimestre de la même année.

**À propos de Verdant**
Verdant est une marque française d'habillement durable dont le siège est à Lyon. Fondée en 2018, l'entreprise conçoit et distribue des collections femme et homme à partir de fibres certifiées GOTS et GRS. Verdant compte 142 collaborateurs, 38 boutiques en France et en Allemagne, et a réalisé un chiffre d'affaires de 92 millions d'euros en 2025. En savoir plus sur verdant.fr.

**À propos de Patagonia**
Patagonia est une entreprise américaine d'habillement outdoor fondée en 1973 à Ventura, Californie. Détenue depuis 2022 par une fiducie environnementale, l'entreprise réalise un chiffre d'affaires annuel d'environ 1,5 milliard de dollars et reverse l'intégralité de ses profits à la protection de la nature. En savoir plus sur patagonia.com.

###

Notes à la rédaction : kit presse (visuels du site, schémas des lignes de production, photos des dirigeants) disponible sur verdant.fr/presse. Visite presse organisée le mercredi 28 mai à 14h00 sur le site de Lyon-Vaise — inscription auprès du contact presse.
```

---

## Style & Tone Guidelines

- **Voice**: third person, declarative, neutral. Never first person ("we", "our") outside of direct quotes.
- **Tense**: present and past, never future-marketing ("will revolutionize"). Use "plans to", "intends to", "expects to" for future statements, never bare future.
- **Numbers**: digits for all quantities, units explicit (€40 million, not €40M in body text — but acceptable in headlines for space). French uses non-breaking spaces: `40 000 €`, `40 M€`. English: `€40 million` or `€40M`.
- **Adjectives**: cut almost all. "Innovative", "leading", "world-class", "best-in-class", "cutting-edge", "next-generation", "game-changing", "groundbreaking" — banned. Replace with specifications.
- **Exclamation marks**: zero in a release.
- **Citations**: always attributed by full name + title + company. Anonymous quotes belong in news articles, not releases.
- **Tense in quotes**: spoken voice; allow first person inside quotes only.
- **French specifics**: use `«` `»` for quotes (with non-breaking spaces), `M€` for millions of euros, `Mds€` for billions, `JJ mois AAAA` for dates, capitalization of `Directeur Général` / `Directrice Générale` consistent across release.

---

## Quality Checklist

- [ ] `FOR IMMEDIATE RELEASE` (or embargo line) at the top
- [ ] Media contact block above headline with named contact, phone, email
- [ ] Headline is 5–10 words, declarative, no exclamation, no hype adjectives
- [ ] Dateline uses correct format: `CITY, COUNTRY — Month DD, YYYY —`
- [ ] Lead paragraph contains the 5W1H in ≤ 35 words
- [ ] Body follows inverted pyramid — could be cut from the bottom without losing the news
- [ ] At least one named, attributed quote with full title and company
- [ ] External quote (customer / partner / investor) included where occasion warrants
- [ ] Boilerplate present and identical to other releases this year
- [ ] `###` end marker present
- [ ] Notes to editors below the end marker (press kit URL, interview availability)
- [ ] Total length excluding boilerplate ≤ 600 words
- [ ] No banned hype words ("revolutionary", "groundbreaking", "leading", "innovative", "next-gen", "world-first")
- [ ] No exclamation marks
- [ ] Numbers in digits with units, currencies, and non-breaking spaces (FR)
- [ ] All names spelled and titles verified against LinkedIn or company site
- [ ] Embargo terms respected if any
- [ ] French version uses *Société*, *Directrice Générale*, `« »` quotes, `JJ mois AAAA` dates, `M€`

---

## Common Mistakes

- **Headline as marketing tagline.** "Acme Transforms the Future of Commerce" gets deleted; "Acme Acquires Beta for $150M" gets covered.
- **Adjective stuffing.** Every "revolutionary", "innovative", "leading" reduces the release's credibility with reporters who've seen 1,000 of them this year.
- **Burying the news.** The lede must contain the news. If a journalist has to read paragraph 3 to find what happened, the release fails.
- **Quotes that read like press releases.** Real spokespeople do not say "We are thrilled to leverage synergies across our world-class platform". Strip jargon.
- **Anonymous quotes.** Belong in journalism, not releases. Every quote must be attributed by full name and title.
- **No external validation.** Funding rounds, partnerships, product launches with a customer benefit all benefit from a second quote from an outside party.
- **Wrong dateline format.** Wire services parse this field; deviations break syndication.
- **No boilerplate.** Reporters need the standing description; without it, they paraphrase incorrectly.
- **Exclamation marks.** Signal amateur.
- **Future-tense marketing.** "Will revolutionize" is editorial opinion. Use "is designed to", "is expected to".
- **Embargo broken by accident.** Once you send to journalists, you have lost control of timing unless the embargo is iron-clad and short.
- **Over-disclosing valuation in funding releases.** If the company chose to disclose, fine; if not, do not slip it into the body.
- **French release with English typography** (straight quotes `"` instead of `« »`, missing non-breaking spaces, `40M€` instead of `40 M€`). Reads as machine-translated.
- **No press-kit URL.** Forces journalists to email and wait — many will simply pass on the story.
- **Releasing on Friday afternoon.** Worst pickup window of the week. Default to Tuesday–Thursday morning, local time of the target media.
