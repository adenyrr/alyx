---
name: htmx
description: Build server-driven interactive HTML using HTMX 2, delivered as self-contained HTML artifacts. Use this skill when the user wants hypermedia-style interactivity controlled from HTML attributes (`hx-get`, `hx-post`, `hx-trigger`, `hx-target`, `hx-swap`), progressive enhancement patterns, AJAX-without-JS, TODO apps, infinite scroll, live search, inline edit, optimistic UI, or any pattern that swaps fragments of HTML into the DOM in response to user actions. Trigger on phrases like "build a TODO app", "live search", "inline editing", "swap content with HTMX", "server-driven interactivity", "hypermedia app", "no-build interactivity", or any request describing partial page updates from attributes rather than React state. Do NOT use for: component-state heavy React UIs (→ shadcn skill), rich text editing (→ tiptap skill), reusable encapsulated web components (→ lit skill), chart rendering (→ chartjs skill), or animation-first work (→ animejs / gsap skills).
agents: [dev]
---

# HTMX Skill — v2

HTMX is a tiny (~14 KB gzipped) library that extends HTML with attributes for AJAX, CSS transitions, WebSockets, and Server-Sent Events — without writing JavaScript. The mental model is **hypermedia as the engine of application state**: the server (or a simulated one) returns HTML fragments, and HTMX swaps them into the DOM. In artifacts where there is no real server, we simulate responses with `htmx.defineExtension`, inline JSON, or an in-page fake API using the `htmx:beforeRequest` / `htmx:configRequest` hooks.

---

## Artifact Presentation & Use Cases

Every HTMX artifact is a self-contained HTML page with a dark theme. The visual structure follows the same shell pattern as every Alyx artifact:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) hosts the interactive region
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes what the widget does
- **Hint subtitle** (`p.sub`, 0.82rem, `#94a3b8`) describes the interaction model
- **HTMX-powered region** with `hx-*` attributes wires up declarative behaviour

### Typical use cases

- **TODO / task lists** — add, complete, delete with optimistic UI and no full page reload
- **Inline editing** — click a cell, swap it for an input, save back into the cell
- **Live search / autocomplete** — `hx-trigger="keyup changed delay:300ms"` against a faux endpoint
- **Infinite scroll / load more** — `hx-trigger="revealed"` to fetch the next page when an element enters view
- **Server-sent updates** — `hx-ext="sse"` streams events into a target element
- **Multi-target swaps** — out-of-band (`hx-swap-oob`) updates a counter elsewhere on the page while the main target changes
- **Form-driven flows** — wizards, login, comment boxes, polling status updates

### What the user sees

A page that behaves like a single-page app but is built entirely from declarative attributes. Clicks, key presses, scrolls and intersections trigger fragment swaps; the result feels instant, animates smoothly via CSS transitions, and is fully keyboard-accessible by default because everything is real HTML.

---

## When to Use HTMX vs. Alternatives

| Use HTMX when… | Use another approach when… |
|---|---|
| You want declarative interactivity from HTML attributes | You need full React component trees → **shadcn / React artifacts** |
| The widget is a single self-contained interaction | You need rich text editing → **tiptap** |
| Progressive enhancement / no-build is the goal | You need a reusable, encapsulated web component → **lit** |
| The data flow is fetch-fragment-and-swap | Heavy client-side state machines → **React + useReducer** |
| Forms, lists, inline edit, search, polling | Charts / data visualisation → **chartjs / plotly / d3** |
| You want minimal JS surface area | Animation-first scroll storytelling → **gsap** |

> **Rule of thumb:** if the natural description is "when the user does X, replace Y with HTML returned from Z", HTMX is the right tool. In an artifact context, "Z" is simulated via `htmx.defineExtension` or an inline JSON fixture.

---

## Step 1 — CDN Setup

```html
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
```

### Optional extensions (load after the core script)

```html
<!-- JSON encoding for request bodies -->
<script src="https://unpkg.com/htmx-ext-json-enc@2.0.1/json-enc.js"></script>

<!-- Response targets — route different status codes to different targets -->
<script src="https://unpkg.com/htmx-ext-response-targets@2.0.2/response-targets.js"></script>

<!-- Server-Sent Events -->
<script src="https://unpkg.com/htmx-ext-sse@2.2.2/sse.js"></script>

<!-- _hyperscript — small DSL that pairs naturally with HTMX -->
<script src="https://unpkg.com/hyperscript.org@0.9.13"></script>
```

> **Critical for artifacts:** there is no backend. Always either (a) install an `htmx.defineExtension` request mock, (b) intercept `htmx:beforeRequest` to call `event.preventDefault()` and synthesise a fake response via `htmx.ajax`, or (c) use `_hyperscript` / vanilla JS to manipulate the DOM directly. The "Complete Example" below demonstrates option (a).

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HTMX Artifact</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 24px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
      width: 100%; max-width: 640px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: var(--text); margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 24px; }
  </style>
</head>
<body data-theme="dark">
  <div class="card">
    <h1>Widget Title</h1>
    <p class="sub">Press · type · click to interact</p>
    <div id="app"><!-- HTMX region --></div>
  </div>

  <script src="https://unpkg.com/htmx.org@2.0.4"></script>
  <script>
    // theme tokens + fake API + extensions
  </script>
</body>
</html>
```

---

## Step 3 — Themes (dark default + light)

HTMX itself is themeless — you control all CSS. Define both palettes via CSS variables and switch with a `data-theme` attribute on `<body>`:

```css
/* Dark (default) */
:root,
[data-theme="dark"] {
  --bg:     #0f1117;
  --card:   #1a1d27;
  --border: rgba(255,255,255,0.08);
  --text:   #e2e8f0;
  --muted:  #94a3b8;
  --accent: #6366f1;
}

/* Light */
[data-theme="light"] {
  --bg:     #f8fafc;
  --card:   #ffffff;
  --border: rgba(0,0,0,0.08);
  --text:   #1e293b;
  --muted:  #475569;
  --accent: #6366f1;
}
```

### Switching themes at runtime

```html
<button
  type="button"
  hx-on:click="document.body.dataset.theme =
    document.body.dataset.theme === 'dark' ? 'light' : 'dark'">
  Toggle theme
</button>
```

`hx-on:click` is HTMX's built-in event handler attribute — it accepts any JS expression and runs in the element's scope.

---

## Step 4 — The Attribute System (core)

Every HTMX interaction is one or more attributes on an existing HTML element. The most important six:

| Attribute | Purpose | Example |
|---|---|---|
| `hx-get` | Issue GET, replace target with response | `hx-get="/api/items"` |
| `hx-post` | Issue POST with form / element values | `hx-post="/api/items"` |
| `hx-put` / `hx-patch` / `hx-delete` | Other HTTP verbs | `hx-delete="/api/items/3"` |
| `hx-trigger` | Override default trigger (click for buttons, submit for forms) | `hx-trigger="keyup changed delay:300ms"` |
| `hx-target` | CSS selector for the swap destination | `hx-target="#results"` |
| `hx-swap` | How the response replaces the target | `hx-swap="outerHTML transition:true"` |

### Other commonly used attributes

```html
hx-vals='{"page": 2}'      <!-- Extra request params (JSON) -->
hx-include="[name='q']"    <!-- Include other form fields in the request -->
hx-headers='{"X-CSRF":"…"}'<!-- Custom headers -->
hx-confirm="Delete?"       <!-- Native confirm() prompt before request -->
hx-disable                 <!-- Disable HTMX on this subtree -->
hx-disabled-elt="this"     <!-- Disable element while request in-flight -->
hx-indicator="#spinner"    <!-- Show indicator during request -->
hx-push-url="true"         <!-- Push the response URL into browser history -->
hx-select="#fragment"      <!-- Pick a fragment out of an HTML response -->
hx-boost="true"            <!-- Upgrade anchors/forms to AJAX -->
```

---

## Step 5 — Swap Strategies

`hx-swap` controls how the returned HTML replaces (or augments) the target:

| Value | Effect |
|---|---|
| `innerHTML` (default) | Replace contents of target |
| `outerHTML` | Replace the target element itself |
| `beforebegin` | Insert before target |
| `afterbegin` | Insert as first child |
| `beforeend` | Insert as last child (great for chat / infinite scroll) |
| `afterend` | Insert after target |
| `delete` | Remove target |
| `none` | Do not swap; useful with out-of-band swaps |

### Swap modifiers

```html
hx-swap="innerHTML transition:true swap:200ms settle:300ms scroll:bottom focus-scroll:true"
```

- `transition:true` — use the View Transitions API for animated swaps
- `swap:200ms` / `settle:300ms` — animation timings for the swap and settle phases
- `scroll:top` / `scroll:bottom` — scroll the swapped element after settling
- `show:top` — scroll the swapped element into view
- `focus-scroll:true` — focus + scroll for screen readers

### View Transitions CSS

```css
@keyframes fadeIn  { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeOut { from { opacity: 1; } to { opacity: 0; transform: translateY(-4px); } }
::view-transition-old(root) { animation: fadeOut 180ms cubic-bezier(0.16,1,0.3,1); }
::view-transition-new(root) { animation: fadeIn  220ms cubic-bezier(0.16,1,0.3,1); }
```

---

## Step 6 — Triggers

`hx-trigger` accepts a comma-separated list of trigger specs. Each spec is `event[modifier...][filter]`.

### Common triggers

```html
hx-trigger="click"                          <!-- default for non-form elements -->
hx-trigger="submit"                         <!-- default for forms -->
hx-trigger="change"                         <!-- inputs / selects -->
hx-trigger="keyup changed delay:300ms"      <!-- live search -->
hx-trigger="load"                           <!-- fire as soon as element exists -->
hx-trigger="revealed"                       <!-- fire when scrolled into view (infinite scroll) -->
hx-trigger="intersect once threshold:0.5"   <!-- IntersectionObserver, fire once -->
hx-trigger="every 2s"                       <!-- poll every 2 seconds -->
hx-trigger="mouseenter delay:200ms"
hx-trigger="keyup[key=='Enter']"            <!-- filter by event property -->
```

### Modifiers

| Modifier | Meaning |
|---|---|
| `once` | Fire one time only |
| `changed` | Only fire if the element's value changed |
| `delay:Xms` | Debounce |
| `throttle:Xms` | Throttle |
| `from:CSS` | Listen on a different element |
| `target:CSS` | Filter by event target |
| `consume` | Stop propagation |
| `queue:first|last|all|none` | How to handle concurrent requests |

### Custom events

You can `htmx.trigger(element, 'myEvent', { detail })` and listen via `hx-trigger="myEvent from:body"`.

---

## Step 7 — Out-of-Band Swaps

A single response can update multiple disjoint regions. Mark elements with `hx-swap-oob="true"` in the response HTML — they will be applied wherever their `id` matches in the DOM, regardless of the request's primary target.

```html
<!-- Server response for POST /todos -->
<li id="todo-42">New item</li>
<span id="todo-count" hx-swap-oob="true">7 items</span>
```

The first `<li>` is appended at the original target; the `<span>` updates the counter elsewhere.

### OOB swap with non-default strategy

```html
<div id="flash" hx-swap-oob="beforeend">
  <div class="toast">Saved</div>
</div>
```

---

## Step 8 — Extensions

Load with `<script>` then enable per-subtree with `hx-ext="name"`.

### `json-enc` — POST JSON instead of form-encoded

```html
<form hx-post="/api/items" hx-ext="json-enc">
  <input name="title">
  <button>Add</button>
</form>
```

### `response-targets` — route by status code

```html
<form hx-post="/api/login"
      hx-ext="response-targets"
      hx-target="#ok"
      hx-target-4xx="#error"
      hx-target-5xx="#error">
  …
</form>
```

### `sse` — Server-Sent Events stream

```html
<div hx-ext="sse" sse-connect="/stream" sse-swap="message"></div>
```

In an artifact, simulate SSE by repeatedly calling `htmx.swap('#target', html, { swapStyle: 'beforeend' })` on an interval.

### Defining your own extension (the artifact pattern)

```javascript
htmx.defineExtension('mock-api', {
  onEvent(name, evt) {
    if (name !== 'htmx:beforeRequest') return true;
    evt.preventDefault();
    const xhr = evt.detail.xhr;
    const path = evt.detail.requestConfig.path;
    const verb = evt.detail.requestConfig.verb;
    const body = handle(verb, path, evt.detail.requestConfig.parameters);
    // Mimic server response via the XHR object HTMX is waiting on
    Object.defineProperty(xhr, 'status',       { value: 200 });
    Object.defineProperty(xhr, 'responseText', { value: body });
    Object.defineProperty(xhr, 'response',     { value: body });
    htmx.trigger(evt.target, 'htmx:afterRequest', { xhr, successful: true });
    htmx.trigger(evt.target, 'htmx:beforeSwap',   { xhr, target: evt.detail.target, serverResponse: body, shouldSwap: true });
    htmx.swap(evt.detail.target, body, evt.detail.swapSpec);
    return false;
  }
});
```

In practice, the simplest artifact pattern is to intercept `htmx:beforeRequest`, prevent the real request, and manually call `htmx.swap` (see Complete Example).

---

## Step 9 — Pairing with _hyperscript

`_hyperscript` is a small declarative scripting language whose attribute is `_`. It pairs naturally with HTMX for tiny client-side behaviours:

```html
<button _="on click toggle .active on #menu">Menu</button>

<input _="on keyup if my.value.length > 3 send filter to #list">

<div _="on htmx:afterSwap add .flash then settle then remove .flash">…</div>
```

Use it for: toggling classes, focusing inputs after a swap, dispatching custom events between widgets, simple state toggles. For anything more elaborate, drop to vanilla JS via `hx-on:eventname="…"`.

---

## Step 10 — Accessibility Patterns

HTMX preserves real HTML, so accessibility comes mostly for free — but there are four patterns to apply deliberately:

### 1. Manage focus after swaps

```html
<input
  name="q"
  hx-get="/search"
  hx-trigger="keyup changed delay:300ms"
  hx-target="#results"
  hx-swap="innerHTML focus-scroll:true">
```

For inline edit, focus the new input after swap:

```html
<div hx-on:htmx:after-swap="this.querySelector('input')?.focus()">…</div>
```

### 2. Disable forms on submit (prevent double-submit)

```html
<form hx-post="/api/save" hx-disabled-elt="find button[type='submit']">
  <button type="submit">Save</button>
</form>
```

### 3. Live region for status announcements

```html
<div id="status" role="status" aria-live="polite" class="sr-only"></div>
```

Have the server response include `<div id="status" hx-swap-oob="true" role="status">Saved</div>` so screen readers announce results.

### 4. Indicator with proper ARIA

```html
<button hx-post="/api/save" hx-indicator="#spinner" aria-controls="spinner">Save</button>
<span id="spinner" class="htmx-indicator" role="status" aria-live="polite" aria-hidden="true">Saving…</span>
```

```css
.htmx-indicator { opacity: 0; transition: opacity 200ms; }
.htmx-request .htmx-indicator,
.htmx-request.htmx-indicator { opacity: 1; }
```

### 5. Keyboard support

Always use semantic elements: `<button>`, `<a href>`, `<input>`, `<form>`. Never wire `hx-get` onto a `<div>` — keyboard users will be stranded. If you must, add `role="button" tabindex="0"` and a `keydown[key=='Enter']` trigger.

---

## Step 11 — Useful Events

HTMX dispatches a rich set of CustomEvents on the originating element. Listen via `hx-on:*` attributes or `htmx.on(...)`.

| Event | When |
|---|---|
| `htmx:beforeRequest` | Before any request — `preventDefault()` to cancel |
| `htmx:configRequest` | Mutate headers / parameters before send |
| `htmx:beforeSwap` | After response, before DOM swap |
| `htmx:afterSwap` | DOM has been swapped, settle pending |
| `htmx:afterSettle` | Settle phase complete |
| `htmx:responseError` | Non-2xx response |
| `htmx:sendError` | Network error |
| `htmx:targetError` | Target selector did not match |

```javascript
htmx.on('htmx:afterSwap', (e) => {
  e.target.querySelector('input')?.focus();
});
```

---

## Step 12 — Complete Example: TODO App with Optimistic UI

A fully working artifact: the "server" is a JSON fixture in memory, intercepted via `htmx:beforeRequest`. The list supports add, toggle, delete, with out-of-band counter updates and an entrance transition.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HTMX Todo</title>
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
    .card {
      background: var(--card); border: 1px solid var(--border);
      border-radius: 16px; padding: 32px; width: 100%; max-width: 520px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    }
    .head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
    h1 { font-size: 1.15rem; font-weight: 600; }
    .theme-btn {
      background: transparent; color: var(--muted); border: 1px solid var(--border);
      border-radius: 8px; padding: 4px 10px; font-size: 0.72rem; cursor: pointer;
    }
    .theme-btn:hover { color: var(--text); }
    p.sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 20px; }
    form { display: flex; gap: 8px; margin-bottom: 16px; }
    input[type="text"] {
      flex: 1; background: var(--bg); color: var(--text); border: 1px solid var(--border);
      border-radius: 8px; padding: 10px 12px; font-size: 0.9rem; font-family: inherit;
    }
    input[type="text"]:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
    button.primary {
      background: var(--accent); color: #fff; border: none; border-radius: 8px;
      padding: 0 16px; font-size: 0.85rem; font-weight: 500; cursor: pointer;
      transition: filter 150ms, transform 80ms;
    }
    button.primary:hover { filter: brightness(1.1); }
    button.primary:active { transform: scale(0.97); }
    button.primary[disabled] { opacity: 0.5; cursor: not-allowed; }
    ul#list { list-style: none; display: flex; flex-direction: column; gap: 6px; min-height: 60px; }
    li {
      display: flex; align-items: center; gap: 10px;
      background: var(--bg); border: 1px solid var(--border);
      border-radius: 10px; padding: 10px 12px;
      animation: fadeUp 200ms cubic-bezier(0.16,1,0.3,1);
    }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
    li input[type="checkbox"] { accent-color: var(--accent); width: 16px; height: 16px; cursor: pointer; }
    li .label { flex: 1; font-size: 0.9rem; }
    li.done .label { text-decoration: line-through; color: var(--muted); }
    .delete {
      background: transparent; color: var(--muted); border: none;
      cursor: pointer; padding: 4px 6px; border-radius: 4px; font-size: 1rem;
    }
    .delete:hover { color: #f43f5e; background: rgba(244,63,94,0.08); }
    .footer {
      display: flex; justify-content: space-between; align-items: center;
      margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--border);
      font-size: 0.78rem; color: var(--muted);
    }
    .sr-only {
      position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
      overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0;
    }
    .htmx-indicator { opacity: 0; transition: opacity 150ms; }
    .htmx-request .htmx-indicator { opacity: 1; }
  </style>
</head>
<body data-theme="dark">
  <div class="card">
    <div class="head">
      <h1>Tasks</h1>
      <button class="theme-btn" type="button"
              hx-on:click="document.body.dataset.theme =
                document.body.dataset.theme === 'dark' ? 'light' : 'dark'">
        Toggle theme
      </button>
    </div>
    <p class="sub">Type and press Enter to add &middot; click checkbox to complete &middot; click &times; to delete</p>

    <form hx-post="/api/todos"
          hx-target="#list"
          hx-swap="beforeend"
          hx-disabled-elt="find button"
          hx-on:htmx:after-request="this.reset(); this.querySelector('input').focus()">
      <input type="text" name="title" placeholder="What needs doing?"
             autocomplete="off" required minlength="1" maxlength="80"
             aria-label="New task title">
      <button class="primary" type="submit">Add <span class="htmx-indicator">&middot;&middot;&middot;</span></button>
    </form>

    <ul id="list" role="list" aria-label="Tasks"></ul>

    <div class="footer">
      <span id="count" role="status" aria-live="polite">0 items</span>
      <span>HTMX 2 &middot; fake API in memory</span>
    </div>

    <div id="sr-status" class="sr-only" role="status" aria-live="polite"></div>
  </div>

  <script src="https://unpkg.com/htmx.org@2.0.4"></script>
  <script>
    // ── Fake API state ────────────────────────────────────────
    const db = {
      todos: [
        { id: 1, title: 'Read HTMX docs', done: true  },
        { id: 2, title: 'Build a todo app', done: false },
      ],
      nextId: 3,
    };

    const todoLi = (t) => `
      <li id="todo-${t.id}" class="${t.done ? 'done' : ''}">
        <input type="checkbox" ${t.done ? 'checked' : ''}
               hx-patch="/api/todos/${t.id}/toggle"
               hx-target="#todo-${t.id}"
               hx-swap="outerHTML"
               aria-label="Mark '${t.title}' as ${t.done ? 'not done' : 'done'}">
        <span class="label">${t.title}</span>
        <button class="delete" type="button"
                hx-delete="/api/todos/${t.id}"
                hx-target="#todo-${t.id}"
                hx-swap="outerHTML swap:200ms"
                hx-confirm="Delete this task?"
                aria-label="Delete '${t.title}'">&times;</button>
      </li>`;

    const countOob = () =>
      `<span id="count" hx-swap-oob="true" role="status" aria-live="polite">
        ${db.todos.length} item${db.todos.length === 1 ? '' : 's'}, ${db.todos.filter(t => t.done).length} done
      </span>`;

    const announce = (msg) =>
      `<div id="sr-status" hx-swap-oob="true" class="sr-only" role="status" aria-live="polite">${msg}</div>`;

    // ── Mock router ───────────────────────────────────────────
    function route(verb, path, params) {
      // POST /api/todos
      if (verb === 'POST' && path === '/api/todos') {
        const title = (params.title || '').trim();
        if (!title) return { status: 400, body: '' };
        const t = { id: db.nextId++, title, done: false };
        db.todos.push(t);
        return { status: 200, body: todoLi(t) + countOob() + announce(`Added ${title}`) };
      }
      // PATCH /api/todos/:id/toggle
      const tog = path.match(/^\/api\/todos\/(\d+)\/toggle$/);
      if (verb === 'PATCH' && tog) {
        const t = db.todos.find(x => x.id === +tog[1]);
        if (!t) return { status: 404, body: '' };
        t.done = !t.done;
        return { status: 200, body: todoLi(t) + countOob() };
      }
      // DELETE /api/todos/:id
      const del = path.match(/^\/api\/todos\/(\d+)$/);
      if (verb === 'DELETE' && del) {
        const idx = db.todos.findIndex(x => x.id === +del[1]);
        if (idx < 0) return { status: 404, body: '' };
        const [t] = db.todos.splice(idx, 1);
        return { status: 200, body: '' + countOob() + announce(`Deleted ${t.title}`) };
      }
      // GET /api/todos (initial load)
      if (verb === 'GET' && path === '/api/todos') {
        return { status: 200, body: db.todos.map(todoLi).join('') + countOob() };
      }
      return { status: 404, body: '' };
    }

    // ── Intercept HTMX requests ───────────────────────────────
    htmx.on('htmx:beforeRequest', (e) => {
      const cfg = e.detail.requestConfig;
      if (!cfg.path.startsWith('/api/')) return;
      e.preventDefault();
      const { status, body } = route(cfg.verb.toUpperCase(), cfg.path, cfg.parameters);
      const targetSel = e.detail.target?.id ? '#' + e.detail.target.id : null;
      if (status >= 200 && status < 300 && targetSel) {
        // Honour the original swap strategy ('beforeend' for add, 'outerHTML' for toggle/delete)
        const swap = e.detail.requestConfig.swapSpec?.swapStyle
                  || e.detail.etc?.swapOverride
                  || (e.detail.elt.getAttribute('hx-swap') || 'innerHTML').split(' ')[0];
        htmx.swap(targetSel, body, { swapStyle: swap, settleDelay: 20 });
      }
    });

    // ── Initial load ──────────────────────────────────────────
    htmx.ajax('GET', '/api/todos', { target: '#list', swap: 'innerHTML' });
  </script>
</body>
</html>
```

What this demonstrates:

- Declarative attribute-driven CRUD on a list
- Out-of-band swap to keep a counter in sync
- ARIA live region announcements for screen readers
- Form auto-reset and focus return after submit
- `hx-disabled-elt` to prevent double-submit
- `hx-confirm` for destructive actions
- Fake API via `htmx:beforeRequest` interception (no backend needed)
- Theme tokens for dark + light

---

## Common Mistakes to Avoid

- **Wiring `hx-get` on a `<div>`** — keyboard users cannot trigger it. Use `<button>`, `<a>`, `<form>`, `<input>`, or add `role="button" tabindex="0"` plus a keyboard trigger.
- **Forgetting `hx-target`** — HTMX defaults to replacing the triggering element. For forms and inputs you almost always want an explicit target.
- **Using `innerHTML` when you mean `outerHTML`** — toggling a list item by class needs `outerHTML` so the returned `<li>` replaces the old one (and keeps its `id` stable).
- **Missing fake API in artifacts** — without `htmx:beforeRequest` interception, every request returns 404 and the UI silently does nothing. Always wire a mock router in artifacts.
- **No `hx-disabled-elt` on submit** — users will double-click and submit twice. Always disable the button while in-flight.
- **Targeting an element that doesn't yet exist** — for `hx-target="#thing"` to work, `#thing` must already be in the DOM at request time. If it doesn't exist yet, render an empty placeholder.
- **OOB swap without matching `id`** — `hx-swap-oob="true"` requires the response element's `id` to match an existing element in the page; otherwise nothing happens.
- **Forgetting `hx-trigger` modifiers on text inputs** — `keyup` alone fires on every keystroke including arrows. Use `keyup changed delay:300ms` for live search.
- **Polling without throttle** — `hx-trigger="every 1s"` against a slow endpoint will stack requests; set `queue:none` or `queue:last`.
- **Mixing `_hyperscript` for state and HTMX for fetches** — pick one for each concern. Hyperscript = local DOM tweaks; HTMX = fetch + swap.
- **Manual `htmx.process()` missing** — when you inject HTML via vanilla JS into the DOM, call `htmx.process(el)` so HTMX scans new `hx-*` attributes. Responses from HTMX itself do not need this.
