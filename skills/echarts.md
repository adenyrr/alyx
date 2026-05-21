---
name: echarts
description: Create high-density, interactive data visualizations using Apache ECharts 5, delivered as self-contained HTML artifacts. Use this skill whenever the request involves large datasets (>1000 points), financial charts (candlestick, OHLC, K-line), uncommon chart types (gauge, sankey, treemap, sunburst, parallel coordinates, calendar heatmap, graph/relation, themeRiver, 3D scatter), or polished business dashboards with rich tooltips, brush selection, dataZoom, and toolbox export. Trigger on requests like "plot a candlestick chart", "show stock data with volume", "build a heatmap calendar", "render a sankey of flows", "treemap of categories", "gauge for KPI", "3D scatter", or any data viz where Chart.js would feel limited. Do NOT use for: simple bar/line/pie under 1000 points (→ chartjs skill), scientific 3D surfaces (→ plotly skill), node-edge network graphs (→ vis-network skill), or geographic tile maps (→ leaflet-maps / maplibre skill).
agents: [dev]
---

# Apache ECharts Skill — v5

Apache ECharts is a battle-tested, canvas/SVG charting library (~1 MB) from the Apache Software Foundation. It scales effortlessly to hundreds of thousands of points, ships ~30 built-in chart types, supports rich interactivity (dataZoom, brush, animations, transitions between series), and exposes a single declarative `option` object that describes every aspect of the chart. It is the right tool when Chart.js feels too simple and Plotly feels too scientific.

---

## Artifact Presentation & Use Cases

Every ECharts artifact is a self-contained HTML page with a dark theme by default. The visual structure follows the standard project pattern:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the chart
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes what is being shown
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) provides context and interaction hints
- **Chart container** (`#chart`, fixed height, transparent background) renders the chart, automatically resized via `chart.resize()`

### Typical use cases

- **Finance dashboards** — candlestick + volume + MA overlay with dataZoom for navigation
- **Calendar heatmaps** — GitHub-style commit activity, daily metrics over a year
- **Sankey / Treemap / Sunburst** — flow analysis, budget breakdowns, hierarchical categories
- **Gauges & KPI dials** — single-metric speedometers with animated needles
- **Large scatter plots** — 100K+ points with WebGL (`echarts-gl`) and brush selection
- **Network/graph charts** — relationship visualizations with force layout
- **Multi-axis time series** — temperature + humidity + pressure with separate y-axes

### What the user sees

A polished, interactive chart: hover anywhere for a styled tooltip; the legend at the top toggles series; the bottom dataZoom slider scrubs through time ranges; the toolbox (top-right) exports PNG, restores defaults, and switches between line and bar. The dark card sits on a dark page, the accent color (`#6366f1`) drives data emphasis.

---

## When to Use ECharts vs. Alternatives

| Use ECharts when… | Use another library when… |
|---|---|
| Datasets > 1,000 points (handles 1M with progressive) | < 200 points, simple chart types → **Chart.js** |
| Candlestick / OHLC / K-line financial charts | Scientific 3D surfaces, contour, isosurface → **Plotly** |
| Sankey, treemap, sunburst, parallel, themeRiver | Bespoke SVG layouts, force-directed graphs → **D3** |
| Gauges, calendar heatmaps, funnel | Tile-based geographic maps → **Leaflet / MapLibre** |
| Brush selection, linked dashboards | Editable node-link graphs → **JointJS** |
| Need built-in dataZoom, toolbox, animation | Standard dashboard chart in < 50 lines → **Chart.js** |
| 3D scatter via `echarts-gl` | Real-time WebGL particles → **Three.js / p5.js** |

> **Rule of thumb:** if the chart type starts with "candle", "sankey", "tree", "calendar", "gauge", "sunburst", "themeRiver", "parallel", or "graph" — reach for ECharts. If the dataset is over 1,000 points and Chart.js feels slow, switch to ECharts. For scientific or statistical work, Plotly is still the right call.

---

## Step 1 — CDN Setup

```html
<!-- Core (covers every common chart type) -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
```

### Optional add-ons (load after `echarts.min.js`)
```html
<!-- 3D charts: scatter3D, bar3D, surface, globe -->
<script src="https://cdn.jsdelivr.net/npm/echarts-gl@2/dist/echarts-gl.min.js"></script>

<!-- World/country GeoJSON maps -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5/map/js/world.js"></script>

<!-- Statistics helpers (regression, histogram, clustering) -->
<script src="https://cdn.jsdelivr.net/npm/echarts-stat@1/dist/ecStat.min.js"></script>
```

> **Critical:** the chart container **must have an explicit CSS height** (e.g., `height: 480px`). Without it, the chart renders as a 0px-tall blank area — the most common ECharts mistake.

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
      max-width: 1000px;
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
    #chart { width: 100%; height: 480px; }   /* REQUIRED explicit height */
  </style>
</head>
<body>
  <main class="card" role="region" aria-label="Chart">
    <h1>Chart Title</h1>
    <p class="sub">Data source · hover for details · drag the bottom slider to zoom</p>
    <div id="chart" role="img" aria-label="Descriptive chart label"></div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <script>
    // All ECharts code here
  </script>
</body>
</html>
```

---

## Step 3 — Themes (dark default + light alternative)

ECharts can be themed by either (a) passing a theme name as the second argument of `echarts.init` after registering it, or (b) setting per-option color tokens. The simplest pattern is a JS palette object that you reference in every `option`.

### Dark theme tokens (default)

```javascript
const DARK = {
  bg:      '#0f1117',
  card:    '#1a1d27',
  border:  'rgba(255,255,255,0.08)',
  text:    '#e2e8f0',
  muted:   '#94a3b8',
  faint:   '#475569',
  accent:  '#6366f1',
  grid:    'rgba(255,255,255,0.06)',
  axisLine:'rgba(255,255,255,0.15)',
  palette: ['#6366f1','#8b5cf6','#ec4899','#06b6d4','#22c55e','#eab308','#f97316','#f43f5e'],
  upColor:   '#22c55e',   // bullish candle
  downColor: '#f43f5e',   // bearish candle
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
  faint:   '#94a3b8',
  accent:  '#6366f1',
  grid:    'rgba(0,0,0,0.06)',
  axisLine:'rgba(0,0,0,0.15)',
  palette: ['#6366f1','#8b5cf6','#ec4899','#06b6d4','#22c55e','#eab308','#f97316','#f43f5e'],
  upColor:   '#16a34a',
  downColor: '#dc2626',
};
```

### Theme switcher via `data-theme` attribute

```html
<body data-theme="dark">
  <button id="themeToggle" aria-label="Toggle theme">Switch theme</button>
  <!-- … -->
</body>
<script>
  const themes = { dark: DARK, light: LIGHT };
  let current = document.body.dataset.theme || 'dark';

  function buildOption(t) {
    return {
      backgroundColor: 'transparent',
      color: t.palette,
      textStyle: { color: t.text, fontFamily: 'Segoe UI, sans-serif' },
      title:   { textStyle: { color: t.text }, subtextStyle: { color: t.muted } },
      legend:  { textStyle: { color: t.muted } },
      tooltip: {
        backgroundColor: t.card,
        borderColor: t.border,
        textStyle: { color: t.text },
        extraCssText: 'box-shadow: 0 8px 32px rgba(0,0,0,0.4); border-radius: 10px;',
      },
      xAxis: { axisLine: { lineStyle: { color: t.axisLine } }, splitLine: { lineStyle: { color: t.grid } }, axisLabel: { color: t.muted } },
      yAxis: { axisLine: { lineStyle: { color: t.axisLine } }, splitLine: { lineStyle: { color: t.grid } }, axisLabel: { color: t.muted } },
    };
  }

  // Or follow OS preference:
  // current = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';

  document.getElementById('themeToggle').addEventListener('click', () => {
    current = current === 'dark' ? 'light' : 'dark';
    document.body.dataset.theme = current;
    document.body.style.background = themes[current].bg;
    chart.setOption(buildOption(themes[current]), true);
  });
</script>
```

> Always set `backgroundColor: 'transparent'` so the chart inherits the card surface, never paints a hard rectangle.

---

## Step 4 — Initialisation & the `option` Object

```javascript
const chart = echarts.init(document.getElementById('chart'), null, {
  renderer:  'canvas',   // 'canvas' (fast, default) or 'svg' (crisp, exportable)
  useDirtyRect: true,    // partial redraws — large wins on big datasets
});

chart.setOption({
  backgroundColor: 'transparent',
  color: DARK.palette,
  title:   { text: 'Sales 2024', left: 0, textStyle: { color: DARK.text, fontSize: 14, fontWeight: 600 } },
  tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
  legend:  { top: 0, right: 0, textStyle: { color: DARK.muted } },
  grid:    { left: 40, right: 24, top: 48, bottom: 56, containLabel: true },
  xAxis:   { type: 'category', data: ['Jan','Feb','Mar','Apr','May','Jun'] },
  yAxis:   { type: 'value' },
  series:  [{ name: 'Revenue', type: 'bar', data: [120, 200, 150, 80, 70, 110], itemStyle: { borderRadius: [6, 6, 0, 0] } }],
});

// Make it responsive
window.addEventListener('resize', () => chart.resize());
```

### Anatomy of `option`

| Key | Purpose |
|---|---|
| `title` | Top-left title + optional subtext |
| `tooltip` | `trigger: 'axis' | 'item'`, formatter, axisPointer |
| `legend` | Series toggles, position, icons |
| `grid` | Chart drawing area (left/right/top/bottom margins) |
| `xAxis`, `yAxis` | Axis type (`category`, `value`, `time`, `log`), data, splitLine |
| `series` | Array of chart series — the actual data + render type |
| `dataZoom` | Bottom slider / inside-pan zoom |
| `toolbox` | Built-in actions: saveAsImage, restore, dataView, magicType |
| `dataset` | Shared dataset with `source` + `transform` |
| `visualMap` | Value-to-color/size mapping (heatmaps, choropleths) |
| `brush` | Box / lasso selection across series |

---

## Step 5 — Core Chart Types

### 5.1 — Bar (with rounded tops + gradient)

```javascript
series: [{
  type: 'bar',
  data: [120, 200, 150, 80, 70, 110],
  itemStyle: {
    borderRadius: [6, 6, 0, 0],
    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
      { offset: 0, color: '#818cf8' },
      { offset: 1, color: '#6366f1' },
    ]),
  },
  emphasis: { itemStyle: { color: '#a5b4fc' } },
}]
```

### 5.2 — Line / Area (smooth with gradient fill)

```javascript
series: [{
  type: 'line',
  smooth: true,
  symbol: 'circle',
  symbolSize: 6,
  data: [820, 932, 901, 934, 1290, 1330, 1320],
  lineStyle: { width: 2.5, color: '#6366f1' },
  itemStyle: { color: '#6366f1', borderColor: '#1a1d27', borderWidth: 2 },
  areaStyle: {
    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
      { offset: 0, color: 'rgba(99,102,241,0.45)' },
      { offset: 1, color: 'rgba(99,102,241,0.02)' },
    ]),
  },
}]
```

### 5.3 — Candlestick (OHLC for finance)

```javascript
// Data format: [open, close, low, high]
const ohlc = [
  [20, 34, 10, 38], [40, 35, 30, 50], [31, 38, 33, 44],
  [38, 15, 5, 42],  [15, 10, 5, 22],
];

option = {
  xAxis: { data: ['2024-05-01','2024-05-02','2024-05-03','2024-05-04','2024-05-05'] },
  yAxis: {},
  series: [{
    type: 'candlestick',
    data: ohlc,
    itemStyle: {
      color:        DARK.upColor,        // bullish body
      color0:       DARK.downColor,      // bearish body
      borderColor:  DARK.upColor,        // bullish border
      borderColor0: DARK.downColor,      // bearish border
    },
  }],
  tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
};
```

### 5.4 — Pie / Donut (with center label)

```javascript
series: [{
  type: 'pie',
  radius: ['55%', '78%'],         // [inner, outer] — array makes a donut
  avoidLabelOverlap: true,
  itemStyle: { borderColor: DARK.card, borderWidth: 4, borderRadius: 6 },
  label: { show: true, color: DARK.muted, formatter: '{b}\n{d}%' },
  labelLine: { lineStyle: { color: DARK.faint } },
  data: [
    { value: 1048, name: 'Search' },
    { value: 735,  name: 'Direct' },
    { value: 580,  name: 'Email'  },
    { value: 484,  name: 'Affiliate' },
  ],
}]
```

### 5.5 — Gauge

```javascript
series: [{
  type: 'gauge',
  min: 0, max: 100,
  startAngle: 200, endAngle: -20,
  progress: { show: true, width: 18, itemStyle: { color: DARK.accent } },
  axisLine:  { lineStyle: { width: 18, color: [[1, 'rgba(255,255,255,0.06)']] } },
  axisTick:  { show: false },
  splitLine: { length: 12, lineStyle: { color: DARK.faint } },
  axisLabel: { color: DARK.muted, distance: 18, fontSize: 11 },
  pointer:   { show: false },
  anchor:    { show: false },
  title:     { show: false },
  detail: {
    valueAnimation: true,
    offsetCenter: [0, 0],
    color: DARK.text,
    fontSize: 36,
    fontWeight: 700,
    formatter: '{value}%',
  },
  data: [{ value: 72 }],
}]
```

### 5.6 — Sankey (flows)

```javascript
series: [{
  type: 'sankey',
  data: [
    { name: 'Revenue' }, { name: 'COGS' }, { name: 'Opex' },
    { name: 'R&D' }, { name: 'Marketing' }, { name: 'Profit' },
  ],
  links: [
    { source: 'Revenue', target: 'COGS',      value: 40 },
    { source: 'Revenue', target: 'Opex',      value: 35 },
    { source: 'Revenue', target: 'Profit',    value: 25 },
    { source: 'Opex',    target: 'R&D',       value: 15 },
    { source: 'Opex',    target: 'Marketing', value: 20 },
  ],
  emphasis: { focus: 'adjacency' },
  lineStyle: { color: 'gradient', curveness: 0.5, opacity: 0.5 },
  itemStyle: { borderColor: 'transparent' },
  label: { color: DARK.text, fontSize: 12 },
}]
```

### 5.7 — Treemap

```javascript
series: [{
  type: 'treemap',
  data: [
    { name: 'Engineering', value: 120, children: [
      { name: 'Backend',  value: 70 },
      { name: 'Frontend', value: 50 },
    ]},
    { name: 'Sales',     value: 80 },
    { name: 'Marketing', value: 60 },
  ],
  roam: false,
  nodeClick: 'zoomToNode',
  itemStyle: { gapWidth: 2, borderColor: DARK.card, borderRadius: 4 },
  label: { color: '#fff', fontSize: 12 },
  upperLabel: { show: true, color: DARK.text, height: 24 },
  breadcrumb: { itemStyle: { color: DARK.card, borderColor: DARK.border, textStyle: { color: DARK.muted } } },
}]
```

### 5.8 — Calendar Heatmap

```javascript
visualMap: {
  min: 0, max: 100, calculable: true, orient: 'horizontal',
  left: 'center', bottom: 8, textStyle: { color: DARK.muted },
  inRange: { color: ['#1e2130','#3730a3','#6366f1','#a5b4fc','#ede9fe'] },
},
calendar: {
  range: '2024',
  cellSize: ['auto', 14],
  itemStyle: { color: '#1e2130', borderColor: DARK.bg, borderWidth: 2 },
  dayLabel: { color: DARK.muted },
  monthLabel: { color: DARK.text, fontWeight: 600 },
  yearLabel: { show: false },
  splitLine: { show: false },
},
series: [{
  type: 'heatmap',
  coordinateSystem: 'calendar',
  data: generateDailyData(),   // [['2024-01-01', 42], ['2024-01-02', 17], …]
}]
```

### 5.9 — 3D Scatter (`echarts-gl`)

```javascript
// Requires: <script src="https://cdn.jsdelivr.net/npm/echarts-gl@2/dist/echarts-gl.min.js"></script>
option = {
  grid3D: { viewControl: { autoRotate: true, autoRotateSpeed: 6 }, axisLine: { lineStyle: { color: DARK.muted } } },
  xAxis3D: { type: 'value' },
  yAxis3D: { type: 'value' },
  zAxis3D: { type: 'value' },
  series: [{
    type: 'scatter3D',
    symbolSize: 8,
    data: points,                   // [[x, y, z], …]
    itemStyle: { color: DARK.accent, opacity: 0.85 },
    emphasis: { itemStyle: { color: '#ec4899' } },
  }],
};
```

---

## Step 6 — Dataset & Transforms

ECharts encourages a normalised `dataset.source` so multiple series share data and reactive transforms can filter/sort/aggregate without rebuilding it.

```javascript
chart.setOption({
  dataset: [
    {
      // Source: a 2D array with a header row (or an array of objects)
      source: [
        ['product', 'q1', 'q2', 'q3', 'q4'],
        ['Alpha',     43,   85,   93,  130],
        ['Beta',      83,   73,   55,   53],
        ['Gamma',     86,   65,   82,   53],
      ],
    },
    {
      transform: { type: 'sort', config: { dimension: 'q4', order: 'desc' } },
    },
  ],
  xAxis: { type: 'category' },
  yAxis: {},
  series: [
    { type: 'bar', datasetIndex: 1, encode: { x: 'product', y: 'q4' } },
  ],
});
```

Built-in transforms: `filter`, `sort`. The companion `echarts-stat` plugin adds `regression`, `histogram`, `clustering`.

---

## Step 7 — DataZoom, Toolbox, Brush

```javascript
dataZoom: [
  { type: 'inside', start: 60, end: 100 },                    // pan + wheel zoom on the chart
  { type: 'slider', start: 60, end: 100, height: 22,
    handleStyle: { color: DARK.accent },
    textStyle: { color: DARK.muted },
    borderColor: DARK.border,
    backgroundColor: 'transparent',
    fillerColor: 'rgba(99,102,241,0.18)' },
],

toolbox: {
  right: 0,
  iconStyle: { borderColor: DARK.muted },
  emphasis: { iconStyle: { borderColor: DARK.accent } },
  feature: {
    dataZoom:    { yAxisIndex: 'none' },
    restore:     {},
    saveAsImage: { backgroundColor: DARK.card, name: 'chart' },
    magicType:   { type: ['line', 'bar', 'stack'] },
  },
},

brush: { toolbox: ['rect', 'polygon', 'clear'], xAxisIndex: 0, brushStyle: { color: 'rgba(99,102,241,0.15)' } },
```

---

## Step 8 — Events

```javascript
// Click on a data item
chart.on('click', (params) => {
  console.log(params.seriesName, params.name, params.value);
});

// Hover over an axis category
chart.on('updateAxisPointer', (e) => {
  if (e.axesInfo?.[0]) document.getElementById('hint').textContent = e.axesInfo[0].value;
});

// Brush selection finished — read out selected indices per series
chart.on('brushEnd', (params) => {
  const indices = params.batch[0].selected[0].dataIndex;
  console.log(`Selected ${indices.length} points`);
});

// Legend toggled
chart.on('legendselectchanged', (e) => console.log(e.name, e.selected));

// Detach listeners before destruction
chart.off('click');
chart.dispose();
```

---

## Step 9 — Programmatic Updates

```javascript
// Merge-update — preserves any key you don't pass
chart.setOption({ series: [{ data: newData }] });

// Replace-update — second arg `true` clears the previous option entirely
chart.setOption(buildOption(DARK), true);

// Loading indicator
chart.showLoading('default', { text: 'Loading…', color: DARK.accent, textColor: DARK.text, maskColor: 'rgba(15,17,23,0.85)' });
fetch('/data.json').then(r => r.json()).then(rows => {
  chart.hideLoading();
  chart.setOption({ series: [{ data: rows }] });
});
```

---

## Step 10 — Performance for Large Datasets

```javascript
series: [{
  type: 'scatter',
  data: bigArray,           // 100K+ points
  large:          true,     // bucket renderer
  largeThreshold: 2000,     // turn on `large` at this size
  progressive:    4000,     // chunk size for streaming render
  progressiveThreshold: 10000,
  sampling: 'lttb',         // line charts: keep visual shape, drop points
  symbolSize: 4,
}]
```

Other tips: use `useDirtyRect: true` in `echarts.init`, prefer `canvas` over `svg` for > 5K points, share a single `dataset` across series instead of duplicating arrays.

---

## Step 11 — Accessibility

- Wrap the chart container in a landmark and label it: `<div id="chart" role="img" aria-label="Q4 revenue by region"></div>`
- ECharts has built-in ARIA support via the top-level `aria` option:
  ```javascript
  option.aria = {
    enabled: true,
    label:   { description: 'Quarterly revenue bar chart with 4 series' },
    decal:   { show: true },   // adds pattern fills for colorblind users
  };
  ```
- Keyboard: native keyboard interaction on dataZoom / toolbox is limited — provide alternate controls (filter buttons) for any interaction that gates content
- Maintain ≥ 3:1 contrast between data colors and the card background; the `decal` option layers SVG patterns on series so meaning isn't carried by color alone

---

## Step 12 — Design & Polish Guidelines

- **Always `backgroundColor: 'transparent'`** so the chart sits flush in the card
- **Rounded bar tops** with `itemStyle.borderRadius: [6, 6, 0, 0]` for a modern look
- **Smooth lines** with `smooth: true` for trends; keep `smooth: false` on financial/precise data
- **Gradient fills** via `echarts.graphic.LinearGradient` add depth without noise
- **Grid breathing room** — `grid: { left: 40, right: 24, top: 48, bottom: 56, containLabel: true }`
- **Hide axis tick marks** (`axisTick: { show: false }`) and keep splitLines subtle (`rgba(255,255,255,0.06)`)
- **Tooltip styling** — match the card palette, soft shadow, 10px radius, never default white
- **Entrance animation** — keep `animation: true` (default) and tune `animationDuration: 800, animationEasing: 'cubicOut'`
- **Always call `chart.resize()` on window resize** — otherwise the canvas doesn't reflow

---

## Step 13 — Complete Example: Finance Dashboard (candlestick + volume + MA)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AAPL — 90-day candlestick</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; padding: 24px; display: flex; align-items: center; justify-content: center; }
    .card { width: 100%; max-width: 1080px; background: #1a1d27; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 28px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    .head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; gap: 12px; flex-wrap: wrap; }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; }
    .price { font-size: 1.6rem; font-weight: 700; color: #f1f5f9; font-variant-numeric: tabular-nums; }
    .delta { color: #22c55e; font-size: 0.85rem; font-weight: 600; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
    #chart { width: 100%; height: 540px; }
  </style>
</head>
<body>
  <main class="card" role="region" aria-label="AAPL price chart">
    <div class="head">
      <div>
        <h1>AAPL — 90-day candlestick</h1>
        <p class="sub">Daily OHLC + volume + 20-day moving average · drag the slider to zoom</p>
      </div>
      <div style="text-align:right">
        <div class="price">$214.32</div>
        <div class="delta">+ 1.84 (0.87%)</div>
      </div>
    </div>
    <div id="chart" role="img" aria-label="Apple stock 90-day candlestick chart with volume and 20-day moving average"></div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <script>
    const DARK = {
      bg: '#0f1117', card: '#1a1d27', text: '#e2e8f0', muted: '#94a3b8', faint: '#475569',
      accent: '#6366f1', grid: 'rgba(255,255,255,0.06)', axisLine: 'rgba(255,255,255,0.15)',
      upColor: '#22c55e', downColor: '#f43f5e',
    };

    // ── Synthetic OHLC walk ───────────────────────────────────
    const days  = 90;
    const dates = [];
    const ohlc  = [];   // [open, close, low, high]
    const vols  = [];
    let last = 198;
    const start = new Date(2024, 1, 1);
    for (let i = 0; i < days; i++) {
      const d = new Date(start); d.setDate(start.getDate() + i);
      dates.push(d.toISOString().slice(0, 10));
      const open  = last + (Math.random() - 0.5) * 2;
      const close = open  + (Math.random() - 0.48) * 4;
      const low   = Math.min(open, close) - Math.random() * 2;
      const high  = Math.max(open, close) + Math.random() * 2;
      ohlc.push([+open.toFixed(2), +close.toFixed(2), +low.toFixed(2), +high.toFixed(2)]);
      vols.push([i, Math.round(800000 + Math.random() * 600000), close >= open ? 1 : -1]);
      last = close;
    }

    // ── 20-day moving average ────────────────────────────────
    function ma(period) {
      const out = [];
      for (let i = 0; i < ohlc.length; i++) {
        if (i < period) { out.push('-'); continue; }
        let sum = 0;
        for (let j = 0; j < period; j++) sum += ohlc[i - j][1];
        out.push(+(sum / period).toFixed(2));
      }
      return out;
    }

    const chart = echarts.init(document.getElementById('chart'), null, { renderer: 'canvas', useDirtyRect: true });

    chart.setOption({
      backgroundColor: 'transparent',
      animation: true, animationDuration: 700, animationEasing: 'cubicOut',
      aria: { enabled: true, label: { description: 'Candlestick chart' }, decal: { show: false } },

      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross', crossStyle: { color: DARK.faint } },
        backgroundColor: DARK.card, borderColor: 'rgba(255,255,255,0.1)',
        textStyle: { color: DARK.text, fontSize: 12 },
        extraCssText: 'box-shadow: 0 8px 32px rgba(0,0,0,0.5); border-radius: 10px; padding: 10px 14px;',
      },

      legend: {
        top: 0, right: 0, textStyle: { color: DARK.muted },
        data: ['Price', 'MA20', 'Volume'],
      },

      grid: [
        { left: 50, right: 24, top: 40,  height: '60%' },
        { left: 50, right: 24, top: '78%', height: '14%' },
      ],

      xAxis: [
        { type: 'category', data: dates,
          axisLine: { lineStyle: { color: DARK.axisLine } },
          axisLabel: { color: DARK.muted, fontSize: 10 },
          splitLine: { show: false } },
        { type: 'category', gridIndex: 1, data: dates, axisLabel: { show: false }, axisTick: { show: false }, axisLine: { show: false } },
      ],

      yAxis: [
        { scale: true, axisLine: { show: false }, axisLabel: { color: DARK.muted, formatter: '${value}' },
          splitLine: { lineStyle: { color: DARK.grid } } },
        { gridIndex: 1, scale: true, axisLine: { show: false }, axisLabel: { show: false }, splitLine: { show: false } },
      ],

      dataZoom: [
        { type: 'inside',  xAxisIndex: [0, 1], start: 50, end: 100 },
        { type: 'slider',  xAxisIndex: [0, 1], start: 50, end: 100, height: 20, bottom: 6,
          borderColor: 'transparent', backgroundColor: 'transparent',
          fillerColor: 'rgba(99,102,241,0.18)', handleStyle: { color: DARK.accent },
          textStyle: { color: DARK.muted, fontSize: 10 } },
      ],

      toolbox: {
        right: 96, iconStyle: { borderColor: DARK.muted },
        feature: { restore: {}, saveAsImage: { backgroundColor: DARK.card, name: 'aapl' } },
      },

      series: [
        {
          name: 'Price', type: 'candlestick', data: ohlc,
          itemStyle: {
            color: DARK.upColor, color0: DARK.downColor,
            borderColor: DARK.upColor, borderColor0: DARK.downColor,
            borderWidth: 1.5,
          },
        },
        {
          name: 'MA20', type: 'line', data: ma(20),
          smooth: true, symbol: 'none',
          lineStyle: { color: DARK.accent, width: 2, opacity: 0.9 },
          tooltip: { show: true },
        },
        {
          name: 'Volume', type: 'bar',
          xAxisIndex: 1, yAxisIndex: 1,
          data: vols.map(v => ({ value: v[1], itemStyle: { color: v[2] > 0 ? 'rgba(34,197,94,0.55)' : 'rgba(244,63,94,0.55)' } })),
        },
      ],
    });

    window.addEventListener('resize', () => chart.resize());
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No height on the chart container** — `<div id="chart">` with `height: 0` or `height: auto` renders nothing. Always set explicit pixel or `vh` height in CSS
- **Forgetting `chart.resize()` on window resize** — the canvas keeps its initial pixel size; charts look cropped on narrow viewports
- **Setting `backgroundColor` to a hex value** — paints a hard rectangle over the card. Use `'transparent'` and let the card surface show through
- **Re-creating the chart on every update** — call `chart.setOption({...})` instead; ECharts diffs and animates between states. Re-creating leaks the previous canvas
- **Not calling `chart.dispose()` before re-init** — leads to "There is a chart instance already initialized on the dom" warnings and memory leaks
- **Using `svg` renderer for > 5K points** — switch to `canvas` (default) for any scatter/line with thousands of points
- **`category` axis for time series** — use `xAxis: { type: 'time' }` so labels auto-format and zoom snaps to natural intervals
- **Mixing dataset and series `data` arrays** — pick one source of truth; mixing them silently uses the series array and ignores the dataset
- **Loading `echarts-gl` before `echarts.min.js`** — the GL bundle extends the `echarts` global; load order matters
- **Candlestick data in wrong order** — ECharts expects `[open, close, low, high]`, not the more common `[open, high, low, close]`. Swapping them produces inverted candles
