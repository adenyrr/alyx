---
name: excalidraw
description: Embed a hand-drawn, sketch-style whiteboard using the Excalidraw React component, delivered as a self-contained HTML artifact via React UMD + the @excalidraw/excalidraw production build. Use this skill whenever the request involves a freeform drawing canvas, sketchy diagrams, brainstorming surfaces, collaborative-feel whiteboards, infinite canvas for hand-drawn shapes, rough/wireframe diagrams, on-the-fly architecture sketches, or any "make me a whiteboard" / "let me draw" / "sketch this" output. Trigger on requests like "embed a whiteboard", "let users sketch on a canvas", "rough wireframe diagram", "collaborative drawing board", or "Excalidraw clone in a page". Do NOT use for: precise vector graphics or pixel-perfect canvas editors (→ konva-canvas skill), schematic flowcharts generated from text (→ mermaid-diagrams skill), editable node-link flowcharts with anchored connectors (→ jointjs-flowchart skill), generative art (→ p5js-creative-coding skill), or animated SVG storytelling (→ animejs-animation skill).
agents: [dev]
---

# Excalidraw Skill — Embedded Whiteboard (v0.17 UMD)

Excalidraw is a virtual whiteboard with a hand-drawn, sketchy look. It is a React component published as `@excalidraw/excalidraw`, and it ships a UMD build that runs directly in the browser without any bundler. You wire up `React` + `ReactDOM` from a CDN, mount the `<Excalidraw />` component into a container, and you have a full whiteboard — infinite canvas, freedraw, rectangles, arrows, text, sticky notes, undo/redo, zoom, multi-select, export.

---

## Artifact Presentation & Use Cases

Every Excalidraw artifact is a self-contained HTML page with a dark theme by default. The visual structure follows the standard project pattern:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow, `overflow: hidden`) clips the canvas
- **Card header** carries the title, subtitle, and a custom toolbar (Export PNG, Export SVG, Reset)
- **Whiteboard container** (`#app`, fixed height 540–640px) hosts the React-mounted `<Excalidraw />`
- The component handles its own toolbar, library panel, zoom controls, and shortcut help dialog

### Typical use cases

- **On-page brainstorming canvas** — embed in docs, blog posts, internal tools
- **Architecture / wireframe sketches** — drop into design reviews, technical RFCs
- **Lightweight collaborative-feel board** — capture state via `onChange`, send over a channel, replay on peers
- **Teaching / tutorial annotations** — overlay sketches on screenshots imported via paste
- **Mind-mapping / sticky-note clustering** — sticky notes + arrows in a freeform layout
- **Live demo of a drawing tool** — minimal viable example for showing off the `@excalidraw/excalidraw` API

### What the user sees

A polished, infinite whiteboard inside a dark card: pick a tool from the floating toolbar, draw with the freehand pen, snap rectangles to grid, drop text or sticky notes, drag to pan, scroll/pinch to zoom, undo/redo, and export the current scene as a PNG or SVG via the custom toolbar above the canvas.

---

## When to Use Excalidraw vs. Alternatives

| Use Excalidraw when… | Use another library when… |
|---|---|
| You want a sketchy, hand-drawn whiteboard | You need precise pixel/vector editing → **Konva** |
| Freeform drawing, sticky notes, arrows | Diagrams generated from text (mermaid syntax) → **Mermaid** |
| Infinite canvas with pan + zoom out of the box | Editable node-link graphs with anchored ports → **JointJS** |
| Multi-select, copy/paste, library panel | Force-directed network graphs → **vis-network** |
| Built-in export to PNG / SVG / JSON | Storytelling animations on shapes → **Anime.js / GSAP** |
| "Make a whiteboard" / "let me draw" requests | Sound, particles, generative art → **p5.js** |
| Sketch-style architecture diagrams | Strict UML or BPMN diagramming → **JointJS** |

> **Rule of thumb:** if the user says "whiteboard", "sketch", "rough diagram", or "let me draw", reach for Excalidraw. If they say "flowchart", "wireframe with constraints", or "annotated image", look elsewhere.

---

## Step 1 — CDN Setup

Excalidraw requires React 18 + ReactDOM 18 (peer deps) before the Excalidraw UMD bundle.

```html
<!-- 1. React + ReactDOM 18 (production UMD) -->
<script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"     crossorigin></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>

<!-- 2. Excalidraw v0.17 UMD — exposes the global `ExcalidrawLib` -->
<script src="https://cdn.jsdelivr.net/npm/@excalidraw/excalidraw@0.18.1/dist/excalidraw.production.min.js"></script>
```

The UMD bundle exposes a single global, `ExcalidrawLib`, which contains the React component and the helper utilities:

```javascript
const {
  Excalidraw,                  // the React component
  exportToSvg,                 // → SVGElement
  exportToBlob,                // → Blob (PNG/JPEG)
  exportToCanvas,              // → HTMLCanvasElement
  serializeAsJSON,             // → string (.excalidraw save format)
  loadFromBlob,                // ← .excalidraw / .png / .svg
  THEME,                       // { LIGHT: 'light', DARK: 'dark' }
  MIME_TYPES,
  getSceneVersion,
} = ExcalidrawLib;
```

> **No JSX in the browser.** The UMD bundle doesn't ship a Babel transform. Either write components with `React.createElement(...)` directly, or pull in the Babel standalone runtime if JSX really helps. The examples below use `React.createElement` aliased as `h` — readable, no transform needed.

> **Critical:** the host container **must have an explicit CSS height**. Without it the Excalidraw canvas collapses to 0px and you see an empty card.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Whiteboard</title>
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
    .toolbar { display: flex; gap: 8px; flex-wrap: wrap; }
    .btn {
      background: rgba(255,255,255,0.06); color: #94a3b8;
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 8px; padding: 7px 14px; font-size: 12px; font-weight: 500;
      cursor: pointer; transition: all 200ms cubic-bezier(0.16,1,0.3,1);
    }
    .btn:hover  { background: rgba(255,255,255,0.1); color: #f1f5f9; transform: translateY(-1px); }
    .btn.primary { background: #6366f1; color: #fff; border-color: transparent; }
    .btn.primary:hover { background: #5254cc; }
    .btn:focus-visible { outline: 2px solid #818cf8; outline-offset: 2px; }

    /* REQUIRED: explicit container height */
    #app { width: 100%; height: 620px; position: relative; }
  </style>
</head>
<body>
  <main class="card" role="region" aria-label="Whiteboard">
    <header class="card-header">
      <div>
        <h1>Whiteboard</h1>
        <p class="sub">Pick a tool · click to draw · drag to pan · scroll to zoom</p>
      </div>
      <div class="toolbar" role="toolbar" aria-label="Whiteboard actions">
        <button class="btn" id="reset"      type="button">Reset</button>
        <button class="btn" id="exportSvg"  type="button">Export SVG</button>
        <button class="btn primary" id="exportPng" type="button">Export PNG</button>
      </div>
    </header>
    <div id="app" role="application" aria-label="Excalidraw whiteboard canvas"></div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"     crossorigin></script>
  <script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://cdn.jsdelivr.net/npm/@excalidraw/excalidraw@0.18.1/dist/excalidraw.production.min.js"></script>
  <script>
    // App code here
  </script>
</body>
</html>
```

---

## Step 3 — Themes (dark default + light alternative)

Excalidraw has a first-class `theme` prop: `'dark'` or `'light'`. The component re-styles the canvas, toolbar, and dialogs. Pair it with matching tokens on the surrounding card.

### Dark theme tokens (default)

```javascript
const DARK = {
  bg:      '#0f1117',
  card:    '#1a1d27',
  border:  'rgba(255,255,255,0.08)',
  text:    '#e2e8f0',
  muted:   '#94a3b8',
  accent:  '#6366f1',
  theme:   'dark',           // Excalidraw theme prop
  stroke:  '#a5b4fc',        // default stroke color for new shapes
  fill:    '#1e2130',
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
  theme:   'light',
  stroke:  '#1e293b',
  fill:    '#ffffff',
};
```

### Theme switcher via `data-theme` and `prefers-color-scheme`

```html
<body data-theme="dark">
  <button class="btn" id="themeToggle" type="button" aria-label="Toggle theme">Theme</button>
  <!-- … -->
</body>
```

```javascript
const themes = { dark: DARK, light: LIGHT };
let theme = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
document.body.dataset.theme = theme;

function paintShell(t) {
  document.body.style.background = t.bg;
  document.querySelector('.card').style.background = t.card;
  document.querySelector('.card').style.borderColor = t.border;
  document.querySelector('h1').style.color = t.text;
  document.querySelectorAll('p.sub, .btn').forEach(el => { if (!el.classList.contains('primary')) el.style.color = t.muted; });
}

document.getElementById('themeToggle').addEventListener('click', () => {
  theme = theme === 'dark' ? 'light' : 'dark';
  document.body.dataset.theme = theme;
  paintShell(themes[theme]);
  rerender();   // re-render the React tree with the new theme prop — see Step 4
});
```

> The Excalidraw canvas background follows the `theme` prop and can be overridden via `initialData.appState.viewBackgroundColor`. Match it to the card surface (`#1a1d27` in dark, `#ffffff` in light) so the canvas feels embedded.

---

## Step 4 — Mounting the Component

Use `React.createElement` (aliased as `h`) instead of JSX so no transform is needed.

```javascript
const { Excalidraw, THEME } = ExcalidrawLib;
const h = React.createElement;

let api = null;              // ExcalidrawImperativeAPI — set via ref callback
let currentTheme = 'dark';

function App() {
  // useCallback to keep the ref stable across renders
  const refCallback = React.useCallback((excalidrawApi) => { api = excalidrawApi; }, []);

  return h(Excalidraw, {
    theme: currentTheme === 'dark' ? THEME.DARK : THEME.LIGHT,
    excalidrawAPI: refCallback,
    initialData: {
      elements: [],          // pre-existing shapes (see Step 6)
      appState: {
        viewBackgroundColor: currentTheme === 'dark' ? '#1a1d27' : '#ffffff',
        currentItemStrokeColor: currentTheme === 'dark' ? '#a5b4fc' : '#1e293b',
        currentItemBackgroundColor: 'transparent',
        gridSize: 20,
      },
      scrollToContent: true,
    },
    onChange: (elements, appState, files) => {
      // Fires on every interaction — debounce before persisting
    },
    UIOptions: {
      canvasActions: {
        loadScene: true,
        saveToActiveFile: false,    // hide native file-save (we provide custom Export)
        export: false,              // hide built-in export menu (custom toolbar handles it)
        toggleTheme: false,
        clearCanvas: true,
        changeViewBackgroundColor: true,
      },
    },
    name: 'sketch',           // default filename for built-in saves
    autoFocus: true,          // capture keyboard immediately
    detectScroll: true,
    handleKeyboardGlobally: false,   // don't steal shortcuts outside the canvas
  });
}

const root = ReactDOM.createRoot(document.getElementById('app'));
function rerender() { root.render(h(App)); }
rerender();
```

---

## Step 5 — Key Props Reference

| Prop | Type | Notes |
|---|---|---|
| `theme` | `'light' \| 'dark'` | Switches toolbar + canvas chrome |
| `initialData` | `{ elements, appState, files, scrollToContent }` | Seed the scene on mount |
| `excalidrawAPI` | `(api) => void` | Ref callback exposing the imperative API (Step 7) |
| `onChange` | `(elements, appState, files) => void` | Fires on every edit — debounce for persistence |
| `onPointerUpdate` | `({ pointer, button, pointersMap }) => void` | Live cursor (use for fake-collaborator demos) |
| `onPointerDown` / `onScrollChange` | callbacks | Lower-level pointer hooks |
| `UIOptions.canvasActions` | object | Toggle items in the "hamburger" canvas menu |
| `UIOptions.tools` | `{ image: false }` | Hide the image tool from the toolbar |
| `viewModeEnabled` | boolean | Read-only mode (no editing) |
| `zenModeEnabled` | boolean | Hide UI chrome — pure canvas |
| `gridModeEnabled` | boolean | Show a snap grid |
| `name` | string | Default filename for built-in save |
| `langCode` | e.g. `'en'`, `'fr-FR'` | UI language |
| `autoFocus` | boolean | Capture keyboard on mount |
| `renderTopRightUI` / `renderCustomStats` | functions | Inject custom React UI into Excalidraw |

---

## Step 6 — Excalidraw Element Shape

Every shape on the canvas is an "Excalidraw element" — a plain JS object. You can seed the scene with `initialData.elements`:

```javascript
const seed = [
  {
    type: 'rectangle',
    id: 'r1', x: 200, y: 120, width: 220, height: 110,
    angle: 0, strokeColor: '#a5b4fc', backgroundColor: 'transparent',
    fillStyle: 'hachure', strokeWidth: 2, strokeStyle: 'solid', roughness: 1, opacity: 100,
    seed: 42, version: 1, versionNonce: 0, isDeleted: false,
    groupIds: [], frameId: null, roundness: { type: 3 },
    boundElements: [], updated: 1, link: null, locked: false,
  },
  {
    type: 'text',
    id: 't1', x: 220, y: 160, width: 180, height: 30,
    angle: 0, strokeColor: '#f1f5f9', backgroundColor: 'transparent',
    fillStyle: 'solid', strokeWidth: 1, strokeStyle: 'solid', roughness: 1, opacity: 100,
    seed: 7, version: 1, versionNonce: 0, isDeleted: false,
    groupIds: [], frameId: null, roundness: null,
    boundElements: [], updated: 1, link: null, locked: false,
    text: 'Hello, world', fontSize: 24, fontFamily: 1,
    textAlign: 'center', verticalAlign: 'middle', baseline: 18,
    containerId: null, originalText: 'Hello, world', lineHeight: 1.25,
  },
];
```

`type` can be `rectangle | ellipse | diamond | line | arrow | freedraw | text | image | frame`. In practice you don't hand-write elements often — instead you let users draw, capture the resulting array via `onChange`, and replay it with `initialData.elements`.

---

## Step 7 — Imperative API (via ref callback)

The ref callback supplied to `excalidrawAPI` gives you a programmatic handle on the scene:

```javascript
api.updateScene({ elements: newElements, appState: { ... } });
api.getSceneElements();          // current non-deleted elements
api.getAppState();               // viewport, theme, selected items, …
api.getFiles();                  // image map for embedded images
api.scrollToContent(elements);   // pan/zoom so given elements fill the viewport
api.zoomToFit();                 // alias for scrollToContent(all)
api.resetScene();                // clears the canvas
api.history.clear();             // wipe undo/redo stack
api.refresh();                   // recompute layout (call after container resize)
api.setActiveTool({ type: 'selection' });   // or 'freedraw', 'rectangle', 'arrow', 'text', …
api.addFiles([{ id, dataURL, mimeType, created }]);
```

Keep a reference (`let api = null`) at module scope and use it from your custom toolbar (Step 8).

---

## Step 8 — Custom Toolbar: Reset, Export SVG, Export PNG

The header buttons in Step 2's shell are wired to the imperative API and helper exporters:

```javascript
const { exportToSvg, exportToBlob } = ExcalidrawLib;

document.getElementById('reset').addEventListener('click', () => {
  if (!api) return;
  api.resetScene();
  api.history.clear();
});

document.getElementById('exportSvg').addEventListener('click', async () => {
  if (!api) return;
  const elements = api.getSceneElements();
  if (!elements.length) return flash('Canvas is empty');
  const svg = await exportToSvg({
    elements,
    appState: { ...api.getAppState(), exportBackground: true, exportPadding: 24 },
    files: api.getFiles(),
  });
  const blob = new Blob([new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' });
  download(blob, 'sketch.svg');
});

document.getElementById('exportPng').addEventListener('click', async () => {
  if (!api) return;
  const elements = api.getSceneElements();
  if (!elements.length) return flash('Canvas is empty');
  const blob = await exportToBlob({
    elements,
    appState: { ...api.getAppState(), exportBackground: true, exportPadding: 24 },
    files: api.getFiles(),
    mimeType: 'image/png',
    quality: 0.95,
  });
  download(blob, 'sketch.png');
});

function download(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'), { href: url, download: name });
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 0);
}

function flash(msg) {
  const el = document.createElement('div');
  el.textContent = msg;
  el.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e2130;color:#e2e8f0;border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px 16px;font-size:13px;box-shadow:0 8px 32px rgba(0,0,0,0.5);z-index:1000';
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1500);
}
```

`exportToSvg` returns a real `SVGElement` — useful for inline embedding. `exportToBlob` returns a `Blob` ready for download. `exportToCanvas` returns an `HTMLCanvasElement` for further manipulation.

---

## Step 9 — Persisting & Re-loading Scenes

Excalidraw scenes are pure JSON. Serialize them, store anywhere (state, URL, a backend), and replay via `initialData`.

```javascript
const { serializeAsJSON, loadFromBlob } = ExcalidrawLib;

// Save current scene as a string
function saveScene() {
  return serializeAsJSON(api.getSceneElements(), api.getAppState(), api.getFiles(), 'local');
}

// Load from a JSON string
async function loadScene(jsonText) {
  const blob = new Blob([jsonText], { type: 'application/vnd.excalidraw+json' });
  const data = await loadFromBlob(blob, null, null);
  api.updateScene({ elements: data.elements, appState: data.appState });
  if (data.files) api.addFiles(Object.values(data.files));
}

// onChange + debounce → live persistence (useState / postMessage / WebSocket / …)
let saveTimer = null;
function debouncedSave(elements, appState, files) {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    const payload = serializeAsJSON(elements, appState, files, 'local');
    // sessionStorage / channel.postMessage / fetch('/save', { body: payload }) …
  }, 400);
}
```

> Excalidraw does **not** persist anything itself. The library is purely controlled — every state change comes back through `onChange`, and you choose where to put it.

---

## Step 10 — Collaborative-Feel Touches

Even without a real backend, you can fake a multi-cursor look with `onPointerUpdate` + `api.updateScene({ collaborators })`:

```javascript
const ghostCursors = new Map();
ghostCursors.set('alex',  { username: 'Alex',  pointer: { x: 320, y: 220 }, button: 'up', selectedElementIds: {}, color: { background: '#ec4899', stroke: '#ec4899' } });
ghostCursors.set('priya', { username: 'Priya', pointer: { x: 580, y: 340 }, button: 'up', selectedElementIds: {}, color: { background: '#22c55e', stroke: '#22c55e' } });

setInterval(() => {
  // Gently jitter ghost cursors so the canvas feels alive
  for (const c of ghostCursors.values()) {
    c.pointer.x += (Math.random() - 0.5) * 6;
    c.pointer.y += (Math.random() - 0.5) * 6;
  }
  api?.updateScene({ collaborators: ghostCursors });
}, 60);
```

For a real implementation, swap the `setInterval` for a WebSocket push of remote pointer events.

---

## Step 11 — Accessibility

- The wrapping `<div id="app" role="application" aria-label="…">` exposes the canvas as an interactive region for screen readers.
- Excalidraw's built-in toolbar is keyboard navigable: `1–9` pick tools, `V` for selection, `Z` undo, `Shift+Z` redo, `Delete` removes selection, `Ctrl/Cmd+A` selects all. Document these in the subtitle so users discover them.
- Buttons in the custom toolbar must have `type="button"` (avoid implicit form submission), `aria-label`, and a visible `:focus-visible` outline.
- Keep ≥ 4.5:1 contrast between toolbar text and the card surface — the design tokens in Step 3 satisfy this.
- For canvases used in critical workflows, provide a textual summary or alt-export path — the rendered sketch alone is not screen-reader accessible.

---

## Step 12 — Design & Polish Guidelines

- **Match canvas background to card surface.** Set `appState.viewBackgroundColor` to `#1a1d27` (dark) or `#ffffff` (light) so the whiteboard reads as part of the card.
- **Hide the built-in export/menu items you replace** via `UIOptions.canvasActions: { export: false, saveToActiveFile: false }` — duplicate controls confuse users.
- **Custom toolbar lives in the card header**, never inside the canvas — preserves Excalidraw's familiar shortcuts.
- **Use sketchy fill (`fillStyle: 'hachure'`) for shapes**, solid for text — this is the Excalidraw look.
- **Set `gridSize: 20`** for snapping; toggle with the built-in `G` shortcut.
- **Debounce `onChange` persistence** (300–500 ms). The callback fires on every pointer move; saving raw will flood storage.
- **Resize handling.** If the host container size changes (collapse a panel, switch tabs), call `api.refresh()`.
- **Don't use JSX in the browser.** Without a transform step the file won't parse — use `React.createElement` or `h(...)`.

---

## Step 13 — Complete Example: Collaborative-feel Architecture Sketch

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Architecture sketch</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; padding: 24px; display: flex; flex-direction: column; align-items: center; }
    .card { width: 100%; max-width: 1200px; background: #1a1d27; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    .card-header { padding: 22px 24px 16px; border-bottom: 1px solid rgba(255,255,255,0.07); display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }
    .presence { display: flex; gap: -8px; margin-top: 6px; }
    .avatar { width: 24px; height: 24px; border-radius: 50%; border: 2px solid #1a1d27; font-size: 11px; font-weight: 700; color: #fff; display: flex; align-items: center; justify-content: center; margin-left: -8px; box-shadow: 0 2px 6px rgba(0,0,0,0.4); }
    .toolbar { display: flex; gap: 8px; flex-wrap: wrap; }
    .btn { background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 7px 14px; font-size: 12px; font-weight: 500; cursor: pointer; transition: all 200ms cubic-bezier(0.16,1,0.3,1); }
    .btn:hover { background: rgba(255,255,255,0.1); color: #f1f5f9; transform: translateY(-1px); }
    .btn.primary { background: #6366f1; color: #fff; border-color: transparent; }
    .btn.primary:hover { background: #5254cc; }
    .btn:focus-visible { outline: 2px solid #818cf8; outline-offset: 2px; }
    #app { width: 100%; height: 640px; position: relative; }
    .toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: #1e2130; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 10px 18px; font-size: 13px; box-shadow: 0 8px 32px rgba(0,0,0,0.5); z-index: 1000; opacity: 0; transition: opacity 200ms; }
    .toast.show { opacity: 1; }
  </style>
</head>
<body data-theme="dark">
  <main class="card" role="region" aria-label="Architecture sketch whiteboard">
    <header class="card-header">
      <div>
        <h1>Architecture sketch — System overview</h1>
        <p class="sub">Pick a tool · drag to pan · scroll/pinch to zoom · press <b>1</b>–<b>9</b> for tools · <b>Z</b>/<b>Shift+Z</b> undo · <b>G</b> grid</p>
        <div class="presence" aria-label="Live collaborators">
          <div class="avatar" style="background:#6366f1" title="You">YO</div>
          <div class="avatar" style="background:#ec4899" title="Alex">AL</div>
          <div class="avatar" style="background:#22c55e" title="Priya">PR</div>
        </div>
      </div>
      <div class="toolbar" role="toolbar" aria-label="Whiteboard actions">
        <button class="btn" id="themeToggle" type="button" aria-label="Toggle theme">Theme</button>
        <button class="btn" id="reset"       type="button" aria-label="Clear canvas">Reset</button>
        <button class="btn" id="exportSvg"   type="button" aria-label="Export as SVG">SVG</button>
        <button class="btn primary" id="exportPng" type="button" aria-label="Export as PNG">Export PNG</button>
      </div>
    </header>
    <div id="app" role="application" aria-label="Excalidraw whiteboard canvas"></div>
  </main>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js" crossorigin></script>
  <script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://cdn.jsdelivr.net/npm/@excalidraw/excalidraw@0.18.1/dist/excalidraw.production.min.js"></script>
  <script>
    const { Excalidraw, THEME, exportToSvg, exportToBlob } = ExcalidrawLib;
    const h = React.createElement;

    let api = null;
    let theme = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';

    const SURFACE = { dark: '#1a1d27', light: '#ffffff' };
    const STROKE  = { dark: '#a5b4fc', light: '#1e293b' };

    // ── Seed: a friendly system diagram so the canvas isn't empty on first paint
    function makeElement(over) {
      return {
        angle: 0, backgroundColor: 'transparent', fillStyle: 'hachure',
        strokeWidth: 2, strokeStyle: 'solid', roughness: 1, opacity: 100,
        seed: Math.floor(Math.random() * 1e9), version: 1, versionNonce: 0,
        isDeleted: false, groupIds: [], frameId: null, roundness: { type: 3 },
        boundElements: [], updated: Date.now(), link: null, locked: false,
        ...over,
      };
    }

    const seed = [
      makeElement({ type: 'rectangle', id: 'web',  x: 120, y: 140, width: 200, height: 90, strokeColor: STROKE[theme] }),
      makeElement({ type: 'text', id: 'webT', x: 150, y: 170, width: 140, height: 30, strokeColor: STROKE[theme],
        text: 'Web client', fontSize: 22, fontFamily: 1, textAlign: 'center', verticalAlign: 'middle',
        baseline: 18, containerId: null, originalText: 'Web client', lineHeight: 1.25 }),
      makeElement({ type: 'rectangle', id: 'api', x: 480, y: 140, width: 220, height: 90, strokeColor: STROKE[theme] }),
      makeElement({ type: 'text', id: 'apiT', x: 510, y: 170, width: 160, height: 30, strokeColor: STROKE[theme],
        text: 'API gateway', fontSize: 22, fontFamily: 1, textAlign: 'center', verticalAlign: 'middle',
        baseline: 18, containerId: null, originalText: 'API gateway', lineHeight: 1.25 }),
      makeElement({ type: 'rectangle', id: 'db', x: 860, y: 140, width: 200, height: 90, strokeColor: STROKE[theme] }),
      makeElement({ type: 'text', id: 'dbT', x: 900, y: 170, width: 120, height: 30, strokeColor: STROKE[theme],
        text: 'Postgres', fontSize: 22, fontFamily: 1, textAlign: 'center', verticalAlign: 'middle',
        baseline: 18, containerId: null, originalText: 'Postgres', lineHeight: 1.25 }),
      makeElement({ type: 'arrow', id: 'a1', x: 320, y: 185, width: 160, height: 0, strokeColor: '#6366f1',
        points: [[0,0],[160,0]], startBinding: null, endBinding: null,
        startArrowhead: null, endArrowhead: 'arrow', lastCommittedPoint: null }),
      makeElement({ type: 'arrow', id: 'a2', x: 700, y: 185, width: 160, height: 0, strokeColor: '#6366f1',
        points: [[0,0],[160,0]], startBinding: null, endBinding: null,
        startArrowhead: null, endArrowhead: 'arrow', lastCommittedPoint: null }),
    ];

    // ── Fake collaborator cursors
    const ghosts = new Map([
      ['alex',  { username: 'Alex',  pointer: { x: 540, y: 320, tool: 'pointer' }, button: 'up', selectedElementIds: {}, color: { background: '#ec4899', stroke: '#ec4899' } }],
      ['priya', { username: 'Priya', pointer: { x: 880, y: 280, tool: 'pointer' }, button: 'up', selectedElementIds: {}, color: { background: '#22c55e', stroke: '#22c55e' } }],
    ]);

    function App() {
      const refCb = React.useCallback((excalidrawApi) => {
        api = excalidrawApi;
        api.updateScene({ collaborators: ghosts });
      }, []);

      return h(Excalidraw, {
        theme: theme === 'dark' ? THEME.DARK : THEME.LIGHT,
        excalidrawAPI: refCb,
        initialData: {
          elements: seed,
          appState: {
            viewBackgroundColor: SURFACE[theme],
            currentItemStrokeColor: STROKE[theme],
            currentItemBackgroundColor: 'transparent',
            gridSize: 20,
            zoom: { value: 1 },
          },
          scrollToContent: true,
        },
        onChange: () => {},
        UIOptions: {
          canvasActions: {
            loadScene: false, saveToActiveFile: false, export: false, toggleTheme: false,
            clearCanvas: true, changeViewBackgroundColor: true,
          },
        },
        name: 'architecture-sketch', autoFocus: true, detectScroll: true, handleKeyboardGlobally: false,
      });
    }

    const root = ReactDOM.createRoot(document.getElementById('app'));
    function rerender() { root.render(h(App)); }
    rerender();

    // Drift ghosts so the canvas feels alive
    setInterval(() => {
      for (const c of ghosts.values()) {
        c.pointer.x += (Math.random() - 0.5) * 5;
        c.pointer.y += (Math.random() - 0.5) * 5;
      }
      api?.updateScene({ collaborators: ghosts });
    }, 70);

    // Toast helper
    const toast = document.getElementById('toast');
    function flash(msg) {
      toast.textContent = msg; toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 1400);
    }

    // Theme switcher
    document.getElementById('themeToggle').addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      document.body.dataset.theme = theme;
      document.body.style.background = theme === 'dark' ? '#0f1117' : '#f8fafc';
      document.querySelector('.card').style.background = SURFACE[theme];
      rerender();
      api?.updateScene({ appState: { viewBackgroundColor: SURFACE[theme] } });
    });

    // Reset
    document.getElementById('reset').addEventListener('click', () => {
      if (!api) return;
      api.resetScene();
      api.history.clear();
      flash('Canvas cleared');
    });

    // Export SVG
    document.getElementById('exportSvg').addEventListener('click', async () => {
      if (!api) return;
      const elements = api.getSceneElements();
      if (!elements.length) return flash('Canvas is empty');
      const svg = await exportToSvg({
        elements, files: api.getFiles(),
        appState: { ...api.getAppState(), exportBackground: true, exportPadding: 24 },
      });
      const blob = new Blob([new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' });
      download(blob, 'architecture-sketch.svg');
      flash('SVG downloaded');
    });

    // Export PNG
    document.getElementById('exportPng').addEventListener('click', async () => {
      if (!api) return;
      const elements = api.getSceneElements();
      if (!elements.length) return flash('Canvas is empty');
      const blob = await exportToBlob({
        elements, files: api.getFiles(),
        appState: { ...api.getAppState(), exportBackground: true, exportPadding: 24 },
        mimeType: 'image/png', quality: 0.95,
      });
      download(blob, 'architecture-sketch.png');
      flash('PNG downloaded');
    });

    function download(blob, name) {
      const url = URL.createObjectURL(blob);
      const a = Object.assign(document.createElement('a'), { href: url, download: name });
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 0);
    }

    // Refresh layout if the container ever resizes
    new ResizeObserver(() => api?.refresh()).observe(document.getElementById('app'));
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No height on `#app`** — Excalidraw's canvas collapses to 0px and renders nothing. Set an explicit pixel/vh height
- **Loading Excalidraw before React/ReactDOM** — the UMD bundle reads from `window.React` at script-evaluation time; load order matters
- **Writing JSX without a transform** — the browser can't parse JSX. Use `React.createElement` (often aliased to `h`) or add Babel standalone
- **Mutating the elements array** — Excalidraw treats `elements` as immutable. Always pass new arrays through `api.updateScene({ elements: [...] })`
- **Forgetting `excalidrawAPI` callback** — without it you have no handle on the imperative API; custom toolbar buttons cannot read or update the scene
- **Persisting on every `onChange`** — the callback fires on every pointer tick. Debounce 300–500 ms before writing to storage or the network
- **Stealing global keyboard shortcuts** — leave `handleKeyboardGlobally: false` unless the canvas is the entire viewport. Otherwise `Z`, `Ctrl+A`, etc. fire even when the user is typing elsewhere
- **Duplicate export controls** — when adding a custom export button, hide Excalidraw's built-in via `UIOptions.canvasActions.export: false`
- **Theme prop not re-rendering** — Excalidraw reads `theme` per render; toggling a module-level variable isn't enough, you must trigger a React re-render (e.g., a parent component's `useState`, or re-call `root.render()`)
- **`form` elements wrapping the toolbar** — clicking buttons inside a `<form>` submits and reloads the page. Use `type="button"` on every action button
