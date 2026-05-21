---
name: lit
description: Build reusable, framework-agnostic web components using Lit 3 (LitElement + lit-html), delivered as self-contained HTML artifacts via an ES-module importmap. Use this skill when the user wants encapsulated custom elements (`<weather-card>`, `<rating-stars>`, `<chip-input>`, `<toast-notify>`, `<command-palette>`), embeddable widgets that work in any framework, design-system components with Shadow DOM scoping, or a tiny component-based UI without React. Trigger on phrases like "build a custom element", "create a `<...>` web component", "reusable widget", "Lit component", "shadow DOM component", "framework-agnostic UI", "make X embeddable". Do NOT use for: server-driven HTML fragments (→ htmx), full React UIs with shadcn (→ shadcn / React artifact), rich text editing (→ tiptap), charts (→ chartjs / plotly), generative art (→ p5js / threejs).
agents: [dev]
---

# Lit Skill — v3

Lit is a tiny (~6 KB gzipped) library on top of the Web Components standards (Custom Elements, Shadow DOM, ES Modules). `LitElement` is a base class with reactive properties; `lit-html` is its templating language using tagged template literals (`html\`…\``). Components are real HTML elements — you can drop `<my-component>` into any page, framework, or other component. Lit uses **Shadow DOM** by default, so CSS in `static styles` is scoped to the component and cannot leak in or out.

---

## Artifact Presentation & Use Cases

Every Lit artifact is a self-contained HTML page with a dark theme. The shell is the usual Alyx card, hosting one or more custom elements:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) frames the components
- **Title** (`h1`, 1.15rem, `#f1f5f9`) names the demo
- **Subtitle** (`p.sub`, 0.82rem, `#94a3b8`) describes the props / theme controls
- **Custom element(s)** rendered directly, each styled by its own Shadow DOM
- A theme toggle that flips the `theme` attribute / property on the custom element(s)

### Typical use cases

- **`<weather-card>`** — themed card showing temperature + conditions for a location
- **`<rating-stars>`** — interactive star rating with `value`, `max`, `readonly`, and a `change` event
- **`<chip-input>`** — text input that converts comma- or Enter-separated values into chips
- **`<toast-notify>`** — programmatically dispatched notifications with auto-dismiss
- **`<command-palette>`** — keyboard-first launcher overlay
- **`<copy-button>`** — single-button widget that copies text and confirms visually
- **Design-system primitives** — buttons, badges, cards, dialogs that work in any host page

### What the user sees

The page renders normal-looking HTML — except the elements have custom tag names like `<weather-card>`. They are fully interactive, themed, animated, and dispatch standard DOM `CustomEvent`s the host page can listen to. The Shadow DOM makes them perfectly isolated; nothing on the host page can accidentally restyle them, and they cannot break the host page's layout.

---

## When to Use Lit vs. Alternatives

| Use Lit when… | Use another approach when… |
|---|---|
| You need reusable, encapsulated components | Server-driven HTML swaps → **htmx** |
| The component should work in any framework | Component-state-heavy React UI → **shadcn / React** |
| Style isolation matters (Shadow DOM) | Rich text editing → **tiptap** |
| You want zero build step (importmap) | Data visualisation → **chartjs / plotly / d3** |
| Multiple instances of the same widget | Single one-off interactive page → just HTML + JS |
| Custom HTML element semantics (`<my-toast>`) | Generative art / canvas → **p5js / threejs** |
| Lightweight bundle (~6 KB) | Heavy UI library needs (forms, tables) → React + libraries |

> **Rule of thumb:** if you'd naturally describe the output with a tag name (`<rating-stars>`, `<weather-card>`), Lit is the right tool. If you'd describe it as "a page that does X", reach for plain HTML or htmx.

---

## Step 1 — Importmap & ES Module Setup

Lit ships as ES modules. Use an importmap so bare specifiers (`lit`, `lit/decorators.js`) resolve via a CDN. Decorators require either a build step or a JS engine that natively supports the proposal — **for artifacts, use the no-decorators class syntax** described in Step 4.

```html
<script type="importmap">
{
  "imports": {
    "lit":                       "https://esm.sh/lit@3.2.1",
    "lit/decorators.js":         "https://esm.sh/lit@3.2.1/decorators.js",
    "lit/directives/class-map.js":  "https://esm.sh/lit@3.2.1/directives/class-map.js",
    "lit/directives/style-map.js":  "https://esm.sh/lit@3.2.1/directives/style-map.js",
    "lit/directives/repeat.js":     "https://esm.sh/lit@3.2.1/directives/repeat.js",
    "lit/directives/when.js":       "https://esm.sh/lit@3.2.1/directives/when.js",
    "lit/directives/ref.js":        "https://esm.sh/lit@3.2.1/directives/ref.js",
    "@lit/context":                 "https://esm.sh/@lit/context@1.1.3"
  }
}
</script>
```

Then in a `<script type="module">`:

```javascript
import { LitElement, html, css } from 'lit';
```

> **Critical:** the importmap tag must appear before any `<script type="module">`. Browsers ignore importmaps that arrive late.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lit Component Demo</title>
  <style>
    /* Page chrome only — components style themselves inside their Shadow DOM */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    :root, [data-theme="dark"] {
      --bg:#0f1117; --card:#1a1d27; --border:rgba(255,255,255,0.08);
      --text:#e2e8f0; --muted:#94a3b8; --accent:#6366f1;
    }
    [data-theme="light"] {
      --bg:#f8fafc; --card:#ffffff; --border:rgba(0,0,0,0.08);
      --text:#1e293b; --muted:#475569; --accent:#6366f1;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg); color: var(--text); min-height: 100vh;
      display: flex; align-items: center; justify-content: center; padding: 24px;
      transition: background 200ms, color 200ms;
    }
    .card {
      background: var(--card); border: 1px solid var(--border);
      border-radius: 16px; padding: 32px; max-width: 720px; width: 100%;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
    h1 { font-size: 1.15rem; font-weight: 600; color: var(--text); }
    .theme-btn {
      background: transparent; color: var(--muted); border: 1px solid var(--border);
      border-radius: 8px; padding: 4px 10px; font-size: 0.72rem; cursor: pointer;
    }
    .theme-btn:hover { color: var(--text); }
    p.sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 20px; }
  </style>
</head>
<body data-theme="dark">
  <main class="card">
    <div class="head">
      <h1>Demo</h1>
      <button class="theme-btn" id="themeBtn" type="button">Toggle theme</button>
    </div>
    <p class="sub">Custom elements with isolated styles &middot; flip data-theme to switch</p>
    <!-- <my-component>…</my-component> -->
  </main>

  <script type="importmap">{ "imports": { … see Step 1 … } }</script>
  <script type="module">/* component definitions — see Step 4 */</script>
</body>
</html>
```

---

## Step 3 — Themes (dark + light)

Because Shadow DOM blocks page CSS, theming a Lit component requires one of three patterns:

### Pattern A: CSS custom properties (inheritable)

Custom properties pierce the Shadow DOM. Define tokens on `:host` with fallbacks, and override from the outer page.

```javascript
static styles = css`
  :host {
    --wc-bg:     var(--bg, #0f1117);
    --wc-card:   var(--card, #1a1d27);
    --wc-border: var(--border, rgba(255,255,255,0.08));
    --wc-text:   var(--text, #e2e8f0);
    --wc-muted:  var(--muted, #94a3b8);
    --wc-accent: var(--accent, #6366f1);
    display: block;
  }
`;
```

The outer page sets `--bg`, `--card`, etc. on `body` (or `html`), and they inherit into every component. Flipping `data-theme` on `<body>` updates them for every shadow tree at once.

### Pattern B: `theme` attribute / property

Reflect a `theme` property to an attribute and write `:host([theme="light"])` selectors. This is what the example below uses, so the component is **self-contained** and can override the inherited theme per-instance.

```javascript
static properties = { theme: { type: String, reflect: true } };

static styles = css`
  :host { /* dark defaults */ background: #1a1d27; color: #e2e8f0; }
  :host([theme="light"]) { background: #ffffff; color: #1e293b; }
`;
```

### Pattern C: Adopted stylesheets (advanced)

`document.adoptedStyleSheets` / `shadowRoot.adoptedStyleSheets` for sharing one `CSSStyleSheet` instance across components. Useful for design systems; overkill for single artifacts.

### Token reference (Alyx default palette)

| Token | Dark | Light |
|---|---|---|
| bg | `#0f1117` | `#f8fafc` |
| card | `#1a1d27` | `#ffffff` |
| border | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` |
| text | `#e2e8f0` | `#1e293b` |
| muted | `#94a3b8` | `#475569` |
| accent | `#6366f1` | `#6366f1` |

### Switching themes at runtime

```javascript
// Flips the outer page AND propagates `theme` to every custom element with the class
document.getElementById('themeBtn').addEventListener('click', () => {
  const next = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
  document.body.dataset.theme = next;
  document.querySelectorAll('weather-card').forEach((el) => (el.theme = next));
});
```

---

## Step 4 — LitElement: Class Syntax (No Decorators)

Decorators require a build step. In artifacts, use static class fields — same result, no transpiler.

```javascript
import { LitElement, html, css } from 'lit';

class HelloName extends LitElement {
  // ── Reactive properties ────────────────────────────────
  static properties = {
    name:   { type: String },
    count:  { type: Number, reflect: true },  // reflect = sync to attribute
    open:   { type: Boolean },
    items:  { type: Array,   attribute: false }, // not exposed as attribute
    theme:  { type: String,  reflect: true },
  };

  constructor() {
    super();
    this.name  = 'World';
    this.count = 0;
    this.open  = false;
    this.items = [];
    this.theme = 'dark';
  }

  // ── Scoped styles ──────────────────────────────────────
  static styles = css`
    :host { display: block; }
    button {
      background: #6366f1; color: white; border: none; border-radius: 8px;
      padding: 8px 16px; font-family: inherit; cursor: pointer;
    }
  `;

  // ── Template ───────────────────────────────────────────
  render() {
    return html`
      <p>Hello, ${this.name}.</p>
      <button @click=${this._increment}>Count: ${this.count}</button>
    `;
  }

  _increment() {
    this.count++;
    this.dispatchEvent(new CustomEvent('count-change', {
      detail: { count: this.count }, bubbles: true, composed: true,
    }));
  }
}

customElements.define('hello-name', HelloName);
```

### With decorators (only works if build step is available)

```javascript
import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

@customElement('hello-name')
class HelloName extends LitElement {
  @property({ type: String })  name = 'World';
  @property({ type: Number, reflect: true }) count = 0;
  @state() private _open = false;
  render() { return html`Hello, ${this.name}`; }
}
```

**For Alyx artifacts: always use class syntax** unless an importmap explicitly bundles a transpiler.

---

## Step 5 — Reactive Properties

Every property in `static properties` is reactive: setting it triggers `requestUpdate()`, which schedules a render on the next microtask.

| Option | Meaning |
|---|---|
| `type: String \| Number \| Boolean \| Array \| Object` | Attribute conversion |
| `reflect: true` | Property → attribute sync (lets CSS see it) |
| `attribute: false` | No attribute at all (property-only) |
| `attribute: 'my-name'` | Custom attribute name (kebab-case) |
| `state: true` | Internal state, no attribute, no public API |
| `converter` | Custom attribute ↔ property converter |
| `hasChanged(n, o)` | Skip update when returns false |

Internal-only state: use `state: true` (preferred) or a regular class field with manual `this.requestUpdate()`.

### Lifecycle hooks

```javascript
connectedCallback()        { super.connectedCallback();  /* added to DOM */ }
disconnectedCallback()     { super.disconnectedCallback(); /* removed */ }
willUpdate(changed)        { /* before render, compute derived state */ }
firstUpdated(changed)      { /* DOM exists, focus, measure, attach observers */ }
updated(changed)           { /* after every render */ }

// `changed` is a Map<propName, oldValue>:
updated(changed) {
  if (changed.has('theme')) this._onThemeChange();
}
```

---

## Step 6 — lit-html Template Syntax

`html\`…\`` is a tagged template literal. Bindings happen via `${...}`; prefix names tell Lit what kind of binding it is.

| Syntax | Binds to | Example |
|---|---|---|
| `${expr}` | Text node | `<p>${name}</p>` |
| `attr=${expr}` | Attribute (string) | `<img alt=${label}>` |
| `?disabled=${expr}` | Boolean attribute | `<button ?disabled=${busy}>` |
| `.value=${expr}` | DOM property | `<input .value=${query}>` |
| `@click=${handler}` | Event listener | `<button @click=${this._save}>` |
| `@click=${{handleEvent, once}}` | Listener with options | once / passive / capture |

### Composition & directives

```javascript
import { classMap } from 'lit/directives/class-map.js';
import { styleMap } from 'lit/directives/style-map.js';
import { repeat }   from 'lit/directives/repeat.js';
import { when }     from 'lit/directives/when.js';
import { ref, createRef } from 'lit/directives/ref.js';

const inputRef = createRef();

html`
  <div class=${classMap({ active: this.open, dim: !this.open })}
       style=${styleMap({ color: this.color, padding: '8px' })}>
    ${when(this.items.length, () =>
      html`<ul>${repeat(this.items, (it) => it.id, (it) =>
        html`<li>${it.label}</li>`)}</ul>`,
      () => html`<p class="empty">No items</p>`
    )}
    <input ${ref(inputRef)} placeholder="Search">
  </div>
`;
```

### Conditional rendering shortcuts

```javascript
${this.open ? html`<div>Open</div>` : ''}     // ternary
${this.error && html`<p class="err">${this.error}</p>`}   // short-circuit
${when(condition, () => html`A`, () => html`B`)}          // explicit
```

### Caching subtrees

```javascript
import { cache } from 'lit/directives/cache.js';
html`${cache(this.tab === 'a' ? html`<view-a></view-a>` : html`<view-b></view-b>`)}`;
```

---

## Step 7 — Slots (composition)

Slots let a host page distribute children into the component's Shadow DOM.

```javascript
render() {
  return html`
    <header><slot name="title">Default title</slot></header>
    <section><slot></slot></section>          <!-- default slot -->
    <footer><slot name="actions"></slot></footer>
  `;
}
```

Usage:

```html
<my-card>
  <h2 slot="title">Custom title</h2>
  <p>Body content lands in the default slot.</p>
  <button slot="actions">Save</button>
</my-card>
```

### Styling slotted content

```css
::slotted(h2)      { color: var(--accent); margin: 0; }
::slotted(button)  { font-weight: 500; }
```

`::slotted()` only matches direct children of the slotted element. Deep selectors are not allowed.

### Detecting slot changes

```javascript
render() {
  return html`<slot @slotchange=${this._onSlotChange}></slot>`;
}
_onSlotChange(e) {
  const nodes = e.target.assignedElements({ flatten: true });
  this._count = nodes.length;
}
```

---

## Step 8 — Scoped CSS via `static styles`

`static styles = css\`…\``; this is a `CSSResult` that Lit applies via Constructable StyleSheets (in supporting browsers). Styles are scoped to the Shadow DOM — they cannot leak out, and outer page styles cannot leak in (except inherited properties like custom properties, `color`, `font`).

```javascript
static styles = css`
  :host { display: block; padding: 16px; }
  :host([hidden]) { display: none; }
  :host(:hover) { background: rgba(255,255,255,0.04); }
  :host([theme="light"]) { background: #fff; color: #1e293b; }

  .row { display: flex; gap: 8px; align-items: center; }
  button { font-family: inherit; cursor: pointer; }
  button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

  @media (max-width: 480px) { .row { flex-direction: column; } }
`;
```

### Selector reference

| Selector | Matches |
|---|---|
| `:host` | The host element itself |
| `:host(.cls)` | The host with class `.cls` |
| `:host([open])` | The host with attribute `[open]` |
| `:host-context(.dark)` | The host when an ancestor matches `.dark` |
| `::slotted(p)` | A `<p>` slotted into a default slot |
| `::slotted([slot="title"])` | An element slotted into `slot="title"` |

### Sharing styles between components

```javascript
const sharedButton = css`
  button { background: var(--accent); color: white; border: none; }
`;
static styles = [sharedButton, css`/* extras */`];
```

---

## Step 9 — Events (CustomEvent dispatching)

Components communicate **up** via custom events. Always set `bubbles: true, composed: true` so events cross the Shadow DOM boundary into the host page.

```javascript
this.dispatchEvent(new CustomEvent('rating-change', {
  detail:   { value: this.value, max: this.max },
  bubbles:  true,
  composed: true,    // REQUIRED to escape the shadow root
}));
```

### Listening on the host page

```html
<rating-stars value="3" max="5"></rating-stars>
<script>
  document.querySelector('rating-stars')
    .addEventListener('rating-change', (e) => console.log(e.detail.value));
</script>
```

### Inside another component's template

```javascript
html`<rating-stars value=${this.r} @rating-change=${this._onRate}></rating-stars>`
```

> Don't use camelCase for event names — use kebab-case (`rating-change`, not `ratingChange`). This matches the DOM event convention.

---

## Step 10 — Context API (`@lit/context`)

For sharing state across deeply nested components without prop-drilling, use the Lit context protocol. Producer and consumer are decoupled — any ancestor providing a context key serves any descendant consuming it.

```javascript
import { createContext, provide, consume, ContextProvider, ContextConsumer } from '@lit/context';

// 1. Define the key + type
export const themeContext = createContext('alyx-theme');

// 2. Provider component (without decorators)
class ThemeProvider extends LitElement {
  constructor() {
    super();
    this._provider = new ContextProvider(this, { context: themeContext, initialValue: 'dark' });
  }
  setTheme(t) {
    this._provider.setValue(t);
  }
  render() { return html`<slot></slot>`; }
}
customElements.define('theme-provider', ThemeProvider);

// 3. Consumer component
class ThemedThing extends LitElement {
  static properties = { _theme: { state: true } };
  constructor() {
    super();
    new ContextConsumer(this, {
      context: themeContext,
      subscribe: true,
      callback: (value) => { this._theme = value; },
    });
  }
  render() { return html`<p>Theme is ${this._theme}</p>`; }
}
customElements.define('themed-thing', ThemedThing);
```

```html
<theme-provider>
  <themed-thing></themed-thing>
  <themed-thing></themed-thing>
</theme-provider>
```

---

## Step 11 — Complete Example: `<weather-card>` with Dark/Light Theme

A polished weather card custom element. Supports `location`, `temp`, `conditions`, `humidity`, `wind`, and a `theme` property that switches the whole component between dark and light palettes. Dispatches a `refresh` event when the refresh button is clicked.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>weather-card demo</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    :root, [data-theme="dark"] {
      --bg:#0f1117; --card:#1a1d27; --border:rgba(255,255,255,0.08);
      --text:#e2e8f0; --muted:#94a3b8; --accent:#6366f1;
    }
    [data-theme="light"] {
      --bg:#f8fafc; --card:#ffffff; --border:rgba(0,0,0,0.08);
      --text:#1e293b; --muted:#475569; --accent:#6366f1;
    }
    body {
      font-family: -apple-system, 'Segoe UI', sans-serif;
      background: var(--bg); color: var(--text); min-height: 100vh;
      display: flex; align-items: center; justify-content: center; padding: 24px;
      transition: background 200ms, color 200ms;
    }
    .page {
      max-width: 880px; width: 100%;
      background: var(--card); border: 1px solid var(--border);
      border-radius: 16px; padding: 32px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
    h1 { font-size: 1.15rem; font-weight: 600; }
    .theme-btn {
      background: transparent; color: var(--muted); border: 1px solid var(--border);
      border-radius: 8px; padding: 4px 10px; font-size: 0.72rem; cursor: pointer;
    }
    .theme-btn:hover { color: var(--text); }
    p.sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 20px; }
    .grid {
      display: grid; gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }
    #log {
      margin-top: 18px; padding: 10px 14px;
      background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
      font-family: 'JetBrains Mono', 'Menlo', monospace; font-size: 0.78rem;
      color: var(--muted); min-height: 32px;
    }
  </style>
</head>
<body data-theme="dark">
  <main class="page">
    <div class="head">
      <h1>weather-card</h1>
      <button class="theme-btn" id="themeBtn" type="button">Toggle theme</button>
    </div>
    <p class="sub">Custom element with Shadow DOM, reactive properties, slots, CustomEvents</p>

    <div class="grid">
      <weather-card location="San Francisco" temp="14" conditions="cloudy" humidity="68" wind="12"></weather-card>
      <weather-card location="Tokyo" temp="22" conditions="sunny" humidity="54" wind="6"></weather-card>
      <weather-card location="Reykjavík" temp="-3" conditions="snow" humidity="82" wind="24">
        <span slot="badge">Storm warning</span>
      </weather-card>
    </div>

    <p id="log">Click refresh on any card &middot; event log will appear here</p>
  </main>

  <script type="importmap">
  {
    "imports": {
      "lit": "https://esm.sh/lit@3.2.1"
    }
  }
  </script>

  <script type="module">
    import { LitElement, html, css } from 'lit';

    const ICONS = {
      sunny:  '☀',
      cloudy: '☁',
      rain:   '☂',
      snow:   '❄',
      storm:  '⚡',
    };

    class WeatherCard extends LitElement {
      static properties = {
        location:   { type: String },
        temp:       { type: Number },
        conditions: { type: String },
        humidity:   { type: Number },
        wind:       { type: Number },
        theme:      { type: String, reflect: true },
        _spinning:  { state: true },
      };

      constructor() {
        super();
        this.location   = 'Unknown';
        this.temp       = 0;
        this.conditions = 'sunny';
        this.humidity   = 0;
        this.wind       = 0;
        this.theme      = 'dark';
        this._spinning  = false;
      }

      static styles = css`
        :host {
          display: block;
          background: var(--wc-card, #1a1d27);
          color: var(--wc-text, #e2e8f0);
          border: 1px solid var(--wc-border, rgba(255,255,255,0.08));
          border-radius: 14px;
          padding: 18px 20px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.3);
          transition: background 200ms, color 200ms, border-color 200ms;
          font-family: -apple-system, 'Segoe UI', sans-serif;
        }
        :host([theme="light"]) {
          --wc-card: #ffffff;
          --wc-text: #1e293b;
          --wc-border: rgba(0,0,0,0.08);
          --wc-muted: #475569;
          --wc-bg: #f8fafc;
          background: var(--wc-card); color: var(--wc-text);
          border-color: var(--wc-border);
          box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        :host([theme="dark"]),
        :host(:not([theme])) {
          --wc-card: #1a1d27;
          --wc-text: #e2e8f0;
          --wc-border: rgba(255,255,255,0.08);
          --wc-muted: #94a3b8;
          --wc-bg: #0f1117;
        }

        .head { display: flex; justify-content: space-between; align-items: flex-start; }
        .loc  { font-size: 0.85rem; color: var(--wc-muted); font-weight: 500; letter-spacing: 0.02em; }
        .ico  { font-size: 1.6rem; line-height: 1; }
        .badge {
          display: inline-block;
          background: rgba(244,63,94,0.15); color: #f87171;
          border: 1px solid rgba(244,63,94,0.3);
          border-radius: 999px; padding: 2px 8px;
          font-size: 0.68rem; margin-top: 6px;
        }
        :host([theme="light"]) .badge { color: #be123c; background: rgba(244,63,94,0.1); }

        .temp {
          font-size: 2.6rem; font-weight: 700; margin: 8px 0 0;
          font-variant-numeric: tabular-nums;
        }
        .temp small { font-size: 0.9rem; color: var(--wc-muted); margin-left: 4px; font-weight: 500; }
        .cond { font-size: 0.85rem; color: var(--wc-muted); text-transform: capitalize; }

        .stats {
          display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
          margin-top: 14px; padding-top: 14px;
          border-top: 1px solid var(--wc-border);
        }
        .stat { display: flex; flex-direction: column; gap: 2px; }
        .stat-label { font-size: 0.68rem; color: var(--wc-muted); text-transform: uppercase; letter-spacing: 0.05em; }
        .stat-value { font-size: 0.95rem; font-weight: 600; font-variant-numeric: tabular-nums; }

        .actions { display: flex; justify-content: flex-end; margin-top: 12px; }
        button.refresh {
          background: transparent;
          color: var(--wc-muted);
          border: 1px solid var(--wc-border);
          border-radius: 8px; padding: 6px 12px;
          font-size: 0.78rem; font-family: inherit;
          cursor: pointer; transition: all 150ms;
          display: inline-flex; align-items: center; gap: 6px;
        }
        button.refresh:hover {
          color: var(--wc-text);
          border-color: rgba(99,102,241,0.5);
          background: rgba(99,102,241,0.08);
        }
        button.refresh:focus-visible {
          outline: 2px solid #6366f1; outline-offset: 2px;
        }
        .spin { display: inline-block; transition: transform 600ms cubic-bezier(0.16,1,0.3,1); }
        .spin.is-spinning { transform: rotate(360deg); }

        ::slotted([slot="badge"]) {
          display: inline-block;
          background: rgba(244,63,94,0.15); color: #f87171;
          border: 1px solid rgba(244,63,94,0.3);
          border-radius: 999px; padding: 2px 8px;
          font-size: 0.68rem; margin-top: 6px;
        }
      `;

      render() {
        const icon = ICONS[this.conditions] ?? '·';
        return html`
          <div class="head">
            <div>
              <div class="loc" aria-label="Location">${this.location}</div>
              <slot name="badge"></slot>
            </div>
            <div class="ico" aria-hidden="true">${icon}</div>
          </div>
          <p class="temp" aria-label="Temperature">
            ${Math.round(this.temp)}<small>°C</small>
          </p>
          <p class="cond">${this.conditions}</p>

          <div class="stats">
            <div class="stat">
              <span class="stat-label">Humidity</span>
              <span class="stat-value">${this.humidity}%</span>
            </div>
            <div class="stat">
              <span class="stat-label">Wind</span>
              <span class="stat-value">${this.wind} km/h</span>
            </div>
          </div>

          <div class="actions">
            <button
              class="refresh"
              type="button"
              aria-label="Refresh weather for ${this.location}"
              @click=${this._refresh}>
              <span class="spin ${this._spinning ? 'is-spinning' : ''}" aria-hidden="true">↻</span>
              Refresh
            </button>
          </div>
        `;
      }

      _refresh() {
        if (this._spinning) return;
        this._spinning = true;
        // Simulate a fetch + variation
        setTimeout(() => {
          this.temp     = Math.round(this.temp + (Math.random() * 6 - 3));
          this.humidity = Math.max(0, Math.min(100, Math.round(this.humidity + (Math.random() * 10 - 5))));
          this.wind     = Math.max(0, Math.round(this.wind + (Math.random() * 6 - 3)));
          this._spinning = false;

          this.dispatchEvent(new CustomEvent('refresh', {
            detail: { location: this.location, temp: this.temp },
            bubbles: true, composed: true,
          }));
        }, 600);
      }
    }

    customElements.define('weather-card', WeatherCard);

    // ── Page-level theme toggle: flips body data-theme and the
    //    `theme` property on every <weather-card> instance.
    const log = document.getElementById('log');
    document.getElementById('themeBtn').addEventListener('click', () => {
      const next = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
      document.body.dataset.theme = next;
      document.querySelectorAll('weather-card').forEach((el) => (el.theme = next));
    });

    // ── Listen to CustomEvents bubbled from inside the shadow roots.
    document.addEventListener('refresh', (e) => {
      log.textContent = `↻ Refreshed ${e.detail.location} → ${e.detail.temp}°C  (at ${new Date().toLocaleTimeString()})`;
    });

    // ── Set initial theme on the cards so they match the page default.
    document.querySelectorAll('weather-card').forEach((el) => (el.theme = 'dark'));
  </script>
</body>
</html>
```

What this demonstrates:

- A custom element used like normal HTML (`<weather-card location="…" temp="…">`)
- Reactive properties for all data plus an internal `_spinning` state
- `:host([theme="light"])` and `:host([theme="dark"])` selectors for per-instance theming
- A named slot (`slot="badge"`) for host-provided content, styled via `::slotted`
- A bubbling, composed `CustomEvent` that escapes the Shadow DOM
- Focus-visible outline for keyboard accessibility
- A spin animation triggered by an internal state change
- A page-level theme toggle that updates every instance via the `theme` property

---

## Common Mistakes to Avoid

- **Using decorators without a build step** — `@customElement` and `@property` rely on the decorator proposal, which most browsers don't natively run. Use the class-syntax form (`static properties = { … }`) in artifacts.
- **Forgetting `composed: true` on CustomEvents** — without it, the event stops at the Shadow DOM boundary and the host page never sees it.
- **camelCase event names** — DOM convention is kebab-case (`rating-change`, not `ratingChange`). Mismatches break `@rating-change=${…}` bindings in templates.
- **Setting an array/object property and expecting an update** — Lit only triggers re-render when the property *reference* changes. Mutating an array in place doesn't work; use `this.items = [...this.items, newOne]` (or call `this.requestUpdate()`).
- **Trying to style slotted content with deep selectors** — `::slotted()` only matches direct children. Nested styling must happen in the host's own styles.
- **Importmap declared after `<script type="module">`** — silently ignored; bare imports fail. Importmap must come first.
- **Boolean attributes set as strings** — `<my-el disabled="false">` is **truthy**. Use `?disabled=${expr}` in templates, and treat any presence as true on the attribute side.
- **Calling `render()` directly** — never. Set a property or call `this.requestUpdate()` and let Lit schedule the render.
- **Mutating `this` inside `render()`** — `render()` must be pure. Side effects belong in `updated()` / `firstUpdated()`.
- **Leaving `display: inline` on the host** — by default custom elements are `display: inline`; for layout-bearing widgets always set `:host { display: block; }` (or `inline-block`, `grid`, etc.).
- **Forgetting to call `super.connectedCallback()`** — if you override lifecycle hooks, you must call the super; otherwise property initialisation and rendering break silently.
- **One CSS rule leaking out** — if styles leak, you almost certainly used a global `<style>` instead of `static styles = css\`…\``. Shadow DOM only encapsulates what's inside the shadow root.
