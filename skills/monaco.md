---
name: monaco-editor
description: Embed the Monaco Editor (the VS Code editor as a library) in a self-contained HTML artifact, delivered with a polished card wrapper and dark theme. Use this skill whenever a request needs an in-page code editor, mini-IDE, code playground, REPL, online JSON/SQL/Markdown editor, code review viewer, regex tester, diff viewer, snippet runner, schema/config editor, or interactive coding tutorial — even without explicit mention of Monaco. Trigger on phrases like "code editor", "playground", "REPL", "diff viewer", "syntax highlighting input", "JSON/SQL/Markdown editor", "mini IDE", "show before/after code", or "let me edit and run". Do NOT use for: read-only syntax highlighting of static snippets (→ prism skill), full collaborative IDEs requiring backend execution, mermaid/PlantUML rendering (→ mermaid-diagrams skill), or rich text / WYSIWYG document editors.
agents: [dev]
---

# Monaco Editor Skill — v0.45 (the VS Code editor, embedded)

Monaco is the same editor that powers Visual Studio Code. Loaded via the AMD loader it provides full IntelliSense-style autocomplete, syntax highlighting for ~80 languages, multi-cursor editing, find/replace, diff editing, and per-model state. It is heavy (~3 MB across requested chunks) but unmatched for a real coding experience inside an artifact.

---

## Artifact Presentation & Use Cases

Every Monaco artifact is a self-contained HTML page with a dark theme. The visual structure follows this pattern:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) frames the editor
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the playground
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) explains keyboard shortcuts and behaviour
- **Tab strip** (optional) shows multiple open files with active highlight
- **Editor container** (`#editor`, fixed height, rounded inside) hosts Monaco
- **Toolbar** with Run, Reset, Format buttons and an output panel for REPL-like artifacts

### Typical use cases

- **Code playgrounds** — edit a snippet (JS, TS, Python pseudocode, JSON, SQL) and run it
- **Mini IDE** — multi-file tabbed editor with theme switcher and language picker
- **JSON / YAML / Markdown editors** — schema-aware editing with live preview
- **Diff viewers** — side-by-side original vs modified for code review
- **Regex testers** — input pattern + test text, highlight matches
- **Tutorial scaffolds** — read-only base code plus an editable challenge block
- **Config editors** — TypeScript / JSON config with autocomplete and error squiggles

### What the user sees

A familiar VS Code feel: smooth dark theme, line numbers, multi-cursor with Alt-click, Ctrl+F find, Cmd+/ comment toggle, hover tooltips, and IntelliSense suggestions where the language supports them. The editor is keyboard-first and screen-reader aware out of the box.

---

## When to Use Monaco vs. Alternatives

| Use Monaco when… | Use another library when… |
|---|---|
| User must **edit** code in the page | User only **reads** code → **Prism** (lighter, static) |
| Multi-language IntelliSense, hover, errors | Plain `<textarea>` is enough → vanilla HTML |
| JSON / TypeScript / Markdown / SQL editing | Diagrams as text-source → **Mermaid** |
| Side-by-side diff editor | Visual flowchart editor → **JointJS** |
| Mini-IDE, playground, REPL feel | WYSIWYG rich text / docs | → external rich-text editor |
| Multi-file tabs with shared workspace | Collaborative real-time editing | → CRDT-based editors (out of scope) |

> **Rule of thumb:** if the user will type into it and you want it to feel like VS Code, use Monaco. If it is read-only, use Prism — Monaco is ~3 MB and overkill for display-only code.

---

## Step 1 — CDN Setup (AMD loader)

Monaco ships as an AMD bundle. Load the loader first, configure the base path, then `require(['vs/editor/editor.main'])`.

```html
<!-- Loader (synchronous, defines window.require) -->
<script src="https://unpkg.com/monaco-editor@0.45/min/vs/loader.js"></script>

<script>
  require.config({
    paths: { vs: 'https://unpkg.com/monaco-editor@0.45/min/vs' }
  });

  // Workers must load from the same origin via a blob shim:
  window.MonacoEnvironment = {
    getWorkerUrl: function (_moduleId, _label) {
      return URL.createObjectURL(new Blob([`
        self.MonacoEnvironment = { baseUrl: 'https://unpkg.com/monaco-editor@0.45/min/' };
        importScripts('https://unpkg.com/monaco-editor@0.45/min/vs/base/worker/workerMain.js');
      `], { type: 'text/javascript' }));
    }
  };

  require(['vs/editor/editor.main'], function () {
    // `monaco` global is now available — build your editor here.
  });
</script>
```

> **Critical:** without the `MonacoEnvironment.getWorkerUrl` blob shim, language workers fail with cross-origin errors and IntelliSense / validation silently breaks. The shim above is the standard pattern for CDN usage.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Code Playground</title>
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
      max-width: 1080px;
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 22px 24px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
    }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }

    /* REQUIRED: editor container must have an explicit height */
    #editor { width: 100%; height: 520px; }
  </style>
</head>
<body>
  <main class="card" aria-labelledby="title">
    <header class="card-header">
      <h1 id="title">Code Playground</h1>
      <p class="sub">Cmd/Ctrl+S to save · Cmd/Ctrl+F to find · Alt-click for multi-cursor</p>
    </header>
    <div id="editor" role="textbox" aria-multiline="true" aria-label="Code editor"></div>
  </main>

  <script src="https://unpkg.com/monaco-editor@0.45/min/vs/loader.js"></script>
  <script>
    // require.config + MonacoEnvironment + require(['vs/editor/editor.main'], …)
  </script>
</body>
</html>
```

---

## Step 3 — Themes (dark + light)

Monaco ships four built-in themes: `vs` (light), `vs-dark` (dark, default for artifacts), `hc-black` (high-contrast dark), `hc-light` (high-contrast light).

```javascript
monaco.editor.setTheme('vs-dark');   // dark (default)
monaco.editor.setTheme('vs');        // light
monaco.editor.setTheme('hc-black');  // high-contrast dark (WCAG AAA)
monaco.editor.setTheme('hc-light');  // high-contrast light
```

### Custom themes matching our design system

Define both a dark and a light variant that align with the artifact tokens, then expose a switcher.

```javascript
// DARK custom theme — token-aligned with the Alyx artifact palette
monaco.editor.defineTheme('alyx-dark', {
  base: 'vs-dark',
  inherit: true,
  rules: [
    { token: '',          foreground: 'e2e8f0', background: '0f1117' },
    { token: 'comment',   foreground: '64748b', fontStyle: 'italic' },
    { token: 'keyword',   foreground: '818cf8' },
    { token: 'string',    foreground: '22c55e' },
    { token: 'number',    foreground: 'f97316' },
    { token: 'type',      foreground: '06b6d4' },
    { token: 'function',  foreground: 'ec4899' },
  ],
  colors: {
    'editor.background':              '#0f1117',
    'editor.foreground':              '#e2e8f0',
    'editorLineNumber.foreground':    '#475569',
    'editorLineNumber.activeForeground': '#94a3b8',
    'editor.lineHighlightBackground': '#1a1d2766',
    'editorCursor.foreground':        '#6366f1',
    'editor.selectionBackground':     '#6366f155',
    'editorWidget.background':        '#1a1d27',
    'editorWidget.border':            'rgba(255,255,255,0.08)',
    'editorIndentGuide.background1':  'rgba(255,255,255,0.04)',
    'editorBracketMatch.background':  '#6366f133',
    'scrollbarSlider.background':     'rgba(255,255,255,0.06)',
    'scrollbarSlider.hoverBackground':'rgba(255,255,255,0.12)',
  },
});

// LIGHT custom theme — same accents, light surfaces
monaco.editor.defineTheme('alyx-light', {
  base: 'vs',
  inherit: true,
  rules: [
    { token: '',          foreground: '1e293b', background: 'f8fafc' },
    { token: 'comment',   foreground: '94a3b8', fontStyle: 'italic' },
    { token: 'keyword',   foreground: '6366f1' },
    { token: 'string',    foreground: '15803d' },
    { token: 'number',    foreground: 'c2410c' },
    { token: 'type',      foreground: '0e7490' },
    { token: 'function',  foreground: 'be185d' },
  ],
  colors: {
    'editor.background':              '#ffffff',
    'editor.foreground':              '#1e293b',
    'editorLineNumber.foreground':    '#94a3b8',
    'editorLineNumber.activeForeground': '#475569',
    'editor.lineHighlightBackground': '#f1f5f9',
    'editorCursor.foreground':        '#6366f1',
    'editor.selectionBackground':     '#6366f133',
    'editorWidget.background':        '#ffffff',
    'editorWidget.border':            'rgba(0,0,0,0.08)',
    'editorIndentGuide.background1':  'rgba(0,0,0,0.05)',
  },
});

monaco.editor.setTheme('alyx-dark');
```

### Theme token reference

| Token | Dark | Light |
|---|---|---|
| Page background | `#0f1117` | `#f8fafc` |
| Card background | `#1a1d27` | `#ffffff` |
| Border | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` |
| Text | `#e2e8f0` | `#1e293b` |
| Muted | `#94a3b8` | `#475569` |
| Accent | `#6366f1` | `#6366f1` |

### Live theme switcher

```javascript
const themeBtn = document.getElementById('themeBtn');
let dark = true;
themeBtn.addEventListener('click', () => {
  dark = !dark;
  monaco.editor.setTheme(dark ? 'alyx-dark' : 'alyx-light');
  document.body.style.background = dark ? '#0f1117' : '#f8fafc';
  document.body.style.color      = dark ? '#e2e8f0' : '#1e293b';
  themeBtn.setAttribute('aria-pressed', String(!dark));
});
```

---

## Step 4 — Creating an Editor

```javascript
const editor = monaco.editor.create(document.getElementById('editor'), {
  value: `function greet(name) {\n  return 'Hello, ' + name;\n}\n\ngreet('world');`,
  language: 'javascript',
  theme:    'alyx-dark',

  automaticLayout: true,      // resize editor when container resizes
  fontSize:        14,
  fontFamily:      'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace',
  lineHeight:      22,
  minimap:         { enabled: false },
  scrollBeyondLastLine: false,
  renderWhitespace: 'selection',
  smoothScrolling:  true,
  cursorBlinking:   'smooth',
  bracketPairColorization: { enabled: true },
  padding:          { top: 16, bottom: 16 },
  tabSize:          2,
  wordWrap:         'on',
});
```

> **Critical:** always set `automaticLayout: true` so the editor resizes with its container. Without it, the editor renders at the initial size and never adapts to window resizes or layout changes.

---

## Step 5 — Language Support

Monaco includes built-in tokenizers for ~80 languages. The most commonly used in artifacts:

```javascript
// Language IDs — pass as `language` option
'javascript'    // ES + JSX (use 'typescript' for TS/TSX)
'typescript'    // full TS + .tsx support
'python'        // tokenizer only — no IntelliSense by default
'json'          // full validation + schema-aware completion
'markdown'      // GFM-compatible tokenizer
'html'          // tag/attribute autocomplete
'css'           // property validation
'sql'           // standard SQL tokenizer
'yaml'          // tokenizer only
'shell'         // bash tokenizer
'xml'
'go'  'rust'  'java'  'csharp'  'cpp'  'php'  'ruby'
```

### Change language at runtime

```javascript
const model = editor.getModel();
monaco.editor.setModelLanguage(model, 'python');
```

### TypeScript / JavaScript compiler options

```javascript
monaco.languages.typescript.typescriptDefaults.setCompilerOptions({
  target:           monaco.languages.typescript.ScriptTarget.ES2020,
  module:           monaco.languages.typescript.ModuleKind.ESNext,
  jsx:              monaco.languages.typescript.JsxEmit.React,
  allowNonTsExtensions: true,
  noEmit:           true,
  strict:           true,
});

// Add ambient type definitions (turns red squiggles into intellisense)
monaco.languages.typescript.typescriptDefaults.addExtraLib(
  `declare const PI: number; declare function greet(name: string): string;`,
  'ts:filename/globals.d.ts'
);
```

### JSON schema validation

```javascript
monaco.languages.json.jsonDefaults.setDiagnosticsOptions({
  validate: true,
  schemas: [{
    uri:      'inmemory://schema/config.json',
    fileMatch: ['*'],
    schema: {
      type: 'object',
      required: ['name', 'version'],
      properties: {
        name:    { type: 'string' },
        version: { type: 'string', pattern: '^\\d+\\.\\d+\\.\\d+$' },
        enabled: { type: 'boolean' },
      },
    },
  }],
});
```

---

## Step 6 — Decorations (highlight lines, gutters, inline)

Decorations layer visual annotations over the text without changing the underlying value.

```javascript
const decorations = editor.createDecorationsCollection([
  {
    range: new monaco.Range(3, 1, 3, 1),    // line 3 — full line
    options: {
      isWholeLine: true,
      className:        'highlightedLine',
      glyphMarginClassName: 'glyphWarning',
      hoverMessage: { value: 'This line was modified' },
    },
  },
  {
    range: new monaco.Range(5, 1, 5, 10),   // line 5, cols 1–10 — inline
    options: {
      inlineClassName: 'inlineError',
      hoverMessage: { value: '**Error:** undefined identifier' },
    },
  },
]);

// Add matching CSS in <style>:
// .highlightedLine { background: rgba(99,102,241,0.12); }
// .glyphWarning::before { content: '⚠'; color: #eab308; padding-left: 4px; }
// .inlineError { text-decoration: underline wavy #f43f5e; }

// Replace later
decorations.set([ /* new array */ ]);
// Clear
decorations.clear();
```

### Markers (compiler-style error squiggles)

```javascript
monaco.editor.setModelMarkers(editor.getModel(), 'owner', [{
  startLineNumber: 2, startColumn: 5,
  endLineNumber:   2, endColumn:   12,
  message:  'Unexpected token',
  severity: monaco.MarkerSeverity.Error,   // Error | Warning | Info | Hint
}]);
```

---

## Step 7 — Model Events (onChange, onCursor, onSave)

```javascript
// Fired on every text change
editor.onDidChangeModelContent((e) => {
  const value = editor.getValue();
  document.getElementById('charCount').textContent = `${value.length} chars`;
  // e.changes — array of { range, text, rangeOffset, rangeLength }
});

// Cursor moved
editor.onDidChangeCursorPosition((e) => {
  document.getElementById('pos').textContent = `Ln ${e.position.lineNumber}, Col ${e.position.column}`;
});

// Selection changed
editor.onDidChangeCursorSelection((e) => { /* e.selection */ });

// Focus / blur
editor.onDidFocusEditorText(() => {});
editor.onDidBlurEditorText(() => {});

// Custom keybinding — Cmd/Ctrl+S → save
editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
  const value = editor.getValue();
  console.log('Saved', value.length, 'chars');
});

// Programmatic actions
editor.getAction('editor.action.formatDocument').run();
editor.getAction('actions.find').run();
editor.trigger('keyboard', 'editor.action.commentLine', null);
```

---

## Step 8 — Multi-Model Editing (tabs)

Each open "file" is a `model`. The editor can switch between them while preserving cursor and scroll state per model.

```javascript
// Create one model per virtual file
const models = {
  'index.js': monaco.editor.createModel(
    `import { greet } from './util.js';\nconsole.log(greet('world'));`,
    'javascript',
    monaco.Uri.parse('inmemory://app/index.js')
  ),
  'util.js': monaco.editor.createModel(
    `export const greet = (n) => 'Hello, ' + n;`,
    'javascript',
    monaco.Uri.parse('inmemory://app/util.js')
  ),
  'data.json': monaco.editor.createModel(
    `{\n  "name": "demo",\n  "version": "1.0.0"\n}`,
    'json',
    monaco.Uri.parse('inmemory://app/data.json')
  ),
};

// Per-model view state (cursor + scroll position) for each tab
const viewStates = {};
let activeFile = 'index.js';
editor.setModel(models[activeFile]);

function openTab(file) {
  viewStates[activeFile] = editor.saveViewState();
  activeFile = file;
  editor.setModel(models[file]);
  if (viewStates[file]) editor.restoreViewState(viewStates[file]);
  editor.focus();
}

// Wire up tab buttons
document.querySelectorAll('[data-file]').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('[data-file]').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    openTab(tab.dataset.file);
  });
});
```

---

## Step 9 — Diff Editor (side-by-side)

```javascript
const diffContainer = document.getElementById('diff');
const diffEditor = monaco.editor.createDiffEditor(diffContainer, {
  theme:           'alyx-dark',
  automaticLayout: true,
  renderSideBySide: true,    // false → inline diff
  readOnly:        false,
  originalEditable: false,
  fontSize:        13,
  minimap:         { enabled: false },
});

diffEditor.setModel({
  original: monaco.editor.createModel(`const x = 1;\nconsole.log(x);`,            'javascript'),
  modified: monaco.editor.createModel(`const x = 42;\nconsole.log('answer:', x);`, 'javascript'),
});

// Read the modified side
const newValue = diffEditor.getModel().modified.getValue();
```

---

## Step 10 — Design & Polish Guidelines

- **Always set `automaticLayout: true`** — without it, the editor stops resizing with its container after the first paint
- **Provide an explicit height** on the editor container (e.g. `height: 520px`) — Monaco renders 0px in a flex/auto-height parent
- **Disable the minimap by default** (`minimap: { enabled: false }`) — most artifacts are too narrow to benefit and the minimap eats horizontal space
- **Use `bracketPairColorization: { enabled: true }`** for any code-heavy language — a free polish win
- **Wrap long lines** (`wordWrap: 'on'`) in narrow artifacts unless precise column alignment matters
- **Match the page font** in headings but keep `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` for the editor — never sans-serif inside code
- **Keyboard accessibility is built in** — Tab indent, F1 command palette, Cmd/Ctrl+/ comment line. Add a visible hint in the subtitle so users know
- **Screen readers** — `aria-multiline="true"` and an `aria-label` on the container; Monaco itself exposes accessible role information when focused
- **Contrast** — both `alyx-dark` and `alyx-light` themes above hit WCAG AA on body text against their respective backgrounds
- **Dispose properly** — `editor.dispose()` and `model.dispose()` when removing from the DOM, or memory leaks accumulate after repeated mounts

---

## Step 11 — Complete Example: Multi-Tab Playground with Run Button

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JS Playground</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117; color: #e2e8f0;
      display: flex; flex-direction: column; align-items: center;
      min-height: 100vh; padding: 24px;
    }
    .card {
      width: 100%; max-width: 1080px;
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 16px; overflow: hidden;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 20px 24px 14px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;
    }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.78rem; color: #64748b; margin-top: 3px; }
    .actions { display: flex; gap: 8px; }
    .btn {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1);
      color: #e2e8f0; border-radius: 8px;
      padding: 7px 14px; font-size: 12px; font-weight: 500;
      cursor: pointer; transition: all 0.15s;
    }
    .btn:hover  { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.18); }
    .btn:active { transform: scale(0.97); }
    .btn.primary { background: #6366f1; border-color: #6366f1; color: #fff; }
    .btn.primary:hover { background: #5254cc; }

    .tabs {
      display: flex; gap: 2px;
      background: #14171f;
      padding: 6px 12px 0;
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .tab {
      background: transparent; border: none; color: #94a3b8;
      padding: 8px 14px; font-size: 12px; font-family: inherit;
      border-radius: 8px 8px 0 0; cursor: pointer;
      transition: all 0.15s;
    }
    .tab:hover { background: rgba(255,255,255,0.04); color: #e2e8f0; }
    .tab.active {
      background: #1a1d27; color: #f1f5f9;
      box-shadow: inset 0 2px 0 #6366f1;
    }

    #editor { width: 100%; height: 420px; }

    .console {
      background: #0b0d12;
      border-top: 1px solid rgba(255,255,255,0.07);
      padding: 14px 20px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12.5px; line-height: 1.55;
      color: #94a3b8;
      max-height: 180px; overflow-y: auto;
    }
    .console .line       { white-space: pre-wrap; }
    .console .line.error { color: #f87171; }
    .console .line.info  { color: #a5b4fc; }

    .status {
      display: flex; justify-content: space-between;
      padding: 8px 20px; font-size: 11px; color: #64748b;
      background: #14171f; border-top: 1px solid rgba(255,255,255,0.05);
      font-variant-numeric: tabular-nums;
    }
  </style>
</head>
<body>
  <main class="card" aria-labelledby="title">
    <header class="card-header">
      <div>
        <h1 id="title">JavaScript Playground</h1>
        <p class="sub">Edit any tab · Cmd/Ctrl+Enter to run · Cmd/Ctrl+S to save · Alt-click for multi-cursor</p>
      </div>
      <div class="actions">
        <button class="btn" id="themeBtn" aria-pressed="false">Light theme</button>
        <button class="btn" id="formatBtn">Format</button>
        <button class="btn primary" id="runBtn">Run ▶</button>
      </div>
    </header>

    <div class="tabs" role="tablist" aria-label="Open files">
      <button class="tab active" role="tab" data-file="main.js"  aria-selected="true">main.js</button>
      <button class="tab"        role="tab" data-file="utils.js" aria-selected="false">utils.js</button>
      <button class="tab"        role="tab" data-file="config.json" aria-selected="false">config.json</button>
    </div>

    <div id="editor" role="textbox" aria-multiline="true" aria-label="Code editor"></div>

    <div class="console" id="console" aria-live="polite" aria-label="Output console">
      <div class="line info">// Output will appear here. Click Run ▶ to execute.</div>
    </div>

    <div class="status">
      <span id="pos">Ln 1, Col 1</span>
      <span id="meta">main.js · javascript</span>
    </div>
  </main>

  <script src="https://unpkg.com/monaco-editor@0.45/min/vs/loader.js"></script>
  <script>
    require.config({ paths: { vs: 'https://unpkg.com/monaco-editor@0.45/min/vs' } });

    window.MonacoEnvironment = {
      getWorkerUrl: () => URL.createObjectURL(new Blob([`
        self.MonacoEnvironment = { baseUrl: 'https://unpkg.com/monaco-editor@0.45/min/' };
        importScripts('https://unpkg.com/monaco-editor@0.45/min/vs/base/worker/workerMain.js');
      `], { type: 'text/javascript' })),
    };

    require(['vs/editor/editor.main'], () => {
      // Themes
      monaco.editor.defineTheme('alyx-dark', {
        base: 'vs-dark', inherit: true,
        rules: [
          { token: 'comment',  foreground: '64748b', fontStyle: 'italic' },
          { token: 'keyword',  foreground: '818cf8' },
          { token: 'string',   foreground: '22c55e' },
          { token: 'number',   foreground: 'f97316' },
          { token: 'function', foreground: 'ec4899' },
        ],
        colors: {
          'editor.background':              '#1a1d27',
          'editor.foreground':              '#e2e8f0',
          'editorLineNumber.foreground':    '#475569',
          'editorLineNumber.activeForeground': '#94a3b8',
          'editor.lineHighlightBackground': '#22273366',
          'editorCursor.foreground':        '#6366f1',
          'editor.selectionBackground':     '#6366f155',
        },
      });
      monaco.editor.defineTheme('alyx-light', {
        base: 'vs', inherit: true,
        rules: [
          { token: 'comment', foreground: '94a3b8', fontStyle: 'italic' },
          { token: 'keyword', foreground: '6366f1' },
          { token: 'string',  foreground: '15803d' },
          { token: 'number',  foreground: 'c2410c' },
          { token: 'function',foreground: 'be185d' },
        ],
        colors: {
          'editor.background':              '#ffffff',
          'editor.foreground':              '#1e293b',
          'editorLineNumber.foreground':    '#94a3b8',
          'editor.lineHighlightBackground': '#f1f5f9',
          'editorCursor.foreground':        '#6366f1',
        },
      });

      // Files
      const files = {
        'main.js': monaco.editor.createModel(
          `import { greet, sum } from './utils.js';\n\n` +
          `console.log(greet('Alyx'));\n` +
          `console.log('1 + 2 + 3 =', sum(1, 2, 3));`,
          'javascript', monaco.Uri.parse('inmemory://app/main.js')),
        'utils.js': monaco.editor.createModel(
          `export const greet = (name) => 'Hello, ' + name + '!';\n` +
          `export const sum   = (...n) => n.reduce((a, b) => a + b, 0);`,
          'javascript', monaco.Uri.parse('inmemory://app/utils.js')),
        'config.json': monaco.editor.createModel(
          `{\n  "name": "playground",\n  "version": "1.0.0",\n  "enabled": true\n}`,
          'json', monaco.Uri.parse('inmemory://app/config.json')),
      };

      monaco.languages.json.jsonDefaults.setDiagnosticsOptions({
        validate: true,
        schemas: [{
          uri: 'inmemory://schema/config.json',
          fileMatch: ['*config.json'],
          schema: {
            type: 'object', required: ['name', 'version'],
            properties: {
              name:    { type: 'string' },
              version: { type: 'string', pattern: '^\\d+\\.\\d+\\.\\d+$' },
              enabled: { type: 'boolean' },
            },
          },
        }],
      });

      const editor = monaco.editor.create(document.getElementById('editor'), {
        model: files['main.js'],
        theme: 'alyx-dark',
        automaticLayout: true,
        fontSize: 14,
        fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace',
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        bracketPairColorization: { enabled: true },
        padding: { top: 14, bottom: 14 },
        tabSize: 2,
        wordWrap: 'on',
      });

      // Tabs + per-model view state
      const viewStates = {};
      let activeFile = 'main.js';
      function openTab(file) {
        viewStates[activeFile] = editor.saveViewState();
        activeFile = file;
        editor.setModel(files[file]);
        if (viewStates[file]) editor.restoreViewState(viewStates[file]);
        const lang = files[file].getLanguageId();
        document.getElementById('meta').textContent = `${file} · ${lang}`;
        editor.focus();
      }
      document.querySelectorAll('[data-file]').forEach(tab => {
        tab.addEventListener('click', () => {
          document.querySelectorAll('[data-file]').forEach(t => {
            t.classList.remove('active'); t.setAttribute('aria-selected', 'false');
          });
          tab.classList.add('active'); tab.setAttribute('aria-selected', 'true');
          openTab(tab.dataset.file);
        });
      });

      // Cursor status
      editor.onDidChangeCursorPosition(e => {
        document.getElementById('pos').textContent =
          `Ln ${e.position.lineNumber}, Col ${e.position.column}`;
      });

      // Console helpers
      const consoleEl = document.getElementById('console');
      function log(msg, kind = '') {
        const line = document.createElement('div');
        line.className = 'line ' + kind;
        line.textContent = typeof msg === 'string' ? msg : JSON.stringify(msg, null, 2);
        consoleEl.appendChild(line);
        consoleEl.scrollTop = consoleEl.scrollHeight;
      }

      // Run button — evaluates main.js + utils.js together (toy bundler)
      function run() {
        consoleEl.innerHTML = '';
        log('// Running…', 'info');
        try {
          const utils = files['utils.js'].getValue()
            .replace(/export\s+const\s+/g, 'const ');
          const main  = files['main.js'].getValue()
            .replace(/^\s*import[^;]+;\s*\n/m, '');
          const captured = [];
          const fakeConsole = { log: (...a) => captured.push(a.map(String).join(' ')) };
          new Function('console', utils + '\n' + main)(fakeConsole);
          captured.forEach(line => log(line));
          log(`// Done in ${performance.now().toFixed(1)} ms`, 'info');
        } catch (err) {
          log('Error: ' + err.message, 'error');
        }
      }
      document.getElementById('runBtn').addEventListener('click', run);
      editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, run);
      editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => log('// Saved', 'info'));

      document.getElementById('formatBtn').addEventListener('click', () => {
        editor.getAction('editor.action.formatDocument').run();
      });

      // Theme toggle
      let dark = true;
      const themeBtn = document.getElementById('themeBtn');
      themeBtn.addEventListener('click', () => {
        dark = !dark;
        monaco.editor.setTheme(dark ? 'alyx-dark' : 'alyx-light');
        document.body.style.background = dark ? '#0f1117' : '#f8fafc';
        document.body.style.color      = dark ? '#e2e8f0' : '#1e293b';
        themeBtn.textContent = dark ? 'Light theme' : 'Dark theme';
        themeBtn.setAttribute('aria-pressed', String(!dark));
      });
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Forgetting the `MonacoEnvironment.getWorkerUrl` shim** — language workers fail silently; IntelliSense, validation, and formatting all break
- **No explicit height on the editor container** — Monaco renders at 0×0 inside flex/auto-height parents and the editor appears blank
- **Omitting `automaticLayout: true`** — the editor renders at initial size and never resizes with the window or its container
- **Using `vs/loader.js` from one version with `vs/editor/editor.main` from another** — always pin the same version (`@0.45`) in every URL
- **Creating a new editor on the same container without disposing** — call `editor.dispose()` first or you leak DOM and memory
- **Calling `monaco.editor.setModel(editor, null)` then expecting tab state** — view state is per-model; save with `editor.saveViewState()` before switching, restore with `editor.restoreViewState()` after
- **Inline `<script type="module">` to load Monaco** — Monaco is AMD, not ESM. Use the AMD loader as shown, not `import`
- **Setting `theme` before `defineTheme`** — `defineTheme` must run before any `create()` call that references the custom theme name
- **JSON schema using `fileMatch: ['*.json']`** — `fileMatch` checks the model URI, not extension globs. Use the literal filename pattern (e.g. `'*config.json'`) and create models with `monaco.Uri.parse('inmemory://app/config.json')`
- **Relying on `localStorage` to persist code** — artifacts run in a sandbox where storage may be blocked. Keep state in JS variables
