---
name: tiptap
description: Build polished rich text editors using Tiptap v2 (headless, ProseMirror-based) delivered as self-contained HTML artifacts via an ES-module importmap. Use this skill for any request involving a rich text input: comment box, note editor, blog post composer, Notion-style block editor, markdown-like WYSIWYG, inline editable cards, document editors, chat composers with formatting, or any "make a text editor with bold/italic/headings/lists/links/code/quotes" task. Trigger on phrases like "build a rich text editor", "notion-style editor", "comment box with formatting", "blog composer", "WYSIWYG", "markdown editor with toolbar", "slash commands", "bubble menu", "floating menu", "mention picker", "Tiptap". Do NOT use for: simple plain `<textarea>` inputs, code editors with syntax highlighting (→ prism / monaco), Markdown viewers, server-driven HTML swaps (→ htmx skill), reusable web components without text editing (→ lit skill).
agents: [dev]
---

# Tiptap Skill — v2

Tiptap is a **headless** rich text editor framework built on ProseMirror. Headless means it ships zero CSS — you control every pixel. It exposes a clean Editor API plus an extension system: marks (bold, italic, link), nodes (paragraph, heading, list, codeBlock), and behaviour extensions (Placeholder, History, Dropcursor, Mention, BubbleMenu, FloatingMenu). In artifacts we load it via an ES-module importmap from `esm.sh`, so there is no build step.

---

## Artifact Presentation & Use Cases

Every Tiptap artifact is a self-contained HTML page with a dark theme. The visual shell is the standard Alyx card:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) hosts the editor
- **Title** (`h1`, 1.15rem, `#f1f5f9`) names the document/editor
- **Subtitle** (`p.sub`, 0.82rem, `#94a3b8`) hints at supported commands
- **Toolbar** with formatting buttons that mirror the active editor state
- **`.ProseMirror` editor surface** styled by us (prose styles for headings, lists, code, quotes, links)
- Optional **bubble menu** appearing over selected text; optional **floating menu** appearing on empty lines; optional **slash menu** triggered by typing `/`

### Typical use cases

- **Comment box** — minimal toolbar (bold, italic, link, mention) with a fixed-height surface and submit button
- **Note editor** — full prose styles, headings, lists, code blocks, blockquote; autosaves to a JSON state
- **Blog post composer** — large surface, slash menu for block insertion, image embedding, link bubble menu
- **Notion-style block editor** — drag handles, slash commands, bubble menu, floating menu, dark/light themes
- **Inline editable card** — small editor inside a list item, no toolbar, blurs to save

### What the user sees

A blank document area with a blinking cursor and a placeholder ("Start writing…"). Typing produces native prose. Highlighting text shows a bubble menu for bold / italic / link. Typing `/` on an empty line shows a slash command list. Toolbar buttons highlight as the cursor moves through formatted regions. The whole surface is keyboard-accessible (Ctrl+B/I/U, Markdown shortcuts like `# ` for heading, `* ` for list).

---

## When to Use Tiptap vs. Alternatives

| Use Tiptap when… | Use another tool when… |
|---|---|
| Rich text input is the core interaction | Plain text → native `<textarea>` |
| You need formatting marks (bold, italic, link, code) | Code editing with syntax highlighting → **Monaco / CodeMirror** |
| You need block nodes (headings, lists, quotes, code blocks) | Pure Markdown preview → render markdown with `marked.js` |
| You want full visual control (headless) | Pre-styled editor with batteries → **EditorJS / Quill** |
| Slash commands, mentions, bubble menus | Schema-less freeform canvas → **Konva** |
| You want JSON state to persist / sync | Just dispatching server fragments → **htmx** |
| Notion-style block editor | Form-style structured inputs → React Hook Form + shadcn |

> **Rule of thumb:** if the natural description includes "the user writes formatted text", Tiptap is the right tool. For Markdown-as-source workflows, Tiptap with the `Typography` and `Markdown` extensions is still the cleanest path.

---

## Step 1 — Importmap & ES Module Setup

Tiptap is ES-module-first. Use an importmap so the bare specifier `@tiptap/core` resolves through `esm.sh` (which serves them as proper ES modules and resolves peer dependencies). Load the importmap **before** any `<script type="module">`.

```html
<script type="importmap">
{
  "imports": {
    "@tiptap/core":            "https://esm.sh/@tiptap/core@2.10.3",
    "@tiptap/pm/state":        "https://esm.sh/@tiptap/pm@2.10.3/state",
    "@tiptap/pm/view":         "https://esm.sh/@tiptap/pm@2.10.3/view",
    "@tiptap/starter-kit":     "https://esm.sh/@tiptap/starter-kit@2.10.3",
    "@tiptap/extension-placeholder":   "https://esm.sh/@tiptap/extension-placeholder@2.10.3",
    "@tiptap/extension-link":          "https://esm.sh/@tiptap/extension-link@2.10.3",
    "@tiptap/extension-task-list":     "https://esm.sh/@tiptap/extension-task-list@2.10.3",
    "@tiptap/extension-task-item":     "https://esm.sh/@tiptap/extension-task-item@2.10.3",
    "@tiptap/extension-typography":    "https://esm.sh/@tiptap/extension-typography@2.10.3",
    "@tiptap/extension-bubble-menu":   "https://esm.sh/@tiptap/extension-bubble-menu@2.10.3",
    "@tiptap/extension-floating-menu": "https://esm.sh/@tiptap/extension-floating-menu@2.10.3",
    "@tiptap/extension-mention":       "https://esm.sh/@tiptap/extension-mention@2.10.3",
    "@tiptap/suggestion":              "https://esm.sh/@tiptap/suggestion@2.10.3"
  }
}
</script>
```

Then load your code with:

```html
<script type="module">
  import { Editor } from '@tiptap/core';
  import StarterKit from '@tiptap/starter-kit';
  // …
</script>
```

> **Critical:** the importmap must appear before any `<script type="module">` (and ideally before any other `<script>` that might dispatch module loads). Browsers ignore importmaps that arrive after module imports have started.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tiptap Editor</title>
  <style>/* tokens + prose styles + toolbar — see Step 3 */</style>
</head>
<body data-theme="dark">
  <main class="card">
    <header class="head">
      <h1>Document</h1>
      <button class="theme-btn" id="themeBtn" type="button" aria-label="Toggle theme">Toggle theme</button>
    </header>
    <p class="sub">Select text for the bubble menu &middot; type / for blocks &middot; Cmd+B for bold</p>

    <div class="toolbar" role="toolbar" aria-label="Editor formatting">
      <!-- toolbar buttons injected by setup -->
    </div>

    <div id="editor" class="editor-host" aria-label="Document body"></div>

    <footer class="foot">
      <span id="wordcount">0 words</span>
      <button class="primary" id="saveBtn" type="button">Save</button>
    </footer>
  </main>

  <!-- Importmap MUST appear before the module script -->
  <script type="importmap">{ "imports": { … see Step 1 … } }</script>
  <script type="module">/* editor code — see Step 11 */</script>
</body>
</html>
```

---

## Step 3 — Themes (dark + light)

Tiptap ships no CSS, so the entire prose look is yours. Define tokens once; theme the toolbar, editor surface, and ProseMirror children from those tokens. Switching themes is a simple `data-theme` flip on `<body>`.

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
  --accent-soft: rgba(99,102,241,0.18);
  --code-bg: #0b0d13;
}
/* Light */
[data-theme="light"] {
  --bg:     #f8fafc;
  --card:   #ffffff;
  --border: rgba(0,0,0,0.08);
  --text:   #1e293b;
  --muted:  #475569;
  --accent: #6366f1;
  --accent-soft: rgba(99,102,241,0.12);
  --code-bg: #f1f5f9;
}

/* Body + card */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg); color: var(--text);
  min-height: 100vh; padding: 32px;
  transition: background 200ms, color 200ms;
}
.card {
  max-width: 760px; margin: 0 auto;
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 24px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.4);
}

/* Toolbar */
.toolbar {
  display: flex; flex-wrap: wrap; gap: 4px;
  padding: 8px; margin-bottom: 12px;
  background: var(--bg); border: 1px solid var(--border); border-radius: 10px;
}
.toolbar button {
  background: transparent; color: var(--muted); border: 1px solid transparent;
  border-radius: 6px; padding: 6px 10px; font-size: 0.78rem; font-family: inherit;
  cursor: pointer; transition: all 120ms;
  min-width: 30px;
}
.toolbar button:hover { background: var(--accent-soft); color: var(--text); }
.toolbar button.is-active {
  background: var(--accent-soft); color: var(--accent);
  border-color: rgba(99,102,241,0.4);
}

/* Prose styles for the ProseMirror surface */
.ProseMirror {
  min-height: 240px;
  padding: 20px 24px;
  background: var(--bg); border: 1px solid var(--border); border-radius: 10px;
  color: var(--text); font-size: 1rem; line-height: 1.65;
  outline: none;
}
.ProseMirror:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
.ProseMirror p { margin: 0 0 0.7em; }
.ProseMirror h1 { font-size: 1.75rem; font-weight: 700; margin: 1em 0 0.4em; line-height: 1.2; }
.ProseMirror h2 { font-size: 1.35rem; font-weight: 600; margin: 1em 0 0.4em; line-height: 1.25; }
.ProseMirror h3 { font-size: 1.1rem;  font-weight: 600; margin: 1em 0 0.4em; }
.ProseMirror ul, .ProseMirror ol { padding-left: 1.3em; margin: 0 0 0.7em; }
.ProseMirror li { margin: 0.1em 0; }
.ProseMirror blockquote {
  border-left: 3px solid var(--accent); padding: 4px 12px;
  margin: 0 0 0.7em; color: var(--muted); font-style: italic;
}
.ProseMirror code {
  background: var(--code-bg); padding: 2px 6px; border-radius: 4px;
  font-family: 'JetBrains Mono', 'Menlo', monospace; font-size: 0.88em;
}
.ProseMirror pre {
  background: var(--code-bg); padding: 14px 16px; border-radius: 8px;
  border: 1px solid var(--border); overflow-x: auto; margin: 0 0 0.7em;
}
.ProseMirror pre code { background: transparent; padding: 0; }
.ProseMirror a { color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }
.ProseMirror hr { border: none; border-top: 1px solid var(--border); margin: 1.2em 0; }
.ProseMirror p.is-editor-empty:first-child::before {
  content: attr(data-placeholder);
  color: var(--muted); float: left; pointer-events: none; height: 0;
}
.ProseMirror .mention {
  background: var(--accent-soft); color: var(--accent);
  border-radius: 4px; padding: 1px 6px; font-weight: 500;
}
```

### Switching themes at runtime

```javascript
document.getElementById('themeBtn').addEventListener('click', () => {
  const next = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
  document.body.dataset.theme = next;
});
```

---

## Step 4 — Editor Instantiation

```javascript
import { Editor } from '@tiptap/core';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';

const editor = new Editor({
  element: document.querySelector('#editor'),
  extensions: [
    StarterKit,                                         // sensible defaults
    Placeholder.configure({ placeholder: 'Start writing…' }),
  ],
  content: '<p>Hello <strong>world</strong>.</p>',     // initial HTML
  autofocus: true,
  editable: true,
  injectCSS: false,                                    // we provide our own styles
  editorProps: {
    attributes: {
      role: 'textbox',
      'aria-multiline': 'true',
      'aria-label': 'Document body',
    },
  },
  onUpdate: ({ editor }) => updateUI(editor),
  onSelectionUpdate: ({ editor }) => updateUI(editor),
});
```

> `injectCSS: false` is important — otherwise Tiptap injects a minimal default stylesheet that conflicts with our themed prose styles.

### Reading & writing content

```javascript
editor.getHTML();    // '<p>Hello <strong>world</strong>.</p>'
editor.getJSON();    // ProseMirror doc as JSON — best for storage
editor.getText();    // plain text
editor.setContent('<p>Replace me</p>', /* emitUpdate */ true);
editor.commands.setContent(json);            // accepts HTML or ProseMirror JSON
editor.commands.clearContent();
```

### Destroying

```javascript
editor.destroy();   // call on teardown to free ProseMirror resources
```

---

## Step 5 — StarterKit (what you get for free)

StarterKit bundles the most common nodes, marks, and behaviour extensions. Configure or disable any of them:

```javascript
StarterKit.configure({
  heading: { levels: [1, 2, 3] },
  codeBlock: { HTMLAttributes: { class: 'code-block' } },
  bulletList: { keepMarks: true },
  history: { depth: 100, newGroupDelay: 500 },
  // Disable an included extension:
  blockquote: false,
})
```

What StarterKit includes:

| Nodes | Marks | Extensions |
|---|---|---|
| Document, Paragraph, Text | Bold | History (undo/redo) |
| Heading (H1–H6) | Italic | Dropcursor |
| BulletList, OrderedList, ListItem | Strike | Gapcursor |
| Blockquote | Code | HardBreak |
| CodeBlock | Link* | HorizontalRule |
| HardBreak, HorizontalRule | | |

*Link is **not** included by default — add `@tiptap/extension-link` explicitly.

---

## Step 6 — Commands (the imperative API)

All editor mutations go through `editor.chain().focus().XXX().run()`:

```javascript
editor.chain().focus().toggleBold().run();
editor.chain().focus().toggleItalic().run();
editor.chain().focus().toggleStrike().run();
editor.chain().focus().toggleCode().run();
editor.chain().focus().toggleHeading({ level: 2 }).run();
editor.chain().focus().toggleBulletList().run();
editor.chain().focus().toggleOrderedList().run();
editor.chain().focus().toggleTaskList().run();           // requires TaskList extension
editor.chain().focus().toggleBlockquote().run();
editor.chain().focus().toggleCodeBlock().run();
editor.chain().focus().setHorizontalRule().run();
editor.chain().focus().setHardBreak().run();

editor.chain().focus().setLink({ href: 'https://example.com' }).run();
editor.chain().focus().unsetLink().run();

editor.chain().focus().undo().run();
editor.chain().focus().redo().run();
```

### Querying state (toolbar highlighting)

```javascript
editor.isActive('bold');                    // true if cursor is in bold text
editor.isActive('heading', { level: 2 });   // true if cursor is in an H2
editor.isActive('bulletList');
editor.can().toggleBold();                  // false if not allowed in current selection
```

---

## Step 7 — Custom Extensions (creating marks & nodes)

You can extend any built-in or write your own. A minimal custom mark:

```javascript
import { Mark, mergeAttributes } from '@tiptap/core';

const Highlight = Mark.create({
  name: 'highlight',
  parseHTML() { return [{ tag: 'mark' }]; },
  renderHTML({ HTMLAttributes }) {
    return ['mark', mergeAttributes(HTMLAttributes, { class: 'hl' }), 0];
  },
  addCommands() {
    return {
      toggleHighlight: () => ({ commands }) => commands.toggleMark(this.name),
    };
  },
  addKeyboardShortcuts() {
    return { 'Mod-Shift-h': () => this.editor.commands.toggleHighlight() };
  },
});
```

A minimal custom node (block-level callout):

```javascript
import { Node, mergeAttributes } from '@tiptap/core';

const Callout = Node.create({
  name: 'callout',
  group: 'block',
  content: 'block+',
  defining: true,
  parseHTML() { return [{ tag: 'div[data-callout]' }]; },
  renderHTML({ HTMLAttributes }) {
    return ['div', mergeAttributes({ 'data-callout': '', class: 'callout' }, HTMLAttributes), 0];
  },
  addCommands() {
    return {
      setCallout: () => ({ commands }) => commands.wrapIn(this.name),
      unsetCallout: () => ({ commands }) => commands.lift(this.name),
    };
  },
});
```

---

## Step 8 — Bubble & Floating Menus

### Bubble menu (appears over selected text)

```javascript
import BubbleMenu from '@tiptap/extension-bubble-menu';

const bubble = document.querySelector('#bubble-menu');
// In extensions: BubbleMenu.configure({ element: bubble })
```

```html
<div id="bubble-menu" class="bubble-menu" role="toolbar" aria-label="Quick formatting">
  <button data-cmd="bold"   aria-label="Bold">B</button>
  <button data-cmd="italic" aria-label="Italic"><i>I</i></button>
  <button data-cmd="link"   aria-label="Link">&#128279;</button>
</div>
```

```css
.bubble-menu {
  display: flex; gap: 2px; padding: 4px;
  background: #1e2130; border: 1px solid var(--border);
  border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.bubble-menu button {
  background: transparent; color: var(--text); border: none;
  padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 0.85rem;
}
.bubble-menu button:hover { background: var(--accent-soft); color: var(--accent); }
```

### Floating menu (appears on empty new lines)

```javascript
import FloatingMenu from '@tiptap/extension-floating-menu';
// FloatingMenu.configure({ element: document.querySelector('#floating-menu') })
```

Use it as your **slash command launcher** — show a hint like "Type / for commands" anchored to empty lines.

---

## Step 9 — Slash Commands

Slash commands are implemented with `@tiptap/suggestion`, the same primitive that powers Mention. The trigger character is `/`; on each keystroke after the trigger, you receive a query string and decide what to render.

```javascript
import { Extension } from '@tiptap/core';
import Suggestion from '@tiptap/suggestion';

const ITEMS = [
  { title: 'Heading 1', cmd: e => e.chain().focus().toggleHeading({ level: 1 }).run() },
  { title: 'Heading 2', cmd: e => e.chain().focus().toggleHeading({ level: 2 }).run() },
  { title: 'Bullet List', cmd: e => e.chain().focus().toggleBulletList().run() },
  { title: 'Numbered List', cmd: e => e.chain().focus().toggleOrderedList().run() },
  { title: 'Task List', cmd: e => e.chain().focus().toggleTaskList().run() },
  { title: 'Quote', cmd: e => e.chain().focus().toggleBlockquote().run() },
  { title: 'Code Block', cmd: e => e.chain().focus().toggleCodeBlock().run() },
  { title: 'Divider', cmd: e => e.chain().focus().setHorizontalRule().run() },
];

const SlashCommand = Extension.create({
  name: 'slashCommand',
  addOptions() { return { suggestion: { char: '/', startOfLine: false } }; },
  addProseMirrorPlugins() {
    return [
      Suggestion({
        editor: this.editor,
        ...this.options.suggestion,
        command: ({ editor, range, props }) => {
          editor.chain().focus().deleteRange(range).run();
          props.cmd(editor);
        },
        items: ({ query }) =>
          ITEMS.filter(i => i.title.toLowerCase().includes(query.toLowerCase())).slice(0, 8),
        render: () => {
          let popup, items, idx = 0;
          const select = (i) => {
            const item = items[i]; if (!item) return;
            item.command();
          };
          const render = () => {
            popup.innerHTML = items.map((it, i) =>
              `<button class="slash-item ${i === idx ? 'is-active' : ''}" data-i="${i}">${it.title}</button>`
            ).join('');
          };
          return {
            onStart: (props) => {
              popup = document.createElement('div');
              popup.className = 'slash-menu';
              popup.setAttribute('role', 'listbox');
              document.body.appendChild(popup);
              items = props.items;
              const r = props.clientRect();
              popup.style.cssText = `position:fixed; top:${r.bottom + 6}px; left:${r.left}px;`;
              render();
              popup.addEventListener('mousedown', (e) => {
                const i = +e.target.dataset.i;
                if (!isNaN(i)) { props.command(items[i]); }
              });
            },
            onUpdate: (props) => {
              items = props.items; idx = 0; render();
            },
            onKeyDown: ({ event }) => {
              if (event.key === 'ArrowDown') { idx = (idx + 1) % items.length; render(); return true; }
              if (event.key === 'ArrowUp')   { idx = (idx - 1 + items.length) % items.length; render(); return true; }
              if (event.key === 'Enter')     { select(idx); return true; }
              if (event.key === 'Escape')    { popup.remove(); return true; }
              return false;
            },
            onExit: () => popup?.remove(),
          };
        },
      }),
    ];
  },
});
```

Add `SlashCommand` to the editor's extensions list.

---

## Step 10 — Mentions

Mentions use the same `@tiptap/suggestion` primitive, but ship as a node so they serialise cleanly into JSON.

```javascript
import Mention from '@tiptap/extension-mention';

const USERS = ['Ada Lovelace', 'Alan Turing', 'Grace Hopper', 'Linus Torvalds'];

Mention.configure({
  HTMLAttributes: { class: 'mention' },
  suggestion: {
    char: '@',
    items: ({ query }) => USERS.filter(u => u.toLowerCase().includes(query.toLowerCase())).slice(0, 6),
    render: () => {
      // Same pattern as slash menu — small popup, arrow keys, Enter to select.
      // props.command({ id: name, label: name }) inserts the mention node.
      let popup, items = [], idx = 0;
      const draw = () => popup.innerHTML = items.map((u, i) =>
        `<button class="slash-item ${i === idx ? 'is-active' : ''}" data-u="${u}">@${u}</button>`
      ).join('');
      return {
        onStart: (p) => {
          popup = document.createElement('div'); popup.className = 'slash-menu';
          document.body.appendChild(popup);
          items = p.items; const r = p.clientRect();
          popup.style.cssText = `position:fixed; top:${r.bottom + 6}px; left:${r.left}px;`;
          draw();
          popup.addEventListener('mousedown', (e) => {
            const u = e.target.dataset.u;
            if (u) p.command({ id: u, label: u });
          });
        },
        onUpdate: (p) => { items = p.items; idx = 0; draw(); },
        onKeyDown: ({ event }) => {
          if (event.key === 'ArrowDown') { idx = (idx+1) % items.length; draw(); return true; }
          if (event.key === 'ArrowUp')   { idx = (idx-1+items.length) % items.length; draw(); return true; }
          if (event.key === 'Enter')     { const u = items[idx]; if (u) { /* p.command in upstream */ }; return true; }
          if (event.key === 'Escape')    { popup.remove(); return true; }
          return false;
        },
        onExit: () => popup?.remove(),
      };
    },
  },
})
```

---

## Step 11 — JSON / HTML Serialization

Tiptap content has two interchangeable representations:

```javascript
const html = editor.getHTML();
const json = editor.getJSON();   // { type: 'doc', content: [...] }

// Persisting (in artifacts, just keep in memory or pass to a callback):
const snapshot = JSON.stringify(json);

// Restoring:
editor.commands.setContent(JSON.parse(snapshot));

// Markdown? Use @tiptap/extension-typography for smart quotes/dashes,
// and a serialiser like `tiptap-markdown` if real .md is required.
```

**Always prefer JSON for storage.** HTML round-trips lose unknown attributes; JSON is the canonical ProseMirror document.

---

## Step 12 — Complete Example: Notion-Style Block Editor

A polished, self-contained Tiptap editor with a toolbar, bubble menu, slash commands, and a dark/light theme toggle.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Notion-style Editor</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    :root, [data-theme="dark"] {
      --bg:#0f1117; --card:#1a1d27; --border:rgba(255,255,255,0.08);
      --text:#e2e8f0; --muted:#94a3b8; --accent:#6366f1;
      --accent-soft:rgba(99,102,241,0.18); --code-bg:#0b0d13;
    }
    [data-theme="light"] {
      --bg:#f8fafc; --card:#ffffff; --border:rgba(0,0,0,0.08);
      --text:#1e293b; --muted:#475569; --accent:#6366f1;
      --accent-soft:rgba(99,102,241,0.12); --code-bg:#f1f5f9;
    }
    body {
      font-family: -apple-system, 'Segoe UI', sans-serif;
      background: var(--bg); color: var(--text); min-height: 100vh; padding: 32px;
      transition: background 200ms, color 200ms;
    }
    .card {
      max-width: 760px; margin: 0 auto;
      background: var(--card); border: 1px solid var(--border);
      border-radius: 16px; padding: 24px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    }
    .head { display:flex; justify-content:space-between; align-items:baseline; margin-bottom: 4px; }
    h1 { font-size: 1.15rem; font-weight: 600; }
    .theme-btn {
      background: transparent; color: var(--muted); border: 1px solid var(--border);
      border-radius: 8px; padding: 4px 10px; font-size: 0.72rem; cursor: pointer;
    }
    .theme-btn:hover { color: var(--text); }
    p.sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 16px; }

    .toolbar {
      display:flex; flex-wrap:wrap; gap:4px;
      padding:8px; margin-bottom:12px;
      background: var(--bg); border:1px solid var(--border); border-radius:10px;
    }
    .toolbar button {
      background: transparent; color: var(--muted); border: 1px solid transparent;
      border-radius: 6px; padding: 6px 10px; font-size: 0.78rem; font-family: inherit;
      cursor: pointer; transition: all 120ms; min-width: 30px;
    }
    .toolbar button:hover { background: var(--accent-soft); color: var(--text); }
    .toolbar button.is-active {
      background: var(--accent-soft); color: var(--accent);
      border-color: rgba(99,102,241,0.4);
    }
    .toolbar .sep { width:1px; background: var(--border); margin: 4px 6px; align-self: stretch; }

    .ProseMirror {
      min-height: 280px;
      padding: 20px 24px;
      background: var(--bg); border: 1px solid var(--border); border-radius: 10px;
      color: var(--text); font-size: 1rem; line-height: 1.65; outline: none;
    }
    .ProseMirror:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
    .ProseMirror p { margin: 0 0 0.7em; }
    .ProseMirror h1 { font-size: 1.75rem; font-weight: 700; margin: 1em 0 0.4em; }
    .ProseMirror h2 { font-size: 1.35rem; font-weight: 600; margin: 1em 0 0.4em; }
    .ProseMirror h3 { font-size: 1.1rem;  font-weight: 600; margin: 1em 0 0.4em; }
    .ProseMirror ul, .ProseMirror ol { padding-left: 1.3em; margin: 0 0 0.7em; }
    .ProseMirror blockquote {
      border-left: 3px solid var(--accent); padding: 4px 12px;
      margin: 0 0 0.7em; color: var(--muted); font-style: italic;
    }
    .ProseMirror code {
      background: var(--code-bg); padding: 2px 6px; border-radius: 4px;
      font-family: 'JetBrains Mono', 'Menlo', monospace; font-size: 0.88em;
    }
    .ProseMirror pre {
      background: var(--code-bg); padding: 14px 16px; border-radius: 8px;
      border: 1px solid var(--border); overflow-x: auto; margin: 0 0 0.7em;
    }
    .ProseMirror a { color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }
    .ProseMirror hr { border: none; border-top: 1px solid var(--border); margin: 1.2em 0; }
    .ProseMirror p.is-editor-empty:first-child::before {
      content: attr(data-placeholder);
      color: var(--muted); float: left; pointer-events: none; height: 0;
    }

    .bubble-menu {
      display: flex; gap: 2px; padding: 4px;
      background: #1e2130; border: 1px solid var(--border);
      border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    [data-theme="light"] .bubble-menu { background: #ffffff; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
    .bubble-menu button {
      background: transparent; color: var(--text); border: none;
      padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 0.85rem;
    }
    .bubble-menu button:hover { background: var(--accent-soft); color: var(--accent); }

    .slash-menu {
      background: #1e2130; border: 1px solid var(--border);
      border-radius: 8px; padding: 4px; min-width: 200px; z-index: 1000;
      box-shadow: 0 8px 30px rgba(0,0,0,0.5); max-height: 280px; overflow-y: auto;
    }
    [data-theme="light"] .slash-menu { background: #ffffff; box-shadow: 0 8px 30px rgba(0,0,0,0.15); }
    .slash-item {
      display: block; width: 100%; text-align: left;
      background: transparent; color: var(--text); border: none;
      padding: 8px 12px; border-radius: 4px; cursor: pointer;
      font-size: 0.85rem; font-family: inherit;
    }
    .slash-item:hover, .slash-item.is-active { background: var(--accent-soft); color: var(--accent); }

    .foot {
      display: flex; justify-content: space-between; align-items: center;
      margin-top: 14px; font-size: 0.78rem; color: var(--muted);
    }
    .primary {
      background: var(--accent); color: #fff; border: none; border-radius: 8px;
      padding: 7px 16px; font-size: 0.82rem; font-weight: 500; cursor: pointer;
      transition: filter 150ms;
    }
    .primary:hover { filter: brightness(1.1); }
  </style>
</head>
<body data-theme="dark">
  <main class="card">
    <div class="head">
      <h1>Untitled note</h1>
      <button class="theme-btn" id="themeBtn" type="button">Toggle theme</button>
    </div>
    <p class="sub">Select text for the bubble menu &middot; type / for blocks &middot; ⌘B / ⌘I / ⌘K</p>

    <div class="toolbar" role="toolbar" aria-label="Formatting" id="toolbar"></div>

    <div id="editor"></div>
    <div id="bubble-menu" class="bubble-menu" role="toolbar" aria-label="Quick format"></div>

    <div class="foot">
      <span id="wordcount">0 words</span>
      <button class="primary" id="saveBtn" type="button">Save snapshot</button>
    </div>
  </main>

  <script type="importmap">
  {
    "imports": {
      "@tiptap/core":                  "https://esm.sh/@tiptap/core@2.10.3",
      "@tiptap/pm/state":              "https://esm.sh/@tiptap/pm@2.10.3/state",
      "@tiptap/pm/view":               "https://esm.sh/@tiptap/pm@2.10.3/view",
      "@tiptap/starter-kit":           "https://esm.sh/@tiptap/starter-kit@2.10.3",
      "@tiptap/extension-placeholder": "https://esm.sh/@tiptap/extension-placeholder@2.10.3",
      "@tiptap/extension-link":        "https://esm.sh/@tiptap/extension-link@2.10.3",
      "@tiptap/extension-bubble-menu": "https://esm.sh/@tiptap/extension-bubble-menu@2.10.3",
      "@tiptap/suggestion":            "https://esm.sh/@tiptap/suggestion@2.10.3"
    }
  }
  </script>

  <script type="module">
    import { Editor, Extension } from '@tiptap/core';
    import StarterKit from '@tiptap/starter-kit';
    import Placeholder from '@tiptap/extension-placeholder';
    import Link from '@tiptap/extension-link';
    import BubbleMenu from '@tiptap/extension-bubble-menu';
    import Suggestion from '@tiptap/suggestion';

    // ── Slash command extension ────────────────────────────
    const ITEMS = [
      { title: 'Heading 1',     cmd: e => e.chain().focus().toggleHeading({ level: 1 }).run() },
      { title: 'Heading 2',     cmd: e => e.chain().focus().toggleHeading({ level: 2 }).run() },
      { title: 'Heading 3',     cmd: e => e.chain().focus().toggleHeading({ level: 3 }).run() },
      { title: 'Bullet list',   cmd: e => e.chain().focus().toggleBulletList().run() },
      { title: 'Numbered list', cmd: e => e.chain().focus().toggleOrderedList().run() },
      { title: 'Quote',         cmd: e => e.chain().focus().toggleBlockquote().run() },
      { title: 'Code block',    cmd: e => e.chain().focus().toggleCodeBlock().run() },
      { title: 'Divider',       cmd: e => e.chain().focus().setHorizontalRule().run() },
    ];

    const SlashCommand = Extension.create({
      name: 'slashCommand',
      addProseMirrorPlugins() {
        const editor = this.editor;
        return [Suggestion({
          editor, char: '/',
          items: ({ query }) => ITEMS.filter(i => i.title.toLowerCase().includes(query.toLowerCase())).slice(0, 8),
          command: ({ editor, range, props }) => {
            editor.chain().focus().deleteRange(range).run();
            props.cmd(editor);
          },
          render: () => {
            let popup, items = [], idx = 0, currentProps;
            const draw = () => {
              popup.innerHTML = items.map((it, i) =>
                `<button class="slash-item${i === idx ? ' is-active' : ''}" data-i="${i}" role="option" aria-selected="${i === idx}">${it.title}</button>`
              ).join('') || '<div class="slash-item" aria-disabled="true">No match</div>';
            };
            const select = (i) => {
              const item = items[i]; if (!item) return;
              currentProps.command(item);
            };
            return {
              onStart: (p) => {
                popup = document.createElement('div');
                popup.className = 'slash-menu';
                popup.setAttribute('role', 'listbox');
                document.body.appendChild(popup);
                items = p.items; currentProps = p; idx = 0;
                const r = p.clientRect();
                popup.style.cssText = `position:fixed; top:${r.bottom + 6}px; left:${r.left}px;`;
                draw();
                popup.addEventListener('mousedown', (e) => {
                  const i = +e.target.dataset.i;
                  if (!isNaN(i)) { e.preventDefault(); select(i); }
                });
              },
              onUpdate: (p) => { items = p.items; currentProps = p; idx = 0; draw(); },
              onKeyDown: ({ event }) => {
                if (!items.length) return false;
                if (event.key === 'ArrowDown') { idx = (idx + 1) % items.length; draw(); return true; }
                if (event.key === 'ArrowUp')   { idx = (idx - 1 + items.length) % items.length; draw(); return true; }
                if (event.key === 'Enter')     { select(idx); return true; }
                if (event.key === 'Escape')    { popup?.remove(); return true; }
                return false;
              },
              onExit: () => popup?.remove(),
            };
          },
        })];
      },
    });

    // ── Editor instance ────────────────────────────────────
    const editor = new Editor({
      element: document.querySelector('#editor'),
      injectCSS: false,
      autofocus: true,
      editorProps: {
        attributes: {
          role: 'textbox', 'aria-multiline': 'true', 'aria-label': 'Document body',
        },
      },
      extensions: [
        StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
        Placeholder.configure({ placeholder: 'Type / for commands, or just start writing…' }),
        Link.configure({ openOnClick: false, HTMLAttributes: { rel: 'noopener', target: '_blank' } }),
        BubbleMenu.configure({ element: document.querySelector('#bubble-menu') }),
        SlashCommand,
      ],
      content: `
        <h1>Welcome</h1>
        <p>This is a <strong>Tiptap</strong> editor with a <em>bubble menu</em> and <code>/</code> commands.</p>
        <ul><li>Select text → bubble menu</li><li>Type / on a new line → slash menu</li></ul>
      `,
      onUpdate: ({ editor }) => updateUI(editor),
      onSelectionUpdate: ({ editor }) => updateUI(editor),
    });

    // ── Toolbar ────────────────────────────────────────────
    const TB = [
      { cmd: 'bold',                  label: 'B',  active: 'bold',      keys: '⌘B' },
      { cmd: 'italic',                label: '𝑰',  active: 'italic',    keys: '⌘I' },
      { cmd: 'strike',                label: 'S',  active: 'strike' },
      { cmd: 'code',                  label: '</>', active: 'code' },
      { sep: true },
      { cmd: 'heading', arg: 1,       label: 'H1', active: ['heading',{level:1}] },
      { cmd: 'heading', arg: 2,       label: 'H2', active: ['heading',{level:2}] },
      { cmd: 'heading', arg: 3,       label: 'H3', active: ['heading',{level:3}] },
      { sep: true },
      { cmd: 'bulletList',  label: '• List',    active: 'bulletList' },
      { cmd: 'orderedList', label: '1. List',   active: 'orderedList' },
      { cmd: 'blockquote',  label: '“ Quote',   active: 'blockquote' },
      { cmd: 'codeBlock',   label: '⌗ Code',    active: 'codeBlock' },
      { sep: true },
      { cmd: 'link',       label: '🔗',        active: 'link' },
      { cmd: 'undo',       label: '↶' },
      { cmd: 'redo',       label: '↷' },
    ];

    function runCmd(item) {
      const c = editor.chain().focus();
      switch (item.cmd) {
        case 'bold':        return c.toggleBold().run();
        case 'italic':      return c.toggleItalic().run();
        case 'strike':      return c.toggleStrike().run();
        case 'code':        return c.toggleCode().run();
        case 'heading':     return c.toggleHeading({ level: item.arg }).run();
        case 'bulletList':  return c.toggleBulletList().run();
        case 'orderedList': return c.toggleOrderedList().run();
        case 'blockquote':  return c.toggleBlockquote().run();
        case 'codeBlock':   return c.toggleCodeBlock().run();
        case 'undo':        return c.undo().run();
        case 'redo':        return c.redo().run();
        case 'link': {
          const prev = editor.getAttributes('link').href;
          const url  = prompt('URL', prev || 'https://');
          if (url === null) return;
          if (url === '')   return c.unsetLink().run();
          return c.setLink({ href: url }).run();
        }
      }
    }

    function renderToolbar() {
      const host = document.getElementById('toolbar');
      host.innerHTML = '';
      TB.forEach((item, i) => {
        if (item.sep) {
          const s = document.createElement('span'); s.className = 'sep'; host.appendChild(s); return;
        }
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = item.label;
        btn.title = item.keys ? `${item.cmd} (${item.keys})` : item.cmd;
        btn.setAttribute('aria-label', item.cmd);
        btn.dataset.i = i;
        btn.addEventListener('mousedown', (e) => { e.preventDefault(); runCmd(item); });
        host.appendChild(btn);
      });
      // Bubble menu shares the same handler set, minimal subset:
      const bm = document.getElementById('bubble-menu');
      bm.innerHTML = '';
      ['bold','italic','code','link'].forEach(name => {
        const item = TB.find(t => t.cmd === name);
        const btn = document.createElement('button');
        btn.type = 'button'; btn.textContent = item.label; btn.setAttribute('aria-label', name);
        btn.addEventListener('mousedown', (e) => { e.preventDefault(); runCmd(item); });
        bm.appendChild(btn);
      });
    }

    function isActive(item) {
      if (!item.active) return false;
      return Array.isArray(item.active)
        ? editor.isActive(item.active[0], item.active[1])
        : editor.isActive(item.active);
    }

    function updateUI(ed) {
      const buttons = document.querySelectorAll('#toolbar button');
      buttons.forEach((b) => {
        const item = TB[+b.dataset.i];
        if (!item) return;
        b.classList.toggle('is-active', isActive(item));
      });
      const text = ed.getText().trim();
      const words = text ? text.split(/\s+/).length : 0;
      document.getElementById('wordcount').textContent = `${words} word${words === 1 ? '' : 's'}`;
    }

    renderToolbar();
    updateUI(editor);

    // ── Theme + save snapshot ──────────────────────────────
    document.getElementById('themeBtn').addEventListener('click', () => {
      const next = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
      document.body.dataset.theme = next;
    });

    let snapshots = 0;
    document.getElementById('saveBtn').addEventListener('click', () => {
      const json = editor.getJSON();
      snapshots++;
      const btn = document.getElementById('saveBtn');
      btn.textContent = `Saved snapshot #${snapshots}`;
      setTimeout(() => (btn.textContent = 'Save snapshot'), 1500);
      console.log('Snapshot JSON:', json);
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Importmap declared after a `<script type="module">`** — the browser silently ignores it and bare specifiers fail. Importmap must come first.
- **Leaving `injectCSS: true`** — Tiptap injects a small default stylesheet that fights your custom prose styles. Set `injectCSS: false` for any themed artifact.
- **Forgetting `.focus()` in command chains** — `editor.chain().toggleBold().run()` mutates state but leaves focus in the toolbar; always start with `.focus()` so typing continues in the editor.
- **Click-handlers on toolbar buttons use `click`** — clicking the toolbar blurs the editor, losing the selection. Use `mousedown` with `preventDefault()` instead.
- **Mutating the editor without checking `editor.can()`** — running `toggleHeading` inside a code block throws. Guard with `editor.can().toggleHeading()` before enabling the button.
- **Storing HTML instead of JSON** — HTML round-trips lose marks, attributes, and unknown extensions. Always serialise to JSON for persistence.
- **Skipping ARIA on the editor host** — add `role="textbox" aria-multiline="true" aria-label="..."` via `editorProps.attributes`. Without it, screen readers see an empty `div`.
- **Adding `@tiptap/extension-link` and expecting it in StarterKit** — Link is **not** in StarterKit. Add it explicitly and configure `openOnClick: false` to prevent navigation during editing.
- **Not calling `editor.destroy()`** — leaks ProseMirror state if the host element is removed. In artifacts it's fine to skip, but always include in long-lived apps.
- **Mixing two Suggestion popups with overlapping characters** — `/` for commands and `@` for mentions must be on the same Suggestion plugin instances; each has its own `char`. Don't share state between them.
- **Using `dangerouslySetInnerHTML` semantics on `setContent`** — pass trusted HTML or JSON only. Tiptap parses HTML, so untrusted input can introduce arbitrary nodes (sanitise upstream).
