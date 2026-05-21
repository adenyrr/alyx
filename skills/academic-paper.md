---
name: academic-paper
description: Apply this methodology when the user asks the writer agent to produce a peer-reviewable scientific paper in the IMRaD (Introduction, Methods, Results, and Discussion) structure used by biomedical, life-science, social-science, and most STEM journals. Trigger keywords include "rédige un article scientifique", "scientific paper", "research paper", "manuscript", "IMRaD", "journal article", "compose a paper for publication", "draft a manuscript". This skill complements `prisma.md` (used when the paper is a systematic review) and `grade.md` (used when rating certainty of evidence in clinical syntheses). Do NOT use for business reports (use business-report.md), engineering RFCs (use technical-rfc.md), opinion pieces, editorials, narrative reviews, or undergraduate-style essays without primary data or systematic methodology.
agents: [writer]
---

# Academic Paper — IMRaD Scientific Manuscript Methodology

The IMRaD structure (Introduction, Methods, Results, and Discussion) has been the dominant template for empirical scientific papers since the mid-20th century and is endorsed by ICMJE, COPE, and the EQUATOR Network. It enforces a contract with the reader: every claim is traceable to a method, every method to a result, and every result to a discussion of meaning and limits. This skill codifies a publication-ready manuscript at journal-submission depth.

For systematic reviews and meta-analyses, layer this skill on top of `skills/prisma.md` (reporting structure) and `skills/grade.md` (certainty of evidence). For randomized trials, layer on CONSORT; for observational studies, STROBE; for diagnostic accuracy, STARD; for qualitative, SRQR or COREQ.

---

## When to Apply

Apply this methodology when the manuscript is:

- An original research article reporting primary empirical data
- A systematic review or meta-analysis (in combination with `prisma.md` and `grade.md`)
- A methodology paper introducing a new technique, instrument, or model
- A registered report or pre-registered study
- A clinical trial report (in combination with CONSORT)
- A cohort, case-control, or cross-sectional study (in combination with STROBE)
- A qualitative study reported in IMRaD-compatible form

Do NOT apply this methodology for:

- A narrative or non-systematic literature review
- A commentary, editorial, perspective, or opinion piece
- A book chapter or textbook section
- A grant proposal (different structure: Specific Aims, Significance, Innovation, Approach)
- An undergraduate essay without primary or secondary data
- A thesis or dissertation in monograph form (chapter structure differs)
- A conference abstract on its own (use the journal's structured-abstract template)

---

## Document Structure

The manuscript is composed of twelve blocks in fixed IMRaD-compliant order.

1. **Title** — a single declarative sentence describing the study.
2. **Abstract** — 250 words, structured (Background, Methods, Results, Conclusion).
3. **Keywords** — 4–8 indexing terms, preferably MeSH where applicable.
4. **Introduction** — a funnel from broad context to the specific aim.
5. **Methods** — what was done, in enough detail for replication.
6. **Results** — what was found, presented without interpretation.
7. **Discussion** — what the findings mean, in conversation with prior literature.
8. **Conclusion** — a short statement of the take-home message.
9. **Acknowledgements** — non-authorial contributions.
10. **Funding** — sources and roles of funders.
11. **Conflict of interest** — financial and non-financial competing interests.
12. **References** — full bibliography in the target journal's style.

Some journals add: Data availability statement, Author contributions (CRediT taxonomy), Ethics approval statement, Supplementary materials. Include these whenever the target venue requires them.

---

## Section-by-Section Writing Guide

### 1. Title

Purpose: communicate what was studied, in whom, and (where applicable) the design.

Conventions: declarative, no abbreviations except universal ones (DNA, HIV), no marketing verbs ("novel", "innovative", "groundbreaking" are banned by most journals), 10–20 words.

Two acceptable patterns:
- Descriptive: "Prevalence of antimicrobial resistance in *Klebsiella pneumoniae* isolates from a tertiary care hospital, 2019–2023".
- Hypothesis-stating: "Empagliflozin reduces 12-month hospitalization in heart-failure patients with preserved ejection fraction: a multicenter randomized trial".

For systematic reviews, end with ": a systematic review" or ": a systematic review and meta-analysis".

### 2. Abstract

Purpose: stand alone as the published summary indexed by PubMed and search engines.

Structure (250 words, ±10%):
- **Background** (40–60 words): the gap and the rationale.
- **Methods** (60–90 words): design, setting, participants, intervention or exposure, outcomes, analysis.
- **Results** (70–100 words): numerical findings with effect sizes and confidence intervals.
- **Conclusion** (20–40 words): the take-home message, calibrated to the evidence.

Avoid: abbreviations on first use without definition, citations, claims unsupported by the body, marketing language.

### 3. Keywords

Purpose: indexing for discoverability.

Conventions: 4–8 terms; for biomedical papers, prefer MeSH terms; complement free text only where MeSH lacks coverage. Avoid duplicating exact title words.

### 4. Introduction

Purpose: justify the study by funnelling from broad context to the specific question.

The four paragraphs (in order):
- **Broad context** (½ page): the field-level problem, its scale and significance, the current paradigm.
- **What is known** (½ page): a concise synthesis of relevant prior work with citations.
- **The gap** (¼ page): what is unknown, unresolved, or contested; phrased as a specific limitation of existing evidence.
- **The aim and contribution** (¼ page): the precise objective of the present study (hypothesis or research question) and what this paper adds.

Length: 600–900 words. Cite 15–40 sources.

What does NOT belong: a history of the field, a textbook explanation, methods, or results.

### 5. Methods

Purpose: provide enough detail that an independent researcher could repeat the study.

Subsections (in this order):
- **Study design**: type (RCT, cohort, case-control, cross-sectional, qualitative, in vitro, in silico), pre-registration ID if any (ClinicalTrials.gov, ISRCTN, OSF), adherence to a reporting guideline (CONSORT, STROBE, SRQR, ARRIVE).
- **Participants / specimens / dataset**: inclusion and exclusion criteria, recruitment period, setting, sample size with justification (power calculation or saturation argument).
- **Intervention / exposure**: what was given or measured, by whom, when, how, dose, duration. For software, version numbers and configuration. For instruments, manufacturer, model, lot.
- **Outcomes**: primary and secondary, with operational definitions and timing.
- **Analysis**: statistical or analytical approach, software (named with version), handling of missing data, sensitivity analyses, threshold for significance.
- **Ethics**: IRB or ethics committee name and approval number, informed consent process, data protection regime (GDPR, HIPAA), Helsinki Declaration adherence for human research, ARRIVE for animal research.

Length: 800–1500 words. Use past tense throughout.

### 6. Results

Purpose: present findings, in the order set up by the methods, without interpretation.

Structure: open with participant flow (a CONSORT or STROBE diagram if applicable), then baseline characteristics, then the primary outcome, then secondary outcomes, then sensitivity analyses.

Rules:
- Every numerical claim cites a table or figure.
- Effect sizes are reported with confidence intervals, not p-values alone.
- No interpretation, no comparison with prior work, no speculation. Save those for the Discussion.
- Tables and figures stand alone with self-contained captions; the body text highlights the key result, it does not repeat the table.

Length: 600–1500 words plus tables and figures.

### 7. Discussion

Purpose: interpret findings honestly and place them in the wider evidence base.

Six-paragraph structure (in this order):
- **Key findings**: one paragraph restating the principal result in plain language.
- **Mechanism or explanation**: one paragraph offering the most plausible biological, social, or technical mechanism.
- **Comparison with prior literature**: where the result agrees, where it disagrees, and the most credible explanations for disagreement.
- **Strengths and limitations**: honest disclosure of design strengths (e.g., randomization, large sample, blinded outcome assessment) and limitations (selection bias, attrition, confounding, generalizability, statistical power, measurement error).
- **Implications**: for practice, policy, and the field.
- **Future research**: specific, falsifiable next steps; not a wish list.

Length: 1000–1800 words. Use present tense for interpretation, past tense when referring to the study itself.

What does NOT belong: new results, repetition of methods, over-claiming. The discussion must be calibrated to the evidence; phrases like "this proves" are inappropriate for any single study.

### 8. Conclusion

Purpose: deliver the take-home message in 2–4 sentences, calibrated to the evidence.

Avoid: introducing new ideas, citing new references, hedging into meaninglessness, or making policy demands the evidence cannot support.

### 9. Acknowledgements

Purpose: credit contributions that do not meet authorship criteria (ICMJE).

Examples: technical assistance, data collection support, language editing, contributions of patient or public involvement panels.

### 10. Funding

Purpose: disclose the financial provenance of the work and the role of the funder.

Use the format: "This work was supported by `<funder name>` under grant `<number>`. The funder had `<no role / specified role>` in the study design, data collection, analysis, interpretation, or the decision to publish."

### 11. Conflict of Interest

Purpose: disclose any financial or non-financial interest that could bias the work.

If none, state: "The authors declare no competing interests." If any exist, declare them explicitly with the entity, the relationship, and the dates.

### 12. References

Purpose: anchor every claim to a verifiable source.

Use the target journal's style (Vancouver for biomedical journals, APA 7 for psychology and social science, Harvard or Chicago for many others). Be ruthlessly consistent. Use a reference manager (Zotero, EndNote, Mendeley) to avoid format drift.

---

## Output Template

```markdown
# <Title — declarative, 10–20 words, no marketing verbs>

**Authors.** <Author 1>^1^, <Author 2>^2^, <Corresponding Author>^1,\*^

^1^ <Department, Institution, City, Country>
^2^ <Department, Institution, City, Country>
\* Corresponding author: <email>

---

## Abstract

**Background.** <40–60 words: gap and rationale.>

**Methods.** <60–90 words: design, setting, participants, intervention/exposure, outcomes, analysis.>

**Results.** <70–100 words: principal numerical findings with effect sizes and 95% CIs.>

**Conclusion.** <20–40 words: take-home message calibrated to the evidence.>

**Keywords.** <term 1>; <term 2>; <term 3>; <term 4>; <term 5>

**Registration.** <ClinicalTrials.gov / PROSPERO / OSF ID or "Not registered" with justification.>

---

## 1. Introduction

<Paragraph 1 — broad context: the field-level problem, its scale, the current paradigm. Cite landmark sources.>

<Paragraph 2 — what is known: synthesis of relevant prior work, cited.>

<Paragraph 3 — the gap: what is unknown, contested, or methodologically inadequate in prior work.>

<Paragraph 4 — the aim and contribution: the specific objective of the present study and what it adds.>

---

## 2. Methods

### 2.1 Study design
<Type of study, reporting-guideline adherence, registration ID.>

### 2.2 Participants / specimens / dataset
<Inclusion and exclusion criteria, recruitment period, setting, sample-size justification.>

### 2.3 Intervention / exposure
<What was given or measured, by whom, when, how. Specify doses, durations, instruments, software versions.>

### 2.4 Outcomes
- **Primary**: <operational definition, timing, measurement instrument>
- **Secondary**: <list with operational definitions>

### 2.5 Analysis
<Statistical or analytical methods. Named software with version. Missing-data handling. Sensitivity analyses. Significance threshold.>

### 2.6 Ethics
<IRB name and approval number. Consent procedure. Helsinki / ARRIVE / GDPR statements as applicable.>

---

## 3. Results

### 3.1 Participant flow
<Narrative + reference to flow diagram (Figure 1).>

### 3.2 Baseline characteristics
*Table 1. Baseline characteristics of the study population (n = <N>).*

| Characteristic | Group A (n=<n>) | Group B (n=<n>) | Total (n=<N>) |
|---|---|---|---|
| <Age, mean (SD), years> | <value> | <value> | <value> |
| <Sex, female, n (%)> | <value> | <value> | <value> |
| <Other> | <value> | <value> | <value> |

### 3.3 Primary outcome
<Narrative of the primary result with effect size and 95% CI, referencing Table 2 or Figure 2. No interpretation.>

### 3.4 Secondary outcomes
<Narrative, referencing tables/figures.>

### 3.5 Sensitivity and subgroup analyses
<Narrative.>

### 3.6 Adverse events / safety / data quality
<Where applicable.>

---

## 4. Discussion

### 4.1 Key findings
<One paragraph restating the principal result in plain language.>

### 4.2 Mechanism or explanation
<One paragraph offering the most plausible mechanism.>

### 4.3 Comparison with prior literature
<Where the result agrees with prior work, where it disagrees, and credible explanations for disagreement.>

### 4.4 Strengths and limitations
**Strengths.** <e.g., pre-registration, sample size, blinded outcome assessment, multi-site recruitment.>

**Limitations.** <e.g., selection bias, attrition, residual confounding, generalizability, measurement error, statistical power.>

### 4.5 Implications
<For clinical practice, policy, or the field.>

### 4.6 Future research
<Specific, falsifiable next steps.>

---

## 5. Conclusion

<2–4 sentences. Calibrated to the evidence. No new claims, no over-reach.>

---

## Acknowledgements

<Credit non-authorial contributions per ICMJE.>

## Funding

This work was supported by <funder> under grant <number>. The funder had <role / no role> in study design, data collection, analysis, interpretation, or the decision to publish.

## Conflict of Interest

<The authors declare no competing interests. / Author X reports <relationship> with <entity> during the conduct of the study.>

## Author contributions (CRediT)

| Author | Conceptualization | Methodology | Investigation | Analysis | Writing — original | Writing — review | Supervision |
|---|---|---|---|---|---|---|---|
| <Author 1> | X | X | X | X | X |  | X |
| <Author 2> |  | X | X | X |  | X |  |

## Data availability

<Statement: "Data are available from <repository> under accession <ID>." or "Data are available from the corresponding author on reasonable request, subject to ethical approval." or a justified restriction.>

## Ethics approval

<IRB name, country, approval number, date.>

---

## References

1. <Surname AB, Surname CD. Title. *Journal*. YYYY;vol(issue):pages. doi:10.xxxx/xxxx>
2. <Surname EF. *Book title*. Edition. City: Publisher; YYYY.>
3. <Author. Title. URL. Accessed YYYY-MM-DD.>

---

## Supplementary materials

- **S1**: <Detailed protocol>
- **S2**: <Statistical analysis plan>
- **S3**: <Additional tables and figures>
- **S4**: <Reporting checklist (CONSORT / STROBE / PRISMA / SRQR)>
```

---

## Style & Tone Guidelines

- **Voice**: third person, active where possible. "We measured" is acceptable in methods; "It was measured" is also acceptable. Be consistent within sections.
- **Tense**: past in Methods and Results ("we recruited", "the mean was"). Present in Introduction and Discussion when referring to established knowledge ("the gut microbiome regulates"). Past when referring to your own study in Discussion ("our study found").
- **Person**: first person plural ("we") is acceptable in most modern journals; some venues still prefer the passive. Check the target journal's instructions.
- **Tone**: precise, sober, calibrated. Avoid hype, avoid hedging into meaninglessness. "May", "suggests", "is consistent with" are acceptable; "proves", "demonstrates definitively", "revolutionary" are not.
- **Jargon**: define every abbreviation on first use; do not abbreviate terms used fewer than three times.
- **Numbers**: report effect sizes with 95% CIs; report p-values to three decimals (p=0.032, p<0.001), never as "ns" or "significant". Use SI units. Use the same number of decimals throughout a table.
- **Citation style**: follow the target journal exactly. Vancouver for most biomedical (numbered, superscript or bracketed). APA 7 for psychology. Use a reference manager.
- **Tables and figures**: standalone captions. A reader who sees only the figure must understand it. Place captions below figures, above tables, per most journal styles.
- **Length discipline**: most journals cap original articles at 3000–5000 words excluding abstract, references, tables, and figures. Track word count from the first draft.

---

## Quality Checklist

- [ ] The title is declarative and free of marketing verbs
- [ ] The abstract is structured (Background / Methods / Results / Conclusion) and within word limit
- [ ] The Introduction funnels from broad to specific in four paragraphs
- [ ] The aim is stated explicitly and corresponds to the primary outcome
- [ ] The Methods are detailed enough that an independent team could replicate the study
- [ ] A pre-registration ID or a justified absence is recorded
- [ ] Ethics approval and informed consent are stated
- [ ] Results report effect sizes with 95% CIs, not p-values alone
- [ ] No interpretation appears in the Results section
- [ ] The Discussion follows the six-paragraph structure with explicit limitations
- [ ] Conclusions are calibrated to the evidence — no over-reach
- [ ] Funding and competing interests are declared
- [ ] All references follow the target journal's style consistently
- [ ] A reporting-guideline checklist (CONSORT, STROBE, PRISMA, SRQR) is included as a supplement

---

## Common Mistakes

- **Marketing the work in the title.** "Novel", "groundbreaking", "first-of-its-kind" are immediate red flags for editors. Let the data speak.
- **Background dressed up as introduction.** A history of the field is not a justification for the study. State the gap, not the genealogy.
- **Methods missing the why.** Why this sample size, this instrument, this threshold, this analysis? Editors and reviewers will ask; preempt them.
- **Mixing results and interpretation.** "Significantly higher and consistent with the inflammation hypothesis" combines a result with a Discussion claim. Split them.
- **P-values without effect sizes.** A p-value of 0.04 with a clinically negligible effect size is not a finding worth celebrating. Always report magnitude and uncertainty.
- **Cherry-picking the prior literature.** Citing only studies that agree with the result invites a reviewer to send a list of those that disagree. Engage with disagreement.
- **Vague limitations.** "Limitations include sample size" is uninformative. State which inferences are weakened and how.
- **Over-claiming in the conclusion.** A single observational study does not establish causation. Calibrate language to design.
- **Inconsistent numbers.** The N in the abstract must equal the N in Methods, Results, and Table 1. Reconcile before submission.
- **Missing reporting-guideline checklist.** Most journals require CONSORT, STROBE, PRISMA, ARRIVE, or SRQR as a supplement. Omission triggers desk rejection.
- **Conflating systematic review with narrative review.** Use `skills/prisma.md` for systematic reviews; this skill alone is insufficient for evidence synthesis.
- **Forgetting data availability.** Most journals now require a data availability statement. "Available on request" is increasingly unacceptable without justification.
