---
name: grade
description: Apply the GRADE (Grading of Recommendations, Assessment, Development and Evaluations) methodology to rate the certainty of evidence (High / Moderate / Low / Very low) for each outcome in a systematic review, and to formulate the strength of recommendations (Strong / Conditional). Trigger keywords (EN) "GRADE", "certainty of evidence", "quality of evidence", "strength of recommendation", "summary of findings", "evidence-to-decision"; (FR) "certitude des preuves", "qualité des preuves", "niveau de preuve", "force de recommandation", "tableau de synthèse des résultats". Contrast: PRISMA (skills/prisma.md) describes how studies were found and selected; GRADE rates how much we can trust the resulting body of evidence per outcome. Use PRISMA first to define the corpus, then GRADE to appraise it.
agents: [doc]
---

# GRADE — Certainty of Evidence and Strength of Recommendations

GRADE is the de facto international standard for rating the certainty of a body of evidence and grading the strength of clinical or policy recommendations. It is used by the WHO, Cochrane, NICE, ACP, and most clinical practice guideline developers. GRADE operates per outcome (not per study) and produces a transparent audit trail from evidence to recommendation.

---

## When to Apply

Apply GRADE when:

- A systematic review has identified the body of evidence (PRISMA stage complete) and the certainty of that evidence must be communicated to decision-makers.
- A clinical practice guideline, health technology assessment, or policy brief is being prepared.
- The user asks for a "Summary of Findings" table, an "Evidence Profile", or wording like "how confident are we in this estimate?".
- A network meta-analysis requires per-comparison certainty ratings (use GRADE for NMA extension).

Do NOT apply GRADE for:

- Individual study appraisal — use risk-of-bias tools (RoB 2, ROBINS-I, QUADAS-2) directly.
- Diagnostic test accuracy without an outcome framework — use GRADE for diagnostic tests, a distinct extension.
- Qualitative evidence synthesis — use GRADE-CERQual instead.
- Mechanistic, bench, or animal evidence — use OHAT or domain-specific frameworks.

---

## Methodology Overview

GRADE rests on five sequential operations:

1. **Define the question and outcomes** (rate each outcome as critical / important / not important from the patient or decision-maker perspective; rate on a 1–9 scale, with 7–9 critical, 4–6 important, 1–3 not important).
2. **Set the starting certainty** by study design: randomized controlled trials start at **High**; observational studies start at **Low**; case series and case reports at **Very low**.
3. **Apply 5 downgrading factors** that can each lower certainty by one or two levels.
4. **Apply 3 upgrading factors** that can only raise certainty of observational evidence.
5. **Move from evidence to recommendation** using the Evidence-to-Decision framework, producing a Strong or Conditional recommendation.

The four certainty levels:

| Level | Meaning |
|---|---|
| **High** | We are very confident the true effect lies close to the estimate. |
| **Moderate** | We are moderately confident; the true effect is likely close but may be substantially different. |
| **Low** | Our confidence in the estimate is limited; the true effect may be substantially different. |
| **Very low** | We have very little confidence; the true effect is likely to be substantially different from the estimate. |

### Key definitions

- **Outcome-centric** — each outcome (e.g., mortality, quality of life, adverse events) receives its own certainty rating; the overall recommendation typically reflects the lowest certainty among critical outcomes.
- **Body of evidence** — all studies contributing to the estimate for a single outcome.
- **Effect estimate** — the pooled or best available numerical estimate (relative + absolute), expressed with a 95% confidence interval.

---

## Step-by-Step Application

1. **List all outcomes and rate their importance.**
   - Score 7–9: critical for the decision (e.g., mortality, major morbidity).
   - Score 4–6: important but not critical (e.g., minor symptom relief).
   - Score 1–3: not important (e.g., surrogate biomarkers without clinical impact).
   - Only outcomes scoring ≥4 are typically carried forward to the Summary of Findings table.

2. **Set the starting certainty.**
   - RCTs → High.
   - Observational studies (cohort, case-control) → Low.
   - Uncontrolled designs (case series) → Very low.

3. **Assess the 5 downgrading factors.** For each, decide: no concern (no downgrade), serious (-1), or very serious (-2).

   | Factor | Downgrade if… |
   |---|---|
   | **Risk of bias** | Most evidence comes from studies at high RoB on critical domains (RoB 2, ROBINS-I). |
   | **Inconsistency** | Unexplained heterogeneity (I² > 50%, non-overlapping CIs, divergent point estimates) across studies. |
   | **Indirectness** | The evidence does not directly answer the PICO: different population, intervention, comparator, outcome, or only indirect comparisons. |
   | **Imprecision** | The 95% CI crosses a clinically meaningful threshold (MID) or the total sample size / event count is below the optimal information size (OIS). |
   | **Publication bias** | Asymmetric funnel plot, Egger's test p<0.10, missing small negative studies, registry vs. publication discrepancies. |

4. **Assess the 3 upgrading factors.** These can only raise observational evidence (not already downgraded). Each can add +1 or +2.

   | Factor | Upgrade if… |
   |---|---|
   | **Large magnitude of effect** | RR ≥ 2 or ≤ 0.5 from observational studies without plausible confounders (+1); RR ≥ 5 or ≤ 0.2 (+2). |
   | **Dose-response gradient** | Clear monotonic relationship between exposure intensity and effect size. |
   | **Plausible confounding would reduce the effect** | All plausible residual confounders would bias toward the null but an effect is still observed; or would have masked an effect that is nonetheless absent. |

5. **Compute final certainty.** Apply downgrades to starting certainty, then upgrades if applicable.
   - Example: RCT (High) with serious imprecision (-1) and serious inconsistency (-1) → Low.
   - Example: Observational (Low) with large effect (+1) and dose-response (+1) → High (rare).

6. **Construct the Summary of Findings table.** One row per outcome, with absolute and relative effects, number of participants and studies, and the certainty rating with footnoted reasons.

7. **Move from evidence to recommendation.** Using the Evidence-to-Decision (EtD) framework, weigh:
   - Magnitude of desirable vs. undesirable effects
   - Certainty of evidence
   - Patient values and preferences
   - Resource use, equity, acceptability, feasibility

   Recommendation strength:

   | Strength | Wording | When to use |
   |---|---|---|
   | **Strong for** | "We recommend …" | Desirable effects clearly outweigh undesirable; high or moderate certainty; little variability in values. |
   | **Strong against** | "We recommend against …" | Undesirable effects clearly outweigh desirable. |
   | **Conditional (weak) for** | "We suggest …" | Balance is close, low certainty, or important variability in values. |
   | **Conditional against** | "We suggest against …" | Likely undesirable but uncertain. |

   Note: GRADE distinguishes "Conditional" from "Weak"; both terms appear in the literature but "Conditional" is preferred since GRADE 2013.

---

## Output Template

### 1. Summary of Findings Table

**Question:** Should `<intervention>` vs. `<comparator>` be used for `<population>`?
**Setting:** `<setting>`
**Bibliography:** `<systematic review citation>`

| Outcome (importance) | Risk with comparator | Risk with intervention (95% CI) | Relative effect (95% CI) | № of participants (studies) | Certainty of evidence (GRADE) | Comments |
|---|---|---|---|---|---|---|
| `<Outcome 1>` (Critical, 9) | `<n per 1000>` | `<n per 1000>` (`<CI>`) | `<RR/OR/HR (CI)>` | `<N>` (`<k>` RCTs) | **High** ⊕⊕⊕⊕ | `<plain-language interpretation>` |
| `<Outcome 2>` (Critical, 8) | `<n per 1000>` | `<n per 1000>` (`<CI>`) | `<RR/OR/HR (CI)>` | `<N>` (`<k>` studies) | **Moderate** ⊕⊕⊕◯ ᵃ | `<interpretation>` |
| `<Outcome 3>` (Important, 6) | `<mean>` | `<MD (CI)>` | — | `<N>` (`<k>` studies) | **Low** ⊕⊕◯◯ ᵇᶜ | `<interpretation>` |
| `<Outcome 4>` (Important, 5) | `<n per 1000>` | `<n per 1000>` (`<CI>`) | `<RR (CI)>` | `<N>` (`<k>` studies) | **Very low** ⊕◯◯◯ ᵃᵇᵈ | `<interpretation>` |

**Certainty symbols:** ⊕⊕⊕⊕ High · ⊕⊕⊕◯ Moderate · ⊕⊕◯◯ Low · ⊕◯◯◯ Very low

**Footnotes (downgrade reasons):**
ᵃ Downgraded one level for risk of bias: `<specific concern, e.g., 4 of 6 studies at high RoB for blinding>`.
ᵇ Downgraded one level for inconsistency: `<I² = X%, point estimates ranged from … to …>`.
ᶜ Downgraded one level for imprecision: `<95% CI crosses the MID of …; total events = … below OIS>`.
ᵈ Downgraded one level for indirectness: `<population/intervention/outcome difference>`.

### 2. Detailed Evidence Profile (one row per outcome)

| Outcome | Studies (n) | Design | Risk of bias | Inconsistency | Indirectness | Imprecision | Publication bias | Other | Effect (95% CI) | Certainty |
|---|---|---|---|---|---|---|---|---|---|---|
| `<Outcome>` | `<k>` (`<N>`) | `<RCT/obs>` | `<not serious / serious / very serious>` | `<…>` | `<…>` | `<…>` | `<…>` | `<large effect / dose-response / —>` | `<estimate>` | `<level>` |

### 3. Recommendation Statement

> **Recommendation:** We `<recommend / suggest> <for / against>` the use of `<intervention>` for `<population>` (Strong / Conditional recommendation, `<High / Moderate / Low / Very low>` certainty of evidence).
>
> **Justification:** `<brief rationale citing the balance of effects, certainty, values, and resource considerations>`.
>
> **Subgroup considerations:** `<note any populations where the recommendation differs>`.
>
> **Implementation considerations:** `<practical guidance>`.

### 4. Evidence-to-Decision Summary

| Domain | Judgment | Rationale |
|---|---|---|
| Problem priority | `<priority / not a priority>` | |
| Magnitude of desirable effects | `<trivial / small / moderate / large>` | |
| Magnitude of undesirable effects | `<trivial / small / moderate / large>` | |
| Certainty of evidence | `<High / Moderate / Low / Very low>` | |
| Values | `<no important uncertainty / important uncertainty>` | |
| Balance of effects | `<favors intervention / favors comparator / balanced>` | |
| Resources required | `<negligible / moderate / large>` | |
| Equity | `<reduced / probably reduced / probably increased / increased>` | |
| Acceptability | `<no / probably no / probably yes / yes>` | |
| Feasibility | `<no / probably no / probably yes / yes>` | |

---

## Quality Checklist

- [ ] Every outcome critical to the decision appears in the Summary of Findings table
- [ ] Starting certainty matches design (RCT = High; observational = Low)
- [ ] Each of the 5 downgrading factors explicitly considered and judgment recorded
- [ ] Upgrading factors considered only for observational evidence and only when not already downgraded
- [ ] Both relative and absolute effects reported with 95% CI
- [ ] Anticipated absolute risks computed using the comparator baseline risk
- [ ] Footnotes specify the precise reason for each downgrade (not a generic label)
- [ ] Minimal Important Difference (MID) stated when assessing imprecision
- [ ] Recommendation strength (Strong / Conditional) is explicit and justified
- [ ] The lowest certainty among critical outcomes drives the overall recommendation
- [ ] EtD framework completed even for non-clinical recommendations

---

## Common Mistakes

- **Confusing study quality with body-of-evidence certainty.** A single high-quality RCT still produces Low certainty if it is small and imprecise.
- **Downgrading twice for the same problem.** Selection bias and small sample size are different concerns; selection bias and randomization flaws are not — do not double-count.
- **Upgrading downgraded evidence.** Upgrading factors apply only when no downgrades were warranted (typically observational evidence with strong, consistent effects).
- **Reporting only relative effects.** Decision-makers need absolute risk differences per 1000 patients; always include both.
- **Skipping imprecision assessment when CI looks narrow.** Compare the CI to the Minimal Important Difference, not to zero or to statistical significance.
- **Treating I² as the sole heterogeneity criterion.** Inspect point estimates and prediction intervals; I² alone misleads with few studies.
- **Recommending "Strong" with Low certainty.** GRADE permits this only in five paradigmatic exceptions (life-threatening situations, uncertain benefit vs. catastrophic harm, etc.); flag and justify explicitly.
- **Omitting publication bias when k ≥ 10.** Funnel plot and statistical tests (Egger, Peters) are mandatory.
- **One certainty rating for the whole review.** Certainty is per outcome; the overall recommendation reflects the critical outcomes' lowest certainty.
- **Forgetting values and preferences.** A recommendation is not Strong if patients reasonably disagree about the trade-offs.
- **Mixing "weak" and "conditional".** Use "Conditional" — "weak" is misinterpreted as low-quality.
