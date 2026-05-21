---
name: latex-templates
description: Reference for the LaTeX templates and document classes the writer agent emits when the user requests LaTeX source (.tex) output. Covers article, IEEEtran, acmart, beamer, letter, and moderncv classes with their preambles, packages, and minimal bodies. Trigger keywords: "LaTeX", ".tex", "IEEE template", "ACM template", "beamer slides", "moderncv", "thesis template", "letter class", "biblatex", "biber", "lualatex", "pdflatex", "fontspec", "tikz", "booktabs". Do NOT apply when the user wants the rendered PDF directly — this skill produces .tex source; downstream pandoc or texlive performs the compilation. Do NOT apply when the user explicitly asks for a non-LaTeX format (DOCX, HTML, EPUB) — use pandoc-recipes.md instead.
agents: [writer]
---

# LaTeX Templates — Source Patterns for the Writer Agent

LaTeX is the de facto standard for typesetting scientific articles, conference papers, theses, slides, formal letters, and CVs. When the writer agent is asked for `.tex` output (because the user names a venue, a publisher template, or simply says "in LaTeX"), it must emit a complete, compilable source file using the correct document class and minimum viable preamble. This skill catalogues the six classes the writer meets most often and the package patterns that go with each.

Important boundary: this skill produces source. It does not compile to PDF. The Alyx stack delegates compilation to a downstream pandoc → LaTeX → texlive pipeline, or to a user-side TeX installation. The writer's job is to produce a `.tex` file that compiles cleanly when fed to `pdflatex`, `lualatex`, or `xelatex` as indicated.

Authoritative references: the Comprehensive TeX Archive Network (CTAN), the documentation that ships with each class, and the publisher's author kit (IEEE, ACM). When a publisher provides an author template, that template overrides this skill — copy its preamble verbatim and only fill in the body.

---

## When to Apply

Apply LaTeX templates when the request involves any of the following:

- The user asks for `.tex`, "LaTeX source", "Overleaf-compatible code", or names a class (article, beamer, IEEEtran, acmart, moderncv).
- The user names a publication venue that requires LaTeX submission (IEEE conference, ACM SIGCHI, Springer LNCS, NeurIPS, ICLR, arXiv).
- The user is preparing a thesis at an institution that mandates LaTeX (most STEM doctoral schools).
- The user wants slide decks rendered with beamer rather than PowerPoint or reveal.js.
- The user wants a formal letter or CV in LaTeX (letter class, moderncv, awesomecv).
- A math-heavy or symbol-heavy document where Markdown round-trips would degrade equations.

Do NOT apply when:

- The user wants DOCX, HTML, EPUB, ODT, or RTF output — route to pandoc-recipes.md.
- The user wants slides in reveal.js or PowerPoint — route to reveal.md or pandoc.
- The user wants a CV rendered by a non-LaTeX templating system (Markdown + CSS, JSONResume).
- The user wants the PDF directly without seeing source — that still requires the source first, then a downstream compile.

---

## Engine Selection

Three LaTeX engines are in routine use. Choose based on Unicode and font requirements.

| Engine | Best for | Unicode | System fonts |
|---|---|---|---|
| `pdflatex` | Classic academic articles, BibTeX, fast compile, broad package support | Limited (needs `inputenc utf8`) | No (uses TeX fonts) |
| `lualatex` | Modern Unicode, system fonts via `fontspec`, microtypography | Native | Yes |
| `xelatex` | Multilingual, Asian scripts, system fonts via `fontspec` | Native | Yes |

Defaults:

- **English-only article without exotic fonts** → `pdflatex`.
- **French, Spanish, Portuguese with accents and ligatures** → `lualatex` with `fontspec`; falls back to `pdflatex` with `inputenc utf8` and `babel`.
- **Multilingual or non-Latin scripts** → `lualatex` or `xelatex` with `fontspec` and `polyglossia`.
- **IEEEtran, acmart** → check class docs; both support `pdflatex` and `xelatex`. acmart 1.86+ prefers `pdflatex`.

When emitting source for downstream compilation, always state the recommended engine in a top-of-file comment:

```latex
% !TEX program = lualatex
% !BIB program = biber
```

---

## Core Preamble Building Blocks

Independent of the class, the following package groups are nearly always needed.

### Encoding and language

```latex
\usepackage[utf8]{inputenc}     % pdflatex only; omit under lualatex/xelatex
\usepackage[T1]{fontenc}        % accent shaping (pdflatex)
\usepackage[english]{babel}     % or polyglossia for lualatex/xelatex
\usepackage{lmodern}            % scalable Latin Modern fonts (pdflatex)
```

Under lualatex/xelatex:

```latex
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}   % Times-like
\setsansfont{TeX Gyre Heros}    % Helvetica-like
\setmonofont{TeX Gyre Cursor}   % Courier-like
\usepackage{polyglossia}
\setdefaultlanguage{english}
\setotherlanguage{french}
```

### Page geometry, hyperlinks, microtype

```latex
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\hypersetup{colorlinks=true, urlcolor=blue, linkcolor=black, citecolor=black}
\usepackage{microtype}
```

### Math

```latex
\usepackage{amsmath, amssymb, amsthm, mathtools}
\usepackage{siunitx}            % SI units, \SI{3.14}{\meter}
```

### Figures and tables

```latex
\usepackage{graphicx}
\usepackage{booktabs}           % \toprule, \midrule, \bottomrule
\usepackage{tabularx}           % auto-stretch columns
\usepackage{caption}
\usepackage{subcaption}         % subfigures
\usepackage{float}              % H placement
```

### Bibliography (biblatex preferred)

```latex
\usepackage[
  backend=biber,
  style=authoryear,             % or numeric, ieee, alphabetic, apa, chicago-authordate
  sorting=nyt,
  maxbibnames=10,
  maxcitenames=2,
  doi=true,
  url=false,
  isbn=false
]{biblatex}
\addbibresource{references.bib}
```

In the body, `\cite{key}`, `\textcite{key}` (author in text), `\parencite{key}` (parenthetical). At the end: `\printbibliography`.

Compile chain: `lualatex doc.tex && biber doc && lualatex doc.tex && lualatex doc.tex`.

### TikZ for diagrams

```latex
\usepackage{tikz}
\usetikzlibrary{positioning, arrows.meta, shapes.geometric, calc, fit}
```

---

## Class Reference

### 1. article — Generic academic article

- **Scope.** Generic papers, technical reports, preprints, course assignments, journal submissions without a specific class.
- **Default options.** `\documentclass[11pt,a4paper]{article}` (Europe) or `\documentclass[11pt,letterpaper]{article}` (US). For two-column: add `twocolumn`.
- **Sectioning.** `\section`, `\subsection`, `\subsubsection`, `\paragraph`, `\subparagraph`. No `\chapter` — switch to `report` or `book` for that.
- **Front matter.** `\title{}`, `\author{}`, `\date{}`, then `\maketitle`. Optional `\begin{abstract}...\end{abstract}`.
- **Recommended companions.** `geometry`, `hyperref`, `microtype`, `biblatex`, `booktabs`, `graphicx`.

### 2. IEEEtran — IEEE conferences and journals

- **Scope.** IEEE conference papers (ICASSP, INFOCOM, ICRA) and journals (TPAMI, TIT, JSAC). Maintained by Michael Shell.
- **Default options.** `\documentclass[conference]{IEEEtran}` for conferences (two-column letterpaper); `\documentclass[journal]{IEEEtran}` for journal submissions; add `peerreview` for double-spaced peer review copies.
- **Sectioning.** Same as `article` but `\IEEEauthorblockN`, `\IEEEauthorblockA` for the author block.
- **Bibliography.** IEEE provides `IEEEtran.bst` for BibTeX. With biblatex: `style=ieee`.
- **Math.** IEEEtran loads `amsmath` implicitly; do not redeclare.
- **Engine.** `pdflatex` is the canonical engine; `xelatex` works with caveats around microtype.

### 3. acmart — ACM Master Article Template

- **Scope.** ACM conference papers (SIGCHI, SIGGRAPH, CCS, KDD) and ACM journals (TOG, TOPLAS). Maintained by Boris Veytsman.
- **Default options.** `\documentclass[sigconf]{acmart}` for two-column conferences; `acmsmall`, `acmtog`, `acmlarge` for journals; `manuscript` for review; `screen` for screen-PDF.
- **Required ACM metadata.** `\acmConference`, `\acmYear`, `\acmISBN`, `\acmDOI`, `\acmPrice`. Use the values supplied by the ACM submission system; placeholders are acceptable during drafting.
- **Sectioning.** `\section`, `\subsection`, plus `\CCSXML` for the ACM Computing Classification System (CCS) concepts block.
- **Bibliography.** `\bibliographystyle{ACM-Reference-Format}` with BibTeX. With biblatex, use `style=acmnumeric` or `style=acmauthoryear`.
- **Engine.** `pdflatex` is canonical.

### 4. beamer — Slides

- **Scope.** Presentation slides, lecture decks, conference talks.
- **Default options.** `\documentclass{beamer}` with `\usetheme{...}` (Madrid, Berlin, CambridgeUS, metropolis).
- **Frame structure.** Each slide is `\begin{frame}{Title}...\end{frame}`. Use `\frametitle{}` or the title argument.
- **Overlays.** `\pause`, `\onslide<2->{}`, `\only<3>{}` for incremental reveal.
- **Themes.** `metropolis` (modern minimalist), `Madrid` (classic), `Berlin` (info-dense), `CambridgeUS` (formal).
- **Math.** Native via amsmath.
- **Notes.** `\note{}` and `\setbeameroption{show notes on second screen=right}` for presenter notes.

### 5. letter — Formal letters

- **Scope.** Standard business or formal correspondence. Spartan but reliable.
- **Default options.** `\documentclass[11pt]{letter}`.
- **Address.** `\signature{Sender Name}`, `\address{Sender Address}`, then per-letter `\begin{letter}{Recipient Address}`.
- **Body.** `\opening{Dear Dr Smith,}` ... `\closing{Yours sincerely,}` ... optionally `\encl{Enclosures}`, `\cc{CC list}`, `\ps{P.S.}`.
- **For French letters.** Prefer the `lettre` class (Geneva) which adds French conventions (`\lieu`, `\date`, `\nofax`).
- **Alternative for richer letters.** `scrlttr2` (KOMA-Script) gives modern formatting, multi-page support, and configurable letterheads.

### 6. moderncv — CVs and résumés

- **Scope.** One- or two-page CVs, résumés, biographical sketches.
- **Default options.** `\documentclass[11pt,a4paper,sans]{moderncv}`. Then `\moderncvstyle{classic}` (alternatives: `casual`, `oldstyle`, `banking`) and `\moderncvcolor{blue}` (or `red`, `orange`, `green`, `grey`, `black`).
- **Personal data.** `\name{First}{Last}`, `\title{Job Title}`, `\address{Street}{ZIP City}{Country}`, `\phone{}`, `\email{}`, `\homepage{}`, `\social[linkedin]{...}`.
- **Sections.** `\section{Experience}` then `\cventry{years}{role}{employer}{city}{}{description}` for jobs; `\cveducation` patterns vary by style.
- **Alternatives.** `awesomecv` (modern), `europecv` (Europass), `altacv` (sidebar layout).

---

## Templates

### Template 1 — Minimal article (pdflatex, biblatex+biber)

```latex
% !TEX program = pdflatex
% !BIB program = biber
\documentclass[11pt,a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[english]{babel}
\usepackage[margin=1in]{geometry}
\usepackage{microtype}
\usepackage{amsmath, amssymb, mathtools}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{caption}
\usepackage[colorlinks=true, urlcolor=blue, linkcolor=black, citecolor=black]{hyperref}

\usepackage[backend=biber, style=authoryear, sorting=nyt, maxcitenames=2, maxbibnames=10, doi=true, url=false, isbn=false]{biblatex}
\addbibresource{references.bib}

\title{The Effect of Sleep on Memory Consolidation}
\author{Jane A.\ Smith \and Robert B.\ Doe}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
We investigated whether nightly sleep duration predicts next-day recall in a sample of 120 healthy adults. Participants sleeping 7--9 hours showed a 15\% improvement in delayed recall relative to a 5-hour control group (\(p = .003\)).
\end{abstract}

\section{Introduction}
Sleep plays a central role in declarative memory consolidation \parencite{smith2023}.

\section{Methods}
We recruited 120 adults aged 18--35. Each completed a word-list learning task.

\subsection{Statistical analysis}
We fit a mixed-effects model with random intercepts per participant:
\begin{equation}
y_{ij} = \beta_0 + \beta_1 \mathrm{sleep}_i + u_i + \varepsilon_{ij}.
\end{equation}

\section{Results}
Table~\ref{tab:results} summarises the effect.

\begin{table}[h]
\centering
\caption{Recall accuracy by sleep duration}
\label{tab:results}
\begin{tabular}{lrr}
\toprule
Group & N & Recall (\%) \\
\midrule
5 h control & 60 & 62.1 \\
7--9 h treatment & 60 & 77.4 \\
\bottomrule
\end{tabular}
\end{table}

\section{Discussion}
The finding aligns with prior work \parencite{doe2022}.

\printbibliography
\end{document}
```

### Template 2 — IEEE conference (IEEEtran, pdflatex)

```latex
% !TEX program = pdflatex
\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts

\usepackage{cite}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{url}
\usepackage[hidelinks]{hyperref}

\begin{document}

\title{Deep Models for Sleep-Stage Classification}

\author{
  \IEEEauthorblockN{Jane A.\ Smith}
  \IEEEauthorblockA{Department of Computer Science\\
                    Example University\\
                    Email: jsmith@example.edu}
  \and
  \IEEEauthorblockN{Robert B.\ Doe}
  \IEEEauthorblockA{Department of Neuroscience\\
                    Example University\\
                    Email: rdoe@example.edu}
}

\maketitle

\begin{abstract}
We present a convolutional model for automatic sleep-stage classification from single-channel EEG, reaching 88\% per-epoch accuracy on the Sleep-EDF benchmark.
\end{abstract}

\begin{IEEEkeywords}
Sleep staging, EEG, deep learning, convolutional networks.
\end{IEEEkeywords}

\section{Introduction}
Sleep-stage classification is the foundation of polysomnography~\cite{Aboalayon2016}.

\section{Method}
Our network is a 1-D ResNet with 18 residual blocks.

\section{Results}
\begin{table}[t]
\centering
\caption{Per-stage F1 on Sleep-EDF}
\begin{tabular}{lcc}
\toprule
Stage & Baseline & Ours \\
\midrule
Wake & 0.91 & 0.94 \\
N1   & 0.42 & 0.55 \\
N2   & 0.85 & 0.89 \\
N3   & 0.78 & 0.83 \\
REM  & 0.81 & 0.86 \\
\bottomrule
\end{tabular}
\end{table}

\section{Conclusion}
The model improves N1 detection by 13 points.

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
```

### Template 3 — Beamer slides (metropolis theme, lualatex)

```latex
% !TEX program = lualatex
\documentclass[aspectratio=169]{beamer}
\usetheme{metropolis}
\metroset{progressbar=frametitle, numbering=fraction}

\usepackage{fontspec}
\usepackage{polyglossia}
\setdefaultlanguage{english}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tikz}

\title{Sleep and Memory}
\subtitle{A 120-Participant Trial}
\author{Jane A.\ Smith \and Robert B.\ Doe}
\institute{Example University}
\date{\today}

\begin{document}

\maketitle

\begin{frame}{Outline}
\tableofcontents
\end{frame}

\section{Background}

\begin{frame}{Why sleep matters}
\begin{itemize}
  \item Sleep consolidates declarative memory.\pause
  \item Effect sizes vary across studies.\pause
  \item No prior trial isolated 7--9 h vs.\ 5 h.
\end{itemize}
\end{frame}

\section{Results}

\begin{frame}{Recall by group}
\centering
\begin{tabular}{lrr}
\toprule
Group & N & Recall (\%) \\
\midrule
5 h   & 60 & 62.1 \\
7--9 h & 60 & 77.4 \\
\bottomrule
\end{tabular}
\end{frame}

\begin{frame}[standout]
Sleep wins.
\end{frame}

\appendix
\begin{frame}{References}
\footnotesize
\begin{itemize}
  \item Smith JA, Doe RB. 2023.
\end{itemize}
\end{frame}

\end{document}
```

### Template 4 — Formal letter (letter class, pdflatex)

```latex
% !TEX program = pdflatex
\documentclass[11pt,a4paper]{letter}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[english]{babel}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}

\signature{Jane A.\ Smith\\Senior Researcher}
\address{Example University\\1 Campus Drive\\Cambridge CB2 1TN\\United Kingdom}

\begin{document}

\begin{letter}{Editor-in-Chief\\Journal of Cognitive Science\\456 Editorial Way\\Boston, MA 02101\\USA}

\opening{Dear Dr Patel,}

I am pleased to submit our manuscript, ``The Effect of Sleep on Memory Consolidation,'' for consideration as a research article in the \emph{Journal of Cognitive Science}.

The study reports a randomised trial of 120 healthy adults assigned to a 5-hour or 7--9-hour sleep schedule and assessed on next-day delayed recall. We observe a 15\% improvement in recall accuracy in the treatment group (\(p = .003\)), with effect sizes consistent across age and gender strata.

All authors have approved the submission. The work has not been published elsewhere and is not under review at another journal. We have no competing interests to declare.

We thank you for your consideration and look forward to your response.

\closing{Yours sincerely,}

\encl{Manuscript, supplementary materials, signed authorship form}
\cc{Robert B.\ Doe}

\end{letter}

\end{document}
```

### Bonus pattern — moderncv (CV)

```latex
% !TEX program = pdflatex
\documentclass[11pt,a4paper,sans]{moderncv}

\moderncvstyle{classic}
\moderncvcolor{blue}

\usepackage[scale=0.8]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\name{Jane}{Smith}
\title{Senior Cognitive Scientist}
\address{1 Campus Drive}{Cambridge CB2 1TN}{United Kingdom}
\phone[mobile]{+44~7700~900000}
\email{jane.smith@example.edu}
\homepage{example.edu/~jsmith}
\social[linkedin]{jane-smith-research}
\social[orcid]{0000-0001-2345-6789}

\begin{document}
\makecvtitle

\section{Education}
\cventry{2014--2018}{PhD, Cognitive Neuroscience}{Example University}{Cambridge, UK}{}{Thesis on sleep-dependent memory consolidation.}
\cventry{2010--2014}{BSc, Psychology (First Class)}{Example University}{Cambridge, UK}{}{}

\section{Experience}
\cventry{2022--present}{Senior Researcher}{Example University}{Cambridge, UK}{}{Lead of the Sleep \& Memory Lab; 9 publications; 2 grants.}
\cventry{2018--2022}{Postdoctoral Fellow}{Boston Sleep Center}{Boston, MA, USA}{}{NIH-funded postdoctoral position.}

\section{Selected publications}
\cvitem{2023}{Smith, J.\,A.\ \& Doe, R.\,B.\ The effect of sleep on memory consolidation. \emph{J Cogn Sci} 45(3):210--225.}
\cvitem{2022}{Smith, J.\,A. Slow-wave sleep and the hippocampus. \emph{Trends Cogn Sci} 26(11):880--892.}

\section{Skills}
\cvitemwithcomment{Programming}{Python, R, MATLAB}{daily use}
\cvitemwithcomment{Languages}{English (native), French (C1), Spanish (B2)}{}

\end{document}
```

---

## Application Guidelines

1. **Identify the target.** If the user names a venue (IEEE conference, ACM CHI, NeurIPS), use that publisher's official template. NeurIPS provides its own `neurips_2024.sty`; Springer LNCS uses `llncs.cls`. Always state the engine and bibtool in the file header.
2. **Start from a minimal preamble.** Bloat is the enemy: only load what the body uses. Each unused package is a potential collision.
3. **Prefer biblatex + biber over BibTeX.** Biblatex gives modern styling, Unicode handling, and clean separation between style and bibliography file. Exceptions: IEEEtran's `IEEEtran.bst` and ACM's `ACM-Reference-Format.bst` are still common via legacy BibTeX.
4. **Use `booktabs` for tables.** `\toprule`, `\midrule`, `\bottomrule` produce publication-quality rules. Avoid `\hline` and vertical bars.
5. **Use `siunitx` for numbers and units.** `\SI{3.14}{\meter}` aligns decimals and applies typographic conventions.
6. **Use `\autoref` from `hyperref`** for "Figure 3" / "Table 2" references, or `cleveref` for "Figs.\ 3 and 4".
7. **For figures, prefer vector formats** (PDF, EPS, SVG via Inkscape conversion) over PNG/JPEG. Use `\includegraphics[width=0.8\linewidth]{fig.pdf}`.
8. **For TikZ diagrams,** keep them under 200 nodes; beyond that, externalise with `\usetikzlibrary{external}` to speed compilation.
9. **For non-English content,** switch to lualatex with `polyglossia`; pdflatex with `babel` works for European Latin scripts but is brittle for Greek, Arabic, CJK.
10. **Always state the engine.** A top-of-file `% !TEX program = lualatex` line tells downstream tools (Overleaf, latexmk, pandoc) what to invoke.

---

## Quality Checklist

- [ ] The document class matches the target venue (article, IEEEtran, acmart, beamer, letter, moderncv).
- [ ] The recommended engine is stated in a top-of-file comment.
- [ ] `inputenc utf8` and `fontenc T1` are present under pdflatex; `fontspec` is present under lualatex/xelatex.
- [ ] `babel` (pdflatex) or `polyglossia` (lualatex/xelatex) declares the document language.
- [ ] `hyperref` is loaded last among the standard packages (with exceptions for cleveref).
- [ ] `microtype` is loaded for improved typography.
- [ ] Math packages (`amsmath`, `amssymb`, `mathtools`) are loaded if equations appear.
- [ ] Tables use `booktabs` rules, not `\hline` and vertical bars.
- [ ] Figures use vector formats (PDF/EPS) when possible.
- [ ] The bibliography uses `biblatex` + biber or the publisher's mandated BibTeX style.
- [ ] Every `\cite` key has a matching entry in the `.bib` file.
- [ ] Sectioning hierarchy matches the class (no `\chapter` in `article`).
- [ ] The IEEEtran or acmart conference template includes the mandatory metadata (conference, ISBN, DOI, CCS).
- [ ] For beamer: themes and overlays are consistent; no slide overflows.
- [ ] Output file compiles cleanly with no missing-character or undefined-control-sequence warnings.

---

## Common Mistakes

- **Mixing pdflatex with `fontspec`.** `fontspec` requires lualatex or xelatex. Loading it under pdflatex fails immediately.
- **Loading `inputenc` under lualatex.** Modern LaTeX engines are natively UTF-8; `\usepackage[utf8]{inputenc}` is a no-op at best, an error at worst.
- **`\hline` and vertical bars in tables.** Booktabs rules are the publishing-industry standard. Remove vertical bars; replace `\hline` with `\toprule` / `\midrule` / `\bottomrule`.
- **`\usepackage{epsfig}` or `\usepackage{psfig}`.** Both are obsolete; use `graphicx` with `\includegraphics`.
- **Bib styles that don't match the citation command.** Loading `style=numeric` then using `\textcite` produces inconsistent output. Match the style to the citation command.
- **Forgetting to run biber.** With biblatex, the compile chain is lualatex → biber → lualatex → lualatex. Pandoc + texlive handles this if invoked with `--bibliography`.
- **Hard-coding font sizes inside the body.** Use sectioning commands and let the class handle font sizes. `\large \bfseries` mid-paragraph is brittle.
- **Overloading the preamble.** Loading every package "just in case" multiplies risk of conflicts (e.g., `subfigure` vs `subcaption`, `caption` vs class internals).
- **Bare URLs.** Wrap URLs in `\url{}` or `\href{}` (from `hyperref`) so line-breaking and clickability work.
- **Long lines in `verbatim`.** Use `listings` or `minted` with line-wrapping options for code blocks.
- **IEEEtran without `\IEEEauthorblockN` / `\IEEEauthorblockA`.** Plain `\author{}` does not produce the two-line author block IEEE expects.
- **acmart without the rights statement.** ACM requires the rights metadata before the title; missing it triggers warnings.
- **Beamer slides with too much content per frame.** A frame is roughly 4-7 bullets or one figure. If overflow appears, split into two frames.
- **Letter class with custom headers.** The plain `letter` class is bare; for letterheads use `scrlttr2` or design a header manually.
- **moderncv with non-existent style.** Only `casual`, `classic`, `oldstyle`, `banking` ship by default; other styles need separate downloads.
- **Forgetting the encoding of the .bib file.** Save references.bib as UTF-8; mixing Latin-1 and UTF-8 corrupts accented author names.
- **Using `&` outside tables.** `&` is a column separator in LaTeX; outside table environments use `\&`.
- **Math mode for punctuation.** Putting a comma after a display equation outside math mode breaks spacing; place punctuation inside the display.
- **Emitting non-compilable source.** Always sanity-check the brace/environment balance before returning the file to the user.
