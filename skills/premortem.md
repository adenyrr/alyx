---
name: premortem
description: Apply Gary Klein's pre-mortem analysis to surface latent risks before a project starts or at a major checkpoint. The team imagines that the project has already failed catastrophically, then works backward to enumerate plausible root causes — turning hindsight bias into foresight. Trigger keywords include "pre-mortem", "premortem", "what could go wrong", "risk anticipation", "kill the project", "failure modes", "red team". Contrast: SWOT (skills/swot.md) maps current strengths and weaknesses; FMEA scores component failure modes; a pre-mortem specifically harnesses prospective hindsight to break optimism bias on a whole initiative.
agents: [reasoning]
---

# Pre-Mortem — Prospective Hindsight Risk Analysis

A pre-mortem, introduced by decision researcher Gary Klein (Harvard Business Review, 2007), inverts the classic post-mortem: instead of asking "what went wrong?" after failure, the team imagines failure has already happened and asks "what caused it?". The method exploits a robust cognitive effect — prospective hindsight increases the ability to identify reasons for future outcomes by roughly 30%. It surfaces concerns that team members would suppress in a standard "any risks?" round, because permission to imagine failure is explicit.

---

## When to Apply

Apply a pre-mortem when:

- A project is about to be kicked off (charter approved, before execution).
- A go/no-go decision is imminent for a launch, release, deployment, or merger.
- A major milestone, phase gate, or investment tranche is being approved.
- A new strategy is being rolled out.
- Optimism is high and dissent is scarce — the textbook warning sign for groupthink.
- A previous initiative failed and the team is repeating the pattern.

Do NOT apply a pre-mortem when:

- The work is routine, low-stakes, and easily reversible — overhead exceeds value.
- The team has zero psychological safety — the exercise will produce sanitized risks. Fix safety first.
- The decision is already made and immutable — pre-mortem becomes theater.
- Detailed quantitative risk modeling is required (use FMEA, fault tree analysis, Monte Carlo) — pre-mortem complements but does not replace these.
- The project is already in execution and a real post-mortem is more useful.

---

## Methodology Overview

The pre-mortem leverages four principles:

1. **Prospective hindsight.** Reframing "this project might fail" to "this project did fail" unlocks more specific, more causal failure narratives.
2. **Permission to dissent.** The exercise officially sanctions pessimism, neutralizing the social cost of raising concerns.
3. **Silent generation, then sharing.** Individual brainstorming first prevents anchoring on the first speaker.
4. **Categorize and prioritize.** Raw lists become risk registers with owners and mitigations.

### The five stages

1. **Setup** — frame the project, set the failure scenario, invite the right people.
2. **Silent generation** — each participant writes failure causes alone for 5–10 minutes.
3. **Round-robin sharing** — each participant reads one cause at a time; facilitator captures verbatim.
4. **Categorize** — cluster causes into failure categories (technical, organizational, market, regulatory, etc.).
5. **Prioritize and mitigate** — score each cause on impact × likelihood; assign owners and mitigation actions.

### Key definitions

- **Prospective hindsight** — imagining a future event has already occurred and reasoning backward.
- **Failure category** — a domain bucket grouping related root causes for pattern recognition.
- **Mitigation** — a concrete action that reduces probability, impact, or both. Phrased as verb + outcome.
- **Trigger / watchpoint** — an observable early-warning signal that a risk is materializing.

---

## Step-by-Step Application

1. **Setup the session.**
   - Convene the project team plus 1–3 outsiders (cross-functional perspective is critical).
   - Allow 60–90 minutes for the first pre-mortem of a project; 30–45 minutes for follow-ups at milestones.
   - Distribute the project charter, plan, and key assumptions 24 hours before.
   - Appoint a facilitator who will not contribute causes (neutral capture).

2. **Frame the failure scenario.**
   - Read the setup wording verbatim:

     > "It is **`<6 months>`** from now. The project has failed **catastrophically**. The launch did not happen, the goals were missed, the team has disbanded, the budget is gone. We are now meeting to figure out what went wrong. **Spend the next 10 minutes writing down, alone, every plausible reason this failure occurred.**"

   - Adjust the horizon (3 months / 12 months / 24 months) to match the project length.
   - Adjust "catastrophic" to match scale; the word "failed" must remain.

3. **Silent generation (10 minutes).**
   - Each participant writes failure causes individually, one per line, on cards, sticky notes, or a shared doc with private cells.
   - Encourage quantity over quality; 10–20 causes per person is typical.

4. **Round-robin sharing.**
   - Each participant reads one cause; facilitator captures verbatim with attribution suppressed.
   - Continue rotating until all causes are surfaced. Do not debate at this stage.
   - Typical raw output: 40–120 causes for a 6-person session.

5. **Cluster into failure categories.**
   - Apply the four standard buckets (extend as needed):
     - **Technical** — architecture, scalability, dependencies, debt, integration.
     - **Organizational** — team capacity, skills gap, communication, governance, leadership.
     - **Market** — demand, competition, timing, pricing, channel.
     - **Regulatory / Legal / Compliance** — approvals, data protection, certification, IP.
     - (Optional) **Financial** — cash runway, FX, vendor solvency.
     - (Optional) **External** — macroeconomic, geopolitical, supply chain, force majeure.
   - Merge duplicates; sharpen wording.

6. **Score impact × likelihood.**
   - Impact: 1 (negligible) → 5 (project-killing).
   - Likelihood: 1 (rare) → 5 (highly likely without mitigation).
   - Risk score = Impact × Likelihood (1–25).

7. **Prioritize.**
   - **Score 15–25**: critical — mitigation required before the project proceeds.
   - **Score 8–14**: significant — mitigation planned and owned.
   - **Score 3–7**: monitor — assign a watchpoint and review at milestones.
   - **Score 1–2**: accept — log but do not act.

8. **Assign mitigations.**
   - For each critical or significant risk:
     - Define a **mitigation action** (verb + outcome + deadline).
     - Define an **early-warning signal** (observable trigger).
     - Assign a **single owner** (delegate to RACI if needed).

9. **Integrate into the project plan.**
   - Add mitigation actions as work items.
   - Add watchpoints to the dashboard or monitoring.
   - Schedule a pre-mortem re-run at each major milestone.

---

## Output Template

### 1. Session Metadata

- **Project:** `<name>`
- **Failure horizon:** `<N months from now>`
- **Date of session:** `<YYYY-MM-DD>`
- **Participants:** `<list of roles>`
- **Facilitator:** `<role>`

### 2. Failure Scenario Statement

> It is `<N>` months from now. `<Project>` has failed catastrophically. `<Specific failure description: launch missed, deadlines blown, budget overrun, team disbanded, reputation damaged>`. The following root causes were identified by the team working backward from this outcome.

### 3. Categorized Root Causes

#### Technical
| ID | Root cause | Impact (1–5) | Likelihood (1–5) | Score |
|---|---|:---:|:---:|:---:|
| T-01 | `<root cause statement>` | `<n>` | `<n>` | `<n>` |
| T-02 | `<…>` | | | |

#### Organizational
| ID | Root cause | Impact | Likelihood | Score |
|---|---|:---:|:---:|:---:|
| O-01 | `<…>` | | | |

#### Market
| ID | Root cause | Impact | Likelihood | Score |
|---|---|:---:|:---:|:---:|
| M-01 | `<…>` | | | |

#### Regulatory / Legal
| ID | Root cause | Impact | Likelihood | Score |
|---|---|:---:|:---:|:---:|
| R-01 | `<…>` | | | |

### 4. Prioritized Risk Register

| Rank | ID | Root cause | Score | Tier | Mitigation action | Owner | Early-warning signal | Review date |
|---|---|---|:---:|---|---|---|---|---|
| 1 | T-03 | `<…>` | 20 | Critical | `<verb + outcome + by date>` | `<role>` | `<observable trigger>` | `<date>` |
| 2 | O-01 | `<…>` | 16 | Critical | `<…>` | | | |
| 3 | M-02 | `<…>` | 12 | Significant | `<…>` | | | |
| 4 | R-01 | `<…>` | 9 | Significant | `<…>` | | | |
| 5 | T-05 | `<…>` | 6 | Monitor | `<…>` | | | |

### 5. Distribution Snapshot

| Category | Causes raised | Critical | Significant | Monitor | Accept |
|---|:---:|:---:|:---:|:---:|:---:|
| Technical | `<n>` | | | | |
| Organizational | `<n>` | | | | |
| Market | `<n>` | | | | |
| Regulatory | `<n>` | | | | |
| Other | `<n>` | | | | |
| **Total** | | | | | |

### 6. Go / No-Go Recommendation

- **Proceed**: all critical risks have an owned mitigation and a watchpoint.
- **Proceed with conditions**: critical risks `<…>` require pre-launch resolution.
- **Pause**: critical risks `<…>` are unmitigated and exceed the team's risk tolerance.

### 7. Next Pre-Mortem

- **Trigger:** `<next milestone or date>`
- **Scope:** `<full re-run / delta on critical risks>`

---

## Quality Checklist

- [ ] Failure scenario is framed in past tense ("has failed"), not conditional ("might fail")
- [ ] Silent generation precedes any group discussion
- [ ] At least 6 participants contribute, including at least one outsider
- [ ] Each participant raised at least one cause (no free-riders)
- [ ] Causes are clustered into ≥ 3 categories
- [ ] Every cause has an impact and likelihood score
- [ ] Critical and significant risks have a named owner and a verb-form mitigation
- [ ] Each significant risk has an observable early-warning signal
- [ ] Mitigations are added to the project plan, not just the report
- [ ] A re-run cadence is scheduled
- [ ] A go / no-go statement is explicit

---

## Common Mistakes

- **Conditional framing.** "What could go wrong?" reverts to standard risk identification and loses 30% of the foresight. Use past tense: "What did go wrong?".
- **Group brainstorm without silent generation.** The first speaker anchors everyone. Silent first, share second.
- **No outsiders.** Insiders share blind spots. Recruit at least one cross-functional or external participant.
- **Stopping at the list.** A list of risks without owned mitigations is a worry, not a plan.
- **Scoring without grounding.** Impact × Likelihood scores assigned by gut alone produce noise. Sanity-check against base rates and prior projects.
- **One pre-mortem ever.** Risks evolve; re-run at each major milestone.
- **Soft language to spare feelings.** "Some communication issues" hides "the engineering lead does not trust the PM". Pre-mortem only works with candor.
- **Using pre-mortem to kill projects.** It is a risk-surfacing tool, not a veto tool. The output of a pre-mortem should usually be "proceed with mitigations", not "stop".
- **Skipping early-warning signals.** Without triggers, mitigations sit until the risk has already materialized.
- **Confusing pre-mortem with FMEA or risk register.** Pre-mortem is a generative exercise; FMEA is component-level scoring; risk register is the artifact. Use pre-mortem to populate the register.
- **No psychological safety.** If team members fear punishment for naming risks, the exercise will produce a sanitized list. Fix the culture or do not bother.
