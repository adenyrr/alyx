---
name: konva-canvas
description: Create interactive 2D canvas graphics using Konva.js, delivered as self-contained HTML artifacts. Use this skill whenever someone needs a 2D drawing canvas with draggable shapes, image editing, text overlays, freehand drawing, export to PNG/JSON, or any interactive graphics application that needs hit detection and layering but not 3D. Trigger on requests like "make a drawing app", "create a canvas editor", "build a photo annotator", "design a badge/certificate maker", "create a shape editor", or any prompt needing interactive 2D canvas manipulation. Do NOT use for 3D scenes (→ threejs-3d skill), flowcharts/diagrams with connections (→ jointjs-flowchart skill), or generative art (→ p5js-creative-coding skill).
---

# Konva.js Canvas Skill

Konva.js is a 2D canvas framework that provides a Stage/Layer architecture, built-in shapes (Rect, Circle, Text, Image, Path, Arrow, etc.), drag-and-drop, transformers (resize/rotate handles), event handling, grouping, clipping, filters, animation, and export to PNG/JPEG/JSON. It's the go-to library for building drawing editors, photo annotators, and interactive canvas applications.

---

## Artifact Presentation & Use Cases

Every Konva artifact is a self-contained HTML page with a dark theme and an interactive canvas area. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius) centers the canvas and controls
- **Title** (1.15rem, `#f1f5f9`) names the editor/tool
- **Subtitle** (0.82rem, `#64748b`) explains interactions
- **Toolbar** with tool buttons (select, shapes, text, drawing, export)
- **Canvas container** with explicit dimensions — the Konva Stage renders here

### Typical use cases

- **Drawing/whiteboard apps** — freehand drawing, shapes, text annotations
- **Photo annotators** — load image, draw arrows/circles/text overlays, export
- **Badge/certificate makers** — drag text and images into templates
- **Image editors** — crop, filter, arrange layers
- **Floor plan editors** — drag furniture/room elements onto a grid
- **Shape-based games** — interactive 2D scenes with hit detection
- **Signature pads** — capture freehand signatures
- **Meme generators** — image + draggable text overlays + export

### What the user sees

An interactive canvas where shapes, images, and text can be dragged, resized, and rotated using handles. A toolbar provides drawing tools, and an export button saves the canvas as PNG.

---

## When to Use Konva vs. Alternatives

| Use Konva when… | Use another tool when… |
|---|---|
| Interactive 2D canvas with hit detection | 3D scenes → **Three.js** |
| Drag, resize, rotate with handles (Transformer) | Flowchart connections (port-based links) → **JointJS** |
| Export canvas to PNG/JPEG | Generative art / mathematical patterns → **p5.js** |
| Layer-based composition | SVG-based diagrams (not canvas) → **D3** or **JointJS** |
| Image manipulation (crop, filter) | Scroll-driven animation → **GSAP** |
| Performance with many objects (scenegraph) | Simple CSS animations → **Anime.js** |

> **Rule of thumb:** if the user needs to drag, resize, and arrange 2D shapes/images/text with interactive handles and export capability, use Konva. For artistic/mathematical visuals, use p5.js. For connected diagrams, use JointJS.

---

## Step 1 — CDN Setup

```html
<!-- Konva.js -->
<script src="https://cdn.jsdelivr.net/npm/konva@9/konva.min.js"></script>
```

> Konva exposes the `Konva` global. No CSS required.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Canvas Editor</title>
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
      max-width: 900px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 16px; }
    .toolbar { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
    .toolbar button { background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 6px 14px; font-size: 12px; cursor: pointer; transition: all 0.15s; }
    .toolbar button:hover { background: rgba(255,255,255,0.1); color: #f1f5f9; }
    .toolbar button.active { background: #6366f1; color: #fff; border-color: #6366f1; }
    #canvas-container {
      width: 100%;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      overflow: hidden;
      background: #0f1117;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Editor Title</h1>
    <p class="sub">Drag shapes · click to select · use handles to resize/rotate</p>
    <div class="toolbar">
      <button id="btn-rect">Rectangle</button>
      <button id="btn-circle">Circle</button>
      <button id="btn-text">Text</button>
      <button id="btn-export">Export PNG</button>
    </div>
    <div id="canvas-container"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/konva@9/konva.min.js"></script>
  <script>
    // All Konva code here
  </script>
</body>
</html>
```

---

## Step 3 — Stage & Layers

```javascript
const container = document.getElementById('canvas-container');
const WIDTH = container.offsetWidth;
const HEIGHT = 500;

const stage = new Konva.Stage({
  container: 'canvas-container',
  width: WIDTH,
  height: HEIGHT,
});

// Background layer (static)
const bgLayer = new Konva.Layer();
stage.add(bgLayer);

// Main layer (interactive shapes)
const layer = new Konva.Layer();
stage.add(layer);

// Transformer (resize/rotate handles)
const tr = new Konva.Transformer({
  rotateEnabled: true,
  borderStroke: '#6366f1',
  anchorStroke: '#6366f1',
  anchorFill: '#1a1d27',
  anchorSize: 8,
  borderStrokeWidth: 1.5,
});
layer.add(tr);
```

---

## Step 4 — Basic Shapes

```javascript
// Rectangle
const rect = new Konva.Rect({
  x: 100, y: 100,
  width: 150, height: 80,
  fill: '#6366f1',
  cornerRadius: 8,
  draggable: true,
});
layer.add(rect);

// Circle
const circle = new Konva.Circle({
  x: 400, y: 200,
  radius: 50,
  fill: '#22c55e',
  draggable: true,
});
layer.add(circle);

// Ellipse
const ellipse = new Konva.Ellipse({
  x: 300, y: 150,
  radiusX: 80, radiusY: 40,
  fill: '#ec4899',
  draggable: true,
});

// Line / Polyline
const line = new Konva.Line({
  points: [50, 50, 200, 80, 350, 50],
  stroke: '#f97316',
  strokeWidth: 3,
  lineCap: 'round',
  lineJoin: 'round',
  draggable: true,
});

// Arrow
const arrow = new Konva.Arrow({
  points: [100, 300, 300, 300],
  stroke: '#06b6d4',
  fill: '#06b6d4',
  strokeWidth: 3,
  pointerLength: 10,
  pointerWidth: 8,
  draggable: true,
});

// Star
const star = new Konva.Star({
  x: 500, y: 150,
  numPoints: 5,
  innerRadius: 20, outerRadius: 50,
  fill: '#eab308',
  draggable: true,
});
```

---

## Step 5 — Text

```javascript
const text = new Konva.Text({
  x: 100, y: 50,
  text: 'Hello Konva',
  fontSize: 24,
  fontFamily: 'Segoe UI, sans-serif',
  fontStyle: 'bold',
  fill: '#f1f5f9',
  draggable: true,
  padding: 8,
});
layer.add(text);

// Editable text (double-click to edit)
text.on('dblclick', () => {
  const textPosition = text.absolutePosition();
  const input = document.createElement('textarea');
  document.body.appendChild(input);
  input.value = text.text();
  input.style.position = 'absolute';
  input.style.top = stage.container().offsetTop + textPosition.y + 'px';
  input.style.left = stage.container().offsetLeft + textPosition.x + 'px';
  input.style.fontSize = text.fontSize() + 'px';
  input.style.background = 'transparent';
  input.style.color = '#f1f5f9';
  input.style.border = '1px solid #6366f1';
  input.style.outline = 'none';
  input.style.resize = 'none';
  input.focus();

  input.addEventListener('blur', () => {
    text.text(input.value);
    input.remove();
    layer.draw();
  });
});
```

---

## Step 6 — Images

```javascript
const imageObj = new Image();
imageObj.onload = function () {
  const img = new Konva.Image({
    x: 50, y: 50,
    image: imageObj,
    width: 300,
    height: 200,
    draggable: true,
    cornerRadius: 12,
  });
  layer.add(img);
  layer.draw();
};
imageObj.crossOrigin = 'anonymous';
imageObj.src = 'https://picsum.photos/600/400';
```

---

## Step 7 — Transformer (Resize/Rotate Handles)

```javascript
const tr = new Konva.Transformer({
  rotateEnabled: true,
  borderStroke: '#6366f1',
  anchorStroke: '#6366f1',
  anchorFill: '#1a1d27',
  anchorSize: 8,
  borderStrokeWidth: 1.5,
  keepRatio: false,          // allow free resize
  enabledAnchors: ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'middle-right', 'middle-left'],
});
layer.add(tr);

// Click to select
stage.on('click tap', (e) => {
  if (e.target === stage) {
    tr.nodes([]);         // deselect
  } else if (e.target.draggable()) {
    tr.nodes([e.target]); // select clicked shape
  }
  layer.draw();
});
```

---

## Step 8 — Events

```javascript
// Shape events
rect.on('click', () => console.log('Clicked'));
rect.on('dragstart', () => console.log('Drag started'));
rect.on('dragend', () => console.log('Drag ended at', rect.position()));
rect.on('mouseover', () => { document.body.style.cursor = 'pointer'; });
rect.on('mouseout', () => { document.body.style.cursor = 'default'; });

// Stage events
stage.on('click', (e) => {
  const target = e.target;
  const pos = stage.getPointerPosition();
  console.log('Clicked at', pos.x, pos.y, 'on', target.className);
});
```

---

## Step 9 — Groups

```javascript
const group = new Konva.Group({
  x: 200, y: 200,
  draggable: true,
});

group.add(new Konva.Rect({ width: 120, height: 60, fill: '#1e2130', cornerRadius: 8 }));
group.add(new Konva.Text({ text: 'Grouped', fill: '#f1f5f9', fontSize: 14, padding: 8, width: 120, align: 'center', verticalAlign: 'middle' }));

layer.add(group);
```

---

## Step 10 — Freehand Drawing

```javascript
let isDrawing = false;
let currentLine = null;

stage.on('mousedown touchstart', () => {
  isDrawing = true;
  const pos = stage.getPointerPosition();
  currentLine = new Konva.Line({
    stroke: '#6366f1',
    strokeWidth: 3,
    lineCap: 'round',
    lineJoin: 'round',
    globalCompositeOperation: 'source-over',
    points: [pos.x, pos.y],
  });
  layer.add(currentLine);
});

stage.on('mousemove touchmove', (e) => {
  if (!isDrawing || !currentLine) return;
  e.evt.preventDefault();
  const pos = stage.getPointerPosition();
  const newPoints = currentLine.points().concat([pos.x, pos.y]);
  currentLine.points(newPoints);
  layer.batchDraw();
});

stage.on('mouseup touchend', () => {
  isDrawing = false;
  currentLine = null;
});
```

---

## Step 11 — Export

```javascript
// Export to PNG
function exportPNG() {
  const dataURL = stage.toDataURL({ pixelRatio: 2 });
  const a = document.createElement('a');
  a.href = dataURL;
  a.download = 'canvas.png';
  a.click();
}

// Export to JSON
function exportJSON() {
  const json = stage.toJSON();
  const blob = new Blob([json], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'canvas.json';
  a.click();
}

// Import from JSON
function importJSON(jsonString) {
  const newStage = Konva.Node.create(jsonString, 'canvas-container');
  // Note: you may need to re-attach event listeners
}
```

---

## Step 12 — Design & Polish Guidelines

- **Dark canvas background** — set `#0f1117` as the container background; optionally add a Konva.Rect filling the bgLayer as a selectable "canvas" bg
- **Transformer styling** — customize anchor and border colors to match the accent (`#6366f1`); use `anchorFill: '#1a1d27'` for dark handles
- **Cursor feedback** — change cursor on `mouseover`/`mouseout` for draggable shapes; use `pointer` for interactive, `move` for dragging
- **Tool state** — highlight the active tool button with CSS `.active` class; only one tool active at a time
- **Layer separation** — use separate layers for background, shapes, and UI overlay (transformer); this improves redraw performance
- **`batchDraw()`** — use `layer.batchDraw()` during continuous events (drawing, dragging) instead of `layer.draw()` for better performance
- **Export quality** — use `pixelRatio: 2` in `toDataURL()` for retina-quality exports
- **Responsive stage** — listen to `window.resize` and update `stage.width()` / `stage.height()` to match container
- **Hit detection** — enable `hitStrokeWidth` on thin lines/arrows so they're easier to click
- **Z-ordering** — use `shape.moveToTop()` on click to bring selected shapes to front

---

## Step 13 — Complete Example: Shape Editor

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shape Editor</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 24px; width: 100%; max-width: 850px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 14px; }
    .toolbar { display: flex; gap: 6px; margin-bottom: 14px; flex-wrap: wrap; }
    .toolbar button { background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 6px 12px; font-size: 11px; cursor: pointer; transition: all 0.15s; }
    .toolbar button:hover { background: rgba(255,255,255,0.1); color: #f1f5f9; }
    .toolbar button.active { background: #6366f1; color: #fff; border-color: #6366f1; }
    #canvas-container { width: 100%; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; overflow: hidden; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Shape Editor</h1>
    <p class="sub">Add shapes · drag to move · handles to resize/rotate · double-click text to edit · Delete key to remove</p>
    <div class="toolbar">
      <button id="btn-rect">▬ Rect</button>
      <button id="btn-circle">● Circle</button>
      <button id="btn-text">T Text</button>
      <button id="btn-arrow">→ Arrow</button>
      <button id="btn-draw" class="draw-btn">✎ Draw</button>
      <button id="btn-del">✕ Delete</button>
      <button id="btn-export">↓ PNG</button>
    </div>
    <div id="canvas-container"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/konva@9/konva.min.js"></script>
  <script>
    const WIDTH = document.getElementById('canvas-container').offsetWidth;
    const HEIGHT = 420;
    const COLORS = ['#6366f1','#8b5cf6','#ec4899','#22c55e','#06b6d4','#f97316'];
    let colorIdx = 0;
    const nextColor = () => COLORS[colorIdx++ % COLORS.length];

    const stage = new Konva.Stage({ container: 'canvas-container', width: WIDTH, height: HEIGHT });
    const layer = new Konva.Layer();
    stage.add(layer);

    const tr = new Konva.Transformer({
      borderStroke: '#6366f1', anchorStroke: '#6366f1', anchorFill: '#1a1d27', anchorSize: 8, borderStrokeWidth: 1.5,
    });
    layer.add(tr);

    let drawMode = false;
    let isDrawing = false;
    let currentLine = null;

    // Selection
    stage.on('click tap', (e) => {
      if (drawMode) return;
      if (e.target === stage) { tr.nodes([]); layer.draw(); return; }
      if (e.target.draggable && e.target.draggable()) {
        tr.nodes([e.target]);
        e.target.moveToTop();
        tr.moveToTop();
        layer.draw();
      }
    });

    // Delete key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Delete' || e.key === 'Backspace') {
        const nodes = tr.nodes();
        if (nodes.length) { nodes.forEach(n => n.destroy()); tr.nodes([]); layer.draw(); }
      }
    });

    // Add shapes
    function addRect() {
      const r = new Konva.Rect({ x: 80+Math.random()*300, y: 60+Math.random()*200, width: 120, height: 70, fill: nextColor(), cornerRadius: 8, draggable: true, opacity: 0.9 });
      layer.add(r); tr.nodes([r]); tr.moveToTop(); layer.draw();
    }
    function addCircle() {
      const c = new Konva.Circle({ x: 200+Math.random()*200, y: 150+Math.random()*100, radius: 40, fill: nextColor(), draggable: true, opacity: 0.9 });
      layer.add(c); tr.nodes([c]); tr.moveToTop(); layer.draw();
    }
    function addText() {
      const t = new Konva.Text({ x: 100+Math.random()*200, y: 80+Math.random()*200, text: 'Edit me', fontSize: 20, fontFamily: 'Segoe UI', fill: '#f1f5f9', draggable: true, padding: 6 });
      t.on('dblclick dbltap', () => {
        const ta = document.createElement('textarea');
        document.body.appendChild(ta);
        const rect = t.getClientRect();
        const stageBox = stage.container().getBoundingClientRect();
        ta.value = t.text();
        ta.style.cssText = `position:fixed;top:${stageBox.top+rect.y}px;left:${stageBox.left+rect.x}px;font-size:${t.fontSize()}px;color:#f1f5f9;background:#1a1d27;border:1px solid #6366f1;border-radius:6px;outline:none;padding:4px;resize:none;z-index:1000;`;
        ta.focus();
        ta.addEventListener('blur', () => { t.text(ta.value); ta.remove(); layer.draw(); });
      });
      layer.add(t); tr.nodes([t]); tr.moveToTop(); layer.draw();
    }
    function addArrow() {
      const x = 100+Math.random()*200, y = 100+Math.random()*200;
      const a = new Konva.Arrow({ points: [x, y, x+150, y], stroke: nextColor(), fill: nextColor(), strokeWidth: 3, pointerLength: 10, pointerWidth: 8, draggable: true });
      layer.add(a); tr.nodes([a]); tr.moveToTop(); layer.draw();
    }

    // Freehand draw
    function toggleDraw() {
      drawMode = !drawMode;
      document.getElementById('btn-draw').classList.toggle('active', drawMode);
      stage.container().style.cursor = drawMode ? 'crosshair' : 'default';
      layer.find('Rect, Circle, Text, Arrow, Star, Ellipse').forEach(s => s.draggable(!drawMode));
    }
    stage.on('mousedown touchstart', (e) => {
      if (!drawMode) return;
      isDrawing = true;
      const pos = stage.getPointerPosition();
      currentLine = new Konva.Line({ stroke: '#6366f1', strokeWidth: 3, lineCap: 'round', lineJoin: 'round', points: [pos.x, pos.y], draggable: true });
      layer.add(currentLine);
    });
    stage.on('mousemove touchmove', (e) => {
      if (!isDrawing || !currentLine) return;
      e.evt.preventDefault();
      const pos = stage.getPointerPosition();
      currentLine.points(currentLine.points().concat([pos.x, pos.y]));
      layer.batchDraw();
    });
    stage.on('mouseup touchend', () => { isDrawing = false; currentLine = null; });

    // Buttons
    document.getElementById('btn-rect').onclick = addRect;
    document.getElementById('btn-circle').onclick = addCircle;
    document.getElementById('btn-text').onclick = addText;
    document.getElementById('btn-arrow').onclick = addArrow;
    document.getElementById('btn-draw').onclick = toggleDraw;
    document.getElementById('btn-del').onclick = () => { tr.nodes().forEach(n => n.destroy()); tr.nodes([]); layer.draw(); };
    document.getElementById('btn-export').onclick = () => {
      tr.nodes([]); layer.draw();
      const url = stage.toDataURL({ pixelRatio: 2 });
      const a = document.createElement('a'); a.href = url; a.download = 'canvas.png'; a.click();
    };

    // Responsive
    window.addEventListener('resize', () => {
      const w = document.getElementById('canvas-container').offsetWidth;
      stage.width(w);
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No `layer.draw()` after changes** — Konva doesn't auto-redraw; call `layer.draw()` or `layer.batchDraw()` after adding/modifying shapes
- **Stage height 0** — always set an explicit height on the Stage; it won't auto-size from content
- **Transformer not on top** — the Transformer must be the topmost node on its layer; call `tr.moveToTop()` after adding shapes
- **Missing `draggable: true`** — shapes are not draggable by default; explicitly set `draggable: true` on each interactive shape
- **Click events firing on Transformer anchors** — check `e.target === stage` for blank clicks, not just `!e.target.hasName('rect')`
- **Memory leaks** — call `shape.destroy()` when removing shapes; just removing from layer leaves event listeners active
- **`toDataURL()` without clearing selection** — hide the Transformer before export so selection handles don't appear in the PNG
- **Cross-origin images** — set `imageObj.crossOrigin = 'anonymous'` before setting `src` to enable `toDataURL()` export with images
- **Not using `batchDraw()`** — during continuous events (freehand drawing, dragging), `batchDraw()` batches renders for performance; `draw()` is immediate
- **Forgetting touch events** — always handle both `mousedown/mousemove/mouseup` and `touchstart/touchmove/touchend` for mobile
