---
name: chartjs
description: Create polished, interactive data charts using Chart.js v4, delivered as self-contained HTML artifacts. Use this skill for standard data visualization: bar charts, line charts, pie/donut charts, radar charts, polar area charts, scatter plots, bubble charts, and mixed charts. Trigger on requests to visualize metrics, compare values, build dashboards, show trends, create presentation-ready charts, or plot datasets — even without explicit mention of Chart.js. Do NOT use for: scientific/statistical charts like box plots, violins, 3D surfaces (→ plotly skill), network graphs (→ vis-network skill), timelines or Gantt charts (→ vis-timeline skill), or bespoke SVG visualizations with custom layouts (→ d3-charting skill).
---

# Chart.js Skill — v4

Chart.js is a lightweight (~200 KB), canvas-based charting library that produces clean, responsive charts with minimal configuration. It covers the most common chart types (bar, line, pie, doughnut, radar, scatter, bubble, polar area) and supports mixed charts, staggered animations, custom plugins, and dark theming out of the box.

---

## Artifact Presentation & Use Cases

Every Chart.js artifact is a self-contained HTML page with a dark theme. The visual structure follows this pattern:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the chart
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the chart
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context, data source, or interaction hints
- **Canvas element** renders the chart, automatically responsive via `responsive: true`

### Typical use cases

- **Dashboard KPI cards** — bar/line charts showing revenue, users, or metrics over time
- **Comparison charts** — grouped/stacked bar charts comparing categories or time periods
- **Distribution displays** — pie/doughnut charts for market share, budget breakdowns, survey results
- **Trend analysis** — line charts with area fill showing growth, performance, or seasonal patterns
- **Multi-metric overlays** — mixed charts (bar + line on dual axes) for volume vs. price, cost vs. revenue
- **Radar/spider charts** — skill assessments, product comparisons, multi-dimensional scoring

### What the user sees

An immediately interactive chart: hover over any data point for a tooltip, click legend items to toggle series visibility, and the chart smoothly animates on load. The dark card provides a polished, modern aesthetic suitable for presentations and dashboards.

---

## When to Use Chart.js vs. Alternatives

| Use Chart.js when… | Use another library when… |
|---|---|
| Standard chart types (bar, line, pie, scatter, radar) | Statistical charts: box, violin, histogram, heatmap → **Plotly** |
| Quick setup, minimal code | Financial charts: candlestick, OHLC → **Plotly** |
| Dashboards and presentations | 3D surfaces, WebGL scatter → **Plotly** |
| ≤ 100,000 data points | 100K+ data points with WebGL → **Plotly** (`scattergl`) |
| Lightweight bundle (~200 KB) | Deep zoom/pan, lasso select, range sliders → **Plotly** |
| Simple tooltip and legend interaction | Bespoke SVG layouts, force graphs, geo maps → **D3** |
| Mixed chart types (bar + line) | Node-edge network graphs → **vis-network** |

> **Rule of thumb:** if it's a standard chart for a dashboard or presentation, Chart.js is the fastest path. For scientific, statistical, financial, or deeply interactive charts, use Plotly.

---

## Step 1 — CDN Setup

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>
```

### Optional plugin — data labels
```html
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
```

> **⚠️ Critical:** with the UMD build, all chart types and components auto-register. Do NOT call `Chart.register()` manually — it is unnecessary and may cause duplicate registrations.

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
      max-width: 900px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 24px; }
    canvas { max-width: 100%; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Chart Title</h1>
    <p class="sub">Data source or description · hover for details</p>
    <canvas id="chart"></canvas>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>
  <script>
    // All Chart.js code here
  </script>
</body>
</html>
```

---

## Step 3 — Dark Theme Reference

Chart.js uses global defaults for theming. Set them once before creating any chart:

```javascript
Chart.defaults.color       = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
Chart.defaults.font.size   = 13;
```

**Theming tokens (dark theme — default):**

| Token | Value |
|---|---|
| Page background | `#0f1117` |
| Card background | `#1a1d27` |
| Grid lines | `rgba(255,255,255,0.06)` |
| Axis text / labels | `#94a3b8` |
| Title | `#f1f5f9` |
| Subtitle | `#64748b` |
| Accent | `#6366f1` |

Light theme alternative: page `#f8fafc`, card `#ffffff`, grid `rgba(0,0,0,0.08)`, text `#475569`.

---

## Step 4 — Minimal Setup

```javascript
Chart.defaults.color       = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';

const chart = new Chart(document.getElementById('chart').getContext('2d'), {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{
      label: 'Revenue',
      data: [120, 190, 150],
      backgroundColor: 'rgba(99,102,241,0.8)',
      borderRadius: 6,
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
  },
});
```

---

## Step 5 — Chart Types Reference

```javascript
// Bar (vertical)
{ type: 'bar' }

// Horizontal bar
{ type: 'bar', options: { indexAxis: 'y' } }

// Line
{ type: 'line' }

// Area (line with fill)
{ type: 'line', datasets: [{ fill: true, backgroundColor: 'rgba(99,102,241,0.12)' }] }

// Pie
{ type: 'pie' }

// Doughnut
{ type: 'doughnut' }

// Radar / Spider
{ type: 'radar' }

// Polar Area
{ type: 'polarArea' }

// Scatter
{ type: 'scatter', data: { datasets: [{ data: [{x:1,y:2}, {x:3,y:4}] }] } }

// Bubble
{ type: 'bubble', data: { datasets: [{ data: [{x:1,y:2,r:10}, {x:3,y:4,r:20}] }] } }
```

---

## Step 6 — Dataset Configuration

```javascript
{
  label:            'Series Name',
  data:             [120, 190, 150],
  backgroundColor:  'rgba(99,102,241,0.8)',
  borderColor:      'rgb(99,102,241)',
  borderWidth:      2,
  borderRadius:     6,          // rounded bar corners
  borderSkipped:    false,      // round all corners (not just top)
  hoverBackgroundColor: 'rgba(99,102,241,1)',

  // Line-specific
  tension:          0.4,        // 0 = straight, 0.4 = smooth curve
  fill:             true,       // area fill below line
  pointRadius:      4,
  pointHoverRadius: 7,
  pointBackgroundColor: '#6366f1',
  pointBorderColor:    '#818cf8',

  // Stacked
  stack:            'stack0',   // same stack name = stacked bars/areas

  // Dual axis
  yAxisID:          'y',        // 'y' (left) or 'y1' (right)
}
```

---

## Step 7 — Color Palettes

```javascript
const VIVID = ['#6366f1','#8b5cf6','#ec4899','#f43f5e','#f97316','#eab308','#22c55e','#06b6d4'];
const SOFT  = ['rgba(99,102,241,0.8)','rgba(139,92,246,0.8)','rgba(236,72,153,0.8)','rgba(34,197,94,0.8)'];
const MONO  = ['#1e3a8a','#1d4ed8','#3b82f6','#60a5fa','#93c5fd','#bfdbfe'];
```

---

## Step 8 — Options & Scales

```javascript
options: {
  responsive:   true,
  aspectRatio:  2,              // width/height ratio; increase for wider charts
  animation:    { duration: 700, easing: 'easeOutQuart' },

  plugins: {
    legend:  { position: 'top', labels: { usePointStyle: true, padding: 16 } },
    tooltip: { mode: 'index', intersect: false },
    title:   { display: false },
  },

  scales: {
    x: {
      grid: { color: 'rgba(255,255,255,0.05)', display: false },
      ticks: { padding: 8 },
    },
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(255,255,255,0.06)' },
      ticks: { callback: v => '$' + v.toLocaleString() },
    },
    // Dual Y axis
    y1: {
      position: 'right',
      grid: { drawOnChartArea: false },
    },
  },
}
```

---

## Step 9 — Mixed Charts (Bar + Line)

```javascript
{
  type: 'bar',   // base type
  data: {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [
      { type: 'bar',  label: 'Volume', data: [420, 580, 510, 690], yAxisID: 'y',  backgroundColor: 'rgba(99,102,241,0.8)', borderRadius: 6 },
      { type: 'line', label: 'Price',  data: [28, 34, 31, 42],     yAxisID: 'y1', borderColor: '#ec4899', tension: 0.3, pointRadius: 4 },
    ]
  },
  options: {
    scales: {
      y:  { position: 'left' },
      y1: { position: 'right', grid: { drawOnChartArea: false } },
    },
  },
}
```

---

## Step 10 — Animation Patterns

```javascript
// Staggered entry — bars appear one by one
animation: {
  delay: (context) => context.dataIndex * 60,
  duration: 600,
  easing: 'easeOutQuart',
}

// Per-property animation
animation: {
  x:       { duration: 0 },
  y:       { duration: 800, easing: 'easeOutBounce' },
  opacity: { from: 0, duration: 500 },
}
```

---

## Step 11 — Custom Plugins (Inline)

```javascript
// Doughnut center text
plugins: [{
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { width, height } } = chart;
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = 'bold 28px Segoe UI';
    ctx.fillStyle = '#f1f5f9';
    ctx.fillText('72%', width / 2, height / 2);
    ctx.restore();
  }
}]

// Background color for the chart area
plugins: [{
  id: 'bgColor',
  beforeDraw(chart) {
    const { ctx, chartArea: { left, top, width, height } } = chart;
    ctx.save();
    ctx.fillStyle = 'rgba(255,255,255,0.02)';
    ctx.fillRect(left, top, width, height);
    ctx.restore();
  }
}]
```

---

## Step 12 — Programmatic Updates

```javascript
// Update data
chart.data.datasets[0].data = [200, 300, 250];
chart.data.labels = ['Apr', 'May', 'Jun'];
chart.update();                 // re-render with animation
chart.update('none');           // re-render without animation

// Add a dataset
chart.data.datasets.push({ label: 'New', data: [50, 60, 70], backgroundColor: '#22c55e' });
chart.update();

// Destroy and recreate
chart.destroy();
```

---

## Step 13 — Design & Polish Guidelines

- **Responsive always** — `responsive: true` (default) — never hardcode pixel widths on the canvas
- **Rounded bars** — `borderRadius: 6` gives a modern look; pair with `borderSkipped: false` for all-corner rounding
- **Smooth curves** — `tension: 0.4` for line/area charts; 0 for financial or precise data
- **Meaningful tooltips** — `mode: 'index', intersect: false` shows all datasets at a given x-value
- **Legend placement** — top for ≤ 4 series, right for more; use `usePointStyle: true` for cleaner dots
- **Grid cleanup** — hide x-axis grid lines (`display: false`), keep y-axis grid subtle (`rgba(255,255,255,0.06)`)
- **Accessibility** — add `aria-label` on the `<canvas>` element: `<canvas id="chart" aria-label="Revenue chart">`
- **Color contrast** — maintain ≥ 3:1 contrast between data colors and background
- **Staggered entry** — `delay: (ctx) => ctx.dataIndex * 60` adds a professional sequential reveal

---

## Step 14 — Complete Example: Multi-Series Bar Chart

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Revenue by Quarter</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 32px; width: 100%; max-width: 820px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 24px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Revenue by Quarter</h1>
    <p class="sub">Fiscal year 2024 — All regions combined · hover for details</p>
    <canvas id="chart" aria-label="Revenue by quarter bar chart"></canvas>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>
  <script>
    Chart.defaults.color       = '#94a3b8';
    Chart.defaults.borderColor = 'rgba(255,255,255,0.07)';
    Chart.defaults.font.family = 'Segoe UI, sans-serif';

    new Chart(document.getElementById('chart').getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [
          { label: 'North America', data: [420, 580, 510, 690], backgroundColor: 'rgba(99,102,241,0.85)',  borderRadius: 6 },
          { label: 'Europe',        data: [310, 420, 390, 510], backgroundColor: 'rgba(139,92,246,0.85)', borderRadius: 6 },
          { label: 'Asia Pacific',  data: [180, 260, 310, 380], backgroundColor: 'rgba(6,182,212,0.85)',  borderRadius: 6 },
        ]
      },
      options: {
        responsive: true,
        aspectRatio: 2,
        animation: {
          duration: 800,
          easing: 'easeOutQuart',
          delay: (ctx) => ctx.dataIndex * 80,
        },
        plugins: {
          legend: { position: 'top', labels: { usePointStyle: true, padding: 16 } },
          tooltip: { mode: 'index', intersect: false },
        },
        scales: {
          x: { grid: { display: false }, ticks: { padding: 8 } },
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(255,255,255,0.06)' },
            ticks: { callback: v => '$' + v + 'K' },
          },
        },
      },
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **`maintainAspectRatio: false` without explicit height** — use `aspectRatio` in options instead, or pair `maintainAspectRatio: false` with an explicit CSS height on the canvas wrapper
- **Manual `Chart.register()` with UMD** — the UMD build auto-registers all components; calling `Chart.register()` is unnecessary and can cause duplicate registration warnings
- **Running chart code before CDN loads** — always place your `<script>` tag after the Chart.js CDN tag, at the end of `<body>`
- **Hardcoding pixel widths on canvas** — always use `responsive: true` (default) and let the container's CSS width control the chart size
- **Forgetting `beginAtZero: true`** — without it, bar charts can start from a misleading non-zero baseline
- **`tension: 0.4` on financial data** — smooth curves distort precise values; use `tension: 0` for data where exact values matter
- **Stacking without matching `stack` property** — when mixing stacked and non-stacked datasets, assign a `stack` property to each dataset explicitly
- **Not destroying before recreating** — if you update a chart by creating a new `Chart()` on the same canvas, always call `chart.destroy()` first to prevent memory leaks and ghost tooltips
