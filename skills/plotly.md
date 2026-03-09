---
name: plotly
description: Create advanced, interactive scientific and statistical charts using Plotly.js, delivered as self-contained HTML artifacts. Use this skill for: box plots, violin plots, histograms, error bars, contour/heatmaps, 3D surfaces, 3D scatter, candlestick/OHLC financial charts, parallel coordinates, sunbursts, treemaps, funnel charts, waterfall charts, geographic choropleths, and scatter plots with 100K+ data points (WebGL mode). Also use when users need built-in zoom/pan, range sliders, lasso select, or image export. Trigger on keywords like "plot", "distribution", "correlation", "statistical", "3D chart", "financial chart", "candlestick", "box plot", "heatmap", "contour", or when the user's needs exceed simple bar/line/pie charts. Do NOT use for: standard dashboards/presentations with basic charts (→ chartjs skill), network graphs (→ vis-network skill), geographic maps with tiles/markers (→ leaflet skill), or bespoke SVG layouts (→ d3-charting skill).
---

# Plotly.js Skill — Advanced & Scientific Charts

Plotly.js is a high-level, full-featured charting library built on D3 and WebGL. It provides 40+ chart types out of the box—including statistical, scientific, financial, and 3D charts—with built-in interactivity (zoom, pan, hover, lasso select, image export). Ideal for data-rich visualizations where deep exploration matters.

---

## Artifact Presentation & Use Cases

Every Plotly artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the chart
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the chart
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context, data source, or interaction hints
- **`<div id="chart">` container** — Plotly renders its own SVG/WebGL inside

### Typical use cases

- **Statistical analysis** — box plots, violin plots, histograms with KDE overlays
- **Scientific data** — 3D surfaces, contour plots, heatmaps, error bars
- **Financial charts** — candlestick, OHLC, waterfall charts
- **Large datasets** — 100K+ point scatter plots via `scattergl` / WebGL
- **Correlation matrices** — annotated heatmaps showing feature relationships
- **Hierarchical data** — sunbursts, treemaps, icicle charts
- **Multi-panel exploration** — subplots with shared axes, range sliders, and linked hover
- **Geographic analysis** — choropleth maps showing regional data

### What the user sees

A deeply interactive chart: drag to zoom, double-click to reset, hover for rich tooltips, lasso select points, click the export button for SVG/PNG. The Plotly toolbar (modebar) appears on hover and provides pan, zoom, and download tools.

---

## When to Use Plotly vs. Alternatives

| Use Plotly when… | Use another library when… |
|---|---|
| Statistical charts: box, violin, histogram, error bars | Simple bar/line/pie/doughnut for dashboards → **Chart.js** |
| Financial charts: candlestick, OHLC, waterfall | Quick presentation charts → **Chart.js** |
| 3D visualization: surfaces, scatter3d | Interactive tile-based maps with markers → **Leaflet** |
| Large datasets: 100K+ points via WebGL | Node-edge network graphs → **vis-network** |
| Built-in zoom, pan, lasso, range sliders | Bespoke SVG layouts with custom forces → **D3** |
| Subplots with shared axes | Text-to-diagram (flowcharts, sequences) → **Mermaid** |
| Image export (SVG, PNG, WebP) | Pure CSS layouts, no charting → **Tailwind/Bulma** |
| Annotated heatmaps, parallel coordinates | Simple needs with minimal bundle size → **Chart.js** |

> **Rule of thumb:** if the chart type exists in Chart.js and you don't need zoom/lasso/3D/WebGL, use Chart.js for its smaller bundle and simpler API. Use Plotly when Chart.js can't handle the chart type or the dataset size.

---

## Step 1 — CDN Setup

```html
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist@2.35.2/plotly.js"></script>
```

For smaller bundle with only basic charts:
```html
<script src="https://cdn.jsdelivr.net/npm/plotly.js-basic-dist@2.35.2/plotly-basic.js"></script>
```

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chart Title</title>
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
      width: 100%;
      max-width: 960px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 24px; }
    #chart { width: 100%; }

    /* Plotly modebar — blend with dark theme */
    .modebar { top: 8px !important; right: 8px !important; }
    .modebar-btn path { fill: #64748b !important; }
    .modebar-btn:hover path { fill: #e2e8f0 !important; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Chart Title</h1>
    <p class="sub">Data source or description · drag to zoom, double-click to reset</p>
    <div id="chart"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/plotly.js-dist@2.35.2/plotly.js"></script>
  <script>
    // All Plotly code here
  </script>
</body>
</html>
```

---

## Step 3 — Dark Theme Reference

Plotly uses a `layout` object for theming. This dark layout should be used as the base for all charts:

```javascript
const DARK_LAYOUT = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor:  'rgba(0,0,0,0)',
  font: { color: '#94a3b8', family: 'Segoe UI, system-ui, sans-serif', size: 13 },
  margin: { t: 20, r: 20, b: 50, l: 60 },
  xaxis: {
    gridcolor:   'rgba(255,255,255,0.06)',
    zerolinecolor: 'rgba(255,255,255,0.1)',
    tickfont: { color: '#94a3b8' },
  },
  yaxis: {
    gridcolor:   'rgba(255,255,255,0.06)',
    zerolinecolor: 'rgba(255,255,255,0.1)',
    tickfont: { color: '#94a3b8' },
  },
  hoverlabel: {
    bgcolor: '#1e293b',
    bordercolor: '#334155',
    font: { color: '#e2e8f0', size: 13 },
  },
  colorway: ['#6366f1','#8b5cf6','#ec4899','#f43f5e','#f97316','#eab308','#22c55e','#06b6d4'],
};
```

### Color scales for heatmaps and surfaces

```javascript
// Cool-warm continuous
colorscale: [[0,'#312e81'],[0.25,'#4338ca'],[0.5,'#7c3aed'],[0.75,'#ec4899'],[1,'#fbbf24']]

// Sequential blue
colorscale: 'Blues'

// Diverging
colorscale: 'RdBu'
```

---

## Step 4 — Minimal Setup

```javascript
const DARK_LAYOUT = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor:  'rgba(0,0,0,0)',
  font: { color: '#94a3b8', family: 'Segoe UI, sans-serif', size: 13 },
  margin: { t: 20, r: 20, b: 50, l: 60 },
  xaxis: { gridcolor: 'rgba(255,255,255,0.06)' },
  yaxis: { gridcolor: 'rgba(255,255,255,0.06)' },
  colorway: ['#6366f1','#8b5cf6','#ec4899','#22c55e','#06b6d4'],
};

const trace = {
  x: ['Jan', 'Feb', 'Mar'],
  y: [120, 190, 150],
  type: 'bar',
  marker: { color: '#6366f1', opacity: 0.85 },
};

Plotly.newPlot('chart', [trace], DARK_LAYOUT, { responsive: true });
```

---

## Step 5 — Trace Types Reference

### Cartesian 2D

```javascript
// Bar
{ x, y, type: 'bar', marker: { color, opacity } }

// Grouped bar — set barmode in layout
layout: { barmode: 'group' }

// Stacked bar
layout: { barmode: 'stack' }

// Line / Scatter
{ x, y, mode: 'lines+markers', type: 'scatter', line: { shape: 'spline', width: 2 } }

// Area (filled)
{ x, y, type: 'scatter', fill: 'tozeroy', fillcolor: 'rgba(99,102,241,0.12)' }

// Scatter (dots only)
{ x, y, mode: 'markers', marker: { size: 8, color: z, colorscale: 'Viridis', showscale: true } }

// Bubble
{ x, y, mode: 'markers', marker: { size: sizeArray, sizemode: 'area', sizeref: 2 } }
```

### Statistical

```javascript
// Box plot
{ y: data, type: 'box', name: 'Group A', boxmean: 'sd', marker: { color: '#6366f1' } }

// Violin
{ y: data, type: 'violin', name: 'Distribution', box: { visible: true }, meanline: { visible: true } }

// Histogram
{ x: data, type: 'histogram', nbinsx: 30, marker: { color: '#6366f1', opacity: 0.8 } }

// Error bars
{ x, y, error_y: { type: 'data', array: errValues, visible: true, color: '#94a3b8' } }
```

### Financial

```javascript
// Candlestick (OHLC)
{ x: dates, open, high, low, close, type: 'candlestick',
  increasing: { line: { color: '#22c55e' } },
  decreasing: { line: { color: '#ef4444' } } }

// Waterfall
{ x: categories, y: values, type: 'waterfall',
  measure: ['absolute','relative','relative','total'],
  connector: { line: { color: '#64748b' } } }
```

### Heatmaps & Contours

```javascript
// Heatmap
{ z: matrix, type: 'heatmap', colorscale: 'Viridis', zsmooth: 'best',
  colorbar: { tickfont: { color: '#94a3b8' } } }

// Annotated heatmap — add text overlays
{ z: matrix, text: textMatrix, texttemplate: '%{text}', type: 'heatmap' }

// Contour
{ z: matrix, type: 'contour', colorscale: 'RdBu', contours: { coloring: 'heatmap' } }
```

### 3D Charts

```javascript
// 3D Surface
{ z: matrix, type: 'surface', colorscale: 'Viridis' }
// layout: { scene: { xaxis: {}, yaxis: {}, zaxis: {} } }

// 3D Scatter
{ x, y, z, mode: 'markers', type: 'scatter3d',
  marker: { size: 4, color: z, colorscale: 'Portland' } }
```

### Hierarchical

```javascript
// Sunburst
{ labels, parents, values, type: 'sunburst',
  branchvalues: 'total', marker: { colors: palette } }

// Treemap
{ labels, parents, values, type: 'treemap',
  branchvalues: 'total', textinfo: 'label+value' }
```

### Other Specialized

```javascript
// Parallel coordinates
{ type: 'parcoords',
  dimensions: [
    { label: 'X', values: xArr, range: [0, 10] },
    { label: 'Y', values: yArr, range: [0, 100] },
  ],
  line: { color: scores, colorscale: 'Viridis' } }

// Funnel
{ y: stages, x: counts, type: 'funnel',
  marker: { color: ['#6366f1','#8b5cf6','#a78bfa','#c4b5fd'] } }

// Polar / Radar
{ type: 'scatterpolar', r: values, theta: labels, fill: 'toself' }
```

---

## Step 6 — Subplots

```javascript
// Two side-by-side charts
const trace1 = { x, y, type: 'bar', xaxis: 'x', yaxis: 'y' };
const trace2 = { x, y, type: 'scatter', xaxis: 'x2', yaxis: 'y2' };

const layout = {
  ...DARK_LAYOUT,
  grid: { rows: 1, columns: 2, pattern: 'independent', xgap: 0.1 },
  xaxis:  { domain: [0, 0.45], gridcolor: 'rgba(255,255,255,0.06)' },
  xaxis2: { domain: [0.55, 1], gridcolor: 'rgba(255,255,255,0.06)' },
  yaxis:  { gridcolor: 'rgba(255,255,255,0.06)' },
  yaxis2: { gridcolor: 'rgba(255,255,255,0.06)' },
};

Plotly.newPlot('chart', [trace1, trace2], layout, { responsive: true });
```

---

## Step 7 — Annotations & Shapes

```javascript
layout: {
  annotations: [
    {
      x: 'Mar', y: 340,
      text: 'Peak value',
      showarrow: true,
      arrowhead: 2,
      arrowcolor: '#94a3b8',
      font: { color: '#e2e8f0', size: 12 },
      bgcolor: '#1e293b',
      bordercolor: '#334155',
      borderpad: 4,
    }
  ],
  shapes: [
    // Horizontal threshold line
    { type: 'line', x0: 0, x1: 1, xref: 'paper', y0: 200, y1: 200,
      line: { color: '#f43f5e', dash: 'dash', width: 1.5 } },
    // Highlighted region
    { type: 'rect', x0: 'Feb', x1: 'Apr', y0: 0, y1: 1, yref: 'paper',
      fillcolor: 'rgba(99,102,241,0.08)', line: { width: 0 } },
  ],
}
```

---

## Step 8 — Interactivity & Config

```javascript
const config = {
  responsive: true,
  displayModeBar: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['select2d', 'lasso2d', 'autoScale2d'],
  toImageButtonOptions: {
    format: 'svg',
    filename: 'chart-export',
  },
};

Plotly.newPlot('chart', traces, layout, config);
```

### Range slider (useful for time series)

```javascript
layout: {
  xaxis: {
    rangeslider: { visible: true, bgcolor: '#0f1117' },
    type: 'date',
  }
}
```

### Click events

```javascript
document.getElementById('chart').on('plotly_click', (data) => {
  const point = data.points[0];
  console.log(`Clicked: x=${point.x}, y=${point.y}`);
});
```

---

## Step 9 — Live / Dynamic Updates

```javascript
// Extend traces (append data — great for real-time)
Plotly.extendTraces('chart', { x: [[newX]], y: [[newY]] }, [0]);

// Restyle (change appearance)
Plotly.restyle('chart', { 'marker.color': '#ec4899' }, [0]);

// Relayout (change axes, annotations)
Plotly.relayout('chart', { 'yaxis.range': [0, 500] });

// Full data replacement
Plotly.react('chart', newTraces, newLayout, config);
```

---

## Step 10 — Design & Polish Guidelines

- **Transparent backgrounds** — always set `paper_bgcolor` and `plot_bgcolor` to `rgba(0,0,0,0)` so the card background shows through
- **Consistent margins** — `margin: { t: 20, r: 20, b: 50, l: 60 }` as default; increase `l` for long y-axis labels
- **Modebar styling** — use CSS overrides to blend the toolbar with the dark theme (already in the shell)
- **Grid subtlety** — `gridcolor: 'rgba(255,255,255,0.06)'` — barely visible, never distracting
- **Meaningful hover** — use `hovertemplate` for formatted tooltips: `hovertemplate: '<b>%{x}</b><br>Value: %{y:,.0f}<extra></extra>'`
- **Color consistency** — use the `colorway` array in the layout so all traces share a harmonious palette
- **Big data** — for 100K+ points, use `scattergl` instead of `scatter` (WebGL rendering)
- **Accessibility** — add a `role="img"` and `aria-label` on the chart div
- **No title in layout** — the HTML `<h1>` handles the title; set `layout.title` to undefined to prevent a redundant Plotly title
- **Export-ready** — include `toImageButtonOptions` in config for one-click SVG/PNG export

---

## Step 11 — Complete Example: Statistical Dashboard

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Statistical Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 32px; width: 100%; max-width: 960px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 24px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    .plot { width: 100%; min-height: 300px; }
    .modebar { top: 8px !important; right: 8px !important; }
    .modebar-btn path { fill: #64748b !important; }
    .modebar-btn:hover path { fill: #e2e8f0 !important; }
    @media (max-width: 700px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="card">
    <h1>Dataset Analysis</h1>
    <p class="sub">Synthetic data · 500 observations · drag to zoom, double-click to reset</p>
    <div class="grid">
      <div id="box" class="plot" role="img" aria-label="Box plot distribution"></div>
      <div id="hist" class="plot" role="img" aria-label="Histogram with density"></div>
      <div id="scatter" class="plot" role="img" aria-label="Scatter plot with trend"></div>
      <div id="heatmap" class="plot" role="img" aria-label="Correlation heatmap"></div>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/plotly.js-dist@2.35.2/plotly.js"></script>
  <script>
    /* ── Shared helpers ── */
    const DL = {
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor:  'rgba(0,0,0,0)',
      font: { color: '#94a3b8', family: 'Segoe UI, sans-serif', size: 12 },
      margin: { t: 30, r: 15, b: 40, l: 50 },
      xaxis: { gridcolor: 'rgba(255,255,255,0.06)' },
      yaxis: { gridcolor: 'rgba(255,255,255,0.06)' },
      colorway: ['#6366f1','#8b5cf6','#ec4899','#22c55e'],
      hoverlabel: { bgcolor: '#1e293b', bordercolor: '#334155', font: { color: '#e2e8f0', size: 12 } },
    };
    const CFG = { responsive: true, displayModeBar: false };

    /* ── Generate synthetic data ── */
    const N = 500;
    const randn = () => { let u=0, v=0; while(!u) u=Math.random(); v=Math.random(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); };
    const groupA = Array.from({length: N}, () => randn() * 15 + 60);
    const groupB = Array.from({length: N}, () => randn() * 20 + 75);
    const groupC = Array.from({length: N}, () => randn() * 10 + 50);

    /* ── 1. Box Plot ── */
    Plotly.newPlot('box', [
      { y: groupA, type: 'box', name: 'Group A', marker: { color: '#6366f1' }, boxmean: 'sd' },
      { y: groupB, type: 'box', name: 'Group B', marker: { color: '#8b5cf6' }, boxmean: 'sd' },
      { y: groupC, type: 'box', name: 'Group C', marker: { color: '#ec4899' }, boxmean: 'sd' },
    ], { ...DL, title: { text: 'Distribution', font: { color: '#f1f5f9', size: 14 } } }, CFG);

    /* ── 2. Histogram ── */
    Plotly.newPlot('hist', [
      { x: groupA, type: 'histogram', name: 'Group A', opacity: 0.7, marker: { color: '#6366f1' }, nbinsx: 25 },
      { x: groupB, type: 'histogram', name: 'Group B', opacity: 0.7, marker: { color: '#8b5cf6' }, nbinsx: 25 },
    ], { ...DL, barmode: 'overlay', title: { text: 'Frequency', font: { color: '#f1f5f9', size: 14 } } }, CFG);

    /* ── 3. Scatter ── */
    const scX = groupA.slice(0, 200);
    const scY = scX.map((v, i) => v * 0.8 + randn() * 10 + groupB[i] * 0.1);
    Plotly.newPlot('scatter', [
      { x: scX, y: scY, mode: 'markers', type: 'scatter', marker: { size: 5, color: '#6366f1', opacity: 0.7 } },
      { x: scX.sort((a,b) => a-b), y: scX.sort((a,b) => a-b).map(v => v * 0.9 + 10), mode: 'lines', name: 'Trend', line: { color: '#f43f5e', dash: 'dash', width: 2 } },
    ], { ...DL, showlegend: false, title: { text: 'Correlation', font: { color: '#f1f5f9', size: 14 } } }, CFG);

    /* ── 4. Heatmap ── */
    const labels = ['A','B','C','D','E'];
    const matrix = labels.map(() => labels.map(() => +(Math.random() * 2 - 1).toFixed(2)));
    labels.forEach((_, i) => { matrix[i][i] = 1.0; });
    Plotly.newPlot('heatmap', [{
      z: matrix, x: labels, y: labels, type: 'heatmap',
      colorscale: [[0,'#312e81'],[0.5,'#1e1b4b'],[1,'#6366f1']],
      text: matrix.map(r => r.map(v => v.toFixed(2))), texttemplate: '%{text}',
      colorbar: { tickfont: { color: '#94a3b8' } },
    }], { ...DL, title: { text: 'Correlation Matrix', font: { color: '#f1f5f9', size: 14 } } }, CFG);
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Opaque `paper_bgcolor` / `plot_bgcolor`** — set both to `rgba(0,0,0,0)` so the dark card background shows through; a white default instantly breaks the theme
- **Redundant layout title** — the HTML `<h1>` handles the main title; adding `layout.title` creates a cluttered double title (OK for subplot panel labels)
- **Forgetting `responsive: true`** — always pass `{ responsive: true }` in the config object; without it the chart won't resize on window changes
- **Using `scatter` for 100K+ points** — switch to `scattergl` for WebGL rendering; regular SVG-based scatter chokes above ~50K points
- **Not removing `displaylogo`** — set `displaylogo: false` to hide the Plotly watermark and keep the modebar clean
- **Ignoring `hovertemplate`** — default hover labels are often messy; use `hovertemplate: '<b>%{x}</b><br>%{y:,.0f}<extra></extra>'` for clean formatting
- **3D scenes without explicit axis config** — always set `scene.xaxis`, `scene.yaxis`, `scene.zaxis` with matching dark colors; otherwise they default to white backgrounds
- **Placing `<script>` before CDN** — always load `plotly-2.35.2.min.js` first, then your code
- **Calling `Plotly.newPlot` on a non-existent div** — ensure the target `<div id="chart">` exists in the DOM before calling `Plotly.newPlot`
