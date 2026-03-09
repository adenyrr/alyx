---
name: reveal-slides
description: Create interactive HTML presentation slides using Reveal.js, delivered as self-contained HTML artifacts. Use this skill whenever someone needs a slideshow, pitch deck, lecture slides, or any multi-slide presentation with transitions, fragments, code highlighting, speaker notes, or markdown-driven content. Trigger on requests like "make a presentation", "create slides about X", "build a pitch deck", "design lecture slides", or any prompt needing a slide deck. Do NOT use for scrollytelling (→ gsap-animation skill), data dashboards (→ chartjs/recharts skill), or static single-page infographics (→ creative skill).
---

# Reveal.js Slides Skill

Reveal.js is a full-featured HTML presentation framework. It transforms nested `<section>` elements into horizontally and vertically navigable slides with transitions, fragments (incremental reveals), code syntax highlighting (via highlight.js), markdown support, speaker notes, auto-animation, and responsive scaling. Slides are keyboard/touch/swipe navigable.

---

## Artifact Presentation & Use Cases

Every Reveal.js artifact is a self-contained HTML page that loads the framework via CDN. The visual structure follows:

- **Full-viewport slides** — each `<section>` is a slide that fills the screen
- **Dark theme** — custom CSS overriding Reveal's default theme for `#0f1117` body, `#f1f5f9` text, `#6366f1` accents
- **Navigation** — arrow keys, spacebar, swipe, or on-screen controls
- **Fragments** — bullet points or elements that appear one by one on click
- **Code blocks** — syntax-highlighted with line numbers and step-through highlights

### Typical use cases

- **Tech talks** — slides with live code blocks, diagrams, and fragment reveals
- **Pitch decks** — company/product presentations with branded colors and transitions
- **Lecture slides** — educational content with incremental reveals and speaker notes
- **Conference presentations** — full-featured slides with vertical sub-slides
- **Interactive reports** — data-driven slides with embedded charts or diagrams
- **Workshops** — step-by-step tutorial slides with code examples

### What the user sees

A polished slide deck with smooth transitions between slides, click-to-reveal fragments, syntax-highlighted code blocks, and responsive text that scales to any screen size.

---

## When to Use Reveal.js vs. Alternatives

| Use Reveal.js when… | Use another tool when… |
|---|---|
| Multi-slide presentation with navigation | Scroll-driven storytelling → **GSAP + ScrollTrigger** |
| Fragments / incremental reveals | Single-page infographic → **creative** |
| Code syntax highlighting in slides | Interactive data charts → **Chart.js / Recharts** |
| Speaker notes for presenters | Editable diagrams → **JointJS** |
| Keyboard + touch navigation | Animated UI components → **Anime.js** |
| Export to PDF (print stylesheet) | 3D visualizations → **Three.js** |

> **Rule of thumb:** if the user says "slides", "presentation", "deck", or "talk", use Reveal.js.

---

## Step 1 — CDN Setup

```html
<!-- Reveal.js CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">

<!-- Reveal.js Core -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>

<!-- Syntax highlighting plugin (optional) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/monokai.css">
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.js"></script>

<!-- Markdown plugin (optional) -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/markdown/markdown.js"></script>

<!-- Notes plugin (optional, for speaker view) -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.js"></script>
```

> Do NOT load a default theme CSS (`black.css`, `white.css`, etc.) — we apply a custom dark theme via inline styles.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presentation Title</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/monokai.css">
  <style>
    /* Custom dark theme */
    .reveal { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
    :root {
      --r-background-color: #0f1117;
      --r-main-font-size: 32px;
      --r-main-color: #e2e8f0;
      --r-heading-color: #f1f5f9;
      --r-heading-font-weight: 700;
      --r-link-color: #6366f1;
      --r-link-color-hover: #818cf8;
      --r-selection-background-color: rgba(99,102,241,0.3);
    }
    .reveal { color: var(--r-main-color); }
    .reveal h1, .reveal h2, .reveal h3 { color: var(--r-heading-color); }
    .reveal h1 { font-size: 2.2em; }
    .reveal h2 { font-size: 1.5em; }
    .reveal h3 { font-size: 1.1em; }

    .reveal .accent { color: #6366f1; }
    .reveal .subtitle { color: #94a3b8; font-size: 0.7em; }
    .reveal .small { font-size: 0.6em; color: #64748b; }

    .reveal ul { text-align: left; }
    .reveal li { margin-bottom: 0.4em; font-size: 0.85em; line-height: 1.6; color: #cbd5e1; }

    .reveal pre { box-shadow: none; }
    .reveal pre code {
      background: #1a1d27;
      border-radius: 10px;
      padding: 16px 20px;
      font-size: 0.55em;
      line-height: 1.5;
      max-height: 420px;
    }

    .reveal .slide-number { color: #64748b; font-size: 14px; }
    .reveal .controls { color: #6366f1; }
    .reveal .progress span { background: #6366f1; }

    /* Card style for content blocks */
    .card-slide {
      background: #1a1d27;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
      text-align: left;
      max-width: 700px;
      margin: 0 auto;
    }
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">

      <section> <!-- Slide 1 --> </section>
      <section> <!-- Slide 2 --> </section>

    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.js"></script>
  <script>
    Reveal.initialize({
      hash: true,
      slideNumber: true,
      transition: 'slide',
      backgroundTransition: 'fade',
      plugins: [RevealHighlight, RevealNotes],
    });
  </script>
</body>
</html>
```

---

## Step 3 — Slide Structure

```html
<!-- Horizontal slide -->
<section>
  <h2>Slide Title</h2>
  <p>Content here</p>
</section>

<!-- Vertical sub-slides (navigate down) -->
<section>
  <section><h2>Parent</h2></section>
  <section><h2>Child 1</h2></section>
  <section><h2>Child 2</h2></section>
</section>
```

---

## Step 4 — Fragments (Incremental Reveals)

```html
<section>
  <h2>Key Points</h2>
  <ul>
    <li class="fragment">First point appears on click</li>
    <li class="fragment">Second point appears next</li>
    <li class="fragment">Third point appears last</li>
  </ul>
</section>

<!-- Fragment animations -->
<p class="fragment fade-in">fade-in</p>
<p class="fragment fade-out">fade-out</p>
<p class="fragment fade-up">fade-up</p>
<p class="fragment fade-down">fade-down</p>
<p class="fragment highlight-red">highlight-red</p>
<p class="fragment highlight-blue">highlight-blue</p>
<p class="fragment grow">grow</p>
<p class="fragment shrink">shrink</p>
<p class="fragment strike">strike</p>

<!-- Custom order -->
<p class="fragment" data-fragment-index="2">Shows second</p>
<p class="fragment" data-fragment-index="1">Shows first</p>
```

---

## Step 5 — Code Highlighting

```html
<section>
  <h2>Code Example</h2>
  <pre><code class="language-javascript" data-trim data-line-numbers>
function greet(name) {
  console.log(`Hello, ${name}!`);
  return name.toUpperCase();
}
  </code></pre>
</section>

<!-- Step-through highlight (lines light up progressively) -->
<pre><code class="language-python" data-trim data-line-numbers="|1-2|4-5|7">
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')
df = df.dropna()

result = df.groupby('category').mean()
</code></pre>
```

> The `|` delimiter in `data-line-numbers` creates fragment-like progressive highlights.

---

## Step 6 — Speaker Notes

```html
<section>
  <h2>Slide Title</h2>
  <p>Visible content</p>

  <aside class="notes">
    These notes are only visible in speaker view.
    Press 'S' to open the speaker window.
    You can write detailed talking points here.
  </aside>
</section>
```

> Open speaker view by pressing **S** during the presentation.

---

## Step 7 — Transitions

```javascript
// Global transition (in Reveal.initialize)
Reveal.initialize({
  transition: 'slide',           // none, fade, slide, convex, concave, zoom
  backgroundTransition: 'fade',
});
```

```html
<!-- Per-slide override -->
<section data-transition="zoom">
  <h2>Zooms in</h2>
</section>

<section data-transition="fade-in slide-out">
  <h2>Fades in, slides out</h2>
</section>
```

---

## Step 8 — Backgrounds

```html
<!-- Solid color -->
<section data-background-color="#6366f1">
  <h2 style="color:#fff;">Accent Slide</h2>
</section>

<!-- Image -->
<section data-background-image="url" data-background-size="cover" data-background-opacity="0.3">
  <h2>Image Background</h2>
</section>

<!-- Gradient -->
<section data-background-gradient="linear-gradient(135deg, #0f1117, #1e2130)">
  <h2>Gradient</h2>
</section>
```

---

## Step 9 — Auto-Animate

```html
<!-- Elements with matching data-id animate between slides -->
<section data-auto-animate>
  <h2 data-id="title">Hello</h2>
  <p data-id="text" style="font-size: 0.8em; color: #94a3b8;">World</p>
</section>

<section data-auto-animate>
  <h2 data-id="title" style="color: #6366f1;">Hello</h2>
  <p data-id="text" style="font-size: 1.2em; color: #f1f5f9;">World, animated!</p>
</section>
```

> Elements with the same `data-id` across consecutive `data-auto-animate` slides will morph between states.

---

## Step 10 — Markdown Slides

```html
<section data-markdown>
  <textarea data-template>
    ## Markdown Slide

    - Bullet **one**
    - Bullet _two_
    - Bullet `three`

    ---

    ## Next Slide

    Horizontal rule `---` creates a new slide.
  </textarea>
</section>
```

> Requires the Markdown plugin: `plugins: [RevealMarkdown]`

---

## Step 11 — Configuration Reference

```javascript
Reveal.initialize({
  // Navigation
  hash: true,             // URL hash per slide (#/2/1)
  history: true,          // push slide changes to browser history
  slideNumber: true,      // show slide number
  controls: true,         // show arrow controls
  progress: true,         // show progress bar

  // Presentation
  transition: 'slide',    // none | fade | slide | convex | concave | zoom
  transitionSpeed: 'default', // default | fast | slow
  backgroundTransition: 'fade',
  center: true,           // vertical centering
  autoSlide: 0,           // ms, 0 = disabled
  loop: false,

  // Sizing
  width: 960,
  height: 700,
  margin: 0.04,

  // Plugins
  plugins: [RevealHighlight, RevealNotes, RevealMarkdown],
});
```

---

## Step 12 — Design & Polish Guidelines

- **Consistent visual rhythm** — limit slides to one main idea each; avoid cramming too much text
- **Fragment sparingly** — use fragments for 3-5 bullet points, not entire paragraphs; too many clicks frustrate viewers
- **Large font for code** — code font-size should be at least `0.55em` (Reveal's base) for readability; limit code to ~15 lines per slide
- **Accent slide breaks** — use `data-background-color="#6366f1"` for section divider slides with white text
- **Slide numbers** — enable `slideNumber: true` for navigation context; style with `#64748b`
- **Dark code blocks** — use `monokai.css` theme for code; wrap in a `#1a1d27` background with rounded corners
- **Auto-animate for emphasis** — use `data-auto-animate` to morph titles, reposition elements, or highlight changes between steps
- **Speaker notes always** — include `<aside class="notes">` on every slide for presenter preparation
- **Image slides** — set `data-background-opacity="0.2"` or `0.3` for image backgrounds so text remains readable
- **Card-style content** — wrap complex content in a `.card-slide` div for visual containment inside slides
- **Responsive** — Reveal auto-scales; design at the default 960×700 canvas and let the framework handle the rest

---

## Step 13 — Complete Example: Tech Talk

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Modern Web APIs</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/monokai.css">
  <style>
    .reveal { font-family: 'Segoe UI', sans-serif; }
    :root {
      --r-background-color: #0f1117;
      --r-main-color: #e2e8f0;
      --r-heading-color: #f1f5f9;
      --r-link-color: #6366f1;
    }
    .reveal h1, .reveal h2, .reveal h3 { color: var(--r-heading-color); }
    .reveal h1 { font-size: 2.2em; }
    .reveal h2 { font-size: 1.4em; margin-bottom: 0.3em; }
    .accent { color: #6366f1; }
    .sub { color: #94a3b8; font-size: 0.65em; }
    .reveal li { margin-bottom: 0.3em; font-size: 0.8em; line-height: 1.6; color: #cbd5e1; }
    .reveal pre code { background: #1a1d27; border-radius: 10px; padding: 16px 20px; font-size: 0.5em; }
    .reveal .controls { color: #6366f1; }
    .reveal .progress span { background: #6366f1; }
    .reveal .slide-number { color: #64748b; }
    .card-s { background: #1a1d27; border-radius: 16px; padding: 28px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); text-align: left; max-width: 650px; margin: 0 auto; }
    .card-s h3 { color: #f1f5f9; font-size: 0.95em; margin-bottom: 8px; }
    .card-s p { color: #94a3b8; font-size: 0.65em; line-height: 1.6; }
    .tag { display: inline-block; background: rgba(99,102,241,0.15); color: #818cf8; border-radius: 6px; padding: 4px 12px; font-size: 0.55em; margin: 4px; }
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">

      <!-- Title slide -->
      <section>
        <h1>Modern <span class="accent">Web APIs</span></h1>
        <p class="sub">A tour of the browser's superpowers — 2025 edition</p>
        <aside class="notes">Welcome everyone. Today we'll look at APIs that make the web platform incredibly powerful.</aside>
      </section>

      <!-- Agenda -->
      <section>
        <h2>Agenda</h2>
        <ul>
          <li class="fragment">Performance APIs</li>
          <li class="fragment">Storage & Caching</li>
          <li class="fragment">Media & Streams</li>
          <li class="fragment">Connectivity</li>
        </ul>
        <aside class="notes">Four sections, about 5 minutes each.</aside>
      </section>

      <!-- Section divider -->
      <section data-background-color="#6366f1">
        <h2 style="color:#fff;">Performance APIs</h2>
      </section>

      <!-- Code slide with line highlights -->
      <section>
        <h2>Intersection Observer</h2>
        <pre><code class="language-javascript" data-trim data-line-numbers="|1-4|6-8|10-12">
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, {
  threshold: 0.1
});

document.querySelectorAll('.card').forEach(el => {
  observer.observe(el);
});
        </code></pre>
        <aside class="notes">Intersection Observer is perfect for lazy loading and scroll-triggered animations without GSAP.</aside>
      </section>

      <!-- Auto-animate demo -->
      <section data-auto-animate>
        <h2 data-id="perf">Web Workers</h2>
        <p data-id="desc" style="color:#94a3b8; font-size:0.7em;">Move heavy computation off the main thread.</p>
      </section>
      <section data-auto-animate>
        <h2 data-id="perf" style="font-size:1em; color:#6366f1;">Web Workers</h2>
        <p data-id="desc" style="color:#f1f5f9; font-size:0.85em;">Up to <strong>16×</strong> faster for CPU-bound tasks.</p>
        <div class="tag">SharedArrayBuffer</div>
        <div class="tag">Transferable Objects</div>
        <div class="tag">Comlink</div>
      </section>

      <!-- Card slide -->
      <section>
        <div class="card-s">
          <h3>Key Takeaway</h3>
          <p>The browser is no longer just a document viewer — it's a full application runtime with hardware access, background processing, and real-time networking built in.</p>
        </div>
      </section>

      <!-- Closing -->
      <section>
        <h1>Thank you!</h1>
        <p class="sub">Questions? → <span class="accent">@speaker</span></p>
      </section>

    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.js"></script>
  <script>
    Reveal.initialize({
      hash: true,
      slideNumber: true,
      transition: 'slide',
      backgroundTransition: 'fade',
      plugins: [RevealHighlight, RevealNotes],
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No `reveal.css` loaded** — the framework won't render without its core CSS; always include it before any theme/custom CSS
- **Loading a default theme AND custom styles** — themes like `black.css` override your custom CSS; either use a theme OR write custom styles, not both
- **Nesting `<section>` wrong** — horizontal slides are siblings; vertical sub-slides are nested `<section>` inside a parent `<section>`
- **`data-line-numbers` without highlight plugin** — progressive code highlights require `RevealHighlight` in the plugins array
- **Too much content per slide** — aim for under 50 words of text and under 15 lines of code per slide
- **Forgetting `data-trim`** — without `data-trim` on `<code>`, leading/trailing whitespace appears in the code block
- **Auto-animate without matching `data-id`** — elements only morph between slides if they share the same `data-id` value
- **Missing `hash: true`** — without it, refreshing the page loses your slide position
- **No speaker notes** — every meaningful slide should have `<aside class="notes">` for presenter preparation
- **Testing without pressing S** — always test speaker view (press S) to verify notes and timer work correctly
