---
name: blog-post
description: Apply this methodology when the user asks the writer agent to draft, rewrite, structure, or audit a blog post, article, long-form content piece, thought-leadership piece, technical write-up, opinion essay, or newsletter article for publication on a website or platform like Medium, Substack, dev.to, or a company blog. Trigger keywords include "blog post", "article", "write up", "long-form", "thought leadership", "deep dive", "explainer", "post about X", "newsletter issue", "Substack post". Use this skill for documents whose primary purpose is to inform, persuade, or build authority with a reader who arrived by search or subscription. Do NOT use it for press releases (skills/press-release.md), professional emails (skills/email-pro.md), CVs (skills/cv-resume.md), cover letters (skills/cover-letter.md), or short social-media posts (different length, different cadence).
agents: [writer]
---

# Blog Post / Article — Methodology

A blog post is a contract with a reader who arrived through search, social, or subscription and has roughly twelve seconds to decide whether to keep reading. It must promise a payoff in the first paragraph, deliver it in the body, and earn the right to a call-to-action at the end. This skill teaches the writer agent how to compose well-structured, SEO-friendly, scannable blog posts in clear modern prose.

---

## When to Apply

Apply this skill when the user request implies:

- A 600–2,500 word article published on a company blog, Substack, Medium, dev.to, or personal site
- A thought-leadership piece intended to build authority for an author or company
- A technical explainer, post-mortem write-up, or how-to with substance beyond a quick reference
- An opinion essay or argumentative post taking a defensible position
- A newsletter issue meant to anchor a recurring publication
- Rewriting an existing post for SEO, scannability, or voice consistency

Do NOT apply this skill for:

- Press releases — `skills/press-release.md`
- Professional emails or follow-ups — `skills/email-pro.md`
- CVs / resumes — `skills/cv-resume.md`
- Cover letters — `skills/cover-letter.md`
- Short social-media posts (LinkedIn ≤ 300 words, X threads) — different cadence and structure
- Product landing-page copy — sales-driven, different conversion goal
- API or technical reference documentation — has its own structure (parameters, returns, examples)
- Academic papers — peer-reviewed format, IMRaD structure, citations

---

## Document Structure

A modern blog post follows a near-universal skeleton, designed for both linear reading and scanning:

1. **Title (H1)** — ≤ 60 characters, contains the target keyword, promises a payoff.
2. **Meta description** — ≤ 155 characters, used by search engines and link previews.
3. **Featured image** with descriptive alt text.
4. **Author + date + reading time** (≈ 200 words per minute).
5. **Hook** — 1–2 sentences that promise the payoff and create curiosity.
6. **Context** — 1 paragraph: why this matters *now*.
7. **Thesis** — 1–2 sentences: the single argument or takeaway the rest of the post defends.
8. **Body** — 3–5 H2 sections, each with optional H3 sub-sections, bullets, quotes, code blocks, images.
9. **Counterargument acknowledgement** — 1 H2 ("But what about…?") that anticipates the strongest objection.
10. **Conclusion** — recap of thesis + call to action.
11. **Author bio** — 2–3 sentences.
12. **Suggested reading** — 3–5 related links.

Length targets:

- **Short-form**: 600–1,200 words. News reaction, opinion, tutorial. 3–4 minute read.
- **Standard**: 1,200–2,000 words. Most thought-leadership, technical explainers. 6–10 minute read.
- **Long-form**: 2,000–3,500 words. Deep dives, post-mortems, comprehensive guides. 10–18 minute read.

---

## Section-by-Section Writing Guide

### Title (H1)

The single most-tested element on the page. It appears in search results, social shares, and email subjects.

Rules:

- **≤ 60 characters** so Google does not truncate.
- **Contains the primary keyword phrase** users would search.
- **Promises a specific payoff**, not a vague topic.
- **Number-front titles** outperform on click-through ("7 things…", "Why we cut our…by 38%").
- **Avoid clickbait**: "You won't believe…" damages domain authority over time.
- **Sentence case or title case** depending on publication style — be consistent.

Compare:

| Bad | Good |
|---|---|
| Database Things | How We Cut p95 Query Latency from 480ms to 90ms |
| Some Thoughts on Caching | A Practical Guide to HTTP Caching for Backend Engineers |
| Welcome to Our Blog | Why We Built Our Own Feature Flag System (and Open-Sourced It) |
| AI Stuff | When to Use a Vector Database (and When Not To) |

### Meta description

A 140–155 character paragraph that summarizes the article and includes the keyword. It appears under the title in search results.

Pattern: `{{What the article is about}}. {{What the reader will gain}}.`

Example: `A practical guide to HTTP caching for backend engineers — Cache-Control, ETags, stale-while-revalidate, and when each one matters in production.` (149 chars)

### Featured image + alt text

- Featured image at the top, above or just below the title.
- Alt text describes the image for screen readers and search engines. Be literal: "Diagram of three-tier caching architecture: browser → CDN → origin", not "image of caching".
- Every subsequent image also has alt text.
- File names also matter: `caching-architecture-diagram.png` beats `IMG_2347.png`.

### Hook (1–2 sentences)

The most-read sentences of the post. Their job is to make the reader commit to paragraph 2.

Effective hook patterns:

- **The specific outcome**: "Last quarter we cut our p95 query latency from 480ms to 90ms on a 4TB database. Here's what worked, what didn't, and what we'd do differently."
- **The surprising fact**: "70% of the websites you visit do not set a single Cache-Control header. The cost of this oversight is measured in petabytes per day."
- **The contrarian claim**: "You probably do not need a vector database. Here's how to tell."
- **The named pain**: "If you've ever been paged at 3am for a stuck Kafka consumer, this post is for you."

Avoid:

- "In today's fast-paced world…" (everyone has read this; nobody finishes the paragraph).
- "Have you ever wondered…" (rhetorical question hooks were tired by 2015).
- "I'm excited to share…" (excitement is the reader's job).

### Context (1 paragraph)

Why this matters *now*. Tie to a recent event, a market shift, a regulation, a release. This earns the reader's time.

Pattern: `Since {{recent thing}}, {{change in conditions}}. That makes {{topic}} {{newly relevant}}.`

### Thesis (1–2 sentences)

The single argument the post defends. State it explicitly. The reader should be able to quote it back after reading.

Pattern: `The argument of this post is that {{claim}}, because {{reason}}.`

Example: `The argument of this post is that most teams adopt vector databases too early — a Postgres + pgvector setup serves the first 10M embeddings cheaper, faster to operate, and with simpler failure modes.`

### Body — 3–5 H2 sections

Each H2 advances the argument by one step. A typical 1,500-word post has 4 H2s of roughly 250–350 words each.

Structure per H2:

- **H2 heading** that previews the section's claim, not its topic ("Vector databases are optimized for the wrong cost curve" beats "Cost comparison").
- **Opening sentence** that restates the H2 in a complete sentence.
- **Evidence**: data, code, screenshot, quote, citation. Every claim needs a support.
- **Optional H3 sub-sections** when the H2 has 2–3 sub-points.
- **Optional bullet list** when listing ≥ 3 items.
- **Closing sentence** that summarizes the section's contribution to the thesis.

H3 sub-sections are useful for tutorials and comparisons; avoid them in opinion essays.

### Bullets, quotes, code, images — when to use which

- **Bullets**: 3+ parallel items. Prose is better for 2 items.
- **Numbered lists**: when order matters (steps in a procedure, ranked items).
- **Block quotes**: external citation, customer voice, or punchy single line you want to emphasize.
- **Code blocks**: language-tagged for syntax highlighting; ≤ 30 lines per block.
- **Images / diagrams**: every 400–600 words breaks up the page; always with alt text and caption.
- **Tables**: comparisons across ≥ 3 dimensions and ≥ 3 entries.

### Counterargument acknowledgement

The post earns trust by stating the strongest objection and answering it. One H2 section near the end:

> ## But what about {{strongest counterargument}}?

Two patterns:

- **Concede partially**: "This is true in case X, where the recommended approach is Y." Acknowledge the limit of the argument.
- **Refute with evidence**: "This sounds right but the data show otherwise — at scale Z, the cost shifts."

Skipping the counterargument signals the author has not thought past their own thesis; including it doubles perceived credibility.

### Conclusion

Two-part:

1. **Recap of thesis** in one fresh sentence (not a copy-paste of the intro).
2. **Call to action** — what the reader should do next. Pick ONE:
   - "Subscribe to the newsletter for the next post in this series."
   - "Try the example in this repo: {{URL}}."
   - "Email us if you've solved this differently — we'd love to learn."
   - "Share this with the colleague who'd disagree."

Avoid: "Thanks for reading!" (passive), "Let me know what you think in the comments!" (lazy), no CTA at all (wastes the moment).

### Author bio (2–3 sentences)

Pattern: `{{Name}} is {{role at company}}, where they {{specific responsibility}}. Previously {{relevant prior credential}}. Find them at {{URL or social}}.`

### Suggested reading

3–5 related links — ideally a mix of:

- 1–2 internal links (other posts on the same site that go deeper or sideways).
- 1–2 external links (the authoritative sources you cited or built upon).
- 0–1 link to a tool, repo, or paper.

---

## SEO Basics for the Writer Agent

SEO has matured beyond keyword stuffing into reader-experience signals. Apply these rules invisibly while writing well:

1. **Primary keyword in title (H1), meta description, first 100 words, and at least one H2.** Frequency 0.5–1.5% of total words (≈ 1 mention per 100 words).
2. **One H1 per page only** — the post title. Subsequent headings start at H2.
3. **Hierarchical headings** — H2 → H3 → H4. Do not jump levels (no H2 followed by H4).
4. **Alt text on every image**, descriptive of the image content.
5. **Descriptive file names** for images.
6. **Internal links** to 2–4 other posts on the same site; use descriptive anchor text ("read our HTTP caching guide", not "click here").
7. **External links** to authoritative sources — earn trust and avoid orphan claims.
8. **Reading time** displayed at the top (≈ 200 words per minute; for technical content with code, 150 wpm is more honest).
9. **URL slug** is short and keyword-rich: `/blog/http-caching-guide`, not `/blog/2026/05/21/my-thoughts-on-caching-and-related-topics`.
10. **Last-updated date** for evergreen posts, refreshed when the post is materially edited.
11. **No keyword stuffing** — Google's spam detection penalizes repetition above ~3%.
12. **Schema markup** (JSON-LD `Article`) helps but is the platform's job, not the writer's.

---

## Reading-Time Estimation Rule

`Reading time (minutes) = total words / 200`, rounded up. Display as "5-minute read".

Adjustments:

- Heavily technical with code: divide by 150 instead of 200.
- Listicles with short bullets: divide by 250 (skim-friendly).
- Posts with > 30% code: count code lines as 0.5 words each.

---

## Output Template

```markdown
---
title: "{{60-char title with primary keyword}}"
meta_description: "{{155-char summary with primary keyword}}"
author: "{{Author Name}}"
date: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD if updated}}"
tags: [{{tag1}}, {{tag2}}, {{tag3}}]
slug: "{{kebab-case-slug-with-keyword}}"
reading_time: "{{N}}-minute read"
featured_image: "/images/{{descriptive-filename}}.png"
featured_image_alt: "{{literal description of what the image shows}}"
---

# {{Title — H1, identical to frontmatter title}}

*By {{Author Name}} · {{Month DD, YYYY}} · {{N}}-minute read*

![{{Literal description of the image}}](/images/{{descriptive-filename}}.png)

{{Hook: 1–2 sentences that promise the payoff. Specific outcome, surprising fact, contrarian claim, or named pain.}}

{{Context: 1 paragraph on why this matters now — recent event, market shift, release, regulation. Earn the reader's time.}}

**The argument of this post is that {{thesis claim}}**, because {{single supporting reason}}. The rest of the post walks through {{N}} pieces of evidence and addresses the strongest counterargument.

## {{H2 #1 — section's claim, not its topic}}

{{Opening sentence restating the H2 as a complete sentence.}}

{{Evidence paragraph: data, code, citation, screenshot, quote. Specific, sourced, defensible.}}

### {{Optional H3 sub-section}}

{{Sub-section content if the H2 has 2–3 sub-points.}}

{{Closing sentence connecting this section back to the thesis.}}

## {{H2 #2 — next step in the argument}}

{{Opening sentence.}}

{{Evidence — often with a list or table.}}

| {{Column 1}} | {{Column 2}} | {{Column 3}} |
|---|---|---|
| {{value}} | {{value}} | {{value}} |
| {{value}} | {{value}} | {{value}} |

{{Closing sentence.}}

## {{H2 #3 — next step}}

{{Opening sentence.}}

```{{language}}
// Code block, ≤ 30 lines, with comments only where they add meaning
```

{{Explanation of what the code shows and why it matters.}}

## {{H2 #4 — final supporting section, optional}}

{{Opening sentence.}}

{{Evidence.}}

{{Closing sentence.}}

## But what about {{strongest counterargument}}?

{{Two-sentence acknowledgement of the objection in its strongest form.}}

{{Two-paragraph response: concede partially with the conditions under which the objection holds, then explain why the thesis still stands in the conditions the post addresses.}}

## Wrapping up

{{Fresh one-sentence recap of the thesis — not a copy-paste of the intro.}}

{{Single call to action: subscribe, try the repo, email back, share with a specific person.}}

---

**About the author**

{{Author Name}} is {{role at company}}, where they {{specific responsibility}}. Previously {{relevant prior credential}}. Find them at {{URL or social handle}}.

**Suggested reading**

- [{{Internal post title}}]({{URL}}) — the deep dive on the technique used above.
- [{{Internal post title}}]({{URL}}) — the post that originally proposed {{related idea}}.
- [{{External authoritative source}}]({{URL}}) — the canonical reference on {{topic}}.
- [{{Tool or repo}}]({{URL}}) — the open-source implementation discussed in section {{N}}.
```

---

## Style & Tone Guidelines

- **Voice**: second person ("you") for tutorials and explainers; first person plural ("we") for company posts and post-mortems; first person singular ("I") for opinion essays. Be consistent within a post.
- **Tense**: present tense as the default ("HTTP caching matters because…"). Past tense for war stories and post-mortems ("Last March, our checkout latency tripled overnight."). Avoid bare future.
- **Sentence length**: vary. A run of long sentences exhausts; a run of short ones nags. Mix.
- **Active voice as default**, passive only when the actor is unknown or irrelevant ("The system was deployed in 2019" is fine if who deployed it does not matter).
- **Specificity**: numbers over adjectives ("38% faster" beats "much faster"), named tools over categories ("PostgreSQL" beats "the database"), dated facts over timeless claims ("As of May 2026" beats "Currently").
- **Concrete examples**: every abstract claim earns one example. If you cannot produce an example, the claim is not concrete enough to publish.
- **Cadence**: open with a sentence under 15 words. End paragraphs with sentences that pull the reader into the next paragraph.
- **Adverb diet**: cut "very", "really", "quite", "actually", "basically", "literally", "just" (when used as a softener).
- **Cliché ban**: "at the end of the day", "moving the needle", "low-hanging fruit", "deep dive" (used too often), "game-changer", "leverage" (as a verb when "use" works).
- **Inclusive language**: "they/them" for generic third person; replace "guys" with "folks" / "team" in addresses to mixed groups.
- **Personality**: a small amount of opinion and humor lifts a post from documentation; too much undermines authority. One playful aside per 1,000 words is a sensible ceiling.

---

## Quality Checklist

- [ ] Title is ≤ 60 characters, contains the primary keyword, promises a specific payoff
- [ ] Meta description is ≤ 155 characters and contains the keyword
- [ ] Featured image with literal, descriptive alt text
- [ ] Reading time displayed (≈ 200 wpm; 150 wpm for code-heavy)
- [ ] Hook is 1–2 sentences and avoids banned openers ("In today's fast-paced world…", "Have you ever wondered…")
- [ ] Context paragraph explains why the topic matters *now*
- [ ] Thesis is stated explicitly in one or two sentences
- [ ] Body has 3–5 H2 sections; each H2 advances the argument
- [ ] Heading hierarchy is correct: one H1, then H2s, optionally H3s — no skipped levels
- [ ] Primary keyword appears in title, meta, first 100 words, and ≥ 1 H2; total density 0.5–1.5%
- [ ] At least one image, table, or code block per 600 words for scannability
- [ ] All images have descriptive alt text
- [ ] Counterargument section is present and substantive
- [ ] Conclusion gives a fresh recap (not a copy of the intro) and one specific CTA
- [ ] Author bio of 2–3 sentences with a link
- [ ] Suggested reading: 3–5 links, mix of internal and external
- [ ] Internal links use descriptive anchor text, not "click here"
- [ ] No banned clichés ("at the end of the day", "moving the needle", "deep dive", "game-changer")
- [ ] No adverb stuffing ("very", "really", "actually", "literally")
- [ ] Voice and tense are consistent throughout
- [ ] URL slug is kebab-case, short, keyword-rich
- [ ] Last-updated date set when republishing edited content

---

## Common Mistakes

- **Title that hides the payoff.** "Thoughts on Caching" tells the reader nothing; "Cut p95 by 80% with the Right Cache-Control Headers" earns the click.
- **No thesis.** A post that wanders for 1,500 words without a single sentence stating *the argument* is a notebook entry, not a published post.
- **Wall of text.** Paragraphs longer than 5 lines on a phone are skipped. Break them up.
- **Heading hierarchy violations.** H2 followed by H4 breaks screen readers and search-engine outlines.
- **Keyword stuffing.** Repeating the keyword every two sentences trips spam detection and reads as written-by-bot.
- **No internal links.** Wastes the SEO benefit of the site's existing content and the reader's chance to go deeper.
- **No counterargument.** Reads as motivated reasoning; loses the reader who already disagrees.
- **Generic CTA.** "Thanks for reading!" wastes the most committed reader you have — the one who finished.
- **Borrowed authority instead of original work.** A post that is 80% quotes from other posts adds no value. The author must contribute new evidence, original synthesis, or a clear opinion.
- **No reading-time estimate.** Robs the reader of an informed decision about whether to start.
- **Stock photo at the top.** A diagram, screenshot, or photo *of the actual thing* earns trust; a generic "person at laptop" photo does the opposite.
- **Forgetting the slug.** A long auto-generated URL is unshareable and unmemorable.
- **Inconsistent voice.** Switching from "you" to "we" to "I" mid-post jars the reader.
- **Adjective inflation.** "Truly groundbreaking" is two banned words in one phrase.
- **Last paragraph is "Conclusion: ".** Use a real header that says something ("Wrapping up", "What this means for your team", "The bottom line").
- **Publishing without proofreading.** A typo in the H1 is forever — search engines cache it, social shares fix it, the author wears it.
