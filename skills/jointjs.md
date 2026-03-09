---
name: jointjs-flowchart
description: Create interactive, editable flowcharts and diagrams using JointJS, delivered as self-contained HTML artifacts. Use this skill whenever someone needs draggable nodes, editable connections, port-based linking, custom shapes, or any interactive diagram that users can manipulate — process flows, BPMN workflows, architecture diagrams, data pipelines, decision trees, or whiteboard-style editable diagrams. Trigger on requests like "make an editable flowchart", "create a draggable diagram", "build a visual workflow editor", "design a pipeline builder", or any prompt where the user should be able to drag, connect, and rearrange nodes. Do NOT use for static diagrams (→ mermaid-diagrams skill), network graphs with physics layout (→ vis-network skill), or data charts (→ chartjs / plotly skill).
---

# JointJS Flowchart Skill

JointJS is an open-source JavaScript library for creating interactive diagrams and flowcharts. It provides a Paper (SVG canvas) and a Graph (data model) with built-in support for draggable elements, link routing, ports, custom shapes, undo/redo, serialization, and event handling. Elements and links are fully customizable via SVG markup.

---

## Artifact Presentation & Use Cases

Every JointJS artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the diagram
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the diagram
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context and interaction hints
- **Paper container** (`<div id="paper">`, explicit height) renders the interactive SVG diagram
- **Optional sidebar** with a palette of draggable shape types

### Typical use cases

- **Process flows** — business workflows, approval chains, onboarding steps
- **Architecture diagrams** — microservices, infrastructure, deployment topologies (editable)
- **Data pipelines** — ETL flows, data processing stages with port-based connections
- **Decision trees** — interactive branching logic with yes/no paths
- **BPMN workflows** — swimlanes, gateways, tasks, events
- **Whiteboard editors** — freeform diagram builders where users create and connect shapes

### What the user sees

An interactive diagram editor: drag shapes to reposition, click and drag between ports to create connections, double-click to edit labels. Links route around obstacles automatically. The SVG-based rendering is crisp at any zoom level.

---

## When to Use JointJS vs. Alternatives

| Use JointJS when… | Use another tool when… |
|---|---|
| Users need to drag, edit, and connect nodes | Static, read-only diagrams → **Mermaid** |
| Port-based connections (input/output ports) | Physics-based auto-layout of networks → **vis-network** |
| Custom shapes with SVG markup | Data charts (bar, line, pie) → **Chart.js / Plotly** |
| Link routing with obstacles/vertices | Geographic maps → **Leaflet** |
| Serialization to/from JSON | Timeline/Gantt views → **vis-timeline** |
| Undo/redo support | DOM/SVG animations → **Anime.js / GSAP** |

> **Rule of thumb:** if the user should be able to build or edit a diagram by dragging and connecting shapes, use JointJS. If the diagram is generated from text and read-only, use Mermaid. If the graph needs physics simulation, use vis-network.

---

## Step 1 — CDN Setup

```html
<!-- JointJS (includes Backbone and jQuery dependencies) -->
<script src="https://cdn.jsdelivr.net/npm/@joint/core/dist/joint.js"></script>
```

> JointJS bundles its own CSS. The `joint.js` file includes everything needed — no separate CSS file required for basic usage.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flowchart Editor</title>
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
      max-width: 1100px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
    #paper {
      width: 100%;
      height: 500px;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      overflow: hidden;
      background: #0f1117;
    }

    /* Dark theme for JointJS elements */
    .joint-element .body { stroke: rgba(255,255,255,0.15); }
    .joint-link .connection { stroke: #64748b; }
    .joint-link .marker-target { fill: #64748b; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Flowchart Title</h1>
    <p class="sub">Drag elements to reposition · click + drag ports to connect</p>
    <div id="paper"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/@joint/core/dist/joint.js"></script>
  <script>
    // All JointJS code here
  </script>
</body>
</html>
```

---

## Step 3 — Dark Theme Reference

JointJS renders SVG elements. Theme them via `attrs` on each shape:

```javascript
// Dark shape defaults
const DARK_ATTRS = {
  body: {
    fill: '#1e2130',
    stroke: 'rgba(255,255,255,0.15)',
    strokeWidth: 1.5,
    rx: 8,
    ry: 8,
  },
  label: {
    fill: '#f1f5f9',
    fontSize: 13,
    fontFamily: 'Segoe UI, system-ui, sans-serif',
    fontWeight: 500,
    textVerticalAnchor: 'middle',
    textAnchor: 'middle',
  },
};

// Dark link defaults
const DARK_LINK_ATTRS = {
  line: {
    stroke: '#64748b',
    strokeWidth: 2,
    targetMarker: { type: 'path', fill: '#64748b', d: 'M 10 -5 0 0 10 5 Z' },
  },
};
```

---

## Step 4 — Minimal Setup

```javascript
const { dia, shapes } = joint;

// 1. Create the graph (data model)
const graph = new dia.Graph();

// 2. Create the paper (SVG view) — attach to #paper div
const paper = new dia.Paper({
  el: document.getElementById('paper'),
  model: graph,
  width: '100%',
  height: '100%',
  gridSize: 16,
  background: { color: '#0f1117' },
  defaultLink: () => new shapes.standard.Link({
    attrs: { line: { stroke: '#64748b', strokeWidth: 2, targetMarker: { fill: '#64748b' } } },
  }),
  linkPinning: false,       // links must connect to elements
  defaultConnectionPoint: { name: 'boundary' },
  defaultRouter: { name: 'manhattan' },   // orthogonal link routing
  defaultConnector: { name: 'rounded', args: { radius: 8 } },
  interactive: { linkMove: true },
});

// 3. Add elements
const rect1 = new shapes.standard.Rectangle({
  position: { x: 100, y: 100 },
  size: { width: 160, height: 60 },
  attrs: {
    body: { fill: '#1e2130', stroke: 'rgba(255,255,255,0.15)', rx: 8, ry: 8 },
    label: { text: 'Start', fill: '#f1f5f9', fontSize: 13 },
  },
});

const rect2 = rect1.clone().position(400, 100).attr('label/text', 'Process');
const rect3 = rect1.clone().position(400, 250).attr('label/text', 'End');

graph.addCells([rect1, rect2, rect3]);

// 4. Add links
const link1 = new shapes.standard.Link({
  source: { id: rect1.id },
  target: { id: rect2.id },
  attrs: { line: { stroke: '#6366f1', strokeWidth: 2, targetMarker: { fill: '#6366f1' } } },
});

const link2 = new shapes.standard.Link({
  source: { id: rect2.id },
  target: { id: rect3.id },
  attrs: { line: { stroke: '#6366f1', strokeWidth: 2, targetMarker: { fill: '#6366f1' } } },
});

graph.addCells([link1, link2]);
```

---

## Step 5 — Built-in Shapes

```javascript
// Rectangle
new shapes.standard.Rectangle({ size: { width: 160, height: 60 }, attrs: { body: {}, label: { text: 'Box' } } })

// Circle
new shapes.standard.Circle({ size: { width: 60, height: 60 }, attrs: { body: {}, label: { text: 'C' } } })

// Ellipse
new shapes.standard.Ellipse({ size: { width: 140, height: 60 }, attrs: { body: {}, label: { text: 'Decision' } } })

// Cylinder (database)
new shapes.standard.Cylinder({ size: { width: 80, height: 80 }, attrs: { body: {}, label: { text: 'DB' } } })

// Image (icon node)
new shapes.standard.Image({ size: { width: 60, height: 60 }, attrs: { image: { xlinkHref: 'url' } } })

// Embedded HTML
new shapes.standard.HeaderedRectangle({
  size: { width: 200, height: 100 },
  attrs: {
    header: { fill: '#6366f1', stroke: 'none' },
    headerText: { text: 'Header', fill: '#fff', fontSize: 12 },
    body: { fill: '#1e2130', stroke: 'rgba(255,255,255,0.15)' },
    bodyText: { text: 'Content', fill: '#e2e8f0', fontSize: 11 },
  },
})
```

---

## Step 6 — Ports (Connection Points)

```javascript
const element = new shapes.standard.Rectangle({
  position: { x: 200, y: 100 },
  size: { width: 160, height: 60 },
  attrs: {
    body: { fill: '#1e2130', stroke: 'rgba(255,255,255,0.15)', rx: 8, ry: 8 },
    label: { text: 'Node', fill: '#f1f5f9' },
  },
  ports: {
    groups: {
      in: {
        position: 'left',
        attrs: { circle: { r: 6, fill: '#22c55e', stroke: '#0f1117', strokeWidth: 2, magnet: true } },
      },
      out: {
        position: 'right',
        attrs: { circle: { r: 6, fill: '#6366f1', stroke: '#0f1117', strokeWidth: 2, magnet: true } },
      },
    },
    items: [
      { group: 'in', id: 'in1' },
      { group: 'out', id: 'out1' },
      { group: 'out', id: 'out2' },
    ],
  },
});
```

> With `magnet: true`, users can drag from ports to create new links.

---

## Step 7 — Link Configuration

```javascript
const link = new shapes.standard.Link({
  source: { id: element1.id, port: 'out1' },
  target: { id: element2.id, port: 'in1' },
  attrs: {
    line: {
      stroke: '#6366f1',
      strokeWidth: 2,
      strokeDasharray: '5,5',      // dashed line
      targetMarker: { type: 'path', fill: '#6366f1', d: 'M 10 -5 0 0 10 5 Z' },
    },
  },
  labels: [{
    position: 0.5,
    attrs: {
      text: { text: 'yes', fill: '#94a3b8', fontSize: 11 },
      rect: { fill: '#1a1d27', stroke: 'none', rx: 4, ry: 4 },
    },
  }],
  router: { name: 'manhattan' },      // orthogonal routing
  connector: { name: 'rounded', args: { radius: 8 } },
});
```

### Router types
```javascript
{ name: 'normal' }       // straight line
{ name: 'manhattan' }    // orthogonal (right angles)
{ name: 'metro' }        // rounded orthogonal
{ name: 'orthogonal' }   // like manhattan with more options
```

---

## Step 8 — Events & Interaction

```javascript
// Click on element
paper.on('element:pointerclick', (elementView) => {
  const model = elementView.model;
  console.log('Clicked:', model.attr('label/text'));
});

// Double-click to edit label
paper.on('element:pointerdblclick', (elementView) => {
  const model = elementView.model;
  const newLabel = prompt('Enter label:', model.attr('label/text'));
  if (newLabel !== null) model.attr('label/text', newLabel);
});

// Click on link
paper.on('link:pointerclick', (linkView) => {
  linkView.model.remove();  // click to delete link
});

// Blank area click (deselect)
paper.on('blank:pointerclick', () => {
  // deselect all
});

// Element position change
graph.on('change:position', (cell) => {
  console.log('Moved:', cell.id, cell.position());
});

// Link connected
graph.on('change:target', (link) => {
  if (link.getTargetCell()) {
    console.log('Connected:', link.getSourceCell()?.id, '→', link.getTargetCell()?.id);
  }
});
```

---

## Step 9 — Serialization (Save/Load)

```javascript
// Export to JSON
const json = graph.toJSON();
const jsonString = JSON.stringify(json, null, 2);

// Import from JSON
graph.fromJSON(JSON.parse(jsonString));

// Clear graph
graph.clear();
```

---

## Step 10 — Pan & Zoom

```javascript
// Enable paper panning (drag on blank area)
paper.on('blank:pointerdown', (evt, x, y) => {
  const scale = paper.scale();
  const startX = evt.clientX;
  const startY = evt.clientY;
  const translate = paper.translate();

  const onMouseMove = (e) => {
    paper.translate(
      translate.tx + (e.clientX - startX),
      translate.ty + (e.clientY - startY)
    );
  };
  const onMouseUp = () => {
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
  };
  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
});

// Zoom with scroll wheel
paper.el.addEventListener('wheel', (e) => {
  e.preventDefault();
  const currentScale = paper.scale().sx;
  const delta = e.deltaY > 0 ? -0.1 : 0.1;
  const newScale = Math.max(0.3, Math.min(3, currentScale + delta));
  paper.scale(newScale, newScale);
}, { passive: false });
```

---

## Step 11 — Design & Polish Guidelines

- **Dark Paper background** — set `background: { color: '#0f1117' }` on the Paper for seamless dark theme
- **Consistent shape styling** — define a `DARK_ATTRS` object and spread it into every element's `attrs` for uniform appearance
- **Port colors** — use green (`#22c55e`) for inputs, indigo (`#6366f1`) for outputs; outline with body background color for clean separation
- **Link routing** — `manhattan` router produces clean right-angle connections; `rounded` connector with `radius: 8` softens corners
- **Grid snap** — `gridSize: 16` keeps elements aligned on an invisible grid
- **Link pinning** — set `linkPinning: false` so dangling links (not connected to anything) are automatically removed
- **Double-click editing** — implement label editing via `element:pointerdblclick` for a whiteboard-like experience
- **Selection highlight** — on `element:pointerclick`, add a colored stroke or glow to indicate selection; clear on `blank:pointerclick`
- **Responsive** — `width: '100%'` on the Paper; use CSS to control the container's height
- **Export** — add an "Export JSON" button using `graph.toJSON()` for persistence

---

## Step 12 — Complete Example: Process Flow Editor

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Process Flow Editor</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 28px; width: 100%; max-width: 1000px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 16px; }
    .toolbar { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
    .toolbar button { background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 6px 14px; font-size: 12px; cursor: pointer; transition: all 0.15s; }
    .toolbar button:hover { background: rgba(255,255,255,0.1); color: #f1f5f9; }
    #paper { width: 100%; height: 450px; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; overflow: hidden; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Process Flow Editor</h1>
    <p class="sub">Drag nodes to reposition · drag from ports (●) to connect · double-click to edit labels</p>
    <div class="toolbar">
      <button id="btn-add">+ Add Node</button>
      <button id="btn-export">Export JSON</button>
      <button id="btn-clear">Clear All</button>
    </div>
    <div id="paper"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/@joint/core/dist/joint.js"></script>
  <script>
    const { dia, shapes } = joint;
    const COLORS = ['#6366f1','#8b5cf6','#ec4899','#22c55e','#06b6d4','#f97316'];

    const graph = new dia.Graph();
    const paper = new dia.Paper({
      el: document.getElementById('paper'),
      model: graph,
      width: '100%',
      height: '100%',
      gridSize: 16,
      background: { color: '#0f1117' },
      defaultLink: () => new shapes.standard.Link({
        attrs: { line: { stroke: '#6366f1', strokeWidth: 2, targetMarker: { fill: '#6366f1' } } },
        router: { name: 'manhattan' },
        connector: { name: 'rounded', args: { radius: 8 } },
      }),
      linkPinning: false,
      defaultConnectionPoint: { name: 'boundary' },
      interactive: { linkMove: true },
    });

    function createNode(x, y, label, color) {
      return new shapes.standard.Rectangle({
        position: { x, y },
        size: { width: 160, height: 56 },
        attrs: {
          body: { fill: '#1e2130', stroke: color || '#6366f1', strokeWidth: 2, rx: 10, ry: 10 },
          label: { text: label, fill: '#f1f5f9', fontSize: 13, fontFamily: 'Segoe UI, sans-serif' },
        },
        ports: {
          groups: {
            in:  { position: 'left',  attrs: { circle: { r: 5, fill: '#22c55e', stroke: '#0f1117', strokeWidth: 2, magnet: true } } },
            out: { position: 'right', attrs: { circle: { r: 5, fill: '#6366f1', stroke: '#0f1117', strokeWidth: 2, magnet: true } } },
          },
          items: [{ group: 'in', id: 'in1' }, { group: 'out', id: 'out1' }],
        },
      });
    }

    // Initial flow
    const n1 = createNode(80, 80, 'User Request', '#6366f1');
    const n2 = createNode(340, 80, 'Validate Input', '#8b5cf6');
    const n3 = createNode(340, 220, 'Process Data', '#ec4899');
    const n4 = createNode(600, 150, 'Return Result', '#22c55e');
    graph.addCells([n1, n2, n3, n4]);

    function link(src, tgt) {
      return new shapes.standard.Link({
        source: { id: src.id, port: 'out1' }, target: { id: tgt.id, port: 'in1' },
        attrs: { line: { stroke: '#6366f1', strokeWidth: 2, targetMarker: { fill: '#6366f1' } } },
        router: { name: 'manhattan' }, connector: { name: 'rounded', args: { radius: 8 } },
      });
    }
    graph.addCells([link(n1, n2), link(n2, n3), link(n3, n4)]);

    // Double-click to edit
    paper.on('element:pointerdblclick', (view) => {
      const lbl = prompt('Label:', view.model.attr('label/text'));
      if (lbl !== null) view.model.attr('label/text', lbl);
    });

    // Toolbar
    let nodeCount = 4;
    document.getElementById('btn-add').addEventListener('click', () => {
      const c = COLORS[nodeCount % COLORS.length];
      graph.addCell(createNode(160 + Math.random()*200, 100 + Math.random()*200, 'New Node ' + (++nodeCount), c));
    });
    document.getElementById('btn-export').addEventListener('click', () => {
      const json = JSON.stringify(graph.toJSON(), null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'flowchart.json'; a.click();
    });
    document.getElementById('btn-clear').addEventListener('click', () => { if (confirm('Clear all?')) graph.clear(); });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Missing explicit height on `#paper`** — JointJS Paper renders as zero-height without it; always set a CSS height (e.g., `500px`)
- **Forgetting `linkPinning: false`** — without it, users can drop links on blank areas creating dangling connections
- **No `magnet: true` on ports** — ports won't be interactive (draggable link sources) without `magnet: true`
- **Creating links without router** — links without a router follow straight paths through elements; always use `manhattan` or `orthogonal`
- **Wrong target marker syntax** — `targetMarker` is an object with `type`, `fill`, and `d` (SVG path) — not a CSS property
- **Not handling `change:target`** — when a link is reconnected, validate the new connection to prevent invalid flows
- **Global `joint` object** — the CDN build exposes `joint` globally; destructure `const { dia, shapes } = joint;` at the top of your script
- **SVG vs CSS** — JointJS elements are SVG, not DOM; use `attrs` (SVG attributes) not CSS properties for styling shapes
