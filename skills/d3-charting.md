---
name: d3-charting
description: Create advanced, fully custom data visualizations using D3.js v7, delivered as self-contained HTML artifacts. Use this skill whenever someone needs bespoke SVG charts, force-directed network graphs, geographic maps, hierarchical layouts (treemap, sunburst, pack), animated transitions, interactive brushing/zooming, or any visualization that goes beyond standard chart types. Trigger whenever the user mentions D3.js directly, OR when the request implies pixel-perfect control, unusual chart types (chord diagrams, voronoi, streamgraph, ridgeline, custom radial charts), or rich interaction patterns (drag, lasso, linked views). Prefer this skill over generic charting tools for any visualization requiring custom SVG drawing or physics simulation.
---

# D3.js Charting Skill — v7

D3 (Data-Driven Documents) is not a charting library — it is a **low-level toolkit** for binding data to DOM/SVG elements and applying data-driven transformations. It trades simplicity for unlimited expressiveness. Use it when Chart.js or Plotly cannot produce what is needed.

---

## Artifact Presentation & Use Cases

Every D3 artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the visualization
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the chart
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context and interaction hints
- **SVG element** renders the custom visualization with D3-managed elements
- **Tooltip div** (`position: absolute`, dark themed) appears on hover

### Typical use cases

- **Force-directed network graphs** — visualize relationships between entities with physics simulation
- **Geographic maps** — world/country maps with projections, choropleths, and interactive features
- **Hierarchical layouts** — treemaps, sunbursts, packed circles, dendrograms for nested data
- **Custom chart types** — chord diagrams, streamgraphs, ridgeline plots, Voronoi tessellations
- **Animated transitions** — smooth data-driven enter/update/exit transitions on any element
- **Brushing & zooming** — linked multi-view dashboards with interactive selection and zoom

### What the user sees

A bespoke SVG visualization: hover for detailed tooltips, watch smooth animated transitions on data changes, interact via drag, zoom, or brush. Every visual element is pixel-perfect and tailored to the specific dataset.

---

## When to Use D3 vs. Alternatives

| Use D3 when… | Use Chart.js / Plotly when… |
|---|---|
| Custom SVG shapes, layouts, paths | Standard bar, line, pie, scatter charts |
| Force-directed / network graphs | Quick interactive dashboards |
| Geographic maps + projections | Heavy data exploration with built-in toolbar |
| Hierarchical layouts (treemap, sunburst, pack, tree) | Minimal setup time needed |
| Chord diagrams, streamgraphs, ridgelines, Voronoi | Statistical charts (box, violin, histogram) |
| Pixel-perfect custom animations | 3D charts |
| Linked / brushed multi-view systems | When bundle size is a concern |
| Full programmatic control over every SVG element | |

---

## Step 1 — CDN Setup

### Recommended: UMD bundle via jsDelivr (works everywhere, no import maps needed)
```html
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
```

### Alternative: ESM module (cleaner for modern setups)
```html
<script type="module">
  import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
  // all D3 code here
</script>
```

### Tree-shaken individual modules (lightest, advanced)
```html
<script type="module">
  import { forceSimulation, forceLink, forceManyBody, forceCenter }
    from "https://cdn.jsdelivr.net/npm/d3-force@3/+esm";
</script>
```

**Default choice: UMD `<script src>` tag** — broadest compatibility, no module headaches in single-file artifacts.

---

## Step 2 — HTML Artifact Shell

D3 renders into an **SVG element**. The SVG must be sized and positioned correctly inside the container. Use the **margin convention** (the single most important D3 pattern).

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>D3 Chart</title>
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
    .chart-wrapper {
      background: #1a1d27;
      border-radius: 16px;
      padding: 32px;
      width: 100%;
      max-width: 900px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.25rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.85rem; color: #64748b; margin-bottom: 20px; }

    /* Axis styling */
    .axis path, .axis line { stroke: rgba(255,255,255,0.12); }
    .axis text { fill: #94a3b8; font-size: 12px; }
    .axis .domain { display: none; } /* hide axis spine — clean look */

    /* Tooltip */
    .tooltip {
      position: absolute;
      background: #1e293b;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 13px;
      color: #f1f5f9;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.15s;
    }
  </style>
</head>
<body>
  <div class="chart-wrapper">
    <h1>Chart Title</h1>
    <p class="sub">Subtitle or data source</p>
    <div id="chart"></div>
  </div>
  <!-- Tooltip lives at body level so it can overflow the container -->
  <div class="tooltip" id="tooltip"></div>

  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <script>
    // All D3 code here
  </script>
</body>
</html>
```

---

## Step 3 — The Margin Convention (Always Apply)

```javascript
// ALWAYS start with this pattern
const container = document.getElementById('chart');
const totalWidth  = container.clientWidth || 800;
const totalHeight = 460;

const margin = { top: 30, right: 30, bottom: 50, left: 60 };
const width  = totalWidth  - margin.left - margin.right;   // inner drawing area
const height = totalHeight - margin.top  - margin.bottom;

const svg = d3.select('#chart')
  .append('svg')
    .attr('width',  totalWidth)
    .attr('height', totalHeight)
    // Optional: make fully responsive via viewBox
    .attr('viewBox', `0 0 ${totalWidth} ${totalHeight}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')
  .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);
// All subsequent drawing uses `svg` and refers to the inner [0,width] x [0,height] space
```

---

## Step 4 — Scales Reference

Scales map **data domain → visual range**. Always the first thing to define.

```javascript
// Linear (continuous → continuous)
const x = d3.scaleLinear().domain([0, 100]).range([0, width]);

// Time
const x = d3.scaleTime()
  .domain(d3.extent(data, d => new Date(d.date)))
  .range([0, width]);

// Band (categorical → discrete bands — for bar charts)
const x = d3.scaleBand()
  .domain(data.map(d => d.label))
  .range([0, width])
  .padding(0.2);             // 20% gap between bars
// bar width = x.bandwidth()

// Point (categorical → point positions)
const x = d3.scalePoint().domain(categories).range([0, width]).padding(0.5);

// Log
const y = d3.scaleLog().domain([1, 10000]).range([height, 0]).base(10);

// Sqrt (good for bubble radius — area stays proportional)
const r = d3.scaleSqrt().domain([0, d3.max(data, d => d.value)]).range([2, 40]);

// Ordinal color
const color = d3.scaleOrdinal()
  .domain(categories)
  .range(['#6366f1','#8b5cf6','#ec4899','#f43f5e','#f97316','#22c55e','#06b6d4']);

// Sequential color (continuous → color)
const color = d3.scaleSequential(d3.interpolateViridis).domain([min, max]);

// Diverging color
const color = d3.scaleDiverging(d3.interpolateRdBu).domain([min, 0, max]);
```

### Built-in color schemes (d3-scale-chromatic)
```javascript
// Categorical (discrete)
d3.schemeTableau10      // 10 colors, excellent default
d3.schemeCategory10
d3.schemePastel1
d3.schemeDark2

// Sequential (single hue)
d3.interpolateBlues     d3.interpolateGreens    d3.interpolatePurples
d3.interpolateOranges   d3.interpolateReds      d3.interpolateGreys

// Multi-hue sequential
d3.interpolateViridis   d3.interpolatePlasma    d3.interpolateInferno
d3.interpolateMagma     d3.interpolateCividis   d3.interpolateTurbo

// Diverging
d3.interpolateRdBu      d3.interpolatePRGn      d3.interpolateSpectral
```

---

## Step 5 — Axes

```javascript
// X axis (bottom)
svg.append('g')
  .attr('class', 'axis x-axis')
  .attr('transform', `translate(0,${height})`)
  .call(
    d3.axisBottom(x)
      .ticks(6)
      .tickFormat(d3.format(',.0f'))   // number format
      .tickSize(-height)               // grid lines: set to 0 for no grid
      .tickPadding(10)
  )
  // Style grid lines after rendering
  .call(g => g.selectAll('.tick line').attr('stroke', 'rgba(255,255,255,0.06)'))
  .call(g => g.select('.domain').remove());  // hide the axis spine

// Y axis (left)
svg.append('g')
  .attr('class', 'axis y-axis')
  .call(
    d3.axisLeft(y)
      .ticks(5)
      .tickFormat(d => `$${d3.format('.2s')(d)}`)  // e.g. "$1.2M"
      .tickSize(-width)
      .tickPadding(10)
  )
  .call(g => g.selectAll('.tick line').attr('stroke', 'rgba(255,255,255,0.06)'))
  .call(g => g.select('.domain').remove());

// Axis label
svg.append('text')
  .attr('transform', `translate(${width / 2}, ${height + 40})`)
  .attr('text-anchor', 'middle')
  .attr('fill', '#94a3b8')
  .attr('font-size', 12)
  .text('X Axis Label');

// Time axis format
d3.axisBottom(x).tickFormat(d3.timeFormat('%b %Y'))
```

---

## Step 6 — Data Join (Core D3 Pattern)

D3 v7 uses `.join()` — the modern, simplified API. Understand enter/update/exit conceptually, but use `.join()` in practice.

```javascript
// Modern pattern with .join() — handles enter + update + exit
svg.selectAll('.bar')
  .data(data, d => d.id)   // key function for stable identity on updates
  .join(
    enter  => enter.append('rect').attr('class', 'bar')
                   .attr('opacity', 0)          // start invisible for transition
                   .call(el => el.transition().attr('opacity', 1)),
    update => update,
    exit   => exit.transition().attr('opacity', 0).remove()
  )
  // Common attributes applied to enter + update (returned by .join)
  .attr('x',      d => x(d.label))
  .attr('y',      d => y(d.value))
  .attr('width',  x.bandwidth())
  .attr('height', d => height - y(d.value))
  .attr('fill',   d => color(d.category));

// Shorthand .join('rect') — when you don't need separate enter/update/exit logic
svg.selectAll('.dot')
  .data(data)
  .join('circle')
  .attr('r',  5)
  .attr('cx', d => x(d.x))
  .attr('cy', d => y(d.y));
```

---

## Step 7 — Shape Generators

```javascript
// Line
const line = d3.line()
  .x(d => x(d.date))
  .y(d => y(d.value))
  .curve(d3.curveCatmullRom.alpha(0.5));  // smooth curve
svg.append('path').datum(data).attr('d', line).attr('fill', 'none').attr('stroke', '#6366f1').attr('stroke-width', 2.5);

// Area
const area = d3.area()
  .x(d => x(d.date))
  .y0(height)
  .y1(d => y(d.value))
  .curve(d3.curveCatmullRom);
svg.append('path').datum(data).attr('d', area).attr('fill', 'rgba(99,102,241,0.15)');

// Stacked area
const stack = d3.stack().keys(['a', 'b', 'c']).order(d3.stackOrderNone).offset(d3.stackOffsetNone);
const stackedData = stack(data);
svg.selectAll('.layer').data(stackedData).join('path').attr('d', d3.area().x(d => x(d.data.date)).y0(d => y(d[0])).y1(d => y(d[1])));

// Arc (pie / donut)
const arc = d3.arc().innerRadius(80).outerRadius(140);  // innerRadius 0 = pie
const pie = d3.pie().value(d => d.value).sort(null);
svg.selectAll('.slice').data(pie(data)).join('path').attr('d', arc).attr('fill', d => color(d.data.label));

// Curve types
d3.curveLinear          // straight lines
d3.curveMonotoneX       // monotone (good for time series)
d3.curveCatmullRom      // smooth, organic
d3.curveStep            // step function
d3.curveBasis           // B-spline
d3.curveCardinal        // cardinal spline
```

---

## Step 8 — Transitions & Animation

```javascript
// Basic transition
svg.selectAll('.bar')
  .transition()
    .duration(600)
    .ease(d3.easeCubicOut)
    .attr('height', d => height - y(d.value))
    .attr('y',      d => y(d.value));

// Staggered entry (delay by index)
svg.selectAll('.dot')
  .transition()
    .duration(400)
    .delay((d, i) => i * 30)
    .attr('r', 5)
    .attr('opacity', 1);

// Chained transitions
el.transition().duration(300).attr('opacity', 0)
  .transition().duration(300).attr('fill', 'red').attr('opacity', 1);

// Named transitions (synchronize across selections)
const t = d3.transition('update').duration(750).ease(d3.easeQuadInOut);
bars.transition(t).attr('height', ...);
labels.transition(t).attr('y', ...);

// Easing functions
d3.easeLinear     d3.easeQuadInOut   d3.easeCubicOut
d3.easeElasticOut d3.easeBounceOut   d3.easeBackOut
d3.easeExpOut     d3.easeSinInOut    d3.easeCircleOut

// Path morphing (attrTween for smooth path transitions)
path.transition().duration(800)
  .attrTween('d', function() {
    const prev = d3.select(this).attr('d');
    const next = line(newData);
    return d3.interpolatePath ? d3.interpolatePath(prev, next) : d3.interpolateString(prev, next);
  });
```

---

## Step 9 — Tooltip Pattern

```javascript
// Create tooltip element (once, outside any loop)
const tooltip = d3.select('#tooltip');  // div.tooltip from the HTML shell

// Attach to any element
svg.selectAll('.bar')
  .on('mouseover', (event, d) => {
    tooltip
      .style('opacity', 1)
      .html(`<strong>${d.label}</strong><br>Value: ${d3.format(',.0f')(d.value)}`);
  })
  .on('mousemove', (event) => {
    tooltip
      .style('left', (event.pageX + 14) + 'px')
      .style('top',  (event.pageY - 36) + 'px');
  })
  .on('mouseout', () => {
    tooltip.style('opacity', 0);
  });

// Highlight on hover
svg.selectAll('.bar')
  .on('mouseover', function(event, d) {
    d3.select(this).attr('opacity', 1);
    d3.selectAll('.bar').filter(b => b !== d).attr('opacity', 0.3);
  })
  .on('mouseout', () => {
    d3.selectAll('.bar').attr('opacity', 1);
  });
```

---

## Step 10 — Zoom & Pan

```javascript
// Create zoom behavior
const zoom = d3.zoom()
  .scaleExtent([0.5, 8])          // min / max zoom level
  .on('zoom', (event) => {
    innerGroup.attr('transform', event.transform);  // innerGroup = the <g> with all chart elements
  });

// Apply to SVG
d3.select('svg').call(zoom);

// Programmatic reset
d3.select('svg').transition().duration(500).call(zoom.transform, d3.zoomIdentity);

// Zoom on axes (rescale axes during zoom)
const zoom = d3.zoom().on('zoom', (event) => {
  const newX = event.transform.rescaleX(x);
  const newY = event.transform.rescaleY(y);
  xAxisGroup.call(d3.axisBottom(newX));
  yAxisGroup.call(d3.axisLeft(newY));
  dots.attr('cx', d => newX(d.x)).attr('cy', d => newY(d.y));
});
```

---

## Step 11 — Brush (Range Selection)

```javascript
const brush = d3.brushX()
  .extent([[0, 0], [width, height]])
  .on('end', (event) => {
    if (!event.selection) return;
    const [x0, x1] = event.selection.map(x.invert);
    // x0, x1 are now data domain values
    const selected = data.filter(d => d.date >= x0 && d.date <= x1);
    updateChart(selected);
  });

svg.append('g').attr('class', 'brush').call(brush);
```

---

## Step 12 — Force Simulation (Network Graphs)

```javascript
const nodes = [{ id: 'A' }, { id: 'B' }, { id: 'C' }];
const links = [{ source: 'A', target: 'B' }, { source: 'B', target: 'C' }];

const simulation = d3.forceSimulation(nodes)
  .force('link',    d3.forceLink(links).id(d => d.id).distance(80))
  .force('charge',  d3.forceManyBody().strength(-300))  // negative = repulsion
  .force('center',  d3.forceCenter(width / 2, height / 2))
  .force('collide', d3.forceCollide().radius(20))       // prevent node overlap
  .alphaDecay(0.03)   // slower convergence = more natural movement
  .on('tick', ticked);

// Draw links (behind nodes)
const link = svg.append('g')
  .selectAll('line').data(links).join('line')
  .attr('stroke', 'rgba(255,255,255,0.2)').attr('stroke-width', 1.5);

// Draw nodes
const node = svg.append('g')
  .selectAll('circle').data(nodes).join('circle')
  .attr('r', 10)
  .attr('fill', d => color(d.group))
  .call(drag(simulation));   // drag helper below

// Update positions on each simulation tick
function ticked() {
  link
    .attr('x1', d => d.source.x).attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
  node
    .attr('cx', d => d.x).attr('cy', d => d.y);
}

// Drag behavior for force nodes
function drag(simulation) {
  return d3.drag()
    .on('start', (event, d) => { if (!event.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on('drag',  (event, d) => { d.fx = event.x; d.fy = event.y; })
    .on('end',   (event, d) => { if (!event.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; });
}
```

---

## Step 13 — Hierarchical Layouts

```javascript
// Input data structure
const data = {
  name: 'root',
  children: [
    { name: 'A', value: 30, children: [{ name: 'A1', value: 15 }] },
    { name: 'B', value: 20 },
  ]
};

const root = d3.hierarchy(data).sum(d => d.value).sort((a, b) => b.value - a.value);

// --- Treemap ---
d3.treemap().size([width, height]).padding(3)(root);
svg.selectAll('rect').data(root.leaves()).join('rect')
  .attr('x', d => d.x0).attr('y', d => d.y0)
  .attr('width', d => d.x1 - d.x0).attr('height', d => d.y1 - d.y0)
  .attr('fill', d => color(d.parent.data.name));

// --- Circle Pack ---
d3.pack().size([width, height]).padding(3)(root);
svg.selectAll('circle').data(root.descendants()).join('circle')
  .attr('cx', d => d.x).attr('cy', d => d.y).attr('r', d => d.r);

// --- Sunburst ---
d3.partition().size([2 * Math.PI, Math.min(width, height) / 2])(root);
const arc = d3.arc().startAngle(d => d.x0).endAngle(d => d.x1)
  .innerRadius(d => d.y0).outerRadius(d => d.y1);
svg.attr('transform', `translate(${width/2},${height/2})`);
svg.selectAll('path').data(root.descendants()).join('path').attr('d', arc);

// --- Tree (dendrogram) ---
d3.tree().size([height, width])(root);
svg.selectAll('.link').data(root.links()).join('path')
  .attr('d', d3.linkHorizontal().x(d => d.y).y(d => d.x));
svg.selectAll('.node').data(root.descendants()).join('circle')
  .attr('cx', d => d.y).attr('cy', d => d.x).attr('r', 5);
```

---

## Step 14 — Geographic Maps

```javascript
// Requires topojson for country/region shapes
// <script src="https://cdn.jsdelivr.net/npm/topojson@3"></script>

const projection = d3.geoNaturalEarth1()  // or geoMercator, geoOrthographic, geoAlbersUsa
  .scale(160)
  .translate([width / 2, height / 2]);

const path = d3.geoPath().projection(projection);

// Load and draw world map
d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json').then(world => {
  svg.append('g')
    .selectAll('path')
    .data(topojson.feature(world, world.objects.countries).features)
    .join('path')
      .attr('d', path)
      .attr('fill', '#2d3748')
      .attr('stroke', 'rgba(255,255,255,0.15)')
      .attr('stroke-width', 0.5);
});

// Common projections
d3.geoMercator()        // standard web map
d3.geoNaturalEarth1()   // aesthetic world map
d3.geoOrthographic()    // globe
d3.geoAlbersUsa()       // US-only, Alaska/Hawaii insets
d3.geoAzimuthalEqualArea()
```

---

## Step 15 — Useful Utility Functions

```javascript
// Data summarization
d3.min(data, d => d.value)
d3.max(data, d => d.value)
d3.extent(data, d => d.value)   // [min, max]
d3.mean(data, d => d.value)
d3.median(data, d => d.value)
d3.sum(data, d => d.value)

// Grouping
const grouped = d3.group(data, d => d.category);          // Map
const rollup  = d3.rollup(data, v => d3.sum(v, d => d.value), d => d.category);

// Binning (histogram)
const bins = d3.bin().value(d => d.x).thresholds(20)(data);

// Number formatting
d3.format('.2f')(3.14159)      // "3.14"
d3.format(',.0f')(1234567)     // "1,234,567"
d3.format('.2s')(1234567)      // "1.2M"
d3.format('+.1%')(0.157)       // "+15.7%"

// Date formatting
d3.timeFormat('%B %d, %Y')(new Date())   // "February 27, 2026"
d3.timeParse('%Y-%m-%d')('2026-01-15')  // Date object

// Color manipulation
d3.color('#6366f1').darker(0.5)
d3.color('#6366f1').brighter(0.5)
d3.interpolateRgb('#6366f1', '#ec4899')(0.5)  // midpoint color
```

---

## Step 16 — Complete Example: Animated Bar Chart with Tooltip

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>D3 Bar Chart</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 32px; width: 100%; max-width: 860px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
    .axis path, .axis line { stroke: rgba(255,255,255,0.08); }
    .axis text { fill: #94a3b8; font-size: 12px; }
    .tooltip { position: absolute; background: #1e293b; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 8px 14px; font-size: 13px; color: #f1f5f9; pointer-events: none; opacity: 0; transition: opacity 0.12s; line-height: 1.6; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Monthly Revenue</h1>
    <p class="sub">Fiscal Year 2024 — hover a bar for details</p>
    <div id="chart"></div>
  </div>
  <div class="tooltip" id="tooltip"></div>

  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <script>
    const data = [
      { month: 'Jan', value: 42000 }, { month: 'Feb', value: 55000 },
      { month: 'Mar', value: 48000 }, { month: 'Apr', value: 70000 },
      { month: 'May', value: 65000 }, { month: 'Jun', value: 82000 },
      { month: 'Jul', value: 75000 }, { month: 'Aug', value: 90000 },
      { month: 'Sep', value: 88000 }, { month: 'Oct', value: 95000 },
      { month: 'Nov', value: 102000 },{ month: 'Dec', value: 118000 }
    ];

    const container = document.getElementById('chart');
    const totalWidth  = container.clientWidth || 800;
    const totalHeight = 400;
    const margin = { top: 20, right: 20, bottom: 45, left: 65 };
    const width  = totalWidth  - margin.left - margin.right;
    const height = totalHeight - margin.top  - margin.bottom;

    const svg = d3.select('#chart').append('svg')
      .attr('width', totalWidth).attr('height', totalHeight)
      .attr('viewBox', `0 0 ${totalWidth} ${totalHeight}`)
      .append('g').attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const x = d3.scaleBand().domain(data.map(d => d.month)).range([0, width]).padding(0.25);
    const y = d3.scaleLinear().domain([0, d3.max(data, d => d.value) * 1.1]).range([height, 0]);

    // Axes
    svg.append('g').attr('class', 'axis').attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).tickSize(0).tickPadding(10))
      .call(g => g.select('.domain').remove());

    svg.append('g').attr('class', 'axis')
      .call(d3.axisLeft(y).ticks(5).tickFormat(d => `$${d3.format('.2s')(d)}`).tickSize(-width).tickPadding(10))
      .call(g => g.select('.domain').remove())
      .call(g => g.selectAll('.tick line').attr('stroke', 'rgba(255,255,255,0.06)'));

    // Color gradient via scaleSequential
    const color = d3.scaleSequential(d3.interpolate('#4338ca', '#818cf8'))
      .domain([0, data.length - 1]);

    const tooltip = d3.select('#tooltip');

    // Bars with enter animation
    svg.selectAll('.bar')
      .data(data)
      .join('rect')
        .attr('class', 'bar')
        .attr('x', d => x(d.month))
        .attr('width', x.bandwidth())
        .attr('y', height)          // start at bottom
        .attr('height', 0)          // start with 0 height
        .attr('rx', 5)
        .attr('fill', (d, i) => color(i))
        .transition().duration(700).ease(d3.easeQuadOut)
        .delay((d, i) => i * 40)
        .attr('y', d => y(d.value))
        .attr('height', d => height - y(d.value));

    // Hover after transition — re-select to bind events
    svg.selectAll('.bar')
      .on('mouseover', function(event, d) {
        d3.select(this).attr('opacity', 1);
        d3.selectAll('.bar').filter(b => b !== d).attr('opacity', 0.4);
        tooltip.style('opacity', 1)
          .html(`<strong>${d.month} 2024</strong><br>Revenue: ${d3.format('$,.0f')(d.value)}`);
      })
      .on('mousemove', event => tooltip.style('left', (event.pageX + 14) + 'px').style('top', (event.pageY - 40) + 'px'))
      .on('mouseout', () => { d3.selectAll('.bar').attr('opacity', 1); tooltip.style('opacity', 0); });
  </script>
</body>
</html>
```

---

## Step 17 — Design & Polish Guidelines

- **SVG text**: always set `fill` explicitly — SVG text ignores CSS `color`
- **Clipping**: add a `<clipPath>` when elements may overflow the drawing area (especially after zoom)
- **Performance**: for >5000 elements, switch to Canvas via `d3-canvas` or manual `ctx` drawing
- **Responsive**: wrap the entire chart creation in a function, call it on `resize`, and debounce the resize event
- **Layer order**: append groups in this order — grid lines → areas/fills → bars/lines → axes → labels → tooltips (bottom-most appended first, renders behind)
- **Axis spine**: `.call(g => g.select('.domain').remove())` gives a cleaner modern look; keep it for traditional charts
- **Font**: set font attributes on the `<svg>` or the `<g>` wrapper — child elements inherit them

---

## Step 18 — Common Mistakes to Avoid

- **Forgetting `transform: translate`**: SVG coordinates start at (0,0) top-left; axes and chart content need explicit translation via the margin convention
- **Selecting before appending**: `d3.select('.bar')` on non-existent elements returns empty selection silently — always append first or check `.empty()`
- **Event callbacks in v7**: D3 v7 changed event handlers from `function(d)` to `function(event, d)` — missing `event` as the first argument is a frequent v6→v7 bug
- **Not specifying a key function**: `.data(data)` without a key joins by index, causing incorrect transitions when data order changes; use `.data(data, d => d.id)`
- **Appending SVG to an already-SVG selection**: always `.select('#chart')` on a `<div>`, then `.append('svg')` — double-SVG nesting breaks layout
- **Hardcoded dimensions**: use `container.clientWidth` for width and compute height from it for fluid layouts
- **`d3.event` removed in v7**: use the `event` parameter from the callback — `d3.event` no longer exists
