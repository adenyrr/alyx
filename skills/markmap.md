---
name: markmap
description: Generate beautiful, interactive mind maps from plain Markdown using markmap-autoloader v0.18, delivered as self-contained HTML artifacts. Use this skill whenever the request involves a mind map, knowledge map, concept map, hierarchical outline visualization, study notes rendered as a branching tree, lecture takeaways, brainstorming tree, table-of-contents-as-a-map, or "turn this Markdown into a visual mind map". Trigger on phrases like "mind map of X", "visualize this outline", "map out the topic", "explore this knowledge area", or any request where the source content is hierarchical Markdown headings + lists and the output should be an interactive radial tree. Do NOT use for: editable node-link diagrams with anchored ports (→ jointjs-flowchart skill), force-directed network graphs (→ vis-network skill), schematic flowcharts from text DSLs (→ mermaid-diagrams skill), or freeform sketch whiteboards (→ excalidraw skill).
agents: [dev]
---

# Markmap Skill — Mind Maps From Markdown (v0.18 autoloader)

Markmap is a tiny library that turns a Markdown document into a horizontal, zoomable, collapsible mind map rendered as SVG. The hierarchy comes straight from your `#`/`##`/`###` headings and nested bullet lists — there's no separate DSL to learn, no node objects to wire up. The autoloader build (`markmap-autoloader`) needs **one** `<script>` tag and a single `<div class="markmap">` containing Markdown, and you're done.

---

## Artifact Presentation & Use Cases

Every Markmap artifact is a self-contained HTML page with a dark theme by default. The visual structure follows the standard project pattern:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow, `overflow: hidden`) clips the SVG to rounded corners
- **Card header** carries title, subtitle, and optional toolbar (Expand all / Collapse / Export SVG)
- **Mind map container** — a single `<div class="markmap">` containing your Markdown, sized to a fixed height so the SVG fills the viewport
- The library injects an SVG into the container and handles pan, zoom, click-to-collapse, and node animation

### Typical use cases

- **Knowledge maps** — turning a topic outline (e.g. "Modern web performance", "Machine learning fundamentals") into a navigable tree
- **Study notes** — radial map of chapter → section → key concept → details
- **Meeting takeaways** — capture the discussion as a Markdown outline, render as a shareable mind map
- **Project plans** — milestones → workstreams → tasks, collapsible per workstream
- **Documentation table of contents** — render an entire docs site as a single interactive overview
- **Brainstorming sessions** — quick capture of branching ideas without leaving a Markdown editor

### What the user sees

A horizontally laid out mind map with curved colored links: the root sits on the left, branches spread to the right. Click any node to collapse/expand its subtree. Drag the canvas to pan, scroll to zoom, double-click on empty space to recenter. Nodes inherit a vivid palette so each top-level branch is visually distinct.

---

## When to Use Markmap vs. Alternatives

| Use Markmap when… | Use another library when… |
|---|---|
| Source content is Markdown headings + lists | Source is a DSL like `graph TD; A-->B` → **Mermaid** |
| Hierarchical, tree-shaped data | Arbitrary node-edge networks (cycles, many-to-many) → **vis-network** |
| Quick render — one script, one div | Editable diagram with anchored ports → **JointJS** |
| Mind map, knowledge map, study outline | Freehand sketching → **Excalidraw** |
| Want code blocks, links, KaTeX inline | Plain branch labels only → **D3 (tree layout)** |
| Need collapsible subtrees, zoom, pan | Static printable tree → **Mermaid `mindmap`** |
| Live regeneration from a Markdown source | Multi-axis radial diagrams → **D3 / Plotly** |

> **Rule of thumb:** if you can express the content as a Markdown outline (`#`, `##`, `-`), Markmap is the fastest path to a great-looking mind map. For directed graphs, schemas, or freeform layouts, use one of the alternatives.

---

## Step 1 — CDN Setup

The autoloader bundles `markmap-lib` (parser) + `markmap-view` (renderer) and auto-mounts every `<div class="markmap">` on `DOMContentLoaded`.

```html
<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.18"></script>
```

That's it. No CSS file, no helper scripts required.

### Optional configuration (script tag attributes)

```html
<script
  src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.18"
  data-markmap='{"duration":500,"maxWidth":280,"pan":true,"zoom":true,"colorFreezeLevel":2}'
></script>
```

Configuration can also be supplied per-instance via `data-markmap` on the `<div class="markmap">` itself.

> **Critical:** the container element **must have an explicit CSS height** (and ideally width). The SVG is sized to fill its parent — a `height: auto` container collapses to 0px and the map vanishes.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mind map</title>
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
      max-width: 1180px;
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 22px 24px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }

    /* REQUIRED: explicit height for the autoloader container */
    .markmap {
      width: 100%;
      height: 620px;
      background: #1a1d27;
    }

    /* Style the injected SVG via descendant selectors */
    .markmap svg { font-family: 'Segoe UI', -apple-system, sans-serif; }
    .markmap-foreign div { color: #e2e8f0; line-height: 1.5; }
    .markmap-foreign a    { color: #818cf8; text-decoration: none; border-bottom: 1px dashed rgba(129,140,248,0.4); }
    .markmap-foreign code { background: rgba(255,255,255,0.06); color: #c7d2fe; padding: 1px 5px; border-radius: 4px; font-size: 0.9em; }
    .markmap-foreign pre  { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 8px 10px; }
  </style>
</head>
<body>
  <main class="card" role="region" aria-label="Mind map">
    <header class="card-header">
      <div>
        <h1>Mind map title</h1>
        <p class="sub">Click any node to collapse · drag to pan · scroll to zoom</p>
      </div>
    </header>
    <div class="markmap" role="img" aria-label="Mind map of …">
<script type="text/template">
# Root
## Branch A
- detail
- detail
## Branch B
- detail
</script>
    </div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.18"></script>
</body>
</html>
```

> **Why the inner `<script type="text/template">`?** It's the recommended way to embed Markdown inside a `<div class="markmap">` without HTML parsing it. The autoloader extracts the script body and treats it as Markdown source. Plain text inside the div also works, but inline `<` characters in code blocks will break it.

---

## Step 3 — Themes (dark default + light alternative)

Markmap doesn't ship a theme prop — colors are controlled per-instance via the `color` option (a `d3-scale-chromatic` callback) and per-CSS for the surrounding chrome. Define two token sets and a switcher.

### Dark theme tokens (default)

```javascript
const DARK = {
  bg:      '#0f1117',
  card:    '#1a1d27',
  border:  'rgba(255,255,255,0.08)',
  text:    '#e2e8f0',
  muted:   '#94a3b8',
  accent:  '#6366f1',
  palette: ['#6366f1','#8b5cf6','#ec4899','#06b6d4','#22c55e','#eab308','#f97316','#f43f5e'],
  linkColor: 'rgba(99,102,241,0.55)',
};
```

### Light theme tokens

```javascript
const LIGHT = {
  bg:      '#f8fafc',
  card:    '#ffffff',
  border:  'rgba(0,0,0,0.08)',
  text:    '#1e293b',
  muted:   '#475569',
  accent:  '#6366f1',
  palette: ['#4f46e5','#7c3aed','#db2777','#0891b2','#16a34a','#ca8a04','#ea580c','#dc2626'],
  linkColor: 'rgba(79,70,229,0.45)',
};
```

### Theme switcher (with `prefers-color-scheme` default)

The autoloader runs once at startup. To restyle on the fly, re-render the instance with new options — markmap exposes the `Markmap` class and the parsed `transform` helper via globals when loaded:

```javascript
// After the autoloader has finished, the globals window.markmap and window.markmapAutoloader
// expose what we need.
const { Markmap, loadCSS, loadJS, deriveOptions } = window.markmap;

let theme = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
let mm;   // current Markmap instance

function applyTheme() {
  const t = theme === 'dark' ? DARK : LIGHT;
  document.body.style.background = t.bg;
  const card = document.querySelector('.card');
  card.style.background  = t.card;
  card.style.borderColor = t.border;
  document.querySelector('.markmap').style.background = t.card;
  document.querySelectorAll('.markmap-foreign div').forEach(el => el.style.color = t.text);
  // Re-render the SVG with the new palette
  mm?.setOptions({ color: (n) => t.palette[n.state.path.length % t.palette.length] });
  mm?.fit();
}
document.getElementById('themeToggle')?.addEventListener('click', () => {
  theme = theme === 'dark' ? 'light' : 'dark';
  applyTheme();
});
```

> If you need a full re-render (e.g., to swap data), use `Markmap.create(svg, options, root)` documented in Step 7 instead of the autoloader.

---

## Step 4 — Markdown Syntax Cheatsheet

The hierarchy is driven by heading level **then** by list indentation under the deepest heading.

```markdown
# Root node                         ← level 0 (only ONE allowed at the top)

## Branch A                         ← level 1
- leaf 1                            ← level 2
- leaf 2
  - sub-leaf                        ← level 3
- leaf 3 with **bold** and *italic* and `inline code`

## Branch B
- A link to [Wikipedia](https://wikipedia.org)
- An image: ![alt](https://placehold.co/80x40/png)
- A code block:
  ```js
  const x = 42;
  console.log(x);
  ```
- A math formula: $E = mc^2$
- A blockquote:
  > Worth quoting.

### Sub-branch B.1                  ← level 2 via heading
- leaf 1
```

Supported inline Markdown:
- **bold**, *italic*, ~~strikethrough~~
- `inline code` (styled via `.markmap-foreign code`)
- [links](https://example.com) (open in a new tab by default)
- Images (rendered inline; keep them small)
- Fenced ` ``` ` code blocks (preserved as `<pre><code>`)
- Inline `$x$` and block `$$x$$` math (when KaTeX is loaded)

> The autoloader does **not** auto-load KaTeX or PrismJS by default. If you need math/syntax highlighting, pull them in separately or pass `extraJs` to `data-markmap`:
> ```html
> data-markmap='{"extraJs":["https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.js"]}'
> ```

---

## Step 5 — Configuration Options

Pass options globally on the script tag (`data-markmap` JSON), per-container, or imperatively via `mm.setOptions({...})`.

| Option | Default | Effect |
|---|---|---|
| `color` | category color scale | `(node) => string` — color per node by depth/path |
| `colorFreezeLevel` | `0` | All descendants below this depth inherit their ancestor's color |
| `duration` | `500` | Animation duration in ms for expand/collapse |
| `nodeMinHeight` | `16` | Min row height in px |
| `spacingHorizontal` | `80` | Horizontal gap between depth levels |
| `spacingVertical` | `5` | Vertical gap between sibling nodes |
| `paddingX` | `8` | Inner horizontal padding of each node label |
| `autoFit` | `false` | Auto-fit on every expand/collapse |
| `fitRatio` | `0.95` | How much of the canvas the fit fills (0–1) |
| `maxWidth` | `0` | Max width per node in px (`0` = no limit). Use `260` to wrap long lines. |
| `pan` | `true` | Allow drag panning |
| `zoom` | `true` | Allow scroll/pinch zoom |
| `initialExpandLevel` | `-1` | `-1` = expand all; `2` = only root + 2 levels expanded |
| `embedAssets` | `false` | Inline external CSS/JS in standalone exports |
| `extraJs` / `extraCss` | `[]` | URLs to fetch when rendering (KaTeX, Prism…) |

```html
<div class="markmap"
     data-markmap='{"maxWidth":280,"colorFreezeLevel":2,"initialExpandLevel":3,"duration":650}'>
  <script type="text/template">
# Root
…
  </script>
</div>
```

### Custom color callback

```javascript
const t = DARK;
mm.setOptions({
  color: (node) => t.palette[(node.state.path.length - 1) % t.palette.length],
  colorFreezeLevel: 2,    // root + branch tint everything beneath them
  maxWidth: 280,
  duration: 650,
});
```

---

## Step 6 — Toolbar & Programmatic Control

The autoloader exposes the instance via `el.markmap` once mounted. The standard `markmap-view` Toolbar can be attached for built-in zoom/fit/recenter controls.

```javascript
// Wait for the autoloader to mount, then grab the instance
window.addEventListener('load', () => {
  const container = document.querySelector('.markmap');
  const mm = container.markmap;       // Markmap instance

  // Attach the built-in toolbar (zoom in / zoom out / fit / recenter)
  if (window.markmap?.Toolbar) {
    const { Toolbar } = window.markmap;
    const toolbar = Toolbar.create(mm);
    toolbar.el.style.cssText = 'position:absolute;bottom:16px;right:16px';
    container.style.position = 'relative';
    container.appendChild(toolbar.el);
  }

  // Programmatic
  mm.fit();                            // recenter + scale to fit
  mm.rescale(1.2);                     // zoom in
  mm.setData(root, options);           // swap the displayed tree
});
```

### Custom toolbar in the card header

```html
<div class="toolbar" role="toolbar" aria-label="Mind map actions">
  <button class="btn" id="expand"   type="button" aria-label="Expand all nodes">Expand all</button>
  <button class="btn" id="collapse" type="button" aria-label="Collapse all nodes">Collapse</button>
  <button class="btn" id="fit"      type="button" aria-label="Fit to view">Fit</button>
  <button class="btn primary" id="exportSvg" type="button" aria-label="Export as SVG">Export SVG</button>
</div>
```

```javascript
function walk(node, fn) { fn(node); (node.children || []).forEach(c => walk(c, fn)); }

document.getElementById('expand').addEventListener('click', () => {
  walk(mm.state.data, n => { if (n.payload) n.payload.fold = 0; });
  mm.renderData(); mm.fit();
});
document.getElementById('collapse').addEventListener('click', () => {
  walk(mm.state.data, n => { if (n.payload && n.state.path.length > 1) n.payload.fold = 1; });
  mm.renderData(); mm.fit();
});
document.getElementById('fit').addEventListener('click', () => mm.fit());
```

---

## Step 7 — Manual Mounting (when the autoloader isn't enough)

If you need full control (e.g., swap data on the fly, multiple instances, dynamic Markdown), skip the autoloader and call the library APIs directly. The autoloader bundle still exposes them via `window.markmap`.

```javascript
const { Transformer, Markmap } = window.markmap;

const transformer = new Transformer();
const md = `# Root\n## A\n- one\n- two\n## B\n- three`;

const { root, features } = transformer.transform(md);
// features tells you which extras (KaTeX/Prism) the content used so you can load them on demand

const svg = document.querySelector('#mm-svg');
const mm  = Markmap.create(svg, {
  color: (n) => DARK.palette[n.state.path.length % DARK.palette.length],
  duration: 600,
  maxWidth: 280,
}, root);

// Later — swap data without rebuilding the instance
const next = transformer.transform(`# New tree\n## Updated`).root;
mm.setData(next);
mm.fit();
```

The corresponding HTML:

```html
<svg id="mm-svg" style="width:100%;height:620px;background:#1a1d27"></svg>
```

---

## Step 8 — Exporting to SVG

The injected element is already an `<svg>` — exporting is a matter of serialization + download. For a portable SVG, inline a CSS reset so node labels render outside the page.

```javascript
function exportSvg() {
  const svg = document.querySelector('.markmap svg').cloneNode(true);
  // Inline a tiny stylesheet so labels keep their look outside the page
  const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
  style.textContent = `
    text, div { font-family: Segoe UI, sans-serif; color: #e2e8f0; }
    .markmap-foreign div { color: #e2e8f0; line-height: 1.5; }
    .markmap-foreign code { background: rgba(255,255,255,0.06); color: #c7d2fe; padding: 1px 5px; border-radius: 4px; }
  `;
  svg.insertBefore(style, svg.firstChild);

  const xml = new XMLSerializer().serializeToString(svg);
  const blob = new Blob(['<?xml version="1.0" standalone="no"?>\n', xml], { type: 'image/svg+xml' });
  const url  = URL.createObjectURL(blob);
  const a    = Object.assign(document.createElement('a'), { href: url, download: 'mindmap.svg' });
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 0);
}
document.getElementById('exportSvg').addEventListener('click', exportSvg);
```

For PNG export, draw the SVG into a canvas:

```javascript
async function exportPng() {
  const svgEl = document.querySelector('.markmap svg');
  const bbox  = svgEl.getBoundingClientRect();
  const xml   = new XMLSerializer().serializeToString(svgEl);
  const img   = new Image();
  img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(xml);
  await new Promise((res) => img.onload = res);

  const canvas = document.createElement('canvas');
  canvas.width  = bbox.width  * devicePixelRatio;
  canvas.height = bbox.height * devicePixelRatio;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#1a1d27';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    const url = URL.createObjectURL(blob);
    const a = Object.assign(document.createElement('a'), { href: url, download: 'mindmap.png' });
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
  }, 'image/png');
}
```

---

## Step 9 — Accessibility

- Wrap the container in a labeled region: `<div class="markmap" role="img" aria-label="Knowledge map of …">`.
- The SVG is interactive but not natively focusable for keyboard users — provide a hidden, plain-text outline below the map as a fallback (`<details><summary>Outline</summary><ul>…</ul></details>`) so screen readers can still consume the content.
- Pan/zoom defaults are mouse + wheel + touch only. Document keyboard alternatives (e.g., toolbar buttons for fit/expand/collapse) in the subtitle.
- Maintain ≥ 4.5:1 contrast between node text and the card background — the dark tokens in Step 3 are tuned for this. Verify any custom palette before shipping.
- Avoid color-only encoding for important distinctions — markmap colors branches by depth, which is decorative, not semantic.

---

## Step 10 — Design & Polish Guidelines

- **Set a `maxWidth` of ~280px.** Without it, long bullet items render as one very wide line.
- **Use `colorFreezeLevel: 2`** so every subtree of a top-level branch shares its color — clarifies grouping at a glance.
- **`initialExpandLevel: 3`** is a great default — root + two depths expanded, the rest collapsed. Users still discover but aren't drowning on first paint.
- **Keep one `# Root` only.** Multiple top-level `#` headings produce multiple disconnected trees and break the layout.
- **Use heading levels for major branches, lists for leaves.** Three `##` are easier to read than three `-` at the root.
- **Avoid huge code blocks** as leaves — they balloon nodes vertically. Use a short label and a link to the full snippet.
- **Set an explicit container height** in CSS (`height: 620px` or `vh`). Without it the SVG collapses to 0px.
- **Use `mm.fit()`** after data changes or theme switches to recenter and rescale.
- **Pick a palette with high contrast** against the card background — the vivid set in Step 3 is tuned for `#1a1d27`.

---

## Step 11 — Complete Example: Knowledge Map of "Modern Web Performance"

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Knowledge Map — Modern Web Performance</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; padding: 24px; display: flex; flex-direction: column; align-items: center; }
    .card { width: 100%; max-width: 1200px; background: #1a1d27; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    .card-header { padding: 22px 24px 16px; border-bottom: 1px solid rgba(255,255,255,0.07); display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }
    .toolbar { display: flex; gap: 8px; flex-wrap: wrap; }
    .btn { background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 7px 14px; font-size: 12px; font-weight: 500; cursor: pointer; transition: all 200ms cubic-bezier(0.16,1,0.3,1); }
    .btn:hover { background: rgba(255,255,255,0.1); color: #f1f5f9; transform: translateY(-1px); }
    .btn.primary { background: #6366f1; color: #fff; border-color: transparent; }
    .btn.primary:hover { background: #5254cc; }
    .btn:focus-visible { outline: 2px solid #818cf8; outline-offset: 2px; }

    .markmap-wrap { position: relative; }
    .markmap { width: 100%; height: 640px; background: #1a1d27; }
    .markmap svg { font-family: 'Segoe UI', -apple-system, sans-serif; }
    .markmap-foreign div { color: #e2e8f0; line-height: 1.5; }
    .markmap-foreign a    { color: #818cf8; text-decoration: none; border-bottom: 1px dashed rgba(129,140,248,0.4); }
    .markmap-foreign code { background: rgba(255,255,255,0.06); color: #c7d2fe; padding: 1px 5px; border-radius: 4px; font-size: 0.9em; }

    details.outline { margin: 16px 24px 22px; padding: 12px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; }
    details.outline summary { cursor: pointer; color: #94a3b8; font-size: 12px; }
    details.outline ul { margin: 8px 0 0 18px; color: #cbd5e1; font-size: 12.5px; line-height: 1.6; }
  </style>
</head>
<body data-theme="dark">
  <main class="card" role="region" aria-label="Knowledge map of modern web performance">
    <header class="card-header">
      <div>
        <h1>Modern Web Performance — Knowledge Map</h1>
        <p class="sub">Click a node to collapse · drag to pan · scroll to zoom · use the toolbar for fit / export</p>
      </div>
      <div class="toolbar" role="toolbar" aria-label="Mind map actions">
        <button class="btn" id="themeToggle" type="button" aria-label="Toggle theme">Theme</button>
        <button class="btn" id="expand"      type="button" aria-label="Expand all nodes">Expand all</button>
        <button class="btn" id="collapse"    type="button" aria-label="Collapse to depth 2">Collapse</button>
        <button class="btn" id="fit"         type="button" aria-label="Fit to view">Fit</button>
        <button class="btn primary" id="exportSvg" type="button" aria-label="Export as SVG">Export SVG</button>
      </div>
    </header>

    <div class="markmap-wrap">
      <div class="markmap" role="img" aria-label="Mind map of modern web performance topics"
           data-markmap='{"maxWidth":280,"colorFreezeLevel":2,"initialExpandLevel":3,"duration":600,"spacingHorizontal":90,"spacingVertical":8,"paddingX":10}'>
<script type="text/template">
# Modern Web Performance

## Core Web Vitals
### LCP — Largest Contentful Paint
- Target: < **2.5 s**
- Optimize the hero image (`fetchpriority="high"`, `preload`)
- Avoid blocking CSS / JS in the head
- Serve via [CDN](https://web.dev/cdn-best-practices/)

### INP — Interaction to Next Paint
- Target: < **200 ms**
- Break long tasks with `scheduler.yield()`
- Defer non-essential work to `requestIdleCallback`
- Lighten event handlers (debounce, throttle)

### CLS — Cumulative Layout Shift
- Target: < **0.1**
- Reserve space for images (`width`/`height` or `aspect-ratio`)
- Avoid inserting content above existing content
- Pin web fonts (`font-display: optional`)

## Network
### HTTP/3 + QUIC
- 0-RTT resumption
- Multiplexed streams without head-of-line blocking
### Caching
- `Cache-Control: immutable, max-age=31536000`
- Stale-while-revalidate for dynamic data
### Compression
- Brotli for text (`-q 11` for static assets)
- AVIF/WebP for images, fall back to JPEG/PNG

## Rendering
### Critical CSS
- Inline above-the-fold CSS in the `<head>`
- Defer the rest with `media="print"` + `onload`
### JavaScript
```js
// Defer non-critical scripts
<script src="x.js" defer></script>
```
- Code-split per route
- Tree-shake unused exports
- Prefer ES modules over UMD bundles

### Fonts
- Subset to used glyphs (`unicode-range`)
- Self-host with `preload`
- `font-display: swap` to avoid invisible text

## Measurement
### Field data (RUM)
- Chrome User Experience Report (CrUX)
- `PerformanceObserver` for `largest-contentful-paint`, `layout-shift`
- Send to an analytics endpoint
### Lab data
- Lighthouse CI in the build pipeline
- WebPageTest filmstrip + waterfall
- Chrome DevTools Performance panel

## Architecture
### Edge rendering
- Render at the CDN edge (Cloudflare Workers, Vercel Edge)
- Cache personalized HTML at the edge with ESI / fragments
### Islands
- Server-render the page shell, hydrate interactive widgets only
- Frameworks: Astro, Fresh, Qwik

### Progressive enhancement
- Ship working HTML first
- Layer JS for interactivity
- Layer service workers for offline
</script>
      </div>
    </div>

    <!-- Accessible plain-text fallback for screen readers / no-script -->
    <details class="outline">
      <summary>Outline (text alternative)</summary>
      <ul>
        <li>Core Web Vitals — LCP, INP, CLS</li>
        <li>Network — HTTP/3, caching, compression</li>
        <li>Rendering — critical CSS, JavaScript, fonts</li>
        <li>Measurement — field data, lab data</li>
        <li>Architecture — edge rendering, islands, progressive enhancement</li>
      </ul>
    </details>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.18"></script>
  <script>
    const DARK = {
      bg:'#0f1117', card:'#1a1d27', border:'rgba(255,255,255,0.08)', text:'#e2e8f0', muted:'#94a3b8',
      palette: ['#6366f1','#8b5cf6','#ec4899','#06b6d4','#22c55e','#eab308','#f97316','#f43f5e'],
    };
    const LIGHT = {
      bg:'#f8fafc', card:'#ffffff', border:'rgba(0,0,0,0.08)', text:'#1e293b', muted:'#475569',
      palette: ['#4f46e5','#7c3aed','#db2777','#0891b2','#16a34a','#ca8a04','#ea580c','#dc2626'],
    };

    let theme = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    let mm = null;

    // The autoloader mounts after DOMContentLoaded; wait for the next tick.
    window.addEventListener('load', () => {
      const container = document.querySelector('.markmap');
      mm = container.markmap;        // Markmap instance attached by the autoloader

      applyTheme();

      // Attach built-in toolbar (zoom in / zoom out / fit / recenter) in the bottom-right
      if (window.markmap?.Toolbar) {
        const tb = window.markmap.Toolbar.create(mm);
        tb.el.style.cssText = 'position:absolute;bottom:14px;right:14px;background:rgba(30,33,48,0.85);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:4px;box-shadow:0 4px 16px rgba(0,0,0,0.4)';
        document.querySelector('.markmap-wrap').appendChild(tb.el);
      }
    });

    function walk(n, fn) { fn(n); (n.children || []).forEach(c => walk(c, fn)); }

    function applyTheme() {
      const t = theme === 'dark' ? DARK : LIGHT;
      document.body.style.background = t.bg;
      const card = document.querySelector('.card');
      card.style.background  = t.card;
      card.style.borderColor = t.border;
      document.querySelector('.markmap').style.background = t.card;
      document.querySelectorAll('h1').forEach(el => el.style.color = t.text);
      document.querySelectorAll('p.sub').forEach(el => el.style.color = t.muted);
      mm?.setOptions({ color: (n) => t.palette[(n.state.path.length - 1) % t.palette.length] });
      mm?.fit();
    }

    document.getElementById('themeToggle').addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      document.body.dataset.theme = theme;
      applyTheme();
    });

    document.getElementById('expand').addEventListener('click', () => {
      walk(mm.state.data, n => { if (n.payload) n.payload.fold = 0; });
      mm.renderData(); mm.fit();
    });

    document.getElementById('collapse').addEventListener('click', () => {
      walk(mm.state.data, n => {
        if (n.payload && n.state.path.length > 2) n.payload.fold = 1;
        else if (n.payload) n.payload.fold = 0;
      });
      mm.renderData(); mm.fit();
    });

    document.getElementById('fit').addEventListener('click', () => mm.fit());

    document.getElementById('exportSvg').addEventListener('click', () => {
      const svg = document.querySelector('.markmap svg').cloneNode(true);
      const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
      const t = theme === 'dark' ? DARK : LIGHT;
      style.textContent = `
        text, div { font-family: Segoe UI, -apple-system, sans-serif; color: ${t.text}; }
        .markmap-foreign div  { color: ${t.text}; line-height: 1.5; }
        .markmap-foreign a    { color: #818cf8; }
        .markmap-foreign code { background: rgba(255,255,255,0.06); color: #c7d2fe; padding: 1px 5px; border-radius: 4px; }
      `;
      svg.insertBefore(style, svg.firstChild);
      const xml  = new XMLSerializer().serializeToString(svg);
      const blob = new Blob(['<?xml version="1.0" standalone="no"?>\n', xml], { type: 'image/svg+xml' });
      const url  = URL.createObjectURL(blob);
      const a    = Object.assign(document.createElement('a'), { href: url, download: 'web-performance.svg' });
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 0);
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No height on `.markmap`** — the SVG sizes to its container; `height: auto` collapses it to 0px and the map vanishes
- **Multiple `# Root` headings** — produces disconnected trees and broken layout. Always use exactly one top-level `#`
- **Raw Markdown inside the div** — inline `<` characters (in code or HTML) get parsed as tags. Wrap the Markdown in `<script type="text/template">…</script>` for safety
- **Forgetting the autoloader bundle is async** — it mounts after `DOMContentLoaded`, so reach for `container.markmap` inside `window.onload` or with a small `requestAnimationFrame` delay, not synchronously after the script tag
- **No `maxWidth`** — long bullets render as one very wide row, blowing out the layout. Set `maxWidth: 260–320`
- **Treating the script tag's `data-markmap` as JavaScript** — it must be valid **JSON** (double quotes, no trailing commas)
- **Calling `mm.setData()` with raw Markdown** — `setData()` expects the **transformed root** from `new Transformer().transform(md).root`, not the Markdown string
- **Adding fonts/icons but expecting them to inline on export** — pass `embedAssets: true` if your exported SVG needs to be portable, or inline a `<style>` block manually before serializing (see Step 8)
- **Using `initialExpandLevel: -1` on huge maps** — every node animates in on first paint; with 200+ nodes the first frame stalls. Start at 2–3 and let the user expand
- **Hiding the toolbar entirely and offering no keyboard alternative** — touch + scroll-zoom users need at least a Fit button; provide one in the card header
