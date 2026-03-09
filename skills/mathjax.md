---
name: mathjax-latex
description: Render LaTeX mathematical equations and scientific notation in HTML artifacts using MathJax 3. Use this skill whenever someone needs rendered math equations, formulas, or scientific notation in a web page — inline or display-mode. Trigger on requests like "render this equation", "show a formula", "create a math reference sheet", "display LaTeX in html", or any prompt that includes LaTeX math notation (\frac, \sum, \int, etc.) that must be visually rendered. Do NOT use for data charts (→ chartjs/plotly skill), code highlighting (→ prism-code skill), or Markdown rendering (→ plain HTML).
---

# MathJax LaTeX Skill

MathJax 3 is a JavaScript display engine for LaTeX, MathML, and AsciiMath notation. It converts LaTeX strings into high-quality, scalable SVG or HTML/CSS output, with support for equation numbering, custom macros, dynamic re-rendering, and accessibility (screen reader compatible). It runs entirely in the browser.

---

## Artifact Presentation & Use Cases

Every MathJax artifact is a self-contained HTML page with a dark theme and rendered equations. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius) contains the mathematical content
- **Title** (1.15rem, `#f1f5f9`) names the topic
- **Subtitle** (0.82rem, `#64748b`) adds context
- **Inline math** — LaTeX rendered within paragraph text using `\( ... \)`
- **Display math** — centered, larger equations using `\[ ... \]` or `$$ ... $$`
- **MathJax output** — white/light text on dark background via CSS color override

### Typical use cases

- **Formula reference sheets** — physics, statistics, calculus formula collections
- **Educational explanations** — step-by-step equation derivations
- **Scientific reports** — papers or summaries with inline equations
- **Theorem cards** — mathematical theorems with proofs
- **Cheat sheets** — compact reference with many equations and definitions
- **Interactive calculators** — input values, compute results, display formulas that update

### What the user sees

Beautifully typeset mathematical equations — fractions, integrals, summations, matrices, Greek letters — rendered with the same quality as LaTeX documents, directly in the browser.

---

## When to Use MathJax vs. Alternatives

| Use MathJax when… | Use another tool when… |
|---|---|
| LaTeX math equations in HTML | Data visualization → **Chart.js / D3 / Plotly** |
| Inline + display math | Code syntax highlighting → **Prism.js** |
| Equation numbering & references | Presentation slides with math → use Reveal.js + MathJax together |
| Custom macros (\newcommand) | Simple superscript/subscript → plain HTML `<sup>/<sub>` |
| Accessible math (screen readers) | Math input editor → **MathQuill** (not in stack) |
| Dynamic re-rendering after DOM changes | Static pre-rendered images → use LaTeX compiler |

> **Rule of thumb:** if the content includes LaTeX notation that needs to be rendered in a browser, use MathJax. For simple formatting without real math, plain HTML suffices.

---

## Step 1 — CDN Setup

```html
<!-- MathJax 3 (TeX → CHTML output) -->
<script>
  MathJax = {
    tex: {
      inlineMath: [['\\(', '\\)'], ['$', '$']],
      displayMath: [['\\[', '\\]'], ['$$', '$$']],
      processEscapes: true,
    },
    chtml: {
      scale: 1,
      minScale: 0.5,
    },
    startup: {
      pageReady: () => {
        return MathJax.startup.defaultPageReady();
      },
    },
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.min.js" async></script>
```

> The config object **must** appear before the MathJax script tag. The `async` attribute is recommended.

### Output formats:
- `tex-chtml.min.js` — HTML/CSS output (default, good quality, accessible)
- `tex-svg.min.js` — SVG output (higher quality, heavier)
- `tex-mml-chtml.min.js` — also accepts MathML input

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Math Reference</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 24px;
    }
    .card {
      width: 100%;
      max-width: 800px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
      margin-bottom: 20px;
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    h2 { font-size: 1rem; font-weight: 600; color: #f1f5f9; margin: 20px 0 8px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
    p, li { font-size: 0.9rem; line-height: 1.8; color: #cbd5e1; }

    /* MathJax dark theme overrides */
    mjx-container { color: #e2e8f0 !important; }
    mjx-container[display="true"] {
      margin: 16px 0 !important;
      overflow-x: auto;
    }
  </style>
  <script>
    MathJax = {
      tex: {
        inlineMath: [['\\(', '\\)'], ['$', '$']],
        displayMath: [['\\[', '\\]'], ['$$', '$$']],
        processEscapes: true,
        tags: 'ams',  // equation numbering
      },
    };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.min.js" async></script>
</head>
<body>
  <div class="card">
    <h1>Title</h1>
    <p class="sub">Description</p>
    <!-- Content with math -->
  </div>
</body>
</html>
```

---

## Step 3 — Inline vs. Display Math

```html
<!-- Inline (within text) -->
<p>The quadratic formula is \( x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \) where \( a \neq 0 \).</p>

<!-- Display (centered, own line) -->
\[ E = mc^2 \]

<!-- Or with double-dollar delimiters -->
$$ \int_0^\infty e^{-x^2}\, dx = \frac{\sqrt{\pi}}{2} $$
```

---

## Step 4 — Common LaTeX Commands

```latex
% Fractions
\frac{a}{b}          \dfrac{a}{b}          \tfrac{a}{b}

% Roots
\sqrt{x}             \sqrt[3]{x}

% Greek letters
\alpha \beta \gamma \delta \epsilon \theta \lambda \mu \pi \sigma \omega
\Gamma \Delta \Theta \Lambda \Pi \Sigma \Omega

% Operators
\sum_{i=1}^{n}       \prod_{i=1}^{n}       \int_{a}^{b}
\lim_{x \to 0}       \inf                   \sup

% Subscripts / superscripts
x_i                  x^2                   x_{i,j}^{(n)}

% Text in math
\text{if } x > 0    \quad \text{and} \quad

% Spacing
\,  \;  \quad  \qquad

% Delimiters
\left( \frac{a}{b} \right)
\left[ \right]  \left\{ \right\}  \left| \right|

% Dots
\cdots  \ldots  \vdots  \ddots
```

---

## Step 5 — Matrices

```latex
% Basic matrix
\begin{pmatrix} a & b \\ c & d \end{pmatrix}

% Bracketed
\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}

% Curly braces
\begin{Bmatrix} x \\ y \end{Bmatrix}

% Determinant bars
\begin{vmatrix} a & b \\ c & d \end{vmatrix}

% Augmented matrix (with array)
\left[\begin{array}{cc|c} 1 & 2 & 3 \\ 4 & 5 & 6 \end{array}\right]
```

---

## Step 6 — Equation Numbering & Alignment

```latex
% Numbered equation (with tags: 'ams')
\begin{equation}
  F = ma
\end{equation}

% Aligned equations (single number)
\begin{equation}
\begin{aligned}
  \nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
  \nabla \cdot \mathbf{B} &= 0 \\
  \nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
  \nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{aligned}
\end{equation}

% Multi-line with individual numbers
\begin{align}
  a &= b + c \label{eq:first} \\
  d &= e + f \label{eq:second}
\end{align}

% Reference: see equation \eqref{eq:first}
```

---

## Step 7 — Custom Macros

```javascript
MathJax = {
  tex: {
    macros: {
      R: '\\mathbb{R}',
      N: '\\mathbb{N}',
      Z: '\\mathbb{Z}',
      norm: ['\\left\\| #1 \\right\\|', 1],     // \norm{x} → ‖x‖
      abs: ['\\left| #1 \\right|', 1],           // \abs{x} → |x|
      inner: ['\\langle #1, #2 \\rangle', 2],    // \inner{x}{y} → ⟨x,y⟩
      dd: ['\\mathrm{d}#1', 1],                  // \dd{x} → dx (upright d)
      pd: ['\\frac{\\partial #1}{\\partial #2}', 2],  // \pd{f}{x} → ∂f/∂x
    },
  },
};
```

---

## Step 8 — Dynamic Re-rendering

```javascript
// After modifying DOM content with math:
function addMathContent(html) {
  const container = document.getElementById('output');
  container.innerHTML = html;

  // Tell MathJax to typeset the new content
  MathJax.typesetPromise([container]).then(() => {
    console.log('Math rendered');
  });
}

// Clear MathJax cache for a container before re-rendering
MathJax.typesetClear([container]);
container.innerHTML = newContent;
MathJax.typesetPromise([container]);
```

---

## Step 9 — Design & Polish Guidelines

- **Color override** — MathJax renders black text by default; add `mjx-container { color: #e2e8f0 !important; }` for dark theme
- **Overflow** — display equations can be wider than the card; add `overflow-x: auto` to `mjx-container[display="true"]`
- **Config before script** — the `MathJax = { ... }` config object MUST appear before the MathJax `<script>` tag; otherwise defaults are used
- **`processEscapes: true`** — enables `\$` to render a literal dollar sign when using `$` delimiters
- **Line height** — set `line-height: 1.8` on paragraphs containing inline math for comfortable spacing
- **Equation numbering** — enable with `tags: 'ams'` for `\begin{equation}` auto-numbering
- **async loading** — use `async` on the script tag; MathJax auto-processes the page when ready
- **Card spacing** — add `margin: 16px 0` to display equations for visual breathing room
- **Font scaling** — MathJax CHTML output scales with the surrounding font-size; no extra sizing needed
- **Accessibility** — MathJax 3 includes built-in accessibility (assistive MathML); no extra config required

---

## Step 10 — Complete Example: Calculus Cheat Sheet

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Calculus Cheat Sheet</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 24px; gap: 16px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 24px; width: 100%; max-width: 800px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.4rem; font-weight: 700; color: #f1f5f9; text-align: center; margin-bottom: 4px; }
    h2 { font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px; }
    p.sub { font-size: 0.82rem; color: #64748b; text-align: center; margin-bottom: 16px; }
    p { font-size: 0.88rem; line-height: 1.8; color: #cbd5e1; margin-bottom: 8px; }
    .formula-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .formula-item { background: rgba(255,255,255,0.03); border-radius: 10px; padding: 14px; border: 1px solid rgba(255,255,255,0.06); }
    .formula-item .label { font-size: 0.75rem; color: #94a3b8; margin-bottom: 6px; }
    mjx-container { color: #e2e8f0 !important; }
    mjx-container[display="true"] { margin: 12px 0 !important; overflow-x: auto; }
    @media (max-width: 600px) { .formula-grid { grid-template-columns: 1fr; } }
  </style>
  <script>
    MathJax = {
      tex: {
        inlineMath: [['\\(', '\\)']],
        displayMath: [['\\[', '\\]']],
        processEscapes: true,
        tags: 'ams',
        macros: {
          dd: ['\\mathrm{d}#1', 1],
          R: '\\mathbb{R}',
        },
      },
    };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.min.js" async></script>
</head>
<body>
  <h1>Calculus Cheat Sheet</h1>
  <p class="sub">Essential formulas for derivatives, integrals, and series</p>

  <!-- Derivatives -->
  <div class="card">
    <h2>Derivatives</h2>
    <div class="formula-grid">
      <div class="formula-item">
        <div class="label">Power Rule</div>
        \[ \frac{\dd{}}{{\dd{x}}} x^n = n x^{n-1} \]
      </div>
      <div class="formula-item">
        <div class="label">Chain Rule</div>
        \[ \frac{\dd{}}{{\dd{x}}} f(g(x)) = f'(g(x)) \cdot g'(x) \]
      </div>
      <div class="formula-item">
        <div class="label">Product Rule</div>
        \[ (fg)' = f'g + fg' \]
      </div>
      <div class="formula-item">
        <div class="label">Quotient Rule</div>
        \[ \left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2} \]
      </div>
      <div class="formula-item">
        <div class="label">Exponential</div>
        \[ \frac{\dd{}}{\dd{x}} e^x = e^x \]
      </div>
      <div class="formula-item">
        <div class="label">Natural Log</div>
        \[ \frac{\dd{}}{\dd{x}} \ln x = \frac{1}{x} \]
      </div>
    </div>
  </div>

  <!-- Integrals -->
  <div class="card">
    <h2>Integrals</h2>
    <div class="formula-grid">
      <div class="formula-item">
        <div class="label">Power Rule</div>
        \[ \int x^n \, \dd{x} = \frac{x^{n+1}}{n+1} + C, \quad n \neq -1 \]
      </div>
      <div class="formula-item">
        <div class="label">Exponential</div>
        \[ \int e^x \, \dd{x} = e^x + C \]
      </div>
      <div class="formula-item">
        <div class="label">Gaussian</div>
        \[ \int_{-\infty}^{\infty} e^{-x^2} \, \dd{x} = \sqrt{\pi} \]
      </div>
      <div class="formula-item">
        <div class="label">Integration by Parts</div>
        \[ \int u \, \dd{v} = uv - \int v \, \dd{u} \]
      </div>
    </div>
  </div>

  <!-- Series -->
  <div class="card">
    <h2>Series</h2>
    <p>The Taylor series of \( f(x) \) about \( a \):</p>
    \[ f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!} (x - a)^n \]
    <p>Geometric series (\( |r| < 1 \)):</p>
    \[ \sum_{n=0}^{\infty} r^n = \frac{1}{1 - r} \]
    <p>Euler's identity:</p>
    \[ e^{i\pi} + 1 = 0 \]
  </div>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Config after script** — the `MathJax = { ... }` object must be defined BEFORE the MathJax `<script src="...">` tag; placing it after means defaults are used and custom settings are ignored
- **Using `$...$` without configuring** — single-dollar delimiters are not enabled by default; add `inlineMath: [['$', '$']]` to the tex config, or use `\( ... \)` which works by default
- **Black text on dark background** — MathJax defaults to black; always add `mjx-container { color: #e2e8f0 !important; }`
- **Not calling `MathJax.typesetPromise()`** — dynamically added math content won't render unless you explicitly re-typeset; call `MathJax.typesetPromise([element])` after DOM changes
- **Escaping backslashes in JS strings** — inside JavaScript template literals, write `\\frac` not `\frac` (double backslashes); in HTML content, single backslashes work
- **Display math overflow** — wide equations (like long aligned blocks) can overflow; add `overflow-x: auto` to the container
- **Missing `processEscapes`** — if using `$` delimiters, `processEscapes: true` allows `\$` as a literal dollar sign
- **Loading multiple output formats** — only load one: `tex-chtml.min.js` OR `tex-svg.min.js`, not both
- **Equation numbering not showing** — requires `tags: 'ams'` in the tex config; without it, `\begin{equation}` tags don't number
