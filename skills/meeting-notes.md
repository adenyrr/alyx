---
name: meeting-notes
description: Apply this methodology when the user asks the writer agent to produce formal minutes of a meeting suitable for distribution, archival, audit, or governance purposes. Trigger keywords include "rédige le compte-rendu", "meeting minutes", "minutes of meeting", "MoM", "comptes-rendus", "procès-verbal", "PV de réunion", "formal notes", "write up the meeting", "compose minutes". The output is a structured document with attendees, agenda, discussion summary per item, decisions, an action items table, and a distribution list. Do NOT use for personal note-taking, informal stand-up summaries, transcripts (verbatim), retrospective reports (use business-report.md), strategy memos, or technical design discussions that warrant a full RFC (use technical-rfc.md).
agents: [writer]
---

# Meeting Notes — Formal Minutes Methodology

Formal meeting minutes are the official record of what was discussed, what was decided, and who agreed to do what next. They are read by people who were not in the room, audited months or years later, and sometimes presented as legal evidence of governance. This skill enforces the structural discipline that separates minutes (concise, decision-focused, third-person, distributable) from raw notes (verbose, opinionated, first-person, private).

---

## When to Apply

Apply this methodology when the meeting being recorded is:

- A board, executive committee, or steering committee meeting
- A project governance or change advisory board (CAB) meeting
- A regulatory, compliance, audit, or risk committee meeting
- A vendor or partner formal review meeting
- A works council, union, or HR consultation requiring an official record
- A client kickoff, mid-project review, or formal status meeting
- Any recurring meeting where decisions and action items must be tracked over time

Do NOT apply this methodology for:

- A casual team stand-up or daily scrum — use a shared task tracker
- A 1:1 manager-report conversation — use a private note pattern
- A brainstorm or design workshop — use a workshop-notes pattern
- A verbatim transcript — meeting minutes are summarized, not transcribed
- A retrospective or post-mortem — use the org's dedicated template
- An interview — use an interview-protocol template

---

## Document Structure

Minutes are composed of seven blocks in fixed order.

1. **Header** — date, time, location, meeting type, chair, secretary.
2. **Attendees and apologies** — who was present, absent, and represented.
3. **Agenda** — the ordered list of items addressed.
4. **Per-item record** — for each agenda item: discussion summary, decisions, action items.
5. **Decisions log** — a consolidated table of all decisions made in the meeting.
6. **Action items table** — a consolidated table of all actions assigned.
7. **Next meeting and distribution list** — when the group reconvenes and who receives the minutes.

---

## Section-by-Section Writing Guide

### 1. Header

Purpose: establish the official metadata for archival and audit.

Include: meeting title, date (ISO format YYYY-MM-DD), start and end time with timezone, location (physical address, video link, or "hybrid" with both), meeting type (board, steering, project, governance, etc.), chair, secretary or minute-taker, document version (Draft, Final), and the date the minutes were issued.

Length: a metadata table, no prose.

### 2. Attendees and Apologies

Purpose: establish quorum, presence, and representation.

Include three named lists with roles:
- **Present**: in person or by video; record the modality if relevant.
- **Apologies** (excused absences): with a representative if appointed.
- **Distribution** (not present but receiving minutes): observers, sponsors, archives.

For governance meetings, record quorum status explicitly.

Length: a table.

### 3. Agenda

Purpose: provide the navigable map of the meeting.

Include each item with: number, title, owner, document references (pre-reads), and the time allocated. Items added during the meeting (any other business, AOB) are marked as such.

Length: a single ordered list or table.

### 4. Per-Item Record

Purpose: capture, for each agenda item, what was discussed, what was decided, and what will happen next.

Each item follows the same four-part structure:
- **Discussion summary** (3–8 sentences): a third-person, neutral, paraphrased summary of the substantive points raised. Attribute viewpoints by role, not by name, unless attribution is essential.
- **Decisions** (0–N): the formal outcomes of the discussion, each preceded by "**Decision:**".
- **Action items** (0–N): each with an owner, a due date, a status, and a reference number (A-NN).
- **References**: documents cited or produced during the item.

Apply the **Decision vs. Discussion Rubric** (below) to decide what goes in which bucket.

### 5. Decisions Log

Purpose: a consolidated, scannable index of every formal decision taken.

Each row: decision ID (D-NN), agenda item, decision statement (verb-led, single sentence), decision-maker (the person or body with authority), vote or consensus, dissenting parties if any, effective date.

### 6. Action Items Table

Purpose: a consolidated, accountable list of every commitment made.

Each row: action ID (A-NN), description (verb-led), owner (single name), due date (YYYY-MM-DD), status (Open / In Progress / Blocked / Done / Cancelled), priority (P0/P1/P2), parent decision if any.

### 7. Next Meeting and Distribution List

Purpose: tell the reader when the group reconvenes and who is responsible for receiving the record.

Include: next meeting date, location, draft agenda, and the named distribution list (recipients of the minutes).

---

## The Decision-vs-Discussion Rubric

A common failure mode is to misclassify items. Apply the rubric below to every paragraph drafted in the per-item record.

| Indicator | Discussion | Decision | Action item |
|---|---|---|---|
| Tense used | Past or conditional ("the team noted", "would consider") | Present perfect, normative ("has approved", "will proceed") | Future, verb-led ("draft the policy by 15 June") |
| Owner named | No specific owner required | The authoritative body or role is named | A single named person |
| Date attached | No | Effective date if delayed | Due date mandatory |
| Reversibility | Reversible — discussion can resume | Binding within the body's authority | Tracked until done |
| Test question | "Was an outcome reached?" → No | "Was an outcome reached?" → Yes | "Did someone commit to do something?" → Yes |

Operational rules:
- Every decision needs at least one action item, even if it is "Communicate decision to <stakeholder>".
- Every action item has exactly one owner. Two owners means no owner.
- An item that is "for information" or "for discussion only" must be explicitly tagged as such — readers should never have to guess.
- A decision that is deferred is recorded as a deferral, not as a decision.

---

## Output Template

```markdown
# Minutes of <Meeting type and title>

## Header

| Field | Value |
|---|---|
| Meeting | <e.g., Project Alyx Steering Committee — meeting #12> |
| Date | <YYYY-MM-DD> |
| Start time | <HH:MM, timezone> |
| End time | <HH:MM, timezone> |
| Location | <Room name / video link / hybrid with both> |
| Chair | <Name, Role> |
| Secretary | <Name, Role> |
| Version | <Draft / Final v1.0> |
| Issued on | <YYYY-MM-DD> |
| Document reference | <e.g., MIN-2026-007> |

---

## 1. Attendees and Apologies

### Present
| Name | Role | Organization | Modality |
|---|---|---|---|
| <Name> | <Chair> | <Org> | <In person> |
| <Name> | <Member> | <Org> | <Video> |
| <Name> | <Member> | <Org> | <In person> |
| <Name> | <Observer> | <Org> | <Video> |

### Apologies (excused)
| Name | Role | Represented by |
|---|---|---|
| <Name> | <Member> | <Name> / <None> |

### Quorum
<e.g., "Quorum met: 5 of 7 voting members present (rule: 4/7).">

---

## 2. Agenda

| # | Item | Owner | Pre-reads | Allocated time |
|---|---|---|---|---|
| 1 | <Adoption of previous minutes> | <Chair> | <MIN-2026-006> | <5 min> |
| 2 | <Status update on workstream A> | <Name> | <doc ref> | <15 min> |
| 3 | <Decision: vendor selection for Y> | <Name> | <doc ref> | <30 min> |
| 4 | <Risk register review> | <Name> | <doc ref> | <15 min> |
| 5 | <AOB> | <All> | — | <10 min> |

---

## 3. Per-Item Record

### Item 1 — Adoption of previous minutes

**Discussion summary.** The chair presented the minutes of the previous meeting (MIN-2026-006). One member requested a clarification on action A-014; the secretary confirmed the action remains open with the original owner.

**Decisions.**
- **D-1** — The minutes of MIN-2026-006 are approved without amendment.

**Action items.** None.

**References.** MIN-2026-006.

---

### Item 2 — <Item title>

**Discussion summary.** <3–8 sentences in third person, neutral tone. Paraphrase substantive points, attribute by role when essential. Do not transcribe.>

**Decisions.**
- **D-<N>** — <Verb-led single-sentence decision.>

**Action items.**
| ID | Action | Owner | Due | Status | Priority |
|---|---|---|---|---|---|
| A-<NN> | <Verb-led description> | <Single name> | <YYYY-MM-DD> | <Open> | <P1> |

**References.** <Document ID(s) cited or produced.>

---

### Item 3 — <Item title>

**Discussion summary.** <...>

**Decisions.**
- **D-<N>** — <...>

**Action items.**
| ID | Action | Owner | Due | Status | Priority |
|---|---|---|---|---|---|
| A-<NN> | <...> | <Name> | <YYYY-MM-DD> | <Open> | <P0> |

**References.** <...>

---

### Item 4 — <Item title>

**Discussion summary.** <...>

**Decisions.**
- **D-<N>** — <...>

**Action items.**
| ID | Action | Owner | Due | Status | Priority |
|---|---|---|---|---|---|
| A-<NN> | <...> | <Name> | <YYYY-MM-DD> | <Open> | <P2> |

---

### Item 5 — Any Other Business

**Discussion summary.** <Brief paragraph summarizing items raised outside the formal agenda.>

**Decisions.** <None / list>

**Action items.** <None / table>

---

## 4. Decisions Log

| ID | Item | Decision (single sentence, verb-led) | Decision-maker | Vote or consensus | Dissent | Effective date |
|---|---|---|---|---|---|---|
| D-1 | 1 | Approve minutes of MIN-2026-006 without amendment. | Steering committee | Consensus | None | <YYYY-MM-DD> |
| D-2 | 3 | Award the data-platform contract to <Vendor> for an initial 24-month term. | Steering committee | 5 in favour, 1 against, 0 abstentions | <Member name> | <YYYY-MM-DD> |
| D-3 | 4 | Escalate risk R-019 to corporate risk register at high severity. | Risk owner with chair endorsement | Consensus | None | <YYYY-MM-DD> |

---

## 5. Action Items

| ID | Action | Owner | Due | Status | Priority | Parent decision |
|---|---|---|---|---|---|---|
| A-21 | Notify <Vendor> of contract award and trigger procurement workflow. | <Name> | <YYYY-MM-DD> | Open | P0 | D-2 |
| A-22 | Draft updated risk-treatment plan for R-019 and circulate. | <Name> | <YYYY-MM-DD> | Open | P1 | D-3 |
| A-23 | Update programme dashboard with the revised milestone dates. | <Name> | <YYYY-MM-DD> | Open | P1 | — |
| A-24 | Circulate the technical assessment report referenced in item 3. | <Name> | <YYYY-MM-DD> | Open | P2 | — |

### Carry-over actions (still open from previous meetings)
| ID | Action | Owner | Original due | Revised due | Status | Notes |
|---|---|---|---|---|---|---|
| A-14 | <Description> | <Name> | <YYYY-MM-DD> | <YYYY-MM-DD> | In Progress | <Reason for slip> |
| A-17 | <Description> | <Name> | <YYYY-MM-DD> | <YYYY-MM-DD> | Blocked | <Blocker> |

---

## 6. Next Meeting

| Field | Value |
|---|---|
| Date | <YYYY-MM-DD> |
| Time | <HH:MM, timezone> |
| Location | <room / video link> |
| Provisional agenda | <Item 1>, <Item 2>, <Item 3> |
| Pre-reads due | <YYYY-MM-DD> |

---

## 7. Distribution List

| Recipient | Role | Organization | Reason |
|---|---|---|---|
| <Name> | <Chair> | <Org> | Voting member |
| <Name> | <Member> | <Org> | Voting member |
| <Name> | <Observer> | <Org> | Sponsor |
| <Name> | <Secretary> | <Org> | Archive |
| <Distribution alias> | — | — | Information |

---

## Approvals

| Role | Name | Signature | Date |
|---|---|---|---|
| Chair | <Name> | <electronic signature> | <YYYY-MM-DD> |
| Secretary | <Name> | <electronic signature> | <YYYY-MM-DD> |
```

---

## Style & Tone Guidelines

- **Voice**: third person, neutral, paraphrased. "The committee considered" not "We talked about". Never first person.
- **Tense**: past tense for the discussion ("the committee noted", "the sponsor presented"), present perfect for decisions ("the committee has approved"), future for actions ("the team will deliver").
- **Person**: do not use "I", "we", or "you". Attribute by role ("the chair", "the sponsor", "the CFO") rather than by name except where attribution is essential to the record.
- **Tone**: neutral, factual, official. Strip opinion. Strip humour. Strip jargon that the distribution list would not understand without a glossary.
- **Paraphrase, do not transcribe.** Minutes are a summary, not a verbatim record. A 60-minute meeting yields 1–3 pages of minutes, not 20.
- **Confidentiality.** Mark minutes containing personal data, commercial information, or legally privileged content with the appropriate classification (Confidential, Restricted) and redact distribution accordingly.
- **Naming.** Use the convention `MIN-YYYY-NNN` for document references and `D-NN` / `A-NN` for decisions and actions. Maintain counters across meetings in the same series.
- **Dates.** Always ISO 8601 (YYYY-MM-DD). Always include timezone for times.
- **No editorial commentary.** Minutes do not say "the discussion was excellent" or "a robust debate ensued". They record what was discussed and what was decided.
- **Quote sparingly.** Direct quotation is reserved for cases where the exact words matter (a vote statement, a formal objection, a regulatory commitment), and is attributed by name.

---

## Quality Checklist

- [ ] The header carries date, time, timezone, location, chair, secretary, and document reference
- [ ] Attendees, apologies, and distribution are named with roles and modality
- [ ] Quorum status is recorded for governance meetings
- [ ] Every agenda item has a discussion summary, a decisions block, and an action-items block
- [ ] Every decision is verb-led, single-sentence, and traceable to an item
- [ ] Every action item has exactly one named owner, a due date, a status, and a priority
- [ ] The Decisions Log and Action Items table are consolidated and consistent with the per-item record
- [ ] Carry-over actions from previous meetings are revisited
- [ ] Next meeting date and location are stated
- [ ] Distribution list is explicit and matches the document's confidentiality marking
- [ ] No first-person voice, no editorial commentary, no verbatim transcription
- [ ] Decision-vs-discussion rubric was applied to every paragraph

---

## Common Mistakes

- **Transcribing instead of paraphrasing.** Minutes are not stenography. A 60-minute meeting should produce 1–3 pages, not 20.
- **First-person voice.** "We agreed" reads as informal notes. Use "the committee agreed" or "the steering body approved".
- **Decisions hidden in prose.** A decision buried in a paragraph is invisible. Surface every decision with a "**Decision:**" prefix and an ID.
- **Action items without owners or dates.** "Someone should follow up" is not an action. One name, one date, one status.
- **Discussion masquerading as decision.** "It was felt that…" is discussion. "The committee approved…" is a decision. Apply the rubric.
- **Forgetting carry-over actions.** Open items from previous meetings must reappear until closed. Otherwise the action list silently rots.
- **Omitting apologies.** Recording only who was present hides absences that may matter for governance. Record apologies explicitly.
- **Editorial commentary.** "A vigorous debate" or "a productive exchange" inserts opinion. Strip it.
- **Inconsistent IDs.** Restarting D-1, A-1 each meeting breaks cross-referencing. Maintain rolling counters per meeting series.
- **Late distribution.** Minutes lose value if circulated days after the meeting. Aim for the next business day for draft, one week for final.
- **No confidentiality marking.** Minutes may contain personal or commercial-sensitive data. Mark the classification at the top and align the distribution list to it.
- **Mixing minutes with agenda.** The agenda is what was planned; the minutes are what happened. Do not just publish the agenda as minutes with check marks.
- **Missing approvals.** Formal minutes are not final until approved at the next meeting. State the approval status in the header.
