---
name: plain-language
description: Apply plain-language (vulgarisation) rules whenever the writer agent produces prose intended for a general, non-specialist, or ESL audience, or whenever the user asks for "plain English", "plain language", "langage clair", "vulgarisation", "simplify", "rewrite for a general audience", "explain like I'm 12", or specifies a target reading level (Flesch-Kincaid, CEFR A2/B1). Trigger keywords: "vulgarise", "simplify", "rewrite", "make accessible", "non-technical", "public-facing", "FALC", "easy-to-read". Do NOT apply when the user explicitly requests a specialist register (academic paper, legal contract, technical RFC) — those follow their own conventions in style-guides.md.
agents: [writer]
---

# Plain Language — Vulgarisation and Accessibility Rules

Plain language is not dumbing down. It is the discipline of removing every barrier between the reader and the meaning: shorter sentences, common words, visible structure, and the active voice. A document is in plain language when the intended reader finds what they need, understands what they find, and can use it on the first read. This skill codifies the rules the writer agent applies before any general-audience deliverable leaves the pipeline.

The reference standards are the US Plain Writing Act of 2010 (plainlanguage.gov), the UK Government Digital Service style guide, the OECD "Recommendation on Good Regulatory Practice", the European Commission "How to Write Clearly" guide, the French INPI and DILA "langage clair" guidelines, and the FALC ("Facile à lire et à comprendre") European standard for cognitive accessibility. Where these standards conflict, prefer the stricter (shorter, simpler) constraint.

---

## When to Apply

Apply plain-language rules when the request involves any of the following:

- Public-facing communications: brochures, FAQs, web pages, newsletters, press releases.
- Administrative or government text: forms, letters, decisions, notices, summaries of legislation.
- Patient-facing health content: leaflets, consent forms, discharge instructions, drug information.
- Educational material for a non-expert audience: museum panels, popular science, MOOC scripts.
- ESL or multilingual contexts where the target language is not the reader's first language.
- Internal communications crossing departmental jargon boundaries (engineering to marketing, legal to product).
- Explicit user request for a target reading level (Flesch-Kincaid grade 6-8, CEFR A2-B1) or for "FALC", "easy-read", "vulgarisation", "langage clair".

Do NOT apply when:

- The audience is a domain specialist and the technical register conveys precision that plain language would lose (a cardiology paper, a court ruling, a Kubernetes API spec).
- The user explicitly requests a formal academic, legal, or technical register.
- The artefact is a controlled-vocabulary document where terminology is normative (ISO standard, medical coding, taxonomy).
- The text is creative literature where stylistic choices override clarity rules.

When in doubt, ask: "Who is the primary reader, and what is their reading level in this language?"

---

## Target Reading Level

| Audience | Flesch Reading Ease | Flesch-Kincaid Grade | CEFR | SMOG |
|---|---|---|---|---|
| General public (EN) | 60-70 | 7-8 | B1 | 8-9 |
| Patient-facing health (EN) | 70-80 | 6-7 | A2-B1 | 7-8 |
| Government / civic info (EN) | 60-70 | 7-8 | B1 | 8 |
| ESL learners (EN) | 80-90 | 4-6 | A2 | 6 |
| FALC / easy-read (EN/FR) | 90+ | 3-5 | A1-A2 | 5 |
| Academic specialist (default off) | 30-50 | 12-16 | C1-C2 | 12+ |

Targets for general-public output are Flesch-Kincaid grade 8 and Flesch Reading Ease 60-70. For French, the equivalent indices are the Kandel-Moles or LIX score; aim for LIX 30-40 (corresponds to B1).

The writer agent should self-estimate these scores after drafting. A quick proxy: average words per sentence ≤ 20 AND average syllables per word ≤ 1.6 → grade 8 is reachable.

---

## Core Principles

### 1. Sentence length

- Average sentence length ≤ 20 words.
- Maximum sentence length ≤ 30 words. Break anything longer at the nearest conjunction.
- Vary length: alternate short (5-10 words) and medium (15-20 words) sentences to maintain rhythm.
- One idea per sentence. If a sentence contains "and", "but", "which", or "however" mid-clause, consider splitting.

### 2. Active voice

- Prefer active voice in 80%+ of sentences. The actor comes before the action.
- Passive voice is acceptable only when (a) the actor is unknown or irrelevant, (b) the focus is on the action's object for legal reasons ("the form must be signed"), or (c) the actor is the bureaucratic state and naming it would be redundant.
- Watch for hidden agents: "It was decided that…" → "The committee decided to…".

### 3. Common words over Latinate vocabulary

English borrowed twice: a Germanic Anglo-Saxon core and a Latin-French overlay. The Anglo-Saxon core is shorter, more frequent, and more concrete. Default to it.

### 4. Strip nominalizations

A nominalization turns a verb into a noun ("decide" → "decision", "implement" → "implementation"). It buries the action and inflates the sentence. Restore the verb.

| Nominalized | Verbal |
|---|---|
| Make a decision | Decide |
| Provide an explanation | Explain |
| Conduct an analysis | Analyse |
| Carry out an investigation | Investigate |
| Give consideration to | Consider |
| Reach an agreement | Agree |
| Perform an evaluation | Evaluate |
| Take into account | Consider |
| Make an application | Apply |
| Effect a change | Change |

### 5. Cut hedging and filler

Hedges ("perhaps", "maybe", "somewhat", "rather", "quite", "in some sense") dilute meaning. Use them only when uncertainty is genuinely calibrated and informative. Delete otherwise.

Fillers ("it is important to note that", "as a matter of fact", "in order to", "due to the fact that", "for the purpose of") add length without meaning. Delete or compress: "in order to" → "to"; "due to the fact that" → "because".

### 6. Concrete nouns, strong verbs, sparing adjectives

- Use concrete nouns ("the report", "the patient") over abstract noun chains ("the operational framework deliverable").
- Use specific verbs ("write", "send", "approve") over weak verbs + adverbs ("quickly produce", "carefully review").
- Reserve adjectives for distinguishing information. "The new policy" is fine if there was an old one; otherwise just "the policy".

### 7. Scannable structure

- A heading every ~150 words. Headings answer the question the reader has at that point.
- Bullets ≤ 5 items per list. Beyond 5, group under sub-headings or convert to a table.
- Bullet items are grammatically parallel (all start with a verb, or all are noun phrases).
- Bold the keyword or key phrase the reader scans for, sparingly (no more than 1-2 per paragraph).
- White space matters. Paragraphs of 3-5 sentences; avoid walls of text.

### 8. Front-load the message

Inverted pyramid: the main point in the first sentence of the paragraph, the qualifications and details after. The reader who stops reading after one sentence still gets the answer.

### 9. Examples and analogies

- After defining any non-everyday concept, give an example.
- Use analogies grounded in shared experience (cooking, traffic, mail) rather than other technical domains.
- One concrete example beats three abstract clarifications.

### 10. Define on first use

Spell out every acronym on first use: "Magnetic Resonance Imaging (MRI)". Define every term-of-art the reader might not know, inline ("the *placebo*, a pill with no active drug") or in a glossary.

---

## English Vocabulary Substitution Table

Apply these substitutions during revision. The right column is the default; the left is acceptable only when the technical or legal register demands it.

| Replace | With |
|---|---|
| Utilise / utilize | Use |
| Commence | Start, begin |
| Demonstrate | Show |
| Endeavour | Try |
| Facilitate | Help, ease, make easier |
| Implement | Carry out, do, put in place |
| Initiate | Start, begin |
| Indicate | Show, say |
| Modify | Change |
| Necessitate | Need, require |
| Obtain | Get |
| Optimise | Improve |
| Prior to | Before |
| Subsequent to | After |
| In the event that | If |
| In the absence of | Without |
| With respect to / with regard to | About, on |
| Pursuant to | Under |
| Notwithstanding | Despite, even though |
| Heretofore | Until now |
| Hereinafter | From now on, below |
| Aforementioned | This, that, the |
| Approximately | About |
| Sufficient | Enough |
| Additional | More, extra |
| Furthermore / moreover | Also |
| Therefore / consequently | So |
| However | But |
| Nevertheless | Still |
| Ascertain | Find out, check |
| Comprise | Include, contain, be made of |
| Constitute | Be, form, make up |
| Deem | Consider, think |
| Disseminate | Share, send out |
| Elucidate | Explain, clarify |
| Endeavour to | Try to |
| Exhibit | Show |
| Procure | Get, buy |
| Render | Make, give |
| Terminate | End, stop |
| Transmit | Send |
| Utilisation | Use |

### Before / After — English (15 rewrites)

| Before | After |
|---|---|
| Pursuant to the aforementioned regulation, applicants must submit documentation prior to the deadline. | Under the regulation above, applicants must send their documents before the deadline. |
| It is necessary to ensure that all participants have received adequate notification of the meeting. | Make sure everyone has been told about the meeting. |
| The committee will endeavour to facilitate the implementation of the new policy. | The committee will help put the new policy in place. |
| Subsequent to the completion of the investigation, a report will be disseminated. | After the investigation ends, we will share a report. |
| In the event that the patient experiences adverse effects, medical attention should be sought immediately. | If you have side effects, get medical help right away. |
| Notwithstanding the aforementioned considerations, the project will commence on schedule. | Even so, the project will start on schedule. |
| The utilisation of this product necessitates the prior consultation of the user manual. | Read the manual before you use this product. |
| A determination will be made by the committee regarding the eligibility of the application. | The committee will decide if the application is eligible. |
| The aforementioned modifications were implemented in order to optimise system performance. | We made these changes to improve performance. |
| It has been determined by the relevant authorities that further investigation is required. | The authorities have decided that more investigation is needed. |
| Approximately seventy-five percent of respondents indicated a preference for the proposed solution. | About 75% of respondents preferred the proposed solution. |
| The aforementioned report comprises three distinct sections, each addressing a specific aspect. | The report has three sections, each on one topic. |
| In light of the fact that the deadline is approaching, prioritisation of tasks is recommended. | Because the deadline is near, you should rank your tasks. |
| Due to the inclement weather conditions, the event has been postponed. | We have postponed the event because of bad weather. |
| Should you require any further assistance, please do not hesitate to contact us. | If you need more help, contact us. |

---

## French (Langage Clair) Equivalents

The Direction Interministérielle de la Transformation Publique (DITP), the INPI, and the Ministère de la Culture publish the French "langage clair" reference. The standard is anchored in décret n° 2017-330 and the Charte Marianne. Key rules:

- Privilégier le présent de l'indicatif à la voix active.
- Phrases ≤ 20 mots en moyenne, ≤ 25 mots maximum.
- Bannir les sigles non explicités.
- Préférer le vocabulaire courant au vocabulaire administratif.
- Adresser le lecteur en "vous", l'administration en "nous" ou en sujet nommé.
- Numérotation : chiffres ≥ 10 en chiffres, chiffres 0-9 en lettres sauf usage technique.

### Vocabulaire administratif → vocabulaire courant

| À éviter | Préférer |
|---|---|
| Effectuer | Faire |
| Solliciter | Demander |
| Procéder à | Faire, commencer |
| Diligenter | Mener, lancer |
| Notifier | Informer, faire savoir |
| Statuer sur | Décider de |
| Nonobstant | Malgré, même si |
| Subséquent / ultérieurement | Plus tard, ensuite |
| Préalablement | Avant |
| Dans l'éventualité où | Si |
| Au titre de | Pour, comme |
| À l'effet de | Pour |
| Aux fins de | Pour |
| En vue de | Pour |
| Par voie de conséquence | Donc, alors |
| Susmentionné, susvisé | Ci-dessus, déjà cité |
| Le présent courrier | Cette lettre |
| Vous voudrez bien | Merci de, veuillez |
| Il vous appartient de | Vous devez |
| À toutes fins utiles | (à supprimer) |
| Dans les meilleurs délais | Rapidement, vite, avant le … |
| Prendre en considération | Tenir compte de, regarder |
| Mettre en œuvre | Appliquer, faire |
| Faire parvenir | Envoyer |
| Réceptionner | Recevoir |
| Pièce jointe (PJ) | Document joint |
| Récépissé | Reçu |
| Domicilier | Habiter |
| Résider | Habiter, vivre |

### Formules à éviter (et leur remplacement)

- "Nous avons l'honneur de vous informer que…" → "Nous vous informons que…" ou directement le message.
- "Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées." → "Cordialement." (correspondance courante).
- "Il est porté à votre connaissance que…" → "Nous vous informons que…" ou la phrase directe.
- "Dans l'attente de votre réponse, je vous prie de croire…" → "J'attends votre réponse. Cordialement."
- "Sous réserve de l'examen de votre dossier…" → "Si votre dossier est complet…".
- "Il n'a pas été porté à notre connaissance que…" → "Nous ne savons pas si…".

### Avant / Après — Français (10 réécritures)

| Avant | Après |
|---|---|
| Nous avons l'honneur de porter à votre connaissance que votre demande a fait l'objet d'un rejet. | Votre demande est refusée. |
| Il vous appartient de faire parvenir à nos services les pièces justificatives susmentionnées dans les meilleurs délais. | Envoyez-nous les documents listés ci-dessus le plus vite possible. |
| Préalablement à toute démarche, il convient de procéder à la vérification de l'éligibilité du dossier. | Avant de commencer, vérifiez que votre dossier est éligible. |
| Nonobstant les dispositions prévues à l'article 3, le demandeur peut solliciter une dérogation. | Même si l'article 3 dit le contraire, vous pouvez demander une dérogation. |
| Dans l'éventualité où vous souhaiteriez obtenir des informations complémentaires, vous voudrez bien contacter notre service. | Si vous voulez plus d'informations, contactez-nous. |
| La présente notification fait suite à votre courrier en date du 12 mars 2026, susvisé. | Cette lettre répond à votre courrier du 12 mars 2026. |
| Il est porté à votre connaissance que votre dossier est en cours d'instruction par les services compétents. | Nos services examinent votre dossier. |
| Vous voudrez bien noter que tout retard dans la transmission des documents est susceptible d'entraîner le rejet de la demande. | Si vous envoyez les documents en retard, votre demande peut être refusée. |
| Aux fins de la constitution du dossier, il vous est demandé de bien vouloir produire les justificatifs requis. | Pour préparer le dossier, envoyez les justificatifs demandés. |
| Le présent courrier vaut accusé de réception et vous sera notifié par voie postale. | Cette lettre est votre accusé de réception. Vous la recevez par la poste. |

---

## Application Guidelines

1. **Draft first, then revise.** Write a first pass without policing yourself, then apply the substitution table.
2. **Read aloud.** Any sentence that runs out of breath needs to be cut.
3. **One pass per principle.** Pass 1: sentence length. Pass 2: active voice. Pass 3: vocabulary. Pass 4: nominalizations. Pass 5: scannability.
4. **Show the reader, don't tell.** "We value your time" is hollow; "This form takes 5 minutes" is plain language.
5. **Use the second person.** Address the reader as "you" (or "vous" in French). Address the institution as "we" or by name.
6. **Localise units and dates.** Don't make the reader convert. UK reader: kilometres only if context is global; metric in EU; imperial in US public-facing.
7. **Test on a real reader.** A 30-second comprehension test on one non-expert beats any automated score.

---

## Templates / Sample Patterns

### Pattern A — Restructuring a paragraph

Before (54 words, 1 sentence, grade 18):

> Pursuant to Article 7 of the aforementioned regulation, all applicants who have heretofore submitted documentation prior to the deadline of 31 March 2026 shall be entitled to receive notification of the outcome of their application no later than thirty (30) days subsequent to the date of submission, notwithstanding any unforeseen administrative delays.

After (3 sentences, avg 12 words, grade 8):

> If you sent your application before 31 March 2026, we will tell you the result within 30 days. The 30-day clock starts on the day we receive your application. Administrative delays may push this back; we will let you know if that happens.

### Pattern B — From form letter to plain language

Before:

> The Tax Authority hereby notifies you that, following examination of your tax return for the fiscal year 2025, a discrepancy has been identified necessitating supplementary documentation in support of the deductions claimed.

After:

> We have reviewed your 2025 tax return and found a problem. To fix it, we need more proof of the deductions you claimed. Please send the documents listed on page 2 by 15 June 2026.

### Pattern C — Bulletisation of a wall of text

Before:

> To register, applicants must provide proof of identity, proof of address dated within the last three months, a completed application form bearing the applicant's original signature, the application fee paid by bank transfer or certified cheque, and, where applicable, supporting documents demonstrating eligibility for the requested category.

After:

> To register, send us:
>
> - A proof of identity.
> - A proof of address from the last 3 months.
> - The application form, signed by you.
> - The application fee (bank transfer or certified cheque).
> - Any document proving you qualify for the category you chose.

### Pattern D — FALC (Facile à lire et à comprendre)

FALC adds further constraints on top of plain language for cognitive accessibility:

- One idea per sentence, ≤ 15 words.
- Concrete and present tense only.
- Pictograms next to key words.
- Define every word that is not in the 1500 most common.
- Layout: one sentence per line, large font (14pt+), high contrast.

Example FALC:

> Vous voulez voter ?
> Vous devez avoir 18 ans.
> Vous devez être inscrit sur la liste électorale.
> Pour vous inscrire, allez à la mairie.
> Apportez une carte d'identité.

---

## Quality Checklist (Hemingway-style self-check)

Run this rubric on every paragraph before delivering:

- [ ] Average sentence length ≤ 20 words; longest sentence ≤ 30 words.
- [ ] At least 80% of finite verbs are in the active voice.
- [ ] No nominalization survives where a verb works ("decide" not "make a decision").
- [ ] No Latinate word survives where a Germanic equivalent exists (table above).
- [ ] No hedge ("perhaps", "somewhat", "rather") unless calibrated uncertainty is intended.
- [ ] No filler phrase ("it is important to note that", "in order to", "due to the fact that").
- [ ] Every acronym is spelled out on first use.
- [ ] Every term-of-art is defined inline or in a glossary.
- [ ] One heading at least every 150 words.
- [ ] No bulleted list exceeds 5 items without a sub-grouping.
- [ ] No paragraph exceeds 5 sentences.
- [ ] Main message of each paragraph is in the first sentence.
- [ ] Reader is addressed as "you" / "vous"; institution as "we" / "nous" or named.
- [ ] At least one concrete example for every abstract concept introduced.
- [ ] Estimated Flesch-Kincaid grade ≤ 8 (EN) or LIX ≤ 40 (FR) — verifiable with `textstat`.
- [ ] No adverb-laden weak verb where a strong verb fits ("ran fast" → "sprinted" only if precision matters; usually "ran" is enough).

---

## Common Mistakes

- **Treating plain language as informality.** Plain language is precise and respectful; it is not slang. "Hey there!" is informality, not plain language.
- **Cutting necessary detail.** Plain language shortens prose, not information. If the regulation says "30 days from the date of receipt", do not turn this into "soon".
- **Over-bulleting.** Bullets exist for parallel, scannable items. Turning a narrative into bullets destroys argument structure. Use prose for reasoning, bullets for enumerations.
- **Bolding for emphasis.** Bold marks the keyword the reader scans for, not the word the writer cares about. More than 2 bolds per paragraph and the technique fails.
- **Dropping the active voice when the actor is the state.** "The application will be processed" hides who acts; "We will process your application within 30 days" sets expectations.
- **Pseudo-simplification.** Replacing "utilise" with "use" but keeping a 45-word sentence misses the point. Sentence length and structure dominate the readability score.
- **Trusting only the Flesch score.** Automated metrics catch length and syllables but miss jargon, ambiguity, and missing context. Always pair with human review.
- **Translating English plain-language rules directly to French.** French syntax tolerates longer sentences and demands honorific closings in formal correspondence. Follow the French "langage clair" register, not a word-for-word transposition.
- **Forgetting the audience's prior knowledge.** A patient leaflet on insulin can assume the reader knows what diabetes is; one for a newly diagnosed reader cannot. Calibrate every assumption.
- **Skipping the read-aloud test.** Eye-reading hides rhythm problems and run-on sentences that the ear catches in two seconds.
- **Confusing plain language with FALC.** FALC is a stricter cognitive-accessibility standard. Apply it only when the user explicitly asks; otherwise plain language is enough.
- **Dropping nuance to hit a grade level.** If a 9th-grade word is the right one, use it and define it. Forcing every sentence below grade 8 sacrifices accuracy.
