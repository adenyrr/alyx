---
name: prism-code
description: Add syntax highlighting to code blocks in HTML artifacts using Prism.js. Use this skill whenever someone needs beautifully highlighted code snippets in a web page — documentation pages, tutorials, code cards, API reference pages, or any artifact displaying source code. Trigger on requests like "highlight this code", "show code with syntax coloring", "create a code snippet display", "make a documentation page with code examples", or any prompt that includes code that should be visually highlighted. Do NOT use for interactive code editors (→ CodeMirror, not in stack), presentation slides with code (→ reveal-slides skill which includes highlight.js), or data charts (→ chartjs/plotly skill).
agents: [dev]
---

# Prism.js Code Highlighting Skill

Prism.js is a lightweight, extensible syntax highlighter. It supports 300+ languages via plugins, offers multiple themes, and provides features like line numbers, line highlighting, copy button, diff highlighting, and inline color previews. It processes `<code>` blocks and applies token-based CSS coloring.

---

## Artifact Presentation & Use Cases

Every Prism artifact is a self-contained HTML page with a dark theme and syntax-highlighted code blocks. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius) contains the content
- **Title** (1.15rem, `#f1f5f9`) names the page/doc
- **Subtitle** (0.82rem, `#64748b`) adds context
- **Code blocks** — `<pre><code class="language-xxx">` with Prism-applied syntax colors
- **Optional line numbers** and **line highlighting** for educational emphasis

### Typical use cases

- **Documentation pages** — API docs with highlighted code examples
- **Tutorials** — step-by-step guides with code + explanations
- **Code cards** — shareable snippets with syntax highlighting
- **Cheat sheets** — language reference with highlighted samples
- **Comparison pages** — "before/after" or multi-language code blocks
- **Blog posts** — technical articles with inline code examples
- **README-style pages** — project docs with installation/usage code

### What the user sees

Code blocks with language-appropriate syntax coloring, optional line numbers, highlighted key lines, and a copy-to-clipboard button — professionally styled on a dark background.

---

## When to Use Prism.js vs. Alternatives

| Use Prism.js when… | Use another tool when… |
|---|---|
| Static code display with syntax highlighting | Code in slides → **Reveal.js** (has built-in highlight.js) |
| Line numbers and line highlighting | Interactive code editor → **CodeMirror** (not in stack) |
| Copy-to-clipboard button on code blocks | Terminal output → plain `<pre>` with monospace |
| Multiple languages on one page | Math equations → **MathJax** |
| Lightweight (core is ~2KB) | Data visualization → **Chart.js / D3** |
| Plugin ecosystem (diff, autolinker, etc.) | Markdown rendering → **marked.js** (not in stack) |

> **Rule of thumb:** if the artifact contains code blocks that need syntax highlighting, use Prism.js. If the code is inside a slide deck, Reveal.js handles it natively.

---

## Step 1 — CDN Setup

```html
<!-- Dark theme (default) -->
<link id="prism-theme" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css">

<!-- Light theme (loaded but disabled — toggled via JS) -->
<link id="prism-theme-light" rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css"
      disabled>

<!-- Line numbers plugin (optional) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-numbers/prism-line-numbers.min.css">

<!-- Line highlight plugin (optional) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-highlight/prism-line-highlight.min.css">

<!-- Prism.js Core -->
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>

<!-- Autoloader: pulls in language components on demand (preferred over hand-listing every language) -->
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/autoloader/prism-autoloader.min.js"
        data-autoloader-path="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/"></script>

<!-- Plugins -->
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-highlight/prism-line-highlight.min.js"></script>
```

> Core includes: HTML, CSS, JavaScript, C-like. The **autoloader** fetches `prism-<lang>.min.js` from the CDN as it encounters new `language-*` classes — much cleaner than maintaining a long list of `<script>` tags. Use a hand-list only when you need offline-safe loading.

### Theme pairs (one dark + one light, toggle via `disabled`)
| Dark              | Light       |
|-------------------|-------------|
| `prism-tomorrow`  | `prism`     |
| `prism-okaidia`   | `prism-coy` |
| `prism-twilight`  | `prism-solarizedlight` |

### Theme-switch helper (called on load and on `prefers-color-scheme` change):
```javascript
function applyPrismTheme() {
  const isLight = document.documentElement.dataset.theme === 'light' ||
    (!document.documentElement.dataset.theme &&
     matchMedia('(prefers-color-scheme: light)').matches);
  document.getElementById('prism-theme').disabled       =  isLight;
  document.getElementById('prism-theme-light').disabled = !isLight;
}
applyPrismTheme();
matchMedia('(prefers-color-scheme: light)').addEventListener('change', applyPrismTheme);
```

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Code Reference</title>
  <link id="prism-theme"       rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css">
  <link id="prism-theme-light" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css" disabled>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-numbers/prism-line-numbers.min.css">
  <style>
    :root {
      --bg:        #0f1117;
      --card:      #1a1d27;
      --border:    rgba(255,255,255,0.08);
      --code-bg:   #0f1117;
      --code-bdr:  rgba(255,255,255,0.06);
      --text:      #e2e8f0;
      --title:     #f1f5f9;
      --body:      #cbd5e1;
      --muted:     #64748b;
      --line-bdr:  rgba(255,255,255,0.08);
      --line-num:  #4a4d5a;
      --inline-bg: rgba(255,255,255,0.06);
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg: #f8fafc; --card: #ffffff;
        --border: rgba(0,0,0,0.08);
        --code-bg: #f1f5f9; --code-bdr: rgba(0,0,0,0.08);
        --text: #1e293b; --title: #0f172a; --body: #334155; --muted: #475569;
        --line-bdr: rgba(0,0,0,0.08); --line-num: #94a3b8;
        --inline-bg: rgba(0,0,0,0.06);
      }
    }
    [data-theme="light"] {
      --bg: #f8fafc; --card: #ffffff;
      --border: rgba(0,0,0,0.08);
      --code-bg: #f1f5f9; --code-bdr: rgba(0,0,0,0.08);
      --text: #1e293b; --title: #0f172a; --body: #334155; --muted: #475569;
      --line-bdr: rgba(0,0,0,0.08); --line-num: #94a3b8;
      --inline-bg: rgba(0,0,0,0.06);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg); color: var(--text);
      display: flex; flex-direction: column; align-items: center;
      min-height: 100vh; padding: 24px;
    }
    .card {
      width: 100%; max-width: 800px;
      background: var(--card); border: 1px solid var(--border);
      border-radius: 16px; padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.15);
      margin-bottom: 20px;
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: var(--title); margin-bottom: 4px; }
    h2 { font-size: 1rem;    font-weight: 600; color: var(--title); margin: 20px 0 8px; }
    p.sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 20px; }
    p { font-size: 0.88rem; line-height: 1.7; color: var(--body); margin-bottom: 12px; }

    /* Override Prism background to match card */
    pre[class*="language-"] {
      background: var(--code-bg) !important;
      border-radius: 10px;
      border: 1px solid var(--code-bdr);
      margin: 12px 0; padding: 16px 20px;
      font-size: 13px; line-height: 1.6;
    }
    code[class*="language-"] {
      font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
      font-size: 13px;
    }
    /* Inline code */
    :not(pre) > code {
      background: var(--inline-bg);
      padding: 2px 6px; border-radius: 4px;
      font-size: 0.85em; color: var(--text);
    }
    /* Line numbers */
    .line-numbers .line-numbers-rows { border-right-color: var(--line-bdr); }
    .line-numbers .line-numbers-rows > span::before { color: var(--line-num); }
    /* Preserve focus-visible outlines on the copy button */
    :focus-visible { outline: 2px solid #6366f1; outline-offset: 2px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Title</h1>
    <p class="sub">Description</p>
    <pre class="line-numbers"><code class="language-javascript">
// code here
    </code></pre>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/autoloader/prism-autoloader.min.js"
          data-autoloader-path="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>
  <script>
    function applyPrismTheme() {
      const isLight = document.documentElement.dataset.theme === 'light' ||
        (!document.documentElement.dataset.theme &&
         matchMedia('(prefers-color-scheme: light)').matches);
      document.getElementById('prism-theme').disabled       =  isLight;
      document.getElementById('prism-theme-light').disabled = !isLight;
    }
    applyPrismTheme();
    matchMedia('(prefers-color-scheme: light)').addEventListener('change', applyPrismTheme);
  </script>
</body>
</html>
```

---

## Step 3 — Basic Usage

```html
<!-- JavaScript -->
<pre><code class="language-javascript">
function greet(name) {
  return `Hello, ${name}!`;
}
</code></pre>

<!-- Python -->
<pre><code class="language-python">
def greet(name: str) -> str:
    return f"Hello, {name}!"
</code></pre>

<!-- HTML -->
<pre><code class="language-html">
&lt;div class="container"&gt;
  &lt;h1&gt;Title&lt;/h1&gt;
&lt;/div&gt;
</code></pre>

<!-- CSS -->
<pre><code class="language-css">
.card {
  background: #1a1d27;
  border-radius: 16px;
  padding: 28px;
}
</code></pre>

<!-- Bash -->
<pre><code class="language-bash">
#!/bin/bash
echo "Hello World"
docker compose up -d
</code></pre>
```

> HTML inside Prism code blocks must use HTML entities: `&lt;` for `<`, `&gt;` for `>`, `&amp;` for `&`.

---

## Step 4 — Line Numbers

```html
<!-- Add class "line-numbers" to <pre> -->
<pre class="line-numbers"><code class="language-python">
import pandas as pd

df = pd.read_csv('data.csv')
df.head()
</code></pre>
```

Required CSS + JS:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-numbers/prism-line-numbers.min.css">
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>
```

---

## Step 5 — Line Highlighting

```html
<!-- Highlight specific lines with data-line -->
<pre data-line="2,4-6"><code class="language-javascript">
const x = 1;
const y = 2;  // highlighted
const z = 3;
function add() {  // highlighted
  return x + y;   // highlighted
}                  // highlighted
</code></pre>
```

Required CSS + JS:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-highlight/prism-line-highlight.min.css">
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-highlight/prism-line-highlight.min.js"></script>
```

> Customize highlight color: `.line-highlight { background: rgba(99,102,241,0.12) !important; }`

---

## Step 6 — Copy Button

```html
<!-- Toolbar + Copy button plugins -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/toolbar/prism-toolbar.min.css">
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/toolbar/prism-toolbar.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js"></script>
```

> No HTML changes needed—the copy button auto-appears on every `<pre><code>` block.

Style for dark theme:
```css
.code-toolbar .toolbar-item button {
  background: rgba(255,255,255,0.06) !important;
  color: #94a3b8 !important;
  border-radius: 6px !important;
  font-size: 11px !important;
  padding: 3px 8px !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
}
.code-toolbar .toolbar-item button:hover {
  background: rgba(255,255,255,0.1) !important;
  color: #f1f5f9 !important;
}
```

---

## Step 7 — Diff Highlighting

```html
<pre><code class="language-diff">
- const old = 'before';
+ const updated = 'after';
  const unchanged = 'same';
</code></pre>
```

Or use the Diff Highlight plugin for colored +/- lines within any language:
```html
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/diff-highlight/prism-diff-highlight.min.js"></script>

<pre><code class="language-diff-javascript diff-highlight">
- function old() { return 1; }
+ function updated() { return 2; }
</code></pre>
```

---

## Step 8 — Dynamic Highlighting

```javascript
// Highlight all code blocks (already done on page load)
Prism.highlightAll();

// Highlight a specific element
const codeEl = document.querySelector('#dynamic-code code');
codeEl.textContent = 'const x = 42;';
Prism.highlightElement(codeEl);

// Highlight a string programmatically
const html = Prism.highlight('const x = 42;', Prism.languages.javascript, 'javascript');
document.getElementById('output').innerHTML = `<pre><code>${html}</code></pre>`;
```

---

## Step 9 — Language Reference (Common)

```
language-javascript   language-typescript   language-python
language-html         language-css          language-scss
language-json         language-yaml         language-toml
language-bash         language-shell        language-powershell
language-sql          language-graphql      language-markdown
language-go           language-rust         language-java
language-c            language-cpp          language-csharp
language-php          language-ruby         language-swift
language-kotlin       language-dart         language-r
language-docker       language-nginx        language-regex
language-diff
```

> The component file name matches: `prism-{lang}.min.js`

---

## Step 10 — Design & Polish Guidelines

- **Tomorrow Night theme** — use `prism-tomorrow.min.css` for the best dark theme; override `pre` background to `#0f1117` for seamless integration
- **Code font** — prefer `JetBrains Mono`, `Fira Code`, or `Consolas`; set `font-size: 13px` for readability
- **Border treatment** — add a subtle `border: 1px solid rgba(255,255,255,0.06)` and `border-radius: 10px` to `pre` blocks
- **Inline code** — style `<code>` outside `<pre>` with a slight background (`rgba(255,255,255,0.06)`) and `border-radius: 4px`
- **Line numbers color** — override line number spans to `#4a4d5a` for subtle visibility
- **Line highlight** — use `rgba(99,102,241,0.12)` as the highlight background color matching the accent palette
- **Copy button** — always include the copy-to-clipboard plugin for user convenience; style the button dark
- **HTML entities** — remember to escape `<` and `>` as `&lt;` and `&gt;` inside code blocks; forgetting this breaks the HTML
- **Language label** — the toolbar plugin can show the language name; the `data-label` attribute on `<pre>` adds a custom label
- **Max height** — for long code blocks, add `max-height: 500px; overflow-y: auto;` to `pre` to prevent page scroll domination

---

## Step 11 — Complete Example: API Reference Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>API Reference</title>
  <!-- Theme-aware: load BOTH Prism themes; the inactive one carries the `disabled` attribute -->
  <link id="prism-theme"       rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css">
  <link id="prism-theme-light" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css" disabled>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-numbers/prism-line-numbers.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/toolbar/prism-toolbar.min.css">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 24px; gap: 16px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 24px; width: 100%; max-width: 800px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.4rem; font-weight: 700; color: #f1f5f9; text-align: center; margin-bottom: 4px; }
    h2 { font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 8px; }
    h3 { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin: 16px 0 6px; }
    p.sub { font-size: 0.82rem; color: #64748b; text-align: center; margin-bottom: 16px; }
    p { font-size: 0.85rem; line-height: 1.7; color: #cbd5e1; margin-bottom: 10px; }
    .method { display: inline-block; background: rgba(99,102,241,0.15); color: #818cf8; border-radius: 4px; padding: 2px 8px; font-size: 0.75rem; font-weight: 600; margin-bottom: 4px; }
    .endpoint { font-family: 'Consolas', monospace; color: #f1f5f9; font-size: 0.95rem; }
    pre[class*="language-"] { background: #0f1117 !important; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06); margin: 10px 0; padding: 14px 18px; font-size: 13px; line-height: 1.6; }
    code[class*="language-"] { font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace; font-size: 13px; }
    :not(pre) > code { background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px; font-size: 0.82em; color: #e2e8f0; }
    .line-numbers .line-numbers-rows { border-right-color: rgba(255,255,255,0.08) !important; }
    .line-numbers .line-numbers-rows > span::before { color: #4a4d5a !important; }
    .code-toolbar .toolbar-item button { background: rgba(255,255,255,0.06) !important; color: #94a3b8 !important; border-radius: 6px !important; font-size: 11px !important; padding: 3px 8px !important; border: 1px solid rgba(255,255,255,0.1) !important; }
    .code-toolbar .toolbar-item button:hover { background: rgba(255,255,255,0.1) !important; color: #f1f5f9 !important; }
    hr { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 16px 0; }
  </style>
</head>
<body>
  <h1>Users API Reference</h1>
  <p class="sub">REST endpoints for user management</p>

  <!-- GET users -->
  <div class="card">
    <span class="method">GET</span>
    <span class="endpoint">/api/users</span>
    <p>Retrieve a paginated list of users. Supports <code>?page</code> and <code>?limit</code> query params.</p>

    <h3>Request</h3>
    <pre class="line-numbers"><code class="language-bash">curl -X GET https://api.example.com/api/users?page=1&amp;limit=10 \
  -H "Authorization: Bearer $TOKEN"</code></pre>

    <h3>Response <code>200 OK</code></h3>
    <pre class="line-numbers"><code class="language-json">{
  "data": [
    { "id": 1, "name": "Alice", "email": "alice@example.com" },
    { "id": 2, "name": "Bob", "email": "bob@example.com" }
  ],
  "meta": { "page": 1, "limit": 10, "total": 42 }
}</code></pre>
  </div>

  <!-- POST user -->
  <div class="card">
    <span class="method" style="background:rgba(34,197,94,0.15); color:#22c55e;">POST</span>
    <span class="endpoint">/api/users</span>
    <p>Create a new user. Requires <code>name</code> and <code>email</code> in the request body.</p>

    <h3>Request</h3>
    <pre class="line-numbers"><code class="language-javascript">const response = await fetch('https://api.example.com/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  },
  body: JSON.stringify({
    name: 'Charlie',
    email: 'charlie@example.com',
  }),
});
const user = await response.json();</code></pre>

    <h3>Response <code>201 Created</code></h3>
    <pre class="line-numbers"><code class="language-json">{
  "id": 3,
  "name": "Charlie",
  "email": "charlie@example.com",
  "created_at": "2025-01-15T10:30:00Z"
}</code></pre>
  </div>

  <!-- Python SDK -->
  <div class="card">
    <h2>Python SDK</h2>
    <p>Install the SDK and make API calls with the client library:</p>
    <pre><code class="language-bash">pip install example-sdk</code></pre>
    <pre class="line-numbers"><code class="language-python">from example_sdk import Client

client = Client(api_key="your-api-key")

# List users
users = client.users.list(page=1, limit=10)
for user in users.data:
    print(f"{user.name} ({user.email})")

# Create user
new_user = client.users.create(
    name="Charlie",
    email="charlie@example.com",
)
print(f"Created: {new_user.id}")</code></pre>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-bash.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-json.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/toolbar/prism-toolbar.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js"></script>
  <script>
    // --- Universal theme-detection pattern: data-theme override > OS prefers-color-scheme ---
    const themeQuery = window.matchMedia('(prefers-color-scheme: light)');
    function currentTheme() {
      return document.documentElement.dataset.theme
          || (themeQuery.matches ? 'light' : 'dark');
    }
    function onThemeChange(callback) {
      new MutationObserver(callback).observe(document.documentElement, {
        attributes: true, attributeFilter: ['data-theme'],
      });
      themeQuery.addEventListener('change', callback);
    }
    // Reuses the helper pattern from Step 3 — toggle the inactive sheet via `disabled`
    function applyPrismTheme() {
      const isLight = currentTheme() === 'light';
      document.getElementById('prism-theme').disabled       =  isLight;
      document.getElementById('prism-theme-light').disabled = !isLight;
    }
    applyPrismTheme();
    onThemeChange(applyPrismTheme);
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Wrong language class** — the class must be on `<code>`, not `<pre>`: `<pre><code class="language-python">` — putting it on `<pre>` alone won't work for some plugins
- **Unescaped HTML in code** — `<div>` inside a `<code>` block will be parsed as HTML; use `&lt;div&gt;` instead. Never inject untrusted user input into `innerHTML` of a `<code>` — set `textContent` then call `Prism.highlightElement()`
- **Missing language component** — core only includes HTML/CSS/JS/C-like; either load `prism-<lang>.min.js` explicitly or use the **autoloader** plugin and let it fetch components on demand
- **Toolbar without toolbar plugin** — copy-to-clipboard depends on the toolbar plugin; load `prism-toolbar.min.js` before `prism-copy-to-clipboard.min.js`
- **Line numbers + `padding-top` glitch** — the line-numbers plugin positions numbers absolutely against the `<pre>`'s padding; uneven top/bottom padding causes misalignment. Use symmetric padding (e.g. `padding: 16px 20px`)
- **Theme not matching active CSS-variable theme** — toggle both `prism-tomorrow` and a light counterpart by disabling/enabling the right `<link>` on `prefers-color-scheme` change
- **`Prism.highlightAll()` unnecessary on load** — Prism auto-highlights on DOMContentLoaded; only call `highlightAll()` or `highlightElement()` for dynamically added content
- **Leading whitespace** — code inside `<code>` preserves whitespace; start content on the same line as the `<code>` tag or use `data-trim` patterns
- **Script order** — load `prism.min.js` before language components and plugins; they register against the global `Prism` object
- **Multiple themes loaded simultaneously** — only one Prism theme stylesheet may be active at any time; if both are enabled their selectors collide. Use the `disabled` attribute on `<link>` to toggle
- **Suppressing copy-button focus outlines** — keyboard users tab to the copy button; don't override `:focus-visible` to `outline: none`
