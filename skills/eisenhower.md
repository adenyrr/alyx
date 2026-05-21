---
name: eisenhower
description: Apply the Eisenhower urgent/important matrix to triage and prioritize tasks for one actor (individual or small team) across four quadrants — Q1 Do, Q2 Schedule, Q3 Delegate, Q4 Eliminate. Trigger keywords (EN) "Eisenhower", "urgent vs important", "priority matrix", "time management", "task triage", "what should I work on", "prioritize my backlog"; (FR) "matrice d'Eisenhower", "matrice urgent / important", "priorisation", "gestion du temps", "que dois-je faire en priorité", "trier mes tâches". Use for personal or small-team workload prioritization. Contrast: SWOT (skills/swot.md) is strategic positioning; RACI (skills/raci.md) distributes one task across many actors; Eisenhower distributes many tasks across one actor's time and attention.
agents: [reasoning]
---

# Eisenhower Matrix — Urgent vs. Important Prioritization

The Eisenhower matrix (popularized in Stephen Covey's "7 Habits" from a quote attributed to President Eisenhower) sorts every task on two binary axes — **urgency** and **importance** — producing four quadrants with prescriptive treatment. It is the fastest way to drag attention out of reactive firefighting and toward consequential, non-urgent work.

---

## When to Apply

Apply the Eisenhower matrix when:

- An individual or small team has a backlog of 10–50 tasks and must decide what to do today, this week, this quarter.
- Reactive work dominates and important long-term work keeps slipping.
- A weekly or daily planning ritual is being established.
- A manager wants to coach a report on time allocation.
- Inbox triage, sprint planning, or quarterly OKR breakdown is in progress.

Do NOT apply Eisenhower when:

- The problem is strategic positioning, not task selection (use SWOT).
- Multiple actors must coordinate on one workflow (use RACI).
- Risk anticipation is the goal (use pre-mortem).
- Tasks have complex dependencies and a critical path (use a Gantt / dependency graph).
- The backlog is so large that triage is the bottleneck — first apply a coarse filter (deadline, owner), then Eisenhower.

---

## Methodology Overview

Two axes, four quadrants:

| | **Urgent** | **Not Urgent** |
|---|---|---|
| **Important** | **Q1 — Do** (crises, deadlines today, blockers) | **Q2 — Schedule** (planning, learning, prevention, relationships, deep work) |
| **Not Important** | **Q3 — Delegate** (interruptions, some meetings, others' priorities masquerading as yours) | **Q4 — Eliminate** (busywork, distractions, low-value habits) |

### Key definitions

- **Urgent** — has a hard, near-term deadline (today, this week) or imposes cost if delayed. Urgency is time-bound and externally visible.
- **Important** — contributes meaningfully to the actor's goals, values, or long-term outcomes. Importance is goal-bound and personally judged.
- **Quadrant 2 is the strategic quadrant.** High-functioning actors spend most discretionary time here; low-functioning actors are trapped in Q1 and Q3.

### Treatment per quadrant

| Quadrant | Treatment | Examples |
|---|---|---|
| **Q1 — Do now** | Execute immediately, ideally before lunch. Minimize duration; do not let Q1 cannibalize Q2. | Production outage, today's deadline, urgent customer escalation |
| **Q2 — Schedule** | Place on the calendar with a defined start time, duration, and definition-of-done. Protect from interruption. | Strategy review, skill development, exercise, planning, relationship-building, key architectural work |
| **Q3 — Delegate** | Hand off to someone for whom the task is important. If undelegable, batch and dispatch with minimum attention. | Some meetings, status reports, interruptions, others' urgent requests on non-critical paths |
| **Q4 — Eliminate** | Stop doing. Unsubscribe, decline, archive, automate to zero. | Doomscrolling, low-value notifications, optional meetings without agenda, perfectionism on disposable artifacts |

### Time-allocation targets

A high-performing knowledge worker should aim for approximately:

- **Q1: 15–25%** — necessary but minimized; high Q1 indicates poor planning or bad system design.
- **Q2: 60–70%** — the engine of compounding value.
- **Q3: 5–15%** — kept low through delegation and boundaries.
- **Q4: < 5%** — ideally zero.

If Q1 + Q3 > 50% of time, the system is failing — not the actor.

---

## Step-by-Step Application

1. **Capture every task.**
   - Empty all inputs (inbox, sticky notes, chat backlog, head) into a single list. Aim for 10–50 items.
   - One line per task; verb + object ("Draft Q4 board memo", "Reply to vendor X").

2. **Classify importance.**
   - For each task, ask: "Does this advance a stated goal or value?" Score Important (I) or Not Important (NI).
   - Be ruthless: tasks that feel important because they are loud are often Q3, not Q1.

3. **Classify urgency.**
   - For each task, ask: "Is there a real deadline within ≤ 1 week, or a real cost to delay?" Score Urgent (U) or Not Urgent (NU).
   - Distinguish externally imposed urgency from self-imposed anxiety.

4. **Plot tasks in the matrix.**
   - Place each task in exactly one quadrant.
   - If oscillating between two quadrants, default to the lower-priority one (forces honesty).

5. **Apply quadrant treatments.**
   - Q1: schedule for the current day with a hard time box.
   - Q2: book on the calendar within the next two weeks; treat the slot as a meeting with yourself.
   - Q3: identify the delegate; transfer with context; set a check-back date.
   - Q4: delete, decline, or unsubscribe immediately.

6. **Inspect distribution.**
   - Count tasks per quadrant; compute the percentage.
   - If Q1 dominates: root-cause why (under-planning, over-commitment, missing automation) and create a Q2 task to fix it.
   - If Q4 has many entries: investigate organizational or personal habit drivers.

7. **Repeat on cadence.**
   - Daily: re-triage Q1.
   - Weekly: re-triage Q2 and Q3.
   - Quarterly: review the Q1/Q3 root causes to remove their source.

---

## Output Template

### 1. Context

- **Actor:** `<individual / small team>`
- **Planning horizon:** `<today / this week / this sprint / this quarter>`
- **Date:** `<YYYY-MM-DD>`
- **Total tasks triaged:** `<n>`

### 2. Eisenhower Matrix

| | **Urgent** | **Not Urgent** |
|---|---|---|
| **Important** | **Q1 — Do** <br/>• `<task>` — by `<deadline>`, est. `<time>` <br/>• `<task>` <br/>• `<task>` | **Q2 — Schedule** <br/>• `<task>` — slot: `<day, time>`, est. `<time>` <br/>• `<task>` <br/>• `<task>` |
| **Not Important** | **Q3 — Delegate** <br/>• `<task>` → `<delegate>`, follow-up `<date>` <br/>• `<task>` → `<delegate>` <br/>• `<task>` → automate via `<tool>` | **Q4 — Eliminate** <br/>• `<task>` — drop / unsubscribe / decline <br/>• `<task>` <br/>• `<task>` |

### 3. Today's Plan (Q1 + scheduled Q2 slot)

| Time | Task | Quadrant | Est. duration |
|---|---|---|---|
| `<09:00>` | `<task>` | Q1 | `<30 min>` |
| `<10:00>` | `<task>` | Q2 | `<90 min>` (deep work block) |
| `<14:00>` | `<task>` | Q1 | `<45 min>` |

### 4. Quadrant Distribution

| Quadrant | Count | Share | Target | Δ |
|---|---|---|---|---|
| Q1 — Do | `<n>` | `<%>` | 15–25% | `<over/under>` |
| Q2 — Schedule | `<n>` | `<%>` | 60–70% | |
| Q3 — Delegate | `<n>` | `<%>` | 5–15% | |
| Q4 — Eliminate | `<n>` | `<%>` | < 5% | |

### 5. Root-Cause Notes (when distribution is unhealthy)

- Q1 overload is caused by: `<missing automation / unclear priorities / over-commitment / external chaos>`. Corrective Q2 task: `<…>`.
- Q3 overload is caused by: `<weak boundaries / unclear role / others' lack of planning>`. Corrective action: `<…>`.

---

## Quality Checklist

- [ ] Every captured task is placed in exactly one quadrant
- [ ] Importance is judged against explicitly stated goals or values
- [ ] Urgency is judged against real deadlines, not anxiety
- [ ] Q1 tasks have a deadline and time estimate
- [ ] Q2 tasks have a calendared slot, not just an intention
- [ ] Q3 tasks have a named delegate and a follow-up date
- [ ] Q4 tasks have been acted on (deleted, declined) before the matrix is closed
- [ ] Distribution percentages are computed and compared to targets
- [ ] When Q1 + Q3 exceed 50%, a root-cause analysis is attached
- [ ] The matrix is dated and re-triaged on a defined cadence

---

## Common Mistakes

- **Everything is Q1.** The classic anti-pattern. Either importance or urgency is being inflated. Re-apply the two questions strictly; expect 70% of "Q1" to collapse to Q2 or Q3.
- **Confusing urgency with importance.** A loud Slack ping is urgent, not important. A vague long-term goal is important, not urgent. The matrix exists precisely to separate them.
- **Treating Q2 as optional.** Q2 is the only quadrant that compounds. Skipping it generates tomorrow's Q1.
- **Hoarding Q3 tasks.** Refusing to delegate from ego or perfectionism. Delegate even imperfectly; coach the delegate.
- **Treating Q4 as guilty pleasure.** Q4 is not "fun stuff" — it is low-value activity. Genuine rest is Q2 (restorative for goals), not Q4.
- **Re-triaging too often.** Hourly re-triage is a Q4 activity dressed as productivity. Daily/weekly cadence is enough.
- **Scoring without acting.** A beautifully sorted matrix that nobody executes is worthless. The output of triage is action, not categorization.
- **Using Eisenhower for team coordination.** It is a personal/small-team tool. For multi-actor coordination use RACI.
- **Ignoring the distribution.** The shape of the matrix diagnoses the system. A Q1-dominant chart is a signal to redesign the workload, not just to work harder.
- **Misusing as a status report.** The matrix is a planning tool, not a report. Status belongs in a separate artifact.
