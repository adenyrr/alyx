---
name: swot
description: Apply the SWOT (Strengths, Weaknesses, Opportunities, Threats) analytical framework and its TOWS extension to derive strategic implications. Trigger keywords include "SWOT", "strategic analysis", "strengths and weaknesses", "competitive analysis", "internal/external analysis", "strategy formulation". Use SWOT to inventory the situation; use TOWS to convert that inventory into four families of actionable strategies (SO, WO, ST, WT). Contrast: SWOT is a static diagnosis; for prioritization across many initiatives use Eisenhower (skills/eisenhower.md); for role accountability use RACI (skills/raci.md); for risk anticipation use pre-mortem (skills/premortem.md).
agents: [reasoning]
---

# SWOT + TOWS — Strategic Diagnosis and Implication Generation

SWOT is a two-axis decomposition that separates **internal** factors a subject controls (Strengths, Weaknesses) from **external** factors it does not (Opportunities, Threats). TOWS reverses the order to force strategic synthesis: pairing internal and external factors generates four families of action options. Use SWOT to map the terrain; use TOWS to draw the route.

---

## When to Apply

Apply SWOT/TOWS when:

- A team, product, project, organization, or initiative must be assessed before a strategic decision.
- A new market entry, pivot, partnership, or investment is on the table.
- A periodic strategic review (annual, quarterly) is due.
- The user asks for "strategic options", "competitive positioning", "go/no-go", or wants to "see the big picture".
- A pitch deck, business plan, or strategy memo requires a single-page situational summary.

Do NOT apply SWOT/TOWS when:

- The question is operational, not strategic (use RACI for role clarity, Eisenhower for task triage).
- A quantitative forecast is needed (use scenario analysis, Monte Carlo).
- The risk landscape is the main concern (use pre-mortem, FMEA).
- The decision is a single binary trade-off (use a decision matrix or cost-benefit analysis).
- The subject is too narrow (a single feature, a single meeting) — SWOT will look forced.

---

## Methodology Overview

SWOT classifies every relevant factor along two dichotomies:

1. **Internal vs. External** — Can the subject change this factor by acting on itself? Internal: skills, assets, processes, culture, IP, financials. External: market, regulation, technology, competition, macroeconomy, social trends.
2. **Helpful vs. Harmful** — Does it help or hinder the objective?

The four quadrants emerge:

| | Helpful | Harmful |
|---|---|---|
| **Internal** | **S**trengths | **W**eaknesses |
| **External** | **O**pportunities | **T**hreats |

### TOWS — from diagnosis to strategy

TOWS crosses the quadrants to generate four strategic postures:

| | Opportunities (O) | Threats (T) |
|---|---|---|
| **Strengths (S)** | **SO** — Maxi-Maxi: deploy strengths to seize opportunities (offensive) | **ST** — Maxi-Mini: use strengths to neutralize threats (defensive) |
| **Weaknesses (W)** | **WO** — Mini-Maxi: fix weaknesses to capture opportunities (turnaround) | **WT** — Mini-Mini: minimize weaknesses to avoid threats (survival) |

Each cell yields one or more concrete strategic options.

### Key definitions

- **Strength** — an internal attribute that the subject controls and that contributes to objectives. Must be evidenced (data, benchmark, third-party rating), not aspirational.
- **Weakness** — an internal attribute under the subject's control that hinders objectives. Must be specific (e.g., "12-month sales cycle" not "slow sales").
- **Opportunity** — an external trend, gap, or event the subject could exploit. Must exist independently of the subject's actions.
- **Threat** — an external factor that could damage performance. Must be plausible within the planning horizon.
- **Internal / external test** — if the subject went out of business tomorrow, would the factor still exist? If yes → external. If no → internal.

---

## Step-by-Step Application

1. **Define the subject and the objective.**
   - State the unit of analysis (e.g., "Product X in the EMEA market", "R&D team for FY2026").
   - State the objective in one sentence ("Capture 5% market share within 18 months"). SWOT factors are evaluated against this objective.
   - Define the planning horizon (3, 12, 36 months) — opportunities and threats outside the horizon are dropped.

2. **Brainstorm raw factors.**
   - Generate 10–30 candidate factors with no filtering. Prefer multi-source input (interviews, market data, financial reports, customer feedback).
   - Tag each as Internal or External, Helpful or Harmful — applying the "test" above.

3. **Cluster and consolidate.**
   - Merge duplicates; collapse near-synonyms.
   - Aim for 4–7 entries per quadrant — fewer is too vague, more is unprioritized.

4. **Sharpen each entry.**
   - Replace adjectives with measurable claims. "Strong brand" → "Net Promoter Score 62 (industry median 28)".
   - Cite evidence inline (`[source]`).
   - Mark each entry High/Medium/Low impact and Likely/Possible (for O/T) or Established/Eroding (for S/W).

5. **Render the 2×2 matrix.** See template below.

6. **Generate TOWS strategies.**
   - For each (S, O) pair, ask: "Does this strength let us exploit this opportunity?" If yes, draft an SO strategy.
   - Repeat for (S, T), (W, O), (W, T). Not every pair yields a strategy; one well-supported option per cell is often enough.
   - Phrase strategies as action verbs with a measurable outcome ("Launch X to capture Y by Z").

7. **Prioritize.**
   - Score each strategy on Impact (1–5) × Feasibility (1–5).
   - Surface the top 3–5 strategies as recommendations.

8. **Pressure-test.**
   - Run the strategies through a one-paragraph pre-mortem to surface hidden risks (delegate to skills/premortem.md if needed).
   - Confirm internal vs. external attribution holds.

---

## Output Template

### 1. Context

- **Subject:** `<unit of analysis>`
- **Objective:** `<one-sentence objective>`
- **Horizon:** `<N months>`
- **Date of analysis:** `<YYYY-MM-DD>`

### 2. SWOT Matrix

| | Helpful to objective | Harmful to objective |
|---|---|---|
| **Internal origin** | **Strengths** <br/>• S1: `<sharp claim>` — `<evidence>` `[impact: H/M/L]` <br/>• S2: `<…>` <br/>• S3: `<…>` <br/>• S4: `<…>` | **Weaknesses** <br/>• W1: `<sharp claim>` — `<evidence>` `[impact: H/M/L]` <br/>• W2: `<…>` <br/>• W3: `<…>` <br/>• W4: `<…>` |
| **External origin** | **Opportunities** <br/>• O1: `<sharp claim>` — `<source>` `[likelihood: high/med/low]` <br/>• O2: `<…>` <br/>• O3: `<…>` <br/>• O4: `<…>` | **Threats** <br/>• T1: `<sharp claim>` — `<source>` `[likelihood: high/med/low]` <br/>• T2: `<…>` <br/>• T3: `<…>` <br/>• T4: `<…>` |

### 3. TOWS Matrix — Strategic Implications

| | **O1** `<short>` | **O2** `<short>` | **T1** `<short>` | **T2** `<short>` |
|---|---|---|---|---|
| **S1** `<short>` | **SO**: `<strategy>` | | **ST**: `<strategy>` | |
| **S2** `<short>` | | **SO**: `<strategy>` | | **ST**: `<strategy>` |
| **W1** `<short>` | **WO**: `<strategy>` | | **WT**: `<strategy>` | |
| **W2** `<short>` | | **WO**: `<strategy>` | | **WT**: `<strategy>` |

### 4. Strategy Inventory

| ID | Type | Strategy | Linked factors | Impact (1–5) | Feasibility (1–5) | Score |
|---|---|---|---|---|---|---|
| ST-01 | SO | `<action verb + outcome + horizon>` | S1, O1 | `<n>` | `<n>` | `<n>` |
| ST-02 | WO | `<…>` | W1, O2 | | | |
| ST-03 | ST | `<…>` | S2, T1 | | | |
| ST-04 | WT | `<…>` | W2, T2 | | | |

### 5. Top Recommendations

1. **`<top strategy>`** — Rationale: `<one sentence>`. Owner: `<role>`. Timeline: `<…>`.
2. **`<…>`**
3. **`<…>`**

### 6. Assumptions and Watchpoints

- Assumption: `<…>` — invalidated by `<event>`.
- Watchpoint: `<external signal to monitor>` — frequency: `<weekly/monthly/quarterly>`.

---

## Quality Checklist

- [ ] Objective is stated in one sentence and is measurable
- [ ] Each quadrant has 4–7 entries (not 1, not 20)
- [ ] Every S/W passes the "internal control" test; every O/T passes the "would still exist without us" test
- [ ] Every entry is specific and evidenced (no bare adjectives)
- [ ] Opportunities and threats fall within the stated horizon
- [ ] TOWS produces at least one strategy per active cell
- [ ] Each strategy is phrased as action + outcome + horizon
- [ ] Strategies are scored on Impact × Feasibility and ranked
- [ ] Top 3–5 recommendations are surfaced with owner and timeline
- [ ] Assumptions are explicit and falsifiable

---

## Common Mistakes

- **Vague entries.** "Good team" or "competitive market" carry no information. Force measurable specifics.
- **Confusing internal and external.** "Customers are price-sensitive" is external (market characteristic); "Our prices are too high" is internal. Misclassification breaks TOWS.
- **Listing aspirations as strengths.** "Will launch a new platform" is not a current strength.
- **Treating opportunities as ideas.** An opportunity is an external condition (e.g., "new EU regulation favors low-carbon products"), not an internal project ("launch a green product line"). The latter is a TOWS-derived strategy.
- **Mirror-image entries.** Listing "small team" as a weakness and "agility" as a strength duplicates the same fact.
- **Skipping TOWS.** A bare SWOT lists factors but produces no decisions. Always cross to TOWS.
- **Over-counting threats.** A wall of threats produces paralysis; cluster and prioritize.
- **No prioritization.** Without Impact × Feasibility scoring, all strategies look equal.
- **Stale analysis.** Markets shift; date-stamp the SWOT and revisit on a defined cadence.
- **Confusing SWOT with PESTLE.** PESTLE (Political, Economic, Social, Technological, Legal, Environmental) feeds the O/T quadrants; it is not a substitute.
