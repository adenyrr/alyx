---
name: cv-resume
description: Apply this methodology when the user asks the writer agent to draft, rewrite, audit, or modernize a curriculum vitae, resume, CV, "mon CV", professional bio for hiring, or LinkedIn-style profile summary intended for a job application. Trigger keywords include "resume", "CV", "curriculum vitae", "lebenslauf", "career history", "ATS optimization", "tailor my CV", "rewrite my resume for X role". Use this skill for documents whose primary purpose is to win an interview. Do NOT use it for cover letters (skills/cover-letter.md), professional emails (skills/email-pro.md), or biographical prose for marketing/press (skills/press-release.md or skills/blog-post.md). Do NOT use it for academic publication lists or grant biosketches, which follow discipline-specific formats (NIH, ERC, NSF) not covered here.
agents: [writer]
---

# CV / Resume — Short-Form Career Document Methodology

A resume or CV is the single most-screened document in a candidate's career. It must communicate value in under thirty seconds to a human recruiter and survive parsing by an Applicant Tracking System (ATS) before a human ever sees it. This skill teaches the writer agent how to compose, structure, and adapt a CV across formats, career stages, and national conventions.

---

## When to Apply

Apply this skill when the user request implies one of the following:

- Drafting a CV from scratch given a list of jobs, education, and skills
- Rewriting an existing CV for a different role, sector, or seniority level
- Auditing a CV for ATS compatibility, weak verbs, missing metrics, or formatting issues
- Translating or localizing a CV between US, UK, EU, and French conventions
- Producing parallel English + French versions for a bilingual market
- Condensing a long-form CV into a one-page resume or expanding a resume into a multi-page CV

Do NOT apply this skill for:

- Cover letters or motivation letters — delegate to `skills/cover-letter.md`
- Cold outreach or networking emails — delegate to `skills/email-pro.md`
- Academic biosketches (NIH 5-page format, ERC PI profile) — these require domain conventions not covered here
- LinkedIn full-profile writing (about section, headline, featured) — adapt the resume content but the platform has different micro-rules
- Portfolio narratives or case studies for designers/PMs — these belong in a portfolio site, not a CV

---

## Document Structure

### Format families

A CV/resume can be assembled in three structural families. Pick one and commit; hybrids work only when intentional.

| Format | What it is | When to pick it | When to avoid it |
|---|---|---|---|
| **Chronological** (reverse-chrono) | Jobs listed newest-first; education at bottom (or top for students). The default. | Linear career, steady progression, recognizable employers, no large gaps. ATS-safe. | Large unexplained gaps, frequent short stints, or a deliberate pivot. |
| **Functional** (skills-based) | Skills grouped by theme; jobs reduced to a short list at the end. | Career changers, returners after long absence, military-to-civilian transition. | Mid-to-senior corporate roles; recruiters distrust it because it hides timelines. ATS often mis-parses. |
| **Hybrid** (combined) | A skills/summary block on top, then a full reverse-chronological history below. | Senior ICs, consultants, portfolio careers, anyone with multiple specialties. | Junior candidates with little to summarize. |

**Default recommendation:** chronological for ≤ 7 years experience, hybrid for ≥ 7 years or any pivot, functional only as a last resort and only outside ATS-driven funnels.

### Canonical section list

Pick from this menu, in this order, omitting what does not apply:

1. **Header** — name, role title, location, phone, email, LinkedIn, portfolio/GitHub. No photo (US/UK/IE/CA/AU). Photo permitted in FR/DE/ES/IT/JP — see country variants.
2. **Professional summary** (3–4 lines, hybrid/senior only) or **Objective** (1 line, students only). Mid-career: skip both unless pivoting.
3. **Core competencies / key skills** (6–12 keywords, ATS bait).
4. **Professional experience** — bullets per role.
5. **Education** — top of CV for students, bottom for everyone else.
6. **Certifications & licenses** (if material to the role).
7. **Selected projects** (optional; for engineers, designers, researchers).
8. **Publications / talks / patents** (optional; academic, research, technical roles).
9. **Languages** with CEFR levels (A1–C2) — always for FR/EU; often for US.
10. **Volunteering / community** (optional; juniors should include, executives can omit).
11. **References** — see conventions below.

---

## Section-by-Section Writing Guide

### Header

- **Name** in the largest font on the page (14–18 pt).
- Below the name, a **role descriptor** matching the job target ("Senior Data Engineer", "Product Manager, Fintech"). Not "Seeking opportunities".
- City + Country only; full street address is obsolete and a privacy risk.
- One phone, one email (firstname.lastname@domain, never `partypanda93@`), one LinkedIn vanity URL, one portfolio/GitHub if relevant.
- **No photo** for US/UK/IE/CA/AU/NZ applications (anti-bias norm). Photo expected for FR/DE/BE/ES/IT/JP/CN — neutral headshot, plain background.

### Professional summary (when used)

Three to four lines, written in third person *implied* (no "I"). Pattern:

> [Seniority + role] with [N years] in [domain]. Specialized in [2–3 specialties]. Delivered [signature outcome with metric]. Seeking [target role] focused on [value add].

Example: "Senior Backend Engineer with 9 years in payments infrastructure. Specialized in Go services, Kafka, and PCI-DSS environments. Reduced payment failure rate from 1.8% to 0.4% on a 12 M-transactions-per-day platform. Seeking a staff role to scale event-driven systems at a fintech with global ambitions."

### Core competencies / key skills

A 2- or 3-column block of comma-separated or pipe-separated keywords. Mirror the wording of the target job description verbatim where truthful (ATS keyword matching is literal). Group by family:

- **Languages**: Python, Go, TypeScript, SQL
- **Frameworks**: FastAPI, Django, Next.js
- **Platforms**: AWS (EKS, Lambda, RDS), GCP (BigQuery), Kubernetes
- **Methods**: TDD, DDD, Event Sourcing, OKRs

Do not pad with soft skills ("hardworking", "team player") — they fail ATS scoring and look juvenile.

### Professional experience — the bullets

Every line under a role is a STAR bullet, compressed:

> **[Action verb in past tense]** [object] [context], [result with metric].

The **STAR** mental scaffold:

- **S**ituation — the context, in a fragment.
- **T**ask — what you owned (often merged with S).
- **A**ction — what you actually did (the verb + object).
- **R**esult — the measurable outcome (% / $ / time / scale).

Compress STAR into a single line; the full S-T-A-R is the *thinking*, not the *writing*.

Compare:

- Weak: "Was responsible for the migration of the database."
- OK: "Migrated database to PostgreSQL."
- STAR: "Led 4-engineer migration of 2 TB transactional database from MySQL to PostgreSQL 14 in 9 weeks, cutting p95 query latency from 480 ms to 90 ms with zero downtime."

Rules for bullets:

- **Start with a verb in past tense** (past simple). Present tense only for the current job.
- **One bullet = one accomplishment.** No "and"-stacking three things.
- **Quantify whenever honest.** Money, percentage, time, count, scale, multiple, rank.
- **3–6 bullets per role**, weighted toward the most recent and most relevant role.
- **Reverse-pyramid the role**: heaviest, most-recent, highest-impact bullet first.
- **Cut implied verbs** ("Responsible for", "Worked on", "Helped with") — these dilute every line.

### Action-verb library

Pick verbs that *demonstrate* the work. Avoid the overused trio "managed / handled / worked on". A working palette:

| Family | Verbs |
|---|---|
| **Leadership** | Led, Directed, Headed, Spearheaded, Chaired, Mentored, Coached, Hired, Onboarded, Championed |
| **Build / create** | Built, Designed, Architected, Engineered, Developed, Prototyped, Launched, Shipped, Released, Productionized |
| **Improve / optimize** | Reduced, Cut, Accelerated, Streamlined, Refactored, Hardened, Stabilized, Automated, Consolidated, Migrated |
| **Grow** | Grew, Scaled, Expanded, Doubled, Tripled, 10x'd, Drove (growth) |
| **Analyze / decide** | Analyzed, Modeled, Forecasted, Benchmarked, Diagnosed, Audited, Investigated |
| **Influence** | Negotiated, Persuaded, Aligned, Secured (buy-in), Briefed, Presented, Authored |
| **Save / protect** | Saved, Recovered, Prevented, Mitigated, Eliminated, Avoided |
| **Teach / share** | Taught, Trained, Documented, Open-sourced, Published, Spoke (at) |

Avoid: "responsible for", "involved in", "assisted with", "duties included", "worked on", "helped".

### Education

For each entry: degree, institution, city, graduation year (or "expected YYYY"). Add GPA only if ≥ 3.5/4.0 and within 5 years of graduation, or top-quartile rank for French *grandes écoles*. List honours (cum laude, mention bien), thesis title if research-relevant, relevant coursework only for students.

### Certifications, languages, projects

- **Certifications**: name, issuing body, year, optional credential ID. Drop after 5 years unless still valid.
- **Languages**: always with CEFR level — "French (C2, native)", "Spanish (B2, professional)", "German (A2, conversational)". US norm: native / fluent / professional / conversational / basic.
- **Selected projects**: name, one-line description, tech, link, outcome. 2–4 max.

### References

- **US / UK / FR (most sectors)**: omit. Recruiters assume you have them; do not write "References available upon request" — it wastes a line.
- **Academic / public sector / some EU**: list 2–3 named referees with title, email, and consent obtained beforehand.
- Never list a reference who has not agreed in writing.

---

## Country & Format Variants

### US resume (1 page, ATS-first)

- **One page** for ≤ 10 years; two pages acceptable for senior IC / management; never three.
- No photo, no date of birth, no marital status, no nationality, no headshot.
- Reverse-chronological dominant; functional discouraged.
- ATS-friendly: single column, no text boxes, no headers/footers with critical data, standard fonts (Arial, Calibri, Helvetica, Garamond), bullets as `•` or `-`, 10–12 pt body.
- File format: PDF unless the portal specifies `.docx`.

### UK CV (1–2 pages)

- Called "CV" but follows resume rules: 1–2 pages, reverse-chrono, no photo.
- Includes a 3–4 line **personal statement** at the top.
- Right to work statement at the bottom for non-UK candidates: "Right to work in the UK: Skilled Worker visa, valid until YYYY-MM."

### European multi-page CV (Europass-influenced)

- 2–4 pages acceptable; up to 6 for academics.
- Photo expected in DE, FR, ES, IT, BE, AT, CH; optional in NL, NORDICS.
- DOB, nationality, and sometimes marital status are still common in DE/AT (declining trend).
- The Europass template is *available* but seen as junior — prefer a clean custom layout.

### French CV ("Curriculum Vitae" header)

- **Header literally reads `Curriculum Vitae`** centered or top-left, then name below in larger type.
- 1 page for ≤ 5 years experience, 2 pages otherwise. Going to 3 pages signals lack of synthesis (a French cardinal sin).
- Photo expected (top-right, professional, neutral background).
- Sections in French: *Profil* / *Expériences professionnelles* / *Formation* / *Compétences* / *Langues* / *Centres d'intérêt*.
- "Centres d'intérêt" (hobbies) is *expected*, not optional — 1 short line, specific not generic ("trail running semi-marathon, photographie argentique").
- Dates in DD/MM/YYYY or "mois AAAA" ("janvier 2022 — présent").
- Use *vous* nowhere — the CV is third-person/implied-subject.
- Diplomas: state the full French name (Master 2, Diplôme d'Ingénieur, BUT, BTS, Licence) and the *école* — the *grande école* name matters.
- *Mentions* (bien, très bien) are listed if obtained.

### German Lebenslauf

- Tabular two-column layout still common.
- Photo top-right, DOB, place of birth, nationality, marital status historically expected (declining).
- Signed and dated at the bottom (handwritten signature image acceptable for PDF).

---

## ATS Optimization Rules (non-negotiable)

ATS = Applicant Tracking System. The CV is parsed into structured fields before a human reads it. Misparsing = silent rejection.

1. **Single column.** Multi-column layouts cause field-mixing in 30–60% of parsers. Use one column even if it looks plain.
2. **No tables, no text boxes, no images, no icons** for critical content (name, contact, headers). Decorative-only icons may pass but offer zero ATS benefit.
3. **Standard section headers**: "Experience", "Education", "Skills", "Certifications". Cute headers ("Where I've Been", "Knowledge Stack") break parsers.
4. **Standard fonts**: Arial, Calibri, Helvetica, Garamond, Times New Roman, Cambria, Lato. 10–12 pt body, 14–18 pt name.
5. **Standard bullets**: `•`, `-`, `–`. Avoid emoji, wingdings, custom glyphs.
6. **No headers/footers** for name or contact — many parsers ignore these regions.
7. **Dates in a consistent format**: "Jan 2021 – Mar 2024" or "01/2021 – 03/2024". Never "winter '21".
8. **File format**: PDF (text-selectable, not image-scanned). `.docx` only when the portal explicitly demands it. Never `.pages`, `.odt`, scanned PDF.
9. **Filename**: `Lastname_Firstname_Resume_RoleName.pdf` — recruiters search disk.
10. **Keyword density**: each must-have keyword from the JD appears 1–3 times across summary, skills, and experience. Don't stuff (≥ 4 times triggers spam heuristics in some ATS).
11. **Spell out + abbreviate** acronyms once: "Continuous Integration / Continuous Deployment (CI/CD)".
12. **No hyperlinks as the only carrier of information** — write the URL or label it: "github.com/username".

---

## Output Templates

### Template 1 — Junior (≤ 3 years, student or new grad, US 1-page)

```markdown
# {{Firstname Lastname}}
**{{Target role, e.g., Junior Data Analyst}}** — {{City, Country}}
{{phone}} | {{email}} | linkedin.com/in/{{handle}} | github.com/{{handle}}

## Education
**{{Degree, e.g., M.Sc. Computer Science}}**, {{University}}, {{City}} — {{Graduation MM/YYYY}}
GPA: {{X.X/4.0 if ≥ 3.5}} | Honors: {{cum laude / mention bien / Dean's List}}
Relevant coursework: {{Course 1}}, {{Course 2}}, {{Course 3}}, {{Course 4}}
Thesis: "{{Thesis title}}" — supervised by {{Prof. Name}}.

## Technical Skills
**Languages**: {{Python, SQL, JavaScript}}
**Frameworks**: {{pandas, scikit-learn, FastAPI}}
**Tools**: {{Git, Docker, Airflow, PostgreSQL, Tableau}}

## Experience
**Data Analyst Intern**, {{Company}}, {{City}} — {{MMM YYYY – MMM YYYY}}
- Built a Tableau dashboard tracking 12 KPIs for the marketing team, adopted by 18 stakeholders and replacing three legacy Excel reports.
- Wrote a Python ETL moving daily ad-spend data from 4 sources into Snowflake, cutting weekly reporting time from 6 hours to 25 minutes.
- Identified a tagging error costing $14 k/month in mis-attributed conversions; documented the fix and trained two colleagues on the corrected pipeline.

**Teaching Assistant — Introduction to Statistics**, {{University}} — {{MMM YYYY – MMM YYYY}}
- Led weekly tutorials of 22 students; designed 6 practice problem sets adopted by the course the following year.
- Held office hours averaging 8 students/week; raised mean midterm score by 7 points versus prior cohort.

## Projects
- **{{Project name}}** ({{tech stack}}) — {{one-line description and outcome}}. Code: github.com/{{handle}}/{{repo}}.
- **{{Project name}}** ({{tech stack}}) — {{one-line description and outcome}}. Code: github.com/{{handle}}/{{repo}}.

## Languages
English (C2, native) | French (B2, professional) | Spanish (A2, conversational)

## Volunteering
**Mentor**, {{Org}} — {{YYYY – present}}. Coach two first-year CS students weekly on programming fundamentals.
```

### Template 2 — Mid-career (4–9 years, hybrid format)

```markdown
# {{Firstname Lastname}}
**{{Senior Backend Engineer}}** — {{City, Country}}
{{phone}} | {{email}} | linkedin.com/in/{{handle}} | github.com/{{handle}}

## Summary
Backend engineer with 7 years building distributed systems in fintech and ad-tech. Specialized in Go, event-driven architectures, and PostgreSQL at scale. Shipped systems handling 4 B events/day at 99.98% availability. Looking for a staff role on a payments or risk platform.

## Core Skills
Go, Python, SQL | PostgreSQL, Kafka, Redis | AWS (EKS, RDS, Lambda) | gRPC, REST, GraphQL | OpenTelemetry, Prometheus, Grafana | Event Sourcing, CQRS, DDD

## Experience

**Senior Backend Engineer**, {{Company}}, {{City}} — {{MMM YYYY – present}}
- Architected a Go-based settlement service replacing a legacy PHP monolith, processing $1.4 B/month with 99.99% availability and a 38% infra cost cut.
- Led a 5-engineer team migrating 14 services to gRPC + Protobuf; cut average inter-service latency from 180 ms to 35 ms and reduced bandwidth spend by 22%.
- Designed an idempotency layer on Kafka consumers, eliminating duplicate payouts (~$80 k/month previously refunded as goodwill).
- Mentored two mid-level engineers, both promoted within 14 months.

**Backend Engineer**, {{Previous Company}}, {{City}} — {{MMM YYYY – MMM YYYY}}
- Built the company's first event-sourcing module on EventStoreDB, enabling full audit reconstruction for SOC 2 Type II certification (passed first audit, zero findings on engineering controls).
- Reduced p99 checkout latency from 1.3 s to 280 ms by replacing N+1 ORM queries with a single read-model materialization.
- Open-sourced the team's internal Go middleware library ({{repo name}}); 1.2 k GitHub stars, adopted by 3 other teams internally.

**Junior Backend Engineer**, {{First Company}}, {{City}} — {{MMM YYYY – MMM YYYY}}
- Shipped 11 features across the public REST API in 18 months, including a webhooks system used by 240+ external integrators.
- Cut nightly batch job runtime from 4 h 20 min to 38 min through query plan analysis and partitioning.

## Education
**Diplôme d'Ingénieur en Informatique**, {{École}}, {{City}} — {{YYYY}}. Mention bien.
**B.Sc. Mathematics**, {{University}}, {{City}} — {{YYYY}}.

## Certifications
- AWS Certified Solutions Architect — Associate ({{YYYY}})
- CKAD — Certified Kubernetes Application Developer ({{YYYY}})

## Languages
French (C2, native) | English (C1, professional) | German (B1, intermediate)
```

### Template 3 — Senior / Executive (10+ years, hybrid, 2 pages)

```markdown
# {{Firstname Lastname}}
**{{Director of Engineering / VP Product / Head of Data}}** — {{City, Country}}
{{phone}} | {{email}} | linkedin.com/in/{{handle}}

## Executive Summary
{{Functional title}} with 14 years scaling engineering organizations from 6 to 80+ across SaaS, fintech, and marketplaces. Track record of shipping platform rewrites without downtime, raising engineer NPS from 18 to 64, and cutting hosting spend by 40%+ at each tenure. Seeking a VP Engineering role at a Series C–D B2B SaaS scaling from $20 M to $100 M ARR.

## Selected Outcomes
- Scaled engineering org from 12 to 64 across three years at {{Company}}; 92% retention.
- Led the platform rewrite ({{tech stack}}) that took the product from 2.5 s to 380 ms p95; NPS +22, churn –6 pp.
- Closed 3 enterprise security certifications (SOC 2 II, ISO 27001, HIPAA) on time and on budget.

## Experience

**Director of Engineering**, {{Company}}, {{City}} — {{MMM YYYY – present}}
- Re-organized 4 squads of 48 engineers around platform/product boundaries; deployment frequency went from 1/week to 14/day, change-failure rate from 22% to 4%.
- Led a $4.2 M hosting consolidation from multi-cloud to AWS+CDN; saved $1.6 M/yr while cutting p95 latency 31%.
- Hired and onboarded 28 engineers in 18 months; raised eng-NPS from 31 to 68 (semiannual survey).
- Owned roadmap and budget ($11 M/yr); presented quarterly to board.

**Head of Platform**, {{Previous Company}}, {{City}} — {{MMM YYYY – MMM YYYY}}
- Built the platform team from scratch (0 → 14 engineers in 22 months) and shipped the company's internal developer platform, cutting time-to-first-deploy from 11 days to 90 minutes for new services.
- Drove the move to Kubernetes across 42 services with zero customer-visible downtime over a 9-month migration.
- Reduced security incidents by 71% YoY via automated dependency scanning, secrets rotation, and a quarterly chaos-engineering programme.

**Engineering Manager → Senior EM**, {{Company}}, {{City}} — {{MMM YYYY – MMM YYYY}}
- Managed two squads (16 engineers) building the checkout and pricing systems; checkout conversion +4.1 pp YoY (≈ $9 M ARR).
- Designed the engineering ladder (IC1–IC7, M1–M4) still in use at the company.
- Promoted four engineers to senior and two to staff in two years.

**Staff Engineer**, {{Earlier Company}}, {{City}} — {{MMM YYYY – MMM YYYY}}
- Designed the event-streaming backbone (Kafka, 22 topics, 800 M events/day) replacing 14 cron-based jobs.
- Authored the company's incident-management runbook; MTTR dropped 58% in the first year of adoption.

## Earlier Experience
**Senior Software Engineer**, {{Company}} ({{YYYY – YYYY}}) — Led migration to microservices.
**Software Engineer**, {{First Company}} ({{YYYY – YYYY}}) — Full-stack development on the flagship product.

## Education
**M.Sc. Computer Science**, {{University}}, {{City}} — {{YYYY}}.
**B.Sc. Engineering**, {{University}}, {{City}} — {{YYYY}}.

## Selected Talks & Publications
- "{{Talk title}}", {{Conference}} ({{YYYY}}) — {{audience size}} attendees.
- "{{Article title}}", {{Publication}} ({{YYYY}}).

## Languages
English (C2) | French (C2, native) | German (B2)

## Board & Advisory
- Technical Advisor, {{Startup}} ({{YYYY – present}}).
```

---

## Style & Tone Guidelines

- **Voice**: third-person implied. Never "I" in bullets ("I led" → "Led"). Never "we" — claim only what you owned.
- **Tense**: past simple for prior roles, present simple for the current role only. Be consistent inside each role.
- **Density**: every line must earn its place. If a line could appear on any other engineer's CV, cut or sharpen it.
- **Numbers**: use digits for all quantities (not "five", write "5"). Prefer round-but-honest figures over false precision ("≈$1.2 M" beats "$1,193,448.27").
- **Adjectives**: ration them. "Excellent communicator" is junk; "Briefed C-suite quarterly on roadmap and risks" demonstrates it.
- **Capitalisation**: Title Case for headings, sentence case for bullets, exact brand casing for tools (PostgreSQL, JavaScript, GitHub).
- **Length discipline**: a bullet > 2 lines on screen is a paragraph in disguise — split or compress.
- **Honesty**: never inflate titles, never overlap dates to hide gaps, never claim certifications not held. Background checks catch these.

---

## Quality Checklist

- [ ] Format family (chrono / functional / hybrid) is appropriate to career stage and target sector
- [ ] Header has name, role title, city, email, phone, LinkedIn — and a photo only where culturally expected
- [ ] No two-column layout, text boxes, images, or headers/footers carrying critical data
- [ ] Standard ATS-friendly fonts and bullet glyphs
- [ ] Every bullet starts with a strong past-tense action verb (none from the banned list)
- [ ] Every role has at least one bullet with a quantified result
- [ ] Most-recent / most-relevant role has the longest bullet list (3–6); older roles are compressed
- [ ] No bullet exceeds 2 lines on screen
- [ ] Keywords from the target job description appear 1–3 times across summary, skills, and experience
- [ ] Dates are consistent format and reconcile (no overlaps, no unexplained gaps > 3 months)
- [ ] Languages have CEFR levels
- [ ] Education has degree, institution, city, year; GPA/honors only if recent and high
- [ ] References section omitted unless sector requires it
- [ ] File saved as `Lastname_Firstname_Resume_Role.pdf`, text-selectable
- [ ] Length: 1 page (junior US), 2 pages (mid-senior), max 4 pages (academic/exec EU)
- [ ] French version, if any, has `Curriculum Vitae` header, photo, *Centres d'intérêt*, DD/MM/YYYY dates

---

## Common Mistakes

- **Listing duties, not achievements.** "Responsible for managing the team" tells nothing. "Managed a 6-engineer team that shipped X with Y result" tells everything.
- **No metrics.** A CV without numbers reads as opinion. Even soft outcomes can be quantified (people impacted, decisions influenced, frequency).
- **Verbose summary.** A 10-line "About me" paragraph is read by no one. 3–4 lines maximum.
- **Burying recent wins.** Recency bias is real; the top half of the page sells the candidate. Put the strongest current-role bullets first.
- **One CV for every job.** A generic CV passes no ATS and impresses no recruiter. Tailor the summary, skills, and top bullets per application.
- **Photo on a US/UK resume.** Triggers anti-bias screening; some firms shred the file unread.
- **No photo on a French CV.** Reads as carelessness or hiding something to French recruiters.
- **Cute headers.** "My Journey", "Tech Toolbox" — ATS parsers do not recognize these; use plain "Experience", "Skills".
- **Two-column "designer" layouts.** Beautiful in Figma, broken in Greenhouse/Workday.
- **Mismatched title.** The role descriptor under the name must match the target job title, not the last job title.
- **Acronyms without context.** "Led the BCDR for the EMEA TPS" — spell out at least once.
- **Listing every project ever.** Curate to 2–4 best, relevant to the target role.
- **References block.** "References available upon request" is a 1990s tic; delete it.
- **Inflated language.** "Synergized cross-functional stakeholders to optimize deliverable velocity" → "Worked with product and design to ship features 30% faster."
- **Forgetting the file name.** "Resume_v7_FINAL_final.pdf" lands badly on a recruiter's desktop.
