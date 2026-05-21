---
name: cover-letter
description: Apply this methodology when the user asks the writer agent to draft, rewrite, or audit a cover letter, motivation letter, "lettre de motivation", letter of interest, or application letter accompanying a CV/resume. Trigger keywords include "cover letter", "motivation letter", "lettre de motivation", "letter of interest", "write me a letter for this job", "tailor a cover letter", "rewrite my LM". Use this skill for any short-form personalized letter whose purpose is to win a first interview. Do NOT use it for CVs/resumes (skills/cv-resume.md), professional emails (skills/email-pro.md), recommendation letters, academic statements of purpose, or scholarship essays — these follow different conventions and lengths.
agents: [writer]
---

# Cover Letter / Lettre de Motivation — Methodology

A cover letter is the candidate's one chance to argue *why this role, why this company, why now* in their own voice. It is read in under 90 seconds by a recruiter who already has the CV. Its purpose is not to summarize the CV but to translate it into a value proposition for one specific employer. This skill teaches the writer agent how to compose persuasive, structured, culturally appropriate cover letters in English and French.

---

## When to Apply

Apply this skill when:

- The user provides a job description and a CV/profile and asks for an accompanying letter
- The user asks to tailor an existing cover letter for a new role
- The user wants a French *lettre de motivation* respecting formal conventions (vous, *objet*, *formule de politesse*)
- The user wants a bilingual EN/FR pair for an international application
- The user needs a "letter of interest" for an unadvertised role at a company

Do NOT apply this skill for:

- A CV or resume itself — delegate to `skills/cv-resume.md`
- A short follow-up note or thank-you email after an interview — `skills/email-pro.md`
- A cold outreach DM or LinkedIn message — `skills/email-pro.md` (cold outreach template)
- An academic statement of purpose (1–2 pages, research narrative, different rhetoric)
- A recommendation/reference letter written *about* someone else
- A grant or fellowship motivation essay (longer, prompt-driven)

---

## Document Structure

A cover letter is a one-page persuasive letter. Optimal length: **250–400 words, never more than one page**. The skeleton:

1. **Sender contact block** — your name, address, email, phone, top-left or top-right.
2. **Date** — full date in local convention.
3. **Recipient block** — named hiring manager + title + company + address.
4. **Subject line** (FR mandatory, EN optional) — *Objet:* {{role + reference if any}}.
5. **Salutation** — named ("Dear Ms. Martin,") preferred over generic ("Dear Hiring Manager,").
6. **Opening hook** (1 paragraph, 2–3 sentences) — why *this* company, *now*. Specific signal, not boilerplate.
7. **Value proposition** (1–2 paragraphs) — top 3 results-with-metrics that map to the top 3 requirements of the JD.
8. **Fit narrative** (1 paragraph) — why you + this role + this company is a fit beyond skills (mission, problem, scale, stage, culture cue).
9. **Call to action** (1–2 sentences) — what you want next (a conversation, an interview slot, a portfolio review).
10. **Sign-off** + handwritten or typed signature.

Total: 4–5 short paragraphs, ample white space.

---

## Section-by-Section Writing Guide

### Sender + recipient blocks

- **Sender**: full name, city + country (street optional in 2026), email, phone, LinkedIn vanity URL. No need to repeat what's in the CV header — but consistency wins.
- **Date**: US "May 21, 2026" | UK/EU "21 May 2026" | FR "Paris, le 21 mai 2026" (city precedes date in French letters, this is a tradition).
- **Recipient**: research the actual hiring manager via LinkedIn or the company site. "Dear Ms. Camille Martin, Head of Engineering, Stripe France, 12 rue de la Banque, 75002 Paris". If genuinely unfindable, use "Dear Hiring Manager," — never "To whom it may concern" (it signals zero research).

### Subject line (Objet — mandatory in French letters)

French convention: a one-line *Objet* between recipient and salutation, format:

> **Objet :** Candidature au poste de {{intitulé}} — référence {{ID si applicable}}

English version (optional but useful for email-attached letters):

> **Re:** Application for the {{role title}} position — Ref. {{ID}}

### Salutation

| Context | English | French |
|---|---|---|
| Named woman | Dear Ms. {{Lastname}}, | Madame {{Lastname}}, |
| Named man | Dear Mr. {{Lastname}}, | Monsieur {{Lastname}}, |
| Gender unknown / non-binary | Dear {{Firstname Lastname}}, | Madame, Monsieur, |
| Unknown person | Dear Hiring Manager, | Madame, Monsieur, |
| Multiple recipients | Dear Hiring Team, | Mesdames, Messieurs, |

Avoid "Dear Sir or Madam" (dated), "Hey" (too casual), "Greetings" (cold). Never "Cher/Chère" in FR business letters — too familiar.

### Opening hook — earn the next paragraph

The most common failure: "I am writing to apply for the position of X advertised on Y." This wastes the most-read sentence of the letter. Replace with a *signal*: a specific reason this company at this moment.

Patterns that work:

- **Recent news**: "Stripe's launch of {{product}} last month {{specific implication}} — exactly the problem I have spent the last three years solving at {{prev co}}."
- **Specific fit**: "Your job posting calls for {{requirement}} on {{tech/system}} — I led that exact migration at {{prev co}}, cutting {{metric}}."
- **Mission resonance with proof**: "I have built three platforms for the underbanked — at {{co1}}, {{co2}}, and {{co3}}. Your stated mission of {{mission}} is the next logical role for me, not a pivot."
- **Mutual context** (warm): "{{Name}} suggested I reach out — we worked together at {{co}} where she saw me {{specific work}}."

Do NOT start with "My name is" (it's at the top of the letter) or "I have always wanted to work at" (unprovable).

### Value proposition — 3 results, mapped to JD

Pick the top three requirements in the job description. For each, pair with one accomplishment from your CV. Pattern:

> You're looking for X. I did exactly X at {{co}}, with result Y.

Examples:

- "You're scaling the payments rail to LATAM. At {{co}}, I led the team that launched in 7 LATAM markets in 14 months, reaching $90 M GMV and 99.95% settlement reliability."
- "You need someone fluent in Postgres at scale. I redesigned the indexing strategy on a 4 TB OLTP database at {{co}}, cutting p95 query time from 480 ms to 90 ms with zero downtime."
- "You want a manager who hires. In my last 18 months I hired 11 engineers (52% women, 36% from under-represented groups in tech), 100% still on team at the 12-month mark."

Three is the magic number. Two reads thin; four reads as listing.

### Fit narrative — beyond skills

The recruiter now believes you *can*. This paragraph must answer *why you will stay and thrive*. Tie one of:

- The company's stage (Series B → C scaling, post-IPO consolidation, turnaround)
- A specific technical or domain problem (latency, regulation, multi-tenancy, internationalization)
- The team or leader (you've followed their work, you share a methodology)
- A geographic or life-stage alignment (you're relocating, building roots, returning to market)

Avoid "I would love to be part of your team" (everyone would). Be concrete.

### Call to action

One direct sentence asking for the next step. Match the company's culture:

- Corporate / formal: "I would welcome the opportunity to discuss how my experience could support {{team}}. I am available for a conversation at your convenience."
- Startup / direct: "I'd love a 30-minute call to dig into how I'd ramp on {{team/product}}. I'm free most mornings CET next week."
- Speculative / no posted role: "If you'd be open to a brief conversation about how {{specific capability}} could support your roadmap, I'd welcome it."

### Sign-off

| Register | English | French |
|---|---|---|
| Standard formal | Sincerely, | Veuillez agréer, Madame/Monsieur, l'expression de mes salutations distinguées, |
| Slightly warmer | Best regards, | Cordialement, *(only if relationship is already warm)* |
| US neutral | Best, | n/a |
| Avoid in formal | Cheers, / Thanks, | Bien à vous, *(too familiar for first contact)* |

In French, the *formule de politesse* is a fixed expression — not a creative space. Pick one canonical form and use it verbatim:

- Most formal: "Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées."
- Standard formal: "Veuillez agréer, Madame, l'expression de ma considération distinguée."
- To a senior executive: "Je vous prie de croire, Monsieur le Directeur, en l'assurance de ma considération la plus respectueuse."

Rules: (i) the salutation form ("Madame", "Monsieur") must match the opening salutation exactly; (ii) never abbreviate (no "Mme", no "M."); (iii) the formula is one sentence ending in a comma + newline + signature.

---

## Output Templates

### Template — English cover letter (tech role)

```markdown
{{Firstname Lastname}}
{{City, Country}} · {{email}} · {{phone}} · linkedin.com/in/{{handle}}

{{Month DD, YYYY}}

{{Hiring Manager Name}}
{{Title}}
{{Company}}
{{Address}}

**Re:** Application for the {{Role Title}} position — Ref. {{JD-ID}}

Dear {{Ms./Mr. Lastname}},

{{Opening hook: a specific signal about why this company, this product, this moment — 2–3 sentences referencing a recent launch, specific challenge, or shared mission.}}

The role calls for {{requirement 1}}, {{requirement 2}}, and {{requirement 3}}. These are precisely the problems I have spent the last {{N years}} solving. At {{Previous Company}}, I {{accomplishment 1 with metric}}. Earlier, at {{Previous Previous Company}}, I {{accomplishment 2 with metric}}. And in my current role, I {{accomplishment 3 with metric}}.

Beyond the technical fit, what draws me to {{Company}} is {{specific reason: stage, mission, technical problem, leader}}. {{One sentence elaborating with proof you understand the company.}} {{One sentence on what you'd bring beyond skills — judgment, network, perspective.}}

I would welcome a conversation about how I could contribute to {{specific team or initiative}}. I am available {{availability window}} and reachable at the contact above.

Sincerely,

{{Firstname Lastname}}
```

### Template — Lettre de motivation française (poste cadre)

```markdown
{{Prénom NOM}}
{{Adresse}}
{{Code postal, Ville}}
{{Téléphone}} · {{Email}}

{{Ville}}, le {{JJ mois AAAA}}

{{Nom du destinataire}}
{{Fonction}}
{{Société}}
{{Adresse}}

**Objet :** Candidature au poste de {{intitulé exact du poste}} — référence {{ID}}

Madame, Monsieur,

{{Phrase d'accroche : une raison spécifique et démontrable pour laquelle ce poste, dans cette entreprise, à ce moment. Référence à une actualité, un produit, une difficulté du marché — éviter « Je vous écris pour faire acte de candidature ».}}

L'annonce recherche {{compétence 1}}, {{compétence 2}} et {{compétence 3}}. Ce sont exactement les sujets que j'ai conduits ces {{N dernières années}}. Chez {{société précédente}}, j'ai {{réalisation 1 avec chiffre}}. Auparavant, chez {{société}}, j'ai {{réalisation 2 avec chiffre}}. Dans mon poste actuel, je {{réalisation 3 avec chiffre}}.

Au-delà de la correspondance technique, ce qui me conduit vers {{Société}} est {{raison spécifique : stade de croissance, mission, problème métier}}. {{Une phrase qui démontre la connaissance de l'entreprise.}} {{Une phrase sur la valeur ajoutée non-technique : jugement, réseau, expérience d'un environnement comparable.}}

Je serais ravi(e) d'échanger sur la manière dont je pourrais contribuer à {{équipe ou projet précis}}. Je suis disponible {{créneau}} et joignable aux coordonnées ci-dessus.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{{Prénom NOM}}
*(signature manuscrite si lettre imprimée)*
```

---

## Two Full Sample Letters

### Sample 1 — Tech (Senior Backend Engineer at a fintech)

```markdown
Léa Bernard
Paris, France · lea.bernard@protonmail.com · +33 6 12 34 56 78 · linkedin.com/in/leabernard

May 21, 2026

Camille Martin
Head of Engineering, Payments Platform
NorthStar Pay
12 rue de la Banque, 75002 Paris

**Re:** Application for the Senior Backend Engineer position — Ref. SBE-2026-04

Dear Ms. Martin,

NorthStar's announcement last month of the SEPA Instant rollout across its merchant base was, frankly, the trigger for this letter. I have spent the last four years building the same primitive — idempotent, sub-200 ms settlement on a Go + Kafka stack — at Adyen-adjacent scale, and I'd like to bring that experience to a team that has decided to build it natively in France rather than outsource it.

The role calls for Go services on Kafka, sub-300 ms p95 latency, and a PCI-DSS-aware mindset. At Mangopay, I led the 5-engineer team that rebuilt the settlement service in Go, processing €1.4 B/month at 99.99% availability with a 38% infrastructure cost cut. Earlier, at PayPlug, I designed the idempotency layer on Kafka consumers that eliminated duplicate payouts worth roughly €80 k/month. And throughout, I have been the engineer the security team pulls into PCI audits — we passed our last QSA assessment with zero engineering findings.

What draws me to NorthStar specifically is the bet on a fully European stack and the explicit roadmap to support both card and account-to-account rails on the same platform. I have shipped both in production and have strong opinions on where the abstractions belong; I would expect to be useful in those design conversations from week one.

I would welcome a thirty-minute conversation to dig into the platform's current shape and where I could ramp fastest. I am available mornings CET next week and reachable at the contact above.

Sincerely,

Léa Bernard
```

### Sample 2 — Non-tech (Marketing Director at a sustainable apparel brand)

```markdown
Jordan Okafor
Brooklyn, NY · jordan.okafor@gmail.com · +1 (646) 555-0193 · linkedin.com/in/jordanokafor

May 21, 2026

Priya Shah
Chief Marketing Officer
Verdant Apparel
220 Hudson Street, New York, NY 10013

**Re:** Application for the Director of Marketing, North America position

Dear Ms. Shah,

Verdant's recent decision to publish its full Tier 4 supplier audit — including the suppliers that failed — is the kind of commercially uncomfortable transparency I have spent ten years arguing for from the marketing side. Most brands try to *announce* sustainability; Verdant is, demonstrably, *practising* it. I would like to help you tell that story to a North American audience that is increasingly skeptical of the first kind of brand and starving for the second.

You're looking for a marketing director who can hit a $40 M revenue target, build a brand in a crowded segment, and lead a team of nine. At Pact Apparel, I owned the rebrand that took us from $18 M to $52 M ARR in 30 months, driven by a content engine producing 3 long-form films and 26 short-form pieces per quarter. At Allbirds North America before that, I led the launch of three product lines representing 22% of company revenue in their first year. And I have managed teams of seven to fourteen — currently nine direct reports, with a 100% retention rate over the last two years.

Beyond the numbers, what convinces me about Verdant is the conviction to lead with proof rather than promise. I built my last team on the same principle — every claim we made externally had to be sourceable internally — and I would want to bring that discipline to Verdant's North American chapter. I also know this market intimately, including the press and creators who matter for this segment, and would expect to make introductions productive in the first quarter.

I would love to discuss how I could lead the North American chapter through 2026 and beyond. I am available for a call most afternoons ET and would welcome a coffee in NYC if your team is back in office.

Sincerely,

Jordan Okafor
```

---

## Style & Tone Guidelines

- **Voice**: confident, specific, and warm. The candidate is making an argument, not a request. The default is first-person ("I"), past tense for accomplishments, present tense for the current role, future conditional for the offer ("I would bring", "I would welcome").
- **Tone register**: matches the company. A bank or law firm wants formal English; an early-stage YC startup wants direct, almost-conversational prose. French *always* defaults to *vous* and formal *formule de politesse* on first contact — no exceptions, even for a Paris startup.
- **Specificity over enthusiasm**: "I would love to work here" is worthless; "I have followed your team's work on X since the Y announcement" is currency.
- **Mirror language from the JD** where truthful — recruiters skim for these terms.
- **No CV repetition**: do not list every role; pick the three most-relevant accomplishments and elaborate.
- **No clichés**: "team player", "passionate", "results-driven", "go-getter", "synergy", "value-add" without proof. Replace each with a one-sentence example.
- **Length**: 250–400 words, one page. A cover letter > 1 page is rarely finished by the reader.
- **White space**: paragraphs of 2–5 sentences. A wall of text loses the reader.
- **Spelling**: spell the company name correctly. Triple-check the hiring manager's name and gendered honorifics. One typo here is fatal.

---

## Quality Checklist

- [ ] One page, 250–400 words, four to five paragraphs with white space
- [ ] Recipient block names a real person, role, and company; address optional but accurate if present
- [ ] Salutation is named ("Dear Ms. Lastname," / "Madame Lastname,") whenever possible
- [ ] French letters carry an *Objet* line referencing the role and the JD reference if any
- [ ] Opening sentence is a specific signal, not "I am writing to apply for"
- [ ] Three quantified accomplishments are mapped to three explicit JD requirements
- [ ] Fit narrative names a concrete reason — stage, problem, mission, leader — with evidence of company knowledge
- [ ] Call to action is one clear sentence with availability
- [ ] Sign-off matches the register (formal English vs. French *formule de politesse*)
- [ ] French *formule de politesse* uses the same salutation form ("Madame, Monsieur") as the opening
- [ ] Spelling of company, product, and hiring-manager names is verified
- [ ] Tone matches the company culture (corporate vs. startup vs. agency)
- [ ] No reuse of CV bullets verbatim; the letter expands them
- [ ] No banned clichés ("passionate", "team player", "results-driven" without proof)
- [ ] File saved as `Lastname_Firstname_CoverLetter_Company.pdf`

---

## Common Mistakes

- **Generic "Dear Hiring Manager" when a name is two clicks away.** LinkedIn + company "About" usually surface the hiring manager in 5 minutes.
- **Restating the CV.** The letter must add context the CV cannot: motivation, fit, narrative. Repeating bullets wastes the page.
- **Burying the lede.** A weak first sentence ("I am writing to express my interest…") loses the reader before paragraph two.
- **Generic enthusiasm with no proof.** "I am passionate about your mission" is meaningless without one sentence demonstrating it.
- **Listing five accomplishments instead of three.** Reads as desperate; pick the strongest three and elaborate.
- **Ignoring the company.** A letter that could be sent to ten different employers will be — and the recruiter will know.
- **Wrong honorific or misspelled name.** Treated as disqualifying at most firms. Verify on LinkedIn.
- **Casual sign-off in a formal context.** "Cheers" to a French bank is a category error. Match register.
- **Over-formal *formule de politesse* in casual English.** "Veuillez agréer…" translated literally to English ("Please accept the assurance of my distinguished consideration") sounds ridiculous; use "Sincerely," instead.
- **French letter without *Objet*.** Reads as draft, not a real letter.
- **French *tu* on first contact.** Always *vous*, even at a hip Parisian startup, unless the recruiter has explicitly switched first.
- **Two pages.** Cut. The recruiter will not read past page one.
- **Imperatives on the recruiter.** "Call me at your convenience" sounds entitled — phrase as availability, not as command.
- **PS at the bottom mimicking marketing copy.** Distracting; cut.
- **No matching CV.** A great letter without an attached CV (or with a mismatched CV) signals carelessness.
