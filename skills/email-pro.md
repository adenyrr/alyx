---
name: email-pro
description: Apply this methodology when the user asks the writer agent to draft, rewrite, or audit a professional email of any kind — cold outreach, follow-up, reschedule, polite decline, apology, introduction request, status update, deadline-extension request, or any other short-form business correspondence sent via email. Trigger keywords include "email", "write a follow-up", "reply to this", "professional email", "send a note", "mail pro", "courriel", "relance", "report ce rendez-vous", "annuler", "décliner". Use this skill for any email whose primary purpose is to maintain a working relationship or move a specific business outcome forward. Do NOT use it for cover letters (skills/cover-letter.md), CVs (skills/cv-resume.md), press releases (skills/press-release.md), long-form blog posts (skills/blog-post.md), or transactional system emails (notifications, receipts, password resets).
agents: [writer]
---

# Professional Email — Methodology

A professional email is a precision instrument: it must be readable in 15 seconds on a phone, carry one clear ask, leave the relationship intact, and survive being forwarded to a third party the writer never anticipated. This skill teaches the writer agent how to draft eight common business emails in English and French, with subject-line rules and CC/BCC/reply-all etiquette.

---

## When to Apply

Apply this skill when the user request implies:

- A first-touch cold email to a prospect, candidate, or collaborator
- A follow-up after a meeting, proposal, or unanswered thread
- Rescheduling, cancelling, or declining a meeting or commitment
- Politely declining an offer, request, or invitation
- Apologizing for a delay, mistake, or miscommunication
- Asking a contact for a warm introduction
- Sending a status update to internal or external stakeholders
- Requesting a deadline extension or scope change

Do NOT apply this skill for:

- Cover letters or motivation letters — delegate to `skills/cover-letter.md`
- A CV — delegate to `skills/cv-resume.md`
- A press release or external announcement — delegate to `skills/press-release.md`
- A blog post or thought-leadership article — delegate to `skills/blog-post.md`
- Marketing newsletter copy (different structure, opt-out rules)
- Transactional emails (account notifications, receipts) — these belong to product/dev

---

## Document Structure — Email Anatomy

Every professional email has the same skeleton:

1. **Subject line** — specific, action-oriented, ≤ 50 characters.
2. **Greeting** — appropriate register for the relationship.
3. **Opening line** — context or warm acknowledgement (NOT "I hope this finds you well" if that's all it says).
4. **Body** — one paragraph per idea, max 3 paragraphs.
5. **The ask** — one explicit, scoped request (or one piece of information).
6. **Sign-off** — register-matched, with name and minimal signature.

Aim for 100–150 words. Anything over 250 words demands a TL;DR at the top.

### Subject-line rules

A subject line is a contract with the reader: it must promise the email's content precisely. Rules:

- **≤ 50 characters** (phone preview truncates after ~45 on iOS, ~55 on Gmail mobile).
- **Specific over vague**: not "Quick question", but "Quick question on the Q3 forecast tab".
- **Action-oriented when an action is required**: "Action required: sign DocuSign by Fri 5pm" beats "Re: Contract".
- **Time-stamped if time-sensitive**: include the date or deadline.
- **No clickbait** ("You won't believe…"): destroys trust instantly in B2B.
- **No emojis in formal contexts**; sparingly in informal ones, and never two in a row.
- **One subject per thread**: change the subject only when the topic genuinely changes; do not change for a fresh thread on the same topic (use "Re:" instead).
- **Avoid spam triggers** in cold outreach: ALL CAPS, "FREE", "ACT NOW", excessive punctuation.

Subject-line examples:

| Bad | Good |
|---|---|
| Hi | Intro: Jordan Okafor → Camille Martin, payments lead |
| Update | Q2 status: 3 of 4 milestones met, slippage on launch |
| Question | Question: timing for the Berlin onsite (Sep vs Oct) |
| Following up | Following up: proposal sent 12 May |
| Sorry | Apology: Friday's report sent to wrong distribution list |
| Important!!! | Action required: legal sign-off needed by Thu 4pm |

### Greeting register

| Relationship | English | French |
|---|---|---|
| First contact, formal | Dear Ms./Mr. {{Lastname}}, | Madame {{Nom}}, / Monsieur {{Nom}}, |
| Cold, gender unknown | Dear {{Firstname Lastname}}, | Madame, Monsieur, |
| Established, professional | Hello {{Firstname}}, | Bonjour {{Prénom}}, |
| Warm internal colleague | Hi {{Firstname}}, | Bonjour {{Prénom}}, |
| Team distribution | Hi team, | Bonjour à tous, |
| Reply within active thread | (none) or Hi {{Firstname}}, | (none) or Bonjour {{Prénom}}, |

Avoid "Hey" in first or formal contact; "Greetings" sounds cold; "To whom it may concern" signals zero research.

### Opening line

The opening line is the second-most-read line after the subject. Do not waste it on "I hope this email finds you well" *alone* — pair it with context if you use it at all. Better patterns:

- **Refer to shared context**: "Following our conversation at the Lisbon offsite last week, …"
- **Refer to the trigger**: "I'm writing about the contract draft you shared on Tuesday."
- **Acknowledge time elapsed**: "It's been a while since we last spoke — I wanted to revisit the Q4 idea we discussed in March."
- **Compliment with substance** (cold): "Your post on multi-region failover landed at the exact moment my team is debating that trade-off."

### Body

- **One idea per paragraph**, separated by blank lines for scannability.
- **Lead with the why** before the what; the reader decides in 5 seconds whether to read on.
- **Bullets for ≥ 3 items**; prose for ≤ 2.
- **No walls of text**: anything over 3 paragraphs gets a bullet list or a TL;DR.
- **Hyperlinks**, not pasted URLs, for cleanliness.
- **Avoid embedded screenshots** unless essential — they break on many clients.

### The ask

Make the ask explicit, scoped, and time-bound:

- Not: "Let me know what you think."
- Yes: "Could you confirm by Thursday 17h CET whether we should proceed with option B?"
- Not: "Any chance you have time soon?"
- Yes: "Would Tuesday 13 June 10:00–10:30 CET work for a 30-minute call? If not, here are two alternatives: …"

If you have multiple asks, *number them*. If you have ≥ 4 asks, you have a project, not an email — schedule a meeting or a doc instead.

### Sign-off

| Register | English | French |
|---|---|---|
| Formal first contact | Sincerely, / Kind regards, | Cordialement, *(neutral)* / Bien à vous, *(slightly warm)* |
| Standard business | Best regards, / Best, | Cordialement, |
| Warm internal | Thanks, / Cheers, *(UK)* | Bien cordialement, / Merci, |
| Following heavy ask | Thank you, / With appreciation, | Avec mes remerciements, |
| Most formal (FR, to senior official) | n/a (use Sincerely) | Je vous prie d'agréer, Madame/Monsieur, mes salutations distinguées. |

Below the sign-off: full name, title, company, phone (optional), one URL max. Avoid 12-line signatures with quotes and inspirational images.

### CC / BCC / Reply-all etiquette

- **TO**: people who must act or respond.
- **CC**: people who must be informed but are not expected to respond. Adding someone to CC silently escalates the email — use with care.
- **BCC**: (i) to hide a distribution list from recipients (newsletter, announcement to a large group); (ii) to "drop" someone from a thread (introduce them in BCC, then say "moving Claire to BCC to spare her inbox"); (iii) for compliance archiving.
- **Never BCC** a colleague to a heated thread without telling them — it's politically toxic if discovered.
- **Reply-all** only when the reply genuinely concerns all recipients. The default reply should be to the sender.
- **"Reply-all-pocalypse"**: never reply-all to say "unsubscribe me", "thanks", "+1", "got it". Reply to sender only, or use the platform's reactions.
- **Introducing two people**: A introduces B and C; B and C move A to BCC on their first reply ("moving Anne to BCC and thanking her").

---

## Output Templates

Each template appears in English first, French *vous* second. Replace `{{...}}` with realistic content. Templates are **starting points** — adapt tone, register, and detail to context.

### Template 1 — Cold outreach

**Use when**: first-touch email to a stranger (prospect, candidate, expert) with no prior relationship.

**English**:

```
Subject: Quick intro: Stripe integrations — 15 min next week?

Dear Ms. Martin,

I came across your work on multi-region payments at NorthStar through your KubeCon EU talk last month — the section on idempotency under network partition was exactly what my team has been wrestling with.

I lead the platform team at Helix Pay (Series B, €30 M/month GMV) and we are about to make a similar architectural call. Would you be open to a 15-minute call in the next two weeks to compare notes? I'd value your perspective and would happily share what we have learned about the eventual-consistency edge cases if useful.

Two slots that work for me: Tue 27 May 09:00–09:15 CET, or Thu 29 May 14:00–14:15 CET. If neither fits, propose what suits you.

Best regards,

Jordan Okafor
Head of Platform, Helix Pay
jordan@helixpay.com · linkedin.com/in/jordanokafor
```

**Français**:

```
Objet : Brève prise de contact — paiements multi-régions, 15 min ?

Madame Martin,

Je suis tombé sur votre intervention à KubeCon EU le mois dernier sur les paiements multi-régions chez NorthStar — la partie sur l'idempotence sous partition réseau correspond exactement à un sujet que mon équipe étudie en ce moment.

Je dirige l'équipe Plateforme chez Helix Pay (série B, 30 M€/mois de GMV) et nous sommes sur le point de prendre une décision d'architecture similaire. Seriez-vous disponible pour un échange de 15 minutes dans les deux prochaines semaines ? Je serais ravi de bénéficier de votre regard, et je pourrais partager en retour ce que nous avons appris sur les cas limites de la cohérence à terme.

Deux créneaux qui me conviennent : mardi 27 mai 09h00–09h15 CET, ou jeudi 29 mai 14h00–14h15 CET. Si ces horaires ne vous conviennent pas, proposez ce qui vous arrange.

Cordialement,

Jordan Okafor
Responsable Plateforme, Helix Pay
jordan@helixpay.com · linkedin.com/in/jordanokafor
```

### Template 2 — Follow-up (after meeting / proposal)

**Use when**: re-engaging after a meeting concluded with action items, or a proposal you sent has had no response.

**English**:

```
Subject: Recap + next steps from yesterday's call

Hi Claire,

Thanks for the call yesterday — useful to align on the Q3 scope. Capturing the agreed next steps in writing so we have a single source of truth:

1. I'll send the revised SOW (option B + ramp-down clause) by Thu 30 May EOD.
2. You'll confirm legal's position on the data-residency annex by Tue 4 June.
3. We'll meet again Wed 5 June 10:00 CET to sign off and plan kickoff.

Let me know if any of the above misrepresents what we discussed. Otherwise, talk Wednesday.

Best,
Jordan
```

**For an unanswered proposal**:

```
Subject: Following up: Helix proposal sent 12 May

Hi Claire,

Circling back on the proposal I sent on 12 May for the Q3 platform work. I know your week was tight before the board meeting — wanted to check whether you've had a chance to review, and whether anything in the scope or pricing needs adjusting.

If it's easier, a 15-minute call this week would let us close any open questions in one pass. Free Wed 22 May 14:00 CET or Thu 23 May 11:00 CET?

Best,
Jordan
```

**Français**:

```
Objet : Suite à notre échange : récapitulatif et prochaines étapes

Bonjour Claire,

Merci pour notre échange d'hier — nous avons bien avancé sur le périmètre Q3. Je récapitule par écrit les prochaines étapes pour que nous ayons une référence commune :

1. Je vous envoie le devis révisé (option B + clause de désengagement) d'ici jeudi 30 mai en fin de journée.
2. Vous me confirmez la position du juridique sur l'annexe « résidence des données » d'ici mardi 4 juin.
3. Nous reprenons le mercredi 5 juin à 10h00 CET pour valider et planifier le démarrage.

Dites-moi si l'un de ces points ne correspond pas à ce que nous avons convenu. Sinon, à mercredi.

Cordialement,
Jordan
```

### Template 3 — Reschedule / cancel

**Use when**: you need to move or cancel a previously scheduled meeting.

**English**:

```
Subject: Reschedule request: our Thu 30 May 11:00 CET call

Hi Claire,

Apologies for the late change — a board prep block landed on Thursday morning that I can't move. Could we reschedule our 11:00 CET call?

Three alternatives that work on my side:
- Thu 30 May, 16:00–17:00 CET
- Fri 31 May, 10:00–11:00 CET
- Mon 3 June, 14:00–15:00 CET

If none of these fit, name what works and I'll make it work. Sorry again for the disruption.

Best,
Jordan
```

**To cancel without reschedule**:

```
Subject: Cancelling Thu 30 May 11:00 — will revisit in June

Hi Claire,

The kickoff has slipped on our side and the agenda for Thursday no longer holds together. Rather than meet without substance, I'd like to cancel for now and re-propose dates once we've locked our internal scope — likely mid-June. I'll be back in touch with concrete proposals by 7 June.

Apologies for the late change, and thank you for your flexibility.

Best,
Jordan
```

**Français**:

```
Objet : Demande de report : notre échange du jeudi 30 mai 11h00 CET

Bonjour Claire,

Désolé pour ce changement tardif — une préparation de comité s'est imposée jeudi matin que je ne peux pas décaler. Pourrions-nous reporter notre échange de 11h00 CET ?

Trois créneaux qui fonctionnent de mon côté :
- jeudi 30 mai, 16h00–17h00 CET
- vendredi 31 mai, 10h00–11h00 CET
- lundi 3 juin, 14h00–15h00 CET

Si aucun ne vous convient, indiquez-moi ce qui vous arrange et je m'adapterai. Encore désolé pour la gêne occasionnée.

Cordialement,
Jordan
```

### Template 4 — Decline gracefully

**Use when**: declining a job offer, partnership, speaking invitation, or meeting request.

**English (declining a meeting request from a vendor)**:

```
Subject: Re: 30-min intro on observability tooling

Hi Mark,

Thanks for reaching out and for the context on the platform. We're not actively evaluating observability tooling this quarter — our current stack covers the Q3 roadmap. I'd rather not take 30 minutes of your time on a conversation that can't lead anywhere useful right now.

Happy to circle back if/when we re-open this in 2027. In the meantime, please don't take silence as disinterest if I don't reply to future updates; I'll reach out if the picture changes.

Best,
Jordan
```

**Declining a job offer**:

```
Subject: Decision on the {{Role Title}} offer — with thanks

Dear Ms. Chen,

Thank you for the offer to join {{Company}} as {{Role Title}}, and for the time you and the team invested in the process. It was a difficult decision, but I've accepted another opportunity that more closely matches my plans for the next two years.

I have a lot of respect for what you're building, and I hope our paths cross again. Please pass my thanks to Priya, Marc, and Anna — they each made the conversations memorable.

With appreciation,

Jordan Okafor
```

**Français (décliner un partenariat)**:

```
Objet : Réponse à votre proposition de partenariat

Bonjour Sophie,

Merci pour votre proposition et pour le temps consacré à nous la présenter la semaine dernière. Après discussion en interne, nous ne donnerons pas suite : nos priorités produit du second semestre ne laissent pas l'espace nécessaire pour intégrer correctement ce partenariat, et nous préférons décliner plutôt que vous engager dans un échange qui n'aboutirait pas.

Cette décision n'est en rien un jugement sur la qualité de votre proposition, que nous avons trouvée solide. Nous serons heureux de reprendre la discussion début 2027 si le sujet est toujours d'actualité de votre côté.

Cordialement,
Jordan Okafor
```

### Template 5 — Apology (delay, mistake, miscommunication)

**Use when**: something went wrong and you are responsible (or partly responsible).

**English (sending sensitive data to wrong recipient)**:

```
Subject: Apology + corrective action: Friday's report distribution error

Hi all,

Yesterday at 17:42 CET I sent the Q2 customer-revenue report to the wider sales@ list instead of the intended sales-leads@ alias. The report contains aggregate revenue figures that should have stayed within the leadership group.

What I've done since:
- 18:05 CET: recalled the message via Google Workspace; ~ 30 of 84 recipients had already opened it.
- 18:15 CET: notified data protection (Marc) and security (Anna); no PII was included.
- 09:00 CET today: posted a correction in #sales-announce asking recipients to delete the original.

What I will do going forward:
- Send all leadership reports from a personal draft rather than reply-templates that auto-populate recipients.
- Add a 60-second "recipient sanity check" to my own checklist before any leadership-distribution send.

I'm sorry for the noise this caused and for the additional review work this creates for Marc and Anna. Happy to discuss in person if useful.

Jordan
```

**Français (retard sur livrable)**:

```
Objet : Excuses et nouveau planning pour le rapport Q2

Bonjour Claire,

Je vous dois des excuses : le rapport Q2 que je m'étais engagé à vous transmettre vendredi 17 mai ne vous est pas parvenu. La cause est un retard dans la consolidation des données du module CRM, dont je n'ai pris la mesure que mercredi soir — j'aurais dû vous prévenir à ce moment-là plutôt qu'à l'échéance.

Nouvelle date d'engagement : mardi 21 mai en fin de journée, version validée et chiffres réconciliés. Si vous souhaitez recevoir d'ici là une version partielle pour le comité de jeudi, dites-le moi et je vous la transmets dès ce soir.

Merci pour votre patience, et désolé encore pour la gêne occasionnée.

Cordialement,
Jordan
```

### Template 6 — Introduction request

**Use when**: asking a contact to introduce you to a third party they know.

**English (double opt-in style — preferred)**:

```
Subject: Quick intro ask: would you be open to connecting me with Priya Shah?

Hi Marc,

Hope your sprint is wrapping well. A small ask: I'm exploring how Verdant approaches sustainable-sourcing claims in their marketing — I noticed Priya Shah is their CMO and I think you worked with her at Allbirds.

If you're comfortable, would you be willing to forward the blurb below to Priya, and let her decide whether to connect? If anything in here doesn't fit your read of her, please just say so — no awkwardness either way.

---
"I'm Jordan Okafor, marketing lead at {{Company}}. I'm researching how brands operationalize sustainability claims internally (audit cadence, who owns the data, how marketing and ops align). I'd value 20 minutes of Priya's perspective in the next month if she's open to it. Happy to share notes back in return."
---

Thanks either way, Marc.

Best,
Jordan
```

**Français (demande de mise en relation)**:

```
Objet : Petite demande : pourriez-vous me mettre en relation avec Priya Shah ?

Bonjour Marc,

J'espère que votre sprint touche tranquillement à sa fin. Une petite demande : j'étudie la façon dont Verdant aborde ses claims de sourcing durable côté marketing — j'ai vu que Priya Shah en est la CMO et il me semble que vous avez travaillé avec elle chez Allbirds.

Si vous êtes à l'aise, accepteriez-vous de transférer le paragraphe ci-dessous à Priya, en la laissant décider de donner suite ? Si quelque chose ne correspond pas à votre lecture d'elle, dites-le-moi sans hésiter — aucun souci dans un sens comme dans l'autre.

---
« Je suis Jordan Okafor, responsable marketing chez {{Société}}. J'étudie la manière dont les marques opérationnalisent leurs engagements de durabilité en interne (cadence d'audit, gouvernance de la donnée, alignement marketing/opérations). Je serais reconnaissant de pouvoir bénéficier de 20 minutes du regard de Priya dans le mois qui vient si elle y est ouverte. Je serais heureux de partager mes notes en retour. »
---

Merci en tout cas, Marc.

Cordialement,
Jordan
```

### Template 7 — Status update to stakeholders

**Use when**: weekly/biweekly written update to a leadership audience or external client.

**English**:

```
Subject: Helix platform — week 21 status (on track; one risk)

Hi all,

**TL;DR**: 3 of 4 milestones on track for the 30 June release; 1 risk on the data-migration window we need to surface now.

**Progress this week**
- Settlement service: feature-complete; staging perf at 99.97% / p95 110 ms.
- Webhooks v2: contract signed off by 4 of 6 design partners.
- Observability rollout: OTLP pipeline live in pre-prod; cardinality within budget.

**Risks**
- Data migration window (28 June Sat 22:00–04:00 CET): legal flags that two enterprise contracts forbid downtime > 2h. Mitigation: dual-write window of 14 days; final cutover at 02:00 CET. Need acknowledgement from sales lead by Fri 23 May.

**Asks**
- Sales lead: confirm acknowledgement of dual-write plan (see above) by Fri 23 May 17:00 CET.
- Finance: please pre-approve the €18k AWS reserved instance purchase for July; ticket linked.

Full dashboard: [link]. Next update Mon 26 May.

Best,
Jordan
```

**Français**:

```
Objet : Plateforme Helix — point semaine 21 (dans les temps ; 1 risque)

Bonjour à tous,

**Résumé** : 3 des 4 jalons sont dans les temps pour la mise en production du 30 juin ; 1 risque sur la fenêtre de migration de données à remonter dès maintenant.

**Avancement de la semaine**
- Service de règlement : périmètre fonctionnel terminé ; en pré-production à 99,97 % / p95 110 ms.
- Webhooks v2 : contrat validé par 4 des 6 partenaires de design.
- Observabilité : pipeline OTLP en pré-production ; cardinalité dans la cible.

**Risques**
- Fenêtre de migration des données (samedi 28 juin 22h00–04h00 CET) : le juridique signale que deux contrats grands comptes interdisent une indisponibilité > 2h. Mitigation : fenêtre de double écriture de 14 jours ; bascule finale à 02h00 CET. Confirmation attendue du responsable commercial d'ici vendredi 23 mai.

**Demandes**
- Responsable commercial : accusé de réception du plan de double écriture (voir ci-dessus) d'ici vendredi 23 mai 17h00 CET.
- Finance : merci de pré-approuver l'achat d'instances réservées AWS pour juillet (18 k€) ; ticket en lien.

Tableau de bord complet : [lien]. Prochain point lundi 26 mai.

Cordialement,
Jordan
```

### Template 8 — Deadline extension request

**Use when**: asking for more time on a deliverable, with reason and revised plan.

**English**:

```
Subject: Extension request: Q2 report — new date 28 May (was 21 May)

Hi Claire,

I'd like to ask for a one-week extension on the Q2 report, moving the delivery from Tue 21 May to Tue 28 May 17:00 CET. The cause is a data-integrity issue we found yesterday in the CRM extract — two months of pipeline data were double-counted, and we need to re-derive the figures cleanly rather than ship numbers that won't survive scrutiny in the board meeting.

What this changes:
- Report delivery: Tue 28 May, 17:00 CET.
- Board pack assembly: I'll send the final numbers by 17:00 so your team can fold them in by EOD Wed 29 May.
- Board meeting (Fri 31 May) remains on schedule.

What this does not change:
- Scope, format, or audience of the report.
- The forward forecast: that work is already complete and I can share it on the original date if useful.

Apologies for the disruption. Happy to discuss alternatives if a week is too much — anything from 4 days upwards would be workable on our side.

Best,
Jordan
```

**Français**:

```
Objet : Demande de report : rapport Q2 — nouvelle date 28 mai (au lieu du 21 mai)

Bonjour Claire,

Je sollicite un report d'une semaine sur le rapport Q2, soit une livraison repoussée du mardi 21 mai au mardi 28 mai 17h00 CET. La cause est un problème d'intégrité de données détecté hier dans l'extraction CRM : deux mois de pipeline ont été comptabilisés en double, et il nous faut recalculer proprement plutôt que vous transmettre des chiffres qui ne résisteraient pas à l'examen en comité.

Conséquences :
- Livraison du rapport : mardi 28 mai 17h00 CET.
- Préparation du dossier de comité : je vous transmets les chiffres définitifs à 17h00 afin que votre équipe puisse les intégrer en fin de journée mercredi 29 mai.
- Comité du vendredi 31 mai : maintenu à la date prévue.

Inchangé :
- Périmètre, format et destinataires du rapport.
- La projection prospective : ce travail est déjà finalisé et peut vous être transmis à la date initiale si utile.

Désolé pour la gêne occasionnée. Je suis ouvert à toute alternative si une semaine vous paraît trop : un report de 4 jours minimum reste tenable de notre côté.

Cordialement,
Jordan
```

---

## Style & Tone Guidelines

- **Voice**: clear, warm, professional. Default to first-person ("I"). Use "we" only when speaking for a team you can commit on behalf of.
- **Register**: match the relationship. Cold and corporate → formal English / *vous* French. Internal peer → conversational. Never *tu* in French business email unless the relationship is established.
- **Brevity**: ruthlessly cut. If a sentence can be removed without changing meaning, remove it.
- **Mobile-first**: write for a 4-inch screen. Short paragraphs, blank lines, bullets when listing.
- **Specificity**: dates with day-of-week and time zone ("Thu 30 May 11:00 CET"), not "next week". Numbers with units. Names spelled correctly.
- **Lead with the ask** if the recipient is senior or busy; lead with context if the recipient needs it to engage.
- **Read once aloud** before sending — typos and tone problems surface in 30 seconds.
- **One thread per topic.** Do not braid two unrelated conversations into one thread; spawn a new one with a clear subject.
- **Tone-check for politicized words**: "urgent", "ASAP", "I need", "you must" land harder than the writer expects. Prefer "Could you confirm by…", "Would Tuesday work for…".

---

## Quality Checklist

- [ ] Subject line is ≤ 50 characters, specific, and accurately describes the content
- [ ] Greeting matches the relationship register (formal vs. warm, English vs. French)
- [ ] Opening line adds context — not just "I hope this finds you well"
- [ ] Body has one idea per paragraph, no wall of text, total ≤ 150 words ideally
- [ ] The ask is explicit, scoped, and time-bound (deadline or proposed slots)
- [ ] CC and BCC are correctly used; no surprise additions to politically sensitive threads
- [ ] No "reply-all" when "reply" would do
- [ ] Times include time zone; dates include day-of-week
- [ ] Sign-off matches the relationship register
- [ ] Signature is concise (name, title, company, one URL max)
- [ ] French version uses *vous*, *Madame/Monsieur* honorifics, and *Objet* in subject
- [ ] No banned phrases ("Hey", "To whom it may concern", "Please advise" as lone instruction)
- [ ] No emojis in formal contexts; sparingly elsewhere
- [ ] Spelling of recipient name and company verified
- [ ] If sensitive content, would you be comfortable seeing this forwarded?
- [ ] Read once aloud before sending

---

## Common Mistakes

- **Vague subject line.** "Quick question" leaves the recipient unsure whether to open. Be specific.
- **Burying the ask.** The recipient should know what is wanted by the end of the second paragraph.
- **No deadline.** "When you have a chance" is a black hole. State the date you actually need.
- **Reply-all-pocalypse.** Replying "thanks" to 60 people. Use reply (not reply-all) for acknowledgements.
- **Surprise CC.** Adding a senior person to a CC field without telling the original recipient is read as an escalation.
- **BCC as a weapon.** Secretly CC'ing a manager into a heated thread is unethical and rarely stays hidden.
- **Walls of text on mobile.** Six-line paragraphs scroll forever on a phone. Break them up.
- **Passive-aggressive politeness.** "As per my previous email" reads as a slap; "Per the note I sent on 12 May, …" is neutral.
- **Apology that doesn't own.** "I'm sorry if you were offended" is not an apology. State what you did, what you've done about it, and what changes.
- **Decline that drags.** A polite "no" delivered in one short paragraph is kinder than three paragraphs of hedging.
- **Wrong honorific or misspelled name in French.** Triple-check `Madame` vs `Monsieur`. Never abbreviate (`Mme.`, `M.`) in the salutation of a formal email.
- **`tu` in first-contact French email.** Default *vous* always; let the recipient switch first.
- **Casual sign-off in formal context.** "Cheers" to a French banking client is jarring.
- **Long signature block.** Strip quotes, inspirational images, and tracking pixels in formal contexts.
- **Sending in anger.** Draft, save, sleep on it. Then send (or, often, don't).
