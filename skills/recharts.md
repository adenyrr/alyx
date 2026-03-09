---
name: recharts
description: Create responsive React-based data charts using Recharts, delivered as self-contained HTML artifacts. Use this skill whenever someone needs React-rendered charts — line, bar, area, pie, radar, scatter, composed, funnel, or treemap — especially when data is dynamic or the artifact already uses React/shadcn-ui. Trigger on requests like "make a React chart", "create a dashboard with charts", "build a line chart with React", "show data in a bar chart", or any prompt needing charts within a React-based artifact. Do NOT use for non-React HTML charts (→ chartjs or plotly skill) or for complex scientific/3D plots (→ plotly skill).
---

# Recharts Skill

Recharts is a composable, declarative charting library built on React and D3. It renders SVG charts from React components like `<LineChart>`, `<BarChart>`, `<PieCell>`. Charts are responsive via `<ResponsiveContainer>`, fully themeable, and integrate naturally with React-based artifacts (including shadcn-ui Card wrappers).

---

## Artifact Presentation & Use Cases

Every Recharts artifact is a self-contained HTML page that loads React + Recharts via CDN, then renders chart components into a dark-themed shell. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (either a `<div>` styled like `#1a1d27` or a shadcn-ui `<Card>`) holds each chart
- **Title** (1.15rem, `#f1f5f9`) and **subtitle** (0.82rem, `#64748b`) describe the data
- **`<ResponsiveContainer>`** wraps every chart for automatic width/height
- **Dark grid** — axis lines `#2a2d3a`, tick labels `#94a3b8`, tooltip background `#1a1d27`

### Typical use cases

- **Dashboards** — multiple charts (line, bar, pie) in a grid layout
- **Time series** — line/area charts showing trends over time
- **Comparisons** — grouped/stacked bar charts comparing categories
- **Distributions** — pie/donut charts, radar charts, treemaps
- **Composed charts** — mixed line + bar on the same axes
- **KPI cards** — sparkline mini-charts next to metric numbers

### What the user sees

Clean, responsive SVG charts with animated entry, hover tooltips, and optional interactive legends. Charts resize smoothly with the container.

---

## When to Use Recharts vs. Alternatives

| Use Recharts when… | Use another tool when… |
|---|---|
| Artifact is React-based (JSX, components) | Plain HTML artifact without React → **Chart.js** |
| Declarative JSX composition is preferred | Complex scientific/3D plots → **Plotly** |
| Integration with shadcn-ui / Tailwind Cards | Custom D3 visualizations (force, geo, etc.) → **D3** |
| Standard chart types (line, bar, area, pie, radar) | Interactive diagram editing → **JointJS** |
| Built-in responsive container | Timeline/Gantt → **vis-timeline** |
| React state-driven data updates | Network graphs → **vis-network** |

> **Rule of thumb:** if the artifact is already React-based or the user mentions React, use Recharts. For plain HTML artifacts, Chart.js or Plotly are simpler.

---

## Step 1 — CDN Setup

```html
<!-- React -->
<script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>
<!-- Babel for JSX -->
<script src="https://cdn.jsdelivr.net/npm/@babel/standalone/babel.min.js"></script>
<!-- Recharts -->
<script src="https://cdn.jsdelivr.net/npm/recharts@2/umd/Recharts.min.js"></script>
```

> The UMD build exposes `Recharts` globally. Destructure: `const { LineChart, Line, XAxis, YAxis, ... } = Recharts;`

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chart Dashboard</title>
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
      max-width: 800px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
      margin-bottom: 20px;
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@babel/standalone/babel.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/recharts@2/umd/Recharts.min.js"></script>
  <script type="text/babel">
    const { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } = Recharts;

    function App() {
      return (
        <div className="card">
          <h1>Title</h1>
          <p className="sub">Description</p>
          {/* Chart here */}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

---

## Step 3 — Dark Theme Configuration

Use these values consistently across all Recharts components:

```jsx
// Colors
const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#22c55e', '#06b6d4', '#f97316', '#eab308'];

// Grid
<CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />

// Axes
<XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
<YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />

// Tooltip
<Tooltip
  contentStyle={{ background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, color: '#e2e8f0' }}
  labelStyle={{ color: '#94a3b8' }}
/>

// Legend
<Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
```

---

## Step 4 — Line Chart

```jsx
const data = [
  { month: 'Jan', sales: 400, profit: 240 },
  { month: 'Feb', sales: 300, profit: 139 },
  { month: 'Mar', sales: 500, profit: 380 },
  { month: 'Apr', sales: 450, profit: 310 },
  { month: 'May', sales: 600, profit: 420 },
];

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
    <XAxis dataKey="month" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
    <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
    <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }} />
    <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
    <Line type="monotone" dataKey="sales" stroke="#6366f1" strokeWidth={2} dot={{ r: 4, fill: '#6366f1' }} />
    <Line type="monotone" dataKey="profit" stroke="#22c55e" strokeWidth={2} dot={{ r: 4, fill: '#22c55e' }} />
  </LineChart>
</ResponsiveContainer>
```

---

## Step 5 — Bar Chart

```jsx
<ResponsiveContainer width="100%" height={300}>
  <BarChart data={data}>
    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
    <XAxis dataKey="month" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
    <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
    <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }} />
    <Bar dataKey="sales" fill="#6366f1" radius={[4, 4, 0, 0]} />
    <Bar dataKey="profit" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
  </BarChart>
</ResponsiveContainer>
```

### Stacked variant
```jsx
<Bar dataKey="sales" stackId="a" fill="#6366f1" />
<Bar dataKey="profit" stackId="a" fill="#8b5cf6" />
```

---

## Step 6 — Area Chart

```jsx
<ResponsiveContainer width="100%" height={300}>
  <AreaChart data={data}>
    <defs>
      <linearGradient id="gradSales" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#6366f1" stopOpacity={0.4} />
        <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
      </linearGradient>
    </defs>
    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
    <XAxis dataKey="month" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
    <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
    <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }} />
    <Area type="monotone" dataKey="sales" stroke="#6366f1" fill="url(#gradSales)" strokeWidth={2} />
  </AreaChart>
</ResponsiveContainer>
```

---

## Step 7 — Pie / Donut Chart

```jsx
const pieData = [
  { name: 'Desktop', value: 400 },
  { name: 'Mobile', value: 300 },
  { name: 'Tablet', value: 120 },
];

<ResponsiveContainer width="100%" height={300}>
  <PieChart>
    <Pie
      data={pieData}
      cx="50%" cy="50%"
      innerRadius={60}       /* 0 for solid pie, >0 for donut */
      outerRadius={100}
      paddingAngle={3}
      dataKey="value"
      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
      labelLine={{ stroke: '#64748b' }}
    >
      {pieData.map((_, i) => (
        <Cell key={i} fill={COLORS[i % COLORS.length]} />
      ))}
    </Pie>
    <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }} />
    <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
  </PieChart>
</ResponsiveContainer>
```

---

## Step 8 — Radar Chart

```jsx
const radarData = [
  { skill: 'JS', level: 90 },
  { skill: 'Python', level: 75 },
  { skill: 'CSS', level: 85 },
  { skill: 'SQL', level: 70 },
  { skill: 'DevOps', level: 60 },
];

<ResponsiveContainer width="100%" height={300}>
  <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="75%">
    <PolarGrid stroke="rgba(255,255,255,0.1)" />
    <PolarAngleAxis dataKey="skill" tick={{ fill: '#94a3b8', fontSize: 12 }} />
    <PolarRadiusAxis tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} />
    <Radar dataKey="level" stroke="#6366f1" fill="#6366f1" fillOpacity={0.3} />
    <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }} />
  </RadarChart>
</ResponsiveContainer>
```

---

## Step 9 — Composed Chart (Line + Bar)

```jsx
<ResponsiveContainer width="100%" height={300}>
  <ComposedChart data={data}>
    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
    <XAxis dataKey="month" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
    <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} tickLine={false} />
    <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }} />
    <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
    <Bar dataKey="sales" fill="#6366f1" radius={[4, 4, 0, 0]} />
    <Line type="monotone" dataKey="profit" stroke="#22c55e" strokeWidth={2} />
  </ComposedChart>
</ResponsiveContainer>
```

---

## Step 10 — Scatter Chart

```jsx
const scatterData = [
  { x: 10, y: 30 }, { x: 20, y: 50 }, { x: 30, y: 40 },
  { x: 40, y: 70 }, { x: 50, y: 60 }, { x: 60, y: 90 },
];

<ResponsiveContainer width="100%" height={300}>
  <ScatterChart>
    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
    <XAxis type="number" dataKey="x" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} />
    <YAxis type="number" dataKey="y" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={{ stroke: '#2a2d3a' }} />
    <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }} />
    <Scatter data={scatterData} fill="#6366f1" />
  </ScatterChart>
</ResponsiveContainer>
```

---

## Step 11 — Design & Polish Guidelines

- **Always wrap in `<ResponsiveContainer>`** — without it, charts render at 0px width; always set `width="100%"` and a fixed `height={300}`
- **Dark tooltip** — override `contentStyle` with dark background, subtle border, rounded corners
- **Consistent color palette** — define a shared `COLORS` array and apply it across all charts for visual coherence
- **Grid opacity** — keep CartesianGrid very subtle (`rgba(255,255,255,0.06)`) to avoid visual noise
- **Axis labels** — `#94a3b8` for readability on dark background; remove `tickLine` for cleaner look
- **Bar radius** — `radius={[4,4,0,0]}` rounds the top corners of bars for a softer appearance
- **Area gradients** — use `<defs>` SVG gradients fading from an alpha to transparent for elegant area fills
- **Donut inner radius** — `innerRadius={60}` creates a clean donut; place a centered metric text inside for KPI donut charts
- **Animation** — Recharts animates by default; disable with `isAnimationActive={false}` if performance is a concern
- **No data state** — handle empty `data` arrays with a "No data available" fallback message

---

## Step 12 — Complete Example: Sales Dashboard

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sales Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; justify-content: center; min-height: 100vh; padding: 24px; }
    #root { width: 100%; max-width: 1000px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(440px, 1fr)); gap: 20px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 16px; }
    .page-title { font-size: 1.4rem; font-weight: 700; color: #f1f5f9; margin-bottom: 20px; text-align: center; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@babel/standalone/babel.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/recharts@2/umd/Recharts.min.js"></script>
  <script type="text/babel">
    const {
      LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area,
      XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    } = Recharts;

    const COLORS = ['#6366f1','#8b5cf6','#ec4899','#22c55e','#06b6d4','#f97316'];

    const monthly = [
      { month: 'Jan', revenue: 4200, expenses: 2400 },
      { month: 'Feb', revenue: 3800, expenses: 2200 },
      { month: 'Mar', revenue: 5100, expenses: 2800 },
      { month: 'Apr', revenue: 4700, expenses: 2500 },
      { month: 'May', revenue: 5800, expenses: 3100 },
      { month: 'Jun', revenue: 6200, expenses: 3400 },
    ];

    const channels = [
      { name: 'Direct', value: 400 },
      { name: 'Organic', value: 300 },
      { name: 'Social', value: 180 },
      { name: 'Referral', value: 120 },
    ];

    const axisProps = { tick: { fill: '#94a3b8', fontSize: 12 }, axisLine: { stroke: '#2a2d3a' }, tickLine: false };
    const tipStyle = { background: '#1a1d27', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 };

    function App() {
      return (
        <div>
          <div className="page-title">Sales Dashboard</div>
          <div className="grid">

            {/* Revenue Trend */}
            <div className="card">
              <h1>Revenue Trend</h1>
              <p className="sub">Monthly revenue with gradient fill</p>
              <ResponsiveContainer width="100%" height={250}>
                <AreaChart data={monthly}>
                  <defs>
                    <linearGradient id="gRev" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#6366f1" stopOpacity={0.4} />
                      <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                  <XAxis dataKey="month" {...axisProps} />
                  <YAxis {...axisProps} />
                  <Tooltip contentStyle={tipStyle} />
                  <Area type="monotone" dataKey="revenue" stroke="#6366f1" fill="url(#gRev)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Revenue vs Expenses */}
            <div className="card">
              <h1>Revenue vs Expenses</h1>
              <p className="sub">Side-by-side monthly comparison</p>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={monthly}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                  <XAxis dataKey="month" {...axisProps} />
                  <YAxis {...axisProps} />
                  <Tooltip contentStyle={tipStyle} />
                  <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
                  <Bar dataKey="revenue" fill="#6366f1" radius={[4,4,0,0]} />
                  <Bar dataKey="expenses" fill="#ec4899" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Traffic Channels */}
            <div className="card">
              <h1>Traffic Channels</h1>
              <p className="sub">Distribution by acquisition source</p>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={channels} cx="50%" cy="50%" innerRadius={50} outerRadius={85} paddingAngle={3} dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent*100).toFixed(0)}%`} labelLine={{ stroke: '#64748b' }}>
                    {channels.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip contentStyle={tipStyle} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Growth Lines */}
            <div className="card">
              <h1>Growth Metrics</h1>
              <p className="sub">Revenue and expenses over time</p>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={monthly}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                  <XAxis dataKey="month" {...axisProps} />
                  <YAxis {...axisProps} />
                  <Tooltip contentStyle={tipStyle} />
                  <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
                  <Line type="monotone" dataKey="revenue" stroke="#6366f1" strokeWidth={2} dot={{ r: 4, fill: '#6366f1' }} />
                  <Line type="monotone" dataKey="expenses" stroke="#ec4899" strokeWidth={2} dot={{ r: 4, fill: '#ec4899' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

          </div>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Missing `<ResponsiveContainer>`** — without it, charts render at 0×0; always wrap every chart in `<ResponsiveContainer width="100%" height={N}>`
- **Forgetting `dataKey`** — every `<Line>`, `<Bar>`, `<Area>`, `<Pie>` needs a `dataKey` matching a field in the data array
- **`<Cell>` not imported** — Pie charts need `Cell` from Recharts for per-slice colors; it's easy to forget in the destructure
- **No `type="number"` on scatter axes** — XAxis/YAxis default to `category` type; scatter plots need `type="number"`
- **Using CSS for SVG styling** — Recharts renders SVG; use component props (`fill`, `stroke`, `strokeWidth`) not CSS classes
- **Hard-coded width** — never set `width={500}` on a chart; always use `<ResponsiveContainer>` for responsive behavior
- **`<script type="text/babel">`** — CDN Recharts with JSX requires Babel standalone; forgetting `type="text/babel"` causes syntax errors
- **Tooltip `contentStyle` not dark** — default tooltip is white/light; always override with dark theme colors
- **PieChart without explicit cx/cy** — center defaults may not work well in all containers; always set `cx="50%" cy="50%"`
