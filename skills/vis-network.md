---
name: vis-network
description: Create interactive network and graph visualizations using vis-network, delivered as self-contained HTML artifacts. Use this skill whenever someone needs to display nodes and edges, relationship graphs, dependency trees, organizational charts, knowledge graphs, flow diagrams, social networks, infrastructure maps, or any visualization where entities are connected by links. Trigger on requests mentioning network graphs, node-link diagrams, force-directed graphs, topology maps, relationship maps, org charts, or any mention of "nodes and edges". Prefer this skill for its built-in physics engine, clustering, and rich interaction over D3 force simulations when ease of use matters more than pixel-level customization.
---

# vis-network Skill

vis-network renders interactive node-edge graphs on an HTML Canvas using a built-in physics engine for automatic layout. It supports custom node shapes, edge arrows, clustering, hierarchical layout, drag-and-drop manipulation, and zoom/pan — all with minimal setup.

---

## Artifact Presentation & Use Cases

Every vis-network artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the network graph
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the network
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context and interaction hints
- **Canvas container** (`#network`, fixed height) renders the interactive graph with physics simulation
- **Optional legend** showing node type colors and edge meanings

### Typical use cases

- **Infrastructure maps** — servers, databases, services, and their connections
- **Dependency graphs** — package dependencies, module imports, build pipelines
- **Organizational charts** — hierarchical reporting structures with role information
- **Knowledge graphs** — concept maps, topic relationships, entity connections
- **Social networks** — user connections, interaction patterns, community clusters
- **Flow diagrams** — process flows with directed edges showing data/control flow

### What the user sees

An interactive graph: drag nodes to rearrange, scroll to zoom, hover for tooltips, click to select. The physics engine auto-positions nodes with spring-like forces. Nodes settle into a balanced layout after a brief stabilization animation.

---

## When to Use vis-network vs. Alternatives

| Use vis-network when… | Use another tool when… |
|---|---|
| Interactive node-edge graphs | Static flowcharts, sequence diagrams → **Mermaid** |
| Built-in physics engine for auto-layout | Pixel-perfect custom SVG network layouts → **D3** (force simulation) |
| Drag-and-drop node manipulation | Geographic maps with tiles and markers → **Leaflet** |
| Hierarchical tree/DAG layouts | Data charts (bar, line, pie) → **Chart.js / Plotly** |
| Clustering large graphs (100+ nodes) | Timeline-based views → **vis-timeline** |
| Quick setup, minimal code | Complex SVG animations → **Anime.js + D3** |

> **Rule of thumb:** if the data is nodes connected by edges and users need to interact (drag, zoom, click), vis-network is the simplest and most feature-rich option. For static diagrams, use Mermaid.

---

## Step 1 — CDN Setup (Standalone Build — one file, self-contained)

```html
<!-- Standalone: CSS is auto-injected — only one script tag needed -->
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
```

The standalone build bundles all dependencies and auto-injects its CSS. Use it for all single-file artifacts. The `vis` global is available after loading.

> **Note:** unlike vis-timeline, vis-network's standalone build does **not** require a separate CSS `<link>`. The styles are injected programmatically.

---

## Step 2 — HTML Artifact Shell

The network container **must have an explicit width and height** — it renders on a Canvas.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Network Graph</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 24px;
    }
    .card {
      background: #1a1d27;
      border-radius: 16px;
      padding: 32px;
      width: 100%;
      max-width: 900px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }

    /* Canvas container: MUST have explicit width + height */
    #network {
      width: 100%;
      height: 520px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,0.08);
      background: #161923;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Network Graph</h1>
    <p class="sub">Drag nodes · Scroll to zoom · Click to select</p>
    <div id="network"></div>
  </div>
  <script>
    // All vis-network code here
  </script>
</body>
</html>
```

---

## Step 3 — Data Format

### Nodes

```javascript
const nodes = new vis.DataSet([
  // Minimal node
  { id: 1, label: 'Node A' },

  // Full example
  {
    id: 2,
    label:   'Server\n(prod)',       // \n creates line break in label
    title:   'Tooltip HTML or text', // shown on hover
    group:   'servers',              // maps to groups options
    shape:   'box',                  // see shapes below
    size:    30,                     // only for circle/dot/diamond/star/triangle etc.
    color: {
      border:     '#6366f1',
      background: 'rgba(99,102,241,0.25)',
      highlight:  { border: '#818cf8', background: 'rgba(99,102,241,0.5)' },
      hover:      { border: '#818cf8', background: 'rgba(99,102,241,0.35)' },
    },
    font:    { color: '#e2e8f0', size: 14, face: 'Segoe UI' },
    borderWidth: 2,
    borderWidthSelected: 3,
    shadow:  { enabled: true, color: 'rgba(99,102,241,0.4)', size: 10, x: 0, y: 0 },
    x: 100, y: 50,                   // fixed position (disables physics for this node)
    fixed: { x: true, y: false },    // lock one axis only
    hidden: false,
    physics: true,                   // false = no physics force applied to this node
    mass: 1,                         // higher = harder to move
  },

  // Image node
  { id: 3, label: 'DB', shape: 'image', image: 'https://example.com/db-icon.png', size: 40 },

  // Icon node (requires FontAwesome loaded separately)
  { id: 4, shape: 'icon', icon: { face: 'FontAwesome', code: '\uf007', size: 40, color: '#6366f1' }, label: 'User' },
]);
```

**Node shapes reference:**

| Shape       | Description                                  |
|-------------|----------------------------------------------|
| `'ellipse'` | Default oval (label inside)                  |
| `'circle'`  | Perfect circle (label inside, size by label) |
| `'dot'`     | Small circle (label below, `size` controls radius) |
| `'box'`     | Rectangle (label inside)                     |
| `'diamond'` | Diamond (label below)                        |
| `'star'`    | Star (label below)                           |
| `'triangle'`| Triangle (label below)                       |
| `'triangleDown'` | Inverted triangle                       |
| `'hexagon'` | Hexagon (label below)                        |
| `'square'`  | Square (label below)                         |
| `'image'`   | External image (requires `image` property)   |
| `'circularImage'` | Image cropped to circle                |
| `'icon'`    | Icon font glyph (requires `icon` property)   |
| `'text'`    | Label only, no shape                         |

### Edges

```javascript
const edges = new vis.DataSet([
  // Minimal edge
  { from: 1, to: 2 },

  // Full example
  {
    id:     'e1',
    from:   1,
    to:     3,
    label:  'calls',
    title:  'Tooltip for this edge',
    arrows: { to: { enabled: true, type: 'arrow' } },    // arrow at target
    // arrows: 'to'  ← shorthand string
    // arrows: { from: { enabled: true }, to: { enabled: true } }  ← bidirectional

    color:  { color: 'rgba(99,102,241,0.5)', highlight: '#6366f1', hover: '#818cf8', opacity: 1 },
    width:  2,
    dashes: false,        // true | false | [5, 5] custom dash pattern
    smooth: { type: 'curvedCW', roundness: 0.2 },  // see smooth types below
    font:   { color: '#94a3b8', size: 11, align: 'middle' },
    hidden: false,
    physics: true,
    length: 150,          // preferred spring length (physics)
    selectionWidth: 3,    // extra width when selected
  },
]);
```

**Edge smooth types:**

| `smooth.type`   | Description                           |
|-----------------|---------------------------------------|
| `'dynamic'`     | Default — curve adapts to graph layout |
| `'continuous'   | Simple curve                          |
| `'discrete'`    | Straight with one bend                |
| `'diagonalCross'` | Diagonal                            |
| `'straightCross'` | Straight                            |
| `'horizontal'`  | Always horizontal curve               |
| `'vertical'`    | Always vertical curve                 |
| `'curvedCW'`    | Clockwise curve (good for directed)   |
| `'curvedCCW'`   | Counter-clockwise curve               |
| `'cubicBezier'` | Full Bezier control                   |

---

## Step 4 — Constructor

```javascript
const container = document.getElementById('network');
const data      = { nodes, edges };
const network   = new vis.Network(container, data, options);
```

---

## Step 5 — Key Configuration Options

```javascript
const options = {
  autoResize: true,
  width:  '100%',
  height: '100%',   // fills the container div

  // ── Nodes (global defaults) ───────────────────────────────
  nodes: {
    shape:          'dot',
    size:           18,
    color: {
      border:     '#6366f1',
      background: 'rgba(99,102,241,0.3)',
      highlight:  { border: '#818cf8', background: 'rgba(99,102,241,0.55)' },
      hover:      { border: '#818cf8', background: 'rgba(99,102,241,0.4)' },
    },
    font:           { color: '#e2e8f0', size: 13, face: 'Segoe UI' },
    borderWidth:    2,
    shadow:         { enabled: true, color: 'rgba(0,0,0,0.4)', size: 8 },
  },

  // ── Edges (global defaults) ───────────────────────────────
  edges: {
    color:          { color: 'rgba(148,163,184,0.3)', highlight: '#94a3b8', hover: '#94a3b8' },
    width:          1.5,
    smooth:         { type: 'dynamic' },
    arrows:         { to: { enabled: false } },
    font:           { color: '#64748b', size: 11, align: 'middle' },
    selectionWidth: 3,
    hoverWidth:     2,
  },

  // ── Groups (per-group style presets) ────────────────────────
  groups: {
    servers:  { shape: 'box',     color: { background: 'rgba(99,102,241,0.25)', border: '#6366f1' }, font: { color: '#a5b4fc' } },
    clients:  { shape: 'dot',     color: { background: 'rgba(34,197,94,0.25)',  border: '#22c55e' }, font: { color: '#86efac' } },
    database: { shape: 'diamond', color: { background: 'rgba(234,179,8,0.25)', border: '#eab308' }, font: { color: '#fef08a' } },
  },

  // ── Physics engine ────────────────────────────────────────
  physics: {
    enabled:       true,
    solver:        'barnesHut',      // 'barnesHut' | 'repulsion' | 'hierarchicalRepulsion' | 'forceAtlas2Based'
    barnesHut: {
      gravitationalConstant: -3000,  // more negative = nodes spread further apart
      centralGravity:        0.3,    // pull towards center; 0 = no pull
      springLength:          120,    // preferred edge length
      springConstant:        0.04,   // edge stiffness
      damping:               0.09,   // energy dissipation
      avoidOverlap:          0.2,    // 0–1, prevents node overlap
    },
    stabilization: {
      enabled:    true,
      iterations: 200,
      updateInterval: 50,
      onlyDynamicEdges: false,
      fit: true,                     // fit to view after stabilization
    },
    minVelocity: 0.75,
  },

  // ── Layout ───────────────────────────────────────────────
  layout: {
    randomSeed:        42,           // fixed seed for reproducible layout
    improvedLayout:    true,
    hierarchical: {                  // enable for tree / DAG layouts
      enabled:         false,
      direction:       'UD',         // 'UD'|'DU'|'LR'|'RL'
      sortMethod:      'hubsize',    // 'hubsize' | 'directed'
      levelSeparation: 150,
      nodeSpacing:     100,
      treeSpacing:     200,
      blockShifting:   true,
      edgeMinimization: true,
      parentCentralization: true,
    },
  },

  // ── Interaction ──────────────────────────────────────────
  interaction: {
    dragNodes:      true,
    dragView:       true,
    zoomView:       true,
    zoomSpeed:      1,
    hover:          true,            // fire hover events
    tooltipDelay:   200,
    multiselect:    false,
    selectConnectedEdges: true,
    navigationButtons: false,        // set true for pan/zoom UI buttons
    keyboard:       { enabled: false },
  },

  // ── Manipulation GUI ─────────────────────────────────────
  manipulation: {
    enabled: false,                  // set true for add/edit/delete toolbar
  },
};
```

---

## Step 6 — Methods Reference

```javascript
// ── Data ─────────────────────────────────────────────────────
network.setData({ nodes: newNodes, edges: newEdges });
network.setOptions(newOptions);                         // live update options

// ── Viewport ─────────────────────────────────────────────────
network.fit();                                          // fit all nodes in view
network.fit({ nodes: [1, 2, 3], animation: { duration: 500 } }); // fit subset
network.focus(nodeId, { scale: 1.5, animation: { duration: 400, easingFunction: 'easeInOutQuad' } });
network.moveTo({ position: { x: 0, y: 0 }, scale: 1, animation: true });

network.getScale();                                     // current zoom level
network.getViewPosition();                              // { x, y } canvas center

// ── Node/Edge information ────────────────────────────────────
network.getConnectedNodes(nodeId);                      // array of neighbor ids
network.getConnectedNodes(nodeId, 'to');                // outgoing only
network.getConnectedNodes(nodeId, 'from');              // incoming only
network.getConnectedEdges(nodeId);                      // edge ids
network.getPositions([nodeId1, nodeId2]);               // { id: {x,y}, ... }
network.getPosition(nodeId);                            // {x, y}
network.getBoundingBox(nodeId);                         // {top, left, right, bottom}

// ── Selection ────────────────────────────────────────────────
network.selectNodes([1, 2]);
network.selectEdges(['e1']);
network.unselectAll();
network.getSelectedNodes();                             // [id, ...]
network.getSelectedEdges();                             // [id, ...]

// ── Physics ──────────────────────────────────────────────────
network.startSimulation();
network.stopSimulation();                               // freeze layout
network.stabilize(100);                                 // run N iterations then stop

// ── Node position persistence ────────────────────────────────
network.storePositions();                               // write x/y back into DataSet

// ── Clustering ───────────────────────────────────────────────
network.clusterByConnection(nodeId);
network.clusterByHubsize(3);                            // cluster nodes with ≥3 edges
network.clusterOutliers();                              // cluster 1-edge nodes
network.openCluster(clusterId);

// ── Coordinate conversion ────────────────────────────────────
network.canvasToDOM({ x: 100, y: 200 });               // canvas → DOM pixels
network.DOMtoCanvas({ x: 300, y: 400 });               // DOM pixels → canvas

// ── Misc ─────────────────────────────────────────────────────
network.redraw();
network.setSize('100%', '600px');
network.destroy();
```

---

## Step 7 — Events

```javascript
// Click on node
network.on('click', (params) => {
  // params: { nodes: [id,...], edges: [id,...], event, pointer: { DOM:{x,y}, canvas:{x,y} } }
  if (params.nodes.length > 0) {
    const nodeId = params.nodes[0];
    const node = nodes.get(nodeId);
    console.log('Clicked node:', node);
  }
});

network.on('doubleClick',   (params) => { /* same structure */ });
network.on('oncontext',     (params) => { /* right-click */ });
network.on('hold',          (params) => { /* long press */ });

// Hover
network.on('hoverNode',     ({ node }) => { ... });
network.on('blurNode',      ({ node }) => { ... });
network.on('hoverEdge',     ({ edge }) => { ... });
network.on('blurEdge',      ({ edge }) => { ... });

// Drag
network.on('dragStart',     (params) => { ... });   // params.nodes = dragged node ids
network.on('dragging',      (params) => { ... });
network.on('dragEnd',       (params) => { ... });

// Physics
network.on('stabilizationProgress', ({ iterations, total }) => {
  const pct = Math.round(iterations / total * 100);
  // update a progress bar
});
network.on('stabilizationIterationsDone', () => {
  // layout is stable — hide loader, show graph
});
network.on('stabilized', ({ iterations }) => { ... });

// Zoom / pan
network.on('zoom',          ({ direction, scale, pointer }) => { ... });

// Selection
network.on('select',        ({ nodes, edges }) => { ... });
network.on('selectNode',    ({ nodes }) => { ... });
network.on('deselectNode',  ({ previousSelection }) => { ... });
network.on('selectEdge',    ({ edges }) => { ... });
network.on('deselectEdge',  ({ previousSelection }) => { ... });

// Remove listener
network.off('click', handler);
```

---

## Step 8 — DataSet Live Updates

```javascript
// Add nodes/edges
nodes.add({ id: 10, label: 'New Node', group: 'servers' });
edges.add({ from: 1, to: 10, label: 'connects' });

// Update
nodes.update({ id: 2, color: { background: '#22c55e' }, label: 'Updated' });

// Remove
nodes.remove(5);
edges.remove('e1');

// Batch
nodes.update([
  { id: 1, hidden: true },
  { id: 2, opacity: 0.3 },
]);
```

---

## Step 9 — Stabilization Loading Pattern

Large graphs take time to stabilize. Show a loader until the layout is ready:

```javascript
// Show loader before creating network
document.getElementById('loader').style.display = 'block';
document.getElementById('network').style.opacity = '0';

const network = new vis.Network(container, data, options);

network.on('stabilizationProgress', ({ iterations, total }) => {
  document.getElementById('progress').style.width = `${Math.round(iterations / total * 100)}%`;
});

network.once('stabilizationIterationsDone', () => {
  document.getElementById('loader').style.display = 'none';
  document.getElementById('network').style.transition = 'opacity 0.4s';
  document.getElementById('network').style.opacity = '1';
  network.fit({ animation: { duration: 500 } });
});
```

---

## Step 10 — Hierarchical Layout (Trees & DAGs)

For directed acyclic graphs — org charts, dependency trees, flow diagrams:

```javascript
const options = {
  layout: {
    hierarchical: {
      enabled:          true,
      direction:        'UD',      // 'UD'=top-down, 'DU'=bottom-up, 'LR'=left-right, 'RL'=right-left
      sortMethod:       'directed', // 'directed' (follows edge direction) | 'hubsize'
      levelSeparation:  160,
      nodeSpacing:      120,
      treeSpacing:      250,
      blockShifting:    true,
      edgeMinimization: true,
      parentCentralization: true,
      shakeTowards:     'leaves',  // 'roots' | 'leaves'
    },
  },
  physics: {
    enabled: false,                // MUST disable physics for hierarchical layout
    hierarchicalRepulsion: {       // used only when physics IS enabled with hierarchical
      nodeDistance:    200,
      centralGravity:  0,
      springLength:    100,
      springConstant:  0.01,
      damping:         0.09,
    },
  },
  edges: {
    smooth: { type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.4 },
  },
};
```

---

## Step 11 — Design & Polish Guidelines

- **Dark node palette** — use muted backgrounds (`#6366f1`, `#8b5cf6`, `#22c55e`) with white/light labels; avoid pure white nodes on dark canvas
- **Font contrast** — node labels should use `color: '#f1f5f9'` for readability on dark node backgrounds
- **Edge arrows** — use `arrows: { to: { enabled: true, scaleFactor: 0.8 } }` for directed graphs; omit arrows for undirected relationships
- **Physics tuning** — reduce `solver: 'barnesHut'` with `gravitationalConstant: -3000` for smaller graphs; increase for dense graphs
- **Stabilization** — show a loading indicator during stabilization for large graphs (`stabilizationProgress` event)
- **Clustering** — group related nodes using `network.cluster()` with opening on double-click for manageable views
- **Legend** — add a CSS-based legend outside the canvas showing node colors → categories and edge styles → relationships
- **Canvas background** — set canvas background to transparent so the card background shows through
- **Interaction hints** — add a subtitle like “drag to rearrange · scroll to zoom · click to select” so users know the graph is interactive

---

## Step 12 — Complete Example: Styled Directed Network

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Network Graph</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 32px; width: 100%; max-width: 900px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
    #network { width: 100%; height: 500px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); background: #161923; }

    /* Loader overlay */
    #loader { position: absolute; display: flex; flex-direction: column; align-items: center; gap: 12px; }
    .progress-bar { width: 200px; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; }
    .progress-fill { height: 100%; background: #6366f1; border-radius: 2px; width: 0; transition: width 0.1s; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Microservices Architecture</h1>
    <p class="sub">Drag nodes · Scroll to zoom · Click to highlight connections</p>
    <div style="position:relative; display:flex; align-items:center; justify-content:center;">
      <div id="loader">
        <span style="color:#94a3b8;font-size:13px;">Calculating layout…</span>
        <div class="progress-bar"><div class="progress-fill" id="progress"></div></div>
      </div>
      <div id="network" style="opacity:0;"></div>
    </div>
  </div>

  <script>
    const nodes = new vis.DataSet([
      { id: 1,  label: 'API Gateway',   group: 'gateway'  },
      { id: 2,  label: 'Auth\nService', group: 'service'  },
      { id: 3,  label: 'User\nService', group: 'service'  },
      { id: 4,  label: 'Order\nService',group: 'service'  },
      { id: 5,  label: 'Product\nService', group: 'service' },
      { id: 6,  label: 'Users DB',      group: 'database' },
      { id: 7,  label: 'Orders DB',     group: 'database' },
      { id: 8,  label: 'Redis Cache',   group: 'cache'    },
      { id: 9,  label: 'Message Bus',   group: 'infra'    },
      { id: 10, label: 'Notification\nService', group: 'service' },
    ]);

    const edges = new vis.DataSet([
      { from: 1, to: 2,  arrows: 'to', label: 'verify' },
      { from: 1, to: 3,  arrows: 'to' },
      { from: 1, to: 4,  arrows: 'to' },
      { from: 1, to: 5,  arrows: 'to' },
      { from: 3, to: 6,  arrows: 'to', dashes: true },
      { from: 4, to: 7,  arrows: 'to', dashes: true },
      { from: 3, to: 8,  arrows: 'to', label: 'cache' },
      { from: 4, to: 9,  arrows: 'to' },
      { from: 9, to: 10, arrows: 'to' },
      { from: 2, to: 8,  arrows: 'to', label: 'session' },
    ]);

    const options = {
      groups: {
        gateway:  { shape: 'box',     color: { background: 'rgba(239,68,68,0.25)', border: '#ef4444' }, font: { color: '#fca5a5' }, size: 22 },
        service:  { shape: 'dot',     color: { background: 'rgba(99,102,241,0.3)', border: '#6366f1' }, font: { color: '#a5b4fc' } },
        database: { shape: 'diamond', color: { background: 'rgba(234,179,8,0.25)', border: '#eab308' }, font: { color: '#fef08a' }, size: 20 },
        cache:    { shape: 'square',  color: { background: 'rgba(34,197,94,0.25)', border: '#22c55e' }, font: { color: '#86efac' }, size: 16 },
        infra:    { shape: 'hexagon', color: { background: 'rgba(168,85,247,0.25)',border: '#a855f7' }, font: { color: '#d8b4fe' }, size: 20 },
      },
      nodes: {
        font: { color: '#e2e8f0', size: 13, face: 'Segoe UI' },
        borderWidth: 2,
        shadow: { enabled: true, color: 'rgba(0,0,0,0.5)', size: 10 },
      },
      edges: {
        color: { color: 'rgba(148,163,184,0.25)', highlight: '#6366f1', hover: '#94a3b8' },
        width: 1.5,
        smooth: { type: 'curvedCW', roundness: 0.15 },
        font: { color: '#475569', size: 10, align: 'middle' },
        selectionWidth: 3,
        hoverWidth: 2.5,
      },
      physics: {
        barnesHut: { gravitationalConstant: -4000, centralGravity: 0.3, springLength: 160, avoidOverlap: 0.3 },
        stabilization: { iterations: 300, fit: true },
      },
      interaction: { hover: true, tooltipDelay: 150 },
      layout:  { randomSeed: 7 },
    };

    const network = new vis.Network(document.getElementById('network'), { nodes, edges }, options);

    // Loading progress
    network.on('stabilizationProgress', ({ iterations, total }) => {
      document.getElementById('progress').style.width = `${Math.round(iterations / total * 100)}%`;
    });
    network.once('stabilizationIterationsDone', () => {
      document.getElementById('loader').style.display = 'none';
      const el = document.getElementById('network');
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '1';
      network.fit({ animation: { duration: 600 } });
    });

    // Click: highlight connected nodes
    network.on('click', ({ nodes: sel }) => {
      if (sel.length === 0) {
        nodes.update(nodes.getIds().map(id => ({ id, opacity: 1 })));
        edges.update(edges.getIds().map(id => ({ id, color: undefined })));
        return;
      }
      const nodeId = sel[0];
      const connected = new Set(network.getConnectedNodes(nodeId));
      connected.add(nodeId);
      nodes.update(nodes.getIds().map(id => ({ id, opacity: connected.has(id) ? 1 : 0.2 })));
      const connEdges = new Set(network.getConnectedEdges(nodeId));
      edges.update(edges.getIds().map(id => ({
        id,
        color: connEdges.has(id) ? { color: '#6366f1', opacity: 1 } : { opacity: 0.07 }
      })));
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No explicit height on the container** — the `#network` div must have a CSS height; Canvas rendering requires fixed dimensions
- **Forgetting `physics: { enabled: false }` with hierarchical layout** — hierarchical + physics fighting each other produces unstable jitter
- **Node `id` must be unique** — duplicate ids silently corrupt the DataSet; always use unique numeric or string ids
- **Tooltip (`title` property) is HTML** — sanitize user data to prevent XSS
- **Assigning fixed positions without disabling physics** — set `physics: false` on a per-node basis or globally when using `x`/`y`, or physics will fight the fixed positions
- **Updating opacity via color object** — `opacity` is a top-level node property, not nested in `color`; to dim nodes use `nodes.update({ id, opacity: 0.2 })`
- **Not calling `.destroy()`** — the Canvas and all event listeners persist; always call `network.destroy()` on cleanup
- **Random layout differences between renders** — set `layout.randomSeed` to a fixed number for reproducible initial placement
