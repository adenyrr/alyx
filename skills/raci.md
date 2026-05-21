---
name: raci
description: Apply the RACI (Responsible, Accountable, Consulted, Informed) or RASCI (adds Support) matrix to clarify roles and decision rights in a project, process, or operating model. Trigger keywords include "RACI", "RASCI", "responsibility matrix", "who does what", "role clarification", "decision rights", "DACI", "ARCI". Use when handoffs are unclear, accountability is diffuse, or multiple stakeholders touch the same deliverable. Contrast: SWOT (skills/swot.md) maps the situation; Eisenhower (skills/eisenhower.md) prioritizes tasks for one actor; RACI distributes one task across many actors.
agents: [reasoning]
---

# RACI / RASCI — Role and Accountability Matrix

RACI is a one-page operating-model tool that assigns four (or five) distinct role types to each task or deliverable, eliminating ambiguity about who does the work, who owns the outcome, who must be consulted, and who must be kept informed. RASCI extends the model with a fifth role, **Support**, to distinguish hands-on contributors from the primary doer.

---

## When to Apply

Apply RACI/RASCI when:

- A new project, process, or operating model is being designed.
- Handoffs are slow, blame is diffuse, or "I thought you were doing that" recurs.
- A cross-functional initiative spans multiple teams or vendors.
- A repeatable process (incident response, release management, hiring) needs codification.
- An audit, ISO, or compliance review requires documented role assignments.
- An onboarding pack or runbook is being written.

Do NOT apply RACI when:

- A single individual owns the whole process — RACI adds bureaucracy for no gain.
- Roles change continuously (early-stage research, exploratory R&D) — premature codification kills agility.
- The question is about prioritization across tasks for one person (use Eisenhower).
- A strategic direction is unclear (resolve strategy with SWOT first; then assign roles).
- The matrix would have more than ~15 tasks × 10 roles — split into sub-matrices.

---

## Methodology Overview

The four canonical RACI roles:

| Letter | Role | Meaning |
|---|---|---|
| **R** | Responsible | Performs the work. Exactly one or several per task; the "doer(s)". |
| **A** | Accountable | Owns the outcome and signs off. **Exactly one per task.** The single throat to choke. |
| **C** | Consulted | Two-way communication; their input is sought before the task is completed. SMEs, peer reviewers, affected teams. |
| **I** | Informed | One-way communication; notified after the fact. Stakeholders who need awareness but not approval. |

RASCI adds:

| Letter | Role | Meaning |
|---|---|---|
| **S** | Support | Provides resources or hands-on assistance to the Responsible party. Not the doer; not just consulted. |

### Cardinality rules

- **A: exactly one per task.** Two Accountables = no Accountable.
- **R: at least one, can be several.** All Rs share the doing.
- **C: zero to many.** Bilateral; their input shapes the work.
- **I: zero to many.** Unilateral; broadcast notification only.
- **S: zero to many (RASCI only).** Augments R.

### Variants

- **DACI** — Driver, Approver, Contributor, Informed (decision-oriented, used at Atlassian/Intuit).
- **ARCI** — same roles as RACI, alphabetical reordering.
- **RAPID** — Recommend, Agree, Perform, Input, Decide (decision rights, used by Bain).

This skill defaults to RACI; switch to RASCI when Support is genuinely distinct from R.

---

## Step-by-Step Application

1. **Scope the matrix.**
   - Name the project, process, or operating model.
   - Define the time horizon (one-off project, steady-state process).
   - Confirm the number of tasks (rows) and stakeholders (columns) stays manageable (target ≤ 15 × ≤ 10).

2. **List the tasks (rows).**
   - Phrase each as a verb + object + outcome ("Approve quarterly budget", "Publish release notes").
   - Avoid vague rows ("Manage X"); decompose into discrete deliverables.
   - Order by chronological or process flow.

3. **List the roles (columns).**
   - Use **roles or titles**, not individual names (e.g., "Product Manager", not "Alice"). People change; roles persist.
   - Include external parties (vendor, regulator, customer) when relevant.

4. **Assign letters cell by cell.**
   - Walk task by task. For each task, ask:
     - **Who is Accountable?** Only one. If none, escalate; if more than one, force a choice.
     - **Who does the work (R)?**
     - **Whose input is required before completion (C)?**
     - **Who must be notified after (I)?**
     - (RASCI) **Who provides support to R (S)?**
   - A cell may be left blank if no involvement.
   - A role may be A+R on the same task (manager who owns and does the work in a small team) — note this is a legitimate exception.

5. **Validate horizontally and vertically.**
   - **Each row** has exactly one A and at least one R.
   - **Each column** is balanced — no role overloaded with As or Rs across all tasks; no role with nothing but Is.
   - Flag rows with many Cs (>3): too many cooks slow execution.

6. **Review with stakeholders.**
   - Walk through the matrix with each role represented; capture and resolve disagreements.
   - Date-stamp and version the matrix; recirculate on changes.

7. **Publish and embed.**
   - Place in the runbook, project charter, or onboarding pack.
   - Reference in meeting agendas ("Per the RACI, decision sits with X").

---

## Output Template

### 1. Context

- **Project / process:** `<name>`
- **Scope:** `<one-sentence description>`
- **Version / date:** `<v1.0 / YYYY-MM-DD>`
- **Owner of this matrix:** `<role>`

### 2. RACI Matrix

| Task / Deliverable | `<Role 1>` | `<Role 2>` | `<Role 3>` | `<Role 4>` | `<Role 5>` | `<Role 6>` |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `<Task 1: verb + object>` | A | R | C | I | | |
| `<Task 2>` | I | A | R | C | C | |
| `<Task 3>` | C | I | A | R | | I |
| `<Task 4>` | | C | I | A | R | C |
| `<Task 5>` | A,R | | C | I | | I |
| `<Task 6>` | I | R | A | | C | I |

### 3. RASCI Matrix (when Support is meaningful)

| Task / Deliverable | `<Role 1>` | `<Role 2>` | `<Role 3>` | `<Role 4>` |
|---|:---:|:---:|:---:|:---:|
| `<Task 1>` | A | R | S | I |
| `<Task 2>` | I | A | R | S |
| `<Task 3>` | C | A | R | I |

### 4. Role Definitions

| Role | Definition | Typical seniority | Reports to |
|---|---|---|---|
| `<Role 1>` | `<what this role does in the project>` | `<level>` | `<role>` |
| `<Role 2>` | | | |

### 5. Decision Log (optional but recommended)

| Decision | Date | A | Rationale |
|---|---|---|---|
| `<Decision summary>` | `<YYYY-MM-DD>` | `<Role>` | `<one sentence>` |

### 6. Change Log

| Version | Date | Change | Approved by |
|---|---|---|---|
| v1.0 | `<date>` | Initial matrix | `<role>` |

---

## Quality Checklist

- [ ] Every row (task) has exactly one A
- [ ] Every row has at least one R
- [ ] Columns are titles or roles, never named individuals
- [ ] No role is A on more than ~30% of tasks (accountability overload)
- [ ] No role has only I entries across all tasks (consider dropping the column)
- [ ] Rows with three or more Cs are reviewed for streamlining
- [ ] A+R combinations are intentional, not accidents
- [ ] Tasks are phrased as verb + object + outcome
- [ ] The matrix has been walked through with each role present
- [ ] Version and owner are visible on the document
- [ ] Distinction between Consulted (two-way) and Informed (one-way) is clear to readers

---

## Common Mistakes

- **Multiple Accountables.** The most common defect. "Co-A" is a euphemism for "no A". Force a single owner.
- **Missing Accountable.** A row with only Rs and Cs has no escalation path. Assign A or strike the row.
- **Confusing roles with people.** Naming "Alice" instead of "Product Manager" makes the matrix fragile and personal.
- **A without authority.** Assigning A to someone who cannot direct R or veto the deliverable is fictional accountability.
- **Everyone Consulted on everything.** A 30-stakeholder C-fest produces decision paralysis. Cap Cs at three per task.
- **Everyone Informed on everything.** Same anti-pattern in reverse; signal-to-noise collapses.
- **Confusing C and I.** C must be asked; I is told. If their input doesn't change the work, they are I.
- **Skipping support distinction.** In a RASCI context, marking everyone R conflates doer and helper; use S.
- **Set and forget.** Org changes happen; an outdated RACI is worse than none. Review at every reorg.
- **Using RACI to assign blame.** RACI is a clarity tool, not a punishment tool. If it becomes a weapon, trust evaporates and the matrix dies.
- **Building RACI before strategy.** Codifying roles before the strategy is set institutionalizes the wrong work.
