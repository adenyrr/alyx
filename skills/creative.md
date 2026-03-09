---
name: creative-artifacts
description: Build rich, polished, interactive HTML and React artifacts with exceptional visual quality and creative ambition. This is the **master orchestration skill** — it defines how to encapsulate and present any artifact, which design rules apply universally, which libraries are available, and which specialist skill to reach for. Use this skill for any request involving an interactive web component, mini-application, game, tool, calculator, simulator, generative art piece, animated visualisation, creative UI, dashboard widget, or any deliverable that lives in the browser and benefits from interactivity, animation, or a distinct visual identity. Trigger on requests like "build me a…", "create an interactive…", "make a…tool/game/component/app/widget/demo", or any prompt where the output should feel designed and alive rather than static. Always ask "what would make this feel polished and memorable?" before writing a single line. The default bar is high.
---

# Creative Artifacts — Master Skill

This skill has two roles: **orchestrator** (route to the right specialist skill) and **builder** (provide the universal encapsulation rules, design system, and library catalogue that all artifacts share).

---

## Step 1 — Skill Routing Table

Before writing any code, identify which specialist skill(s) apply. Most artifacts need this skill's design rules **plus** one or more of the following:

| Need | Skill to read |
|---|---|
| Interactive data table with sort/filter/pagination | `tabulator` |
| Geographic map with markers, choropleth, clustering | `leaflet-maps` |
| Line/bar/pie/scatter charts from data | `chartjs` (Chart.js) |
| Statistical, scientific, financial, 3D charts | `plotly` (Plotly.js) |
| Network graph / node-link diagram | `vis-network` |
| Timeline / Gantt-style view | `vis-timeline` |
| Interactive flowchart (editable, draggable nodes) | `jointjs-flowchart` |
| Static text-to-diagram (sequence, ER, state, git) | `mermaid-diagrams` |
| D3 custom data visualisation | `d3-charting` |
| 3D WebGL scene (objects, particles, lighting) | `threejs-3d` |
| Generative art, canvas sketches, simulations | `p5js-creative-coding` |
| DOM/SVG animation with timelines and stagger | `animejs-animation` |
| Scroll-driven animation, parallax, scrollytelling | `gsap-animation` |
| CSS-only component library pages | `bulma-css` |
| Utility-first custom UI design | `tailwind-css` |
| React component-heavy UI with accessible components | `shadcn-ui` |
| React charts (line, bar, pie, radar) in JSX | `recharts` |
| Presentation slides / pitch decks | `reveal-slides` |
| Audio synthesis, instruments, sequencer | `tone-audio` |
| Calendar views, event scheduling | `fullcalendar` |
| LaTeX math equations / formulas | `mathjax-latex` |
| 2D canvas drawing editor, image annotation | `konva-canvas` |
| Code syntax highlighting in docs / pages | `prism-code` |

**Read the relevant skill BEFORE writing code.** This skill's rules apply on top of every specialist skill.

### When multiple skills combine
Many artifacts need more than one skill. Common combinations:
- Dashboard with map + chart + table → `leaflet-maps` + `chartjs` + `tabulator`
- Animated landing page → `tailwind-css` + `animejs-animation`
- Data viz with entrance animation → `chartjs` or `plotly` + `animejs-animation`
- 3D scene with UI controls → `threejs-3d` + `shadcn-ui` (React)
- SVG-heavy interactive diagram → `animejs-animation` + `mermaid-diagrams`
- Presentation with math formulas → `reveal-slides` + `mathjax-latex`
- Technical docs with code blocks → `prism-code` + `mathjax-latex`
- Animated React dashboard → `recharts` + `gsap-animation`
- Drawing app with code export → `konva-canvas` + `prism-code`
- Event planner with analytics → `fullcalendar` + `chartjs`
- Music visualiser → `tone-audio` + `p5js-creative-coding`
- Scrollytelling data story → `gsap-animation` + `d3-charting`

---

## Step 2 — Choose the Right Format

| Use **HTML + vanilla JS** | Use **React (.jsx)** |
|---|---|
| Canvas animations, WebGL, p5.js sketches | Component-heavy UIs, multi-state apps |
| Single interaction / single view | Tabbed interfaces, multi-step flows |
| Animation-first (Anime.js, GSAP) | Dynamic lists, filtered data, forms |
| Performance-critical render loops | Anything needing `useState` / `useEffect` |
| Libraries not available as ES modules | shadcn/ui components (React-only) |
| Self-contained demos with no UI state | Reusable, composable widgets |

**When in doubt: HTML** for visual/animation-first work; **React** for UI-state-heavy work. Never use `<form>` tags in React artifacts — use `onClick`/`onChange` handlers.

---

## Step 3 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Artifact</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      min-height: 100vh;
    }
  </style>
</head>
<body>

  <!-- Markup here -->

  <!-- ALL library <script> tags BEFORE your app script, at end of <body> -->
  <script src="…CDN…"></script>
  <script>
    // App code here
  </script>
</body>
</html>
```

---

## Step 4 — React Artifact Shell

```jsx
import { useState, useEffect, useRef, useCallback, useMemo } from "react";

// NEVER use localStorage, sessionStorage — use useState/useReducer instead

export default function MyArtifact() {
  const [state, setState] = useState(null);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-2xl bg-gray-900 rounded-2xl p-8 shadow-2xl">
        <h1 className="text-2xl font-bold text-white mb-2">Title</h1>
        <p className="text-gray-400 text-sm mb-6">Subtitle</p>
        {/* Content */}
      </div>
    </div>
  );
}
```

**Tailwind in React artifacts:** only pre-compiled core classes — no arbitrary values like `w-[372px]`. Use `style={{}}` for pixel-precise custom dimensions.

---

## Step 5 — Complete Library Catalogue

### HTML artifact libraries (load via `<script>` tags)

```html
<!-- ── DATA VISUALISATION ─────────────────────────────────── -->
<!-- Chart.js — standard charts (bar, line, pie, radar…) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>

<!-- Plotly.js — scientific/interactive charts, 3D plots -->
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist@2.35.2/plotly.js"></script>

<!-- D3.js — custom data visualisation, SVG manipulation -->
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>

<!-- Tabulator — interactive data tables with sort/filter/pagination -->
<link  href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css" rel="stylesheet">
<link  href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_midnight.min.css" rel="stylesheet"> <!-- dark theme -->
<script src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>

<!-- ── GEOGRAPHIC MAPS ────────────────────────────────────── -->
<!-- Leaflet — interactive geographic maps -->
<link  rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<!-- Leaflet plugins (optional, load after leaflet.js) -->
<link  rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
<link  rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>

<!-- ── GRAPHS & DIAGRAMS ──────────────────────────────────── -->
<!-- vis-network — network/node-link graph diagrams -->
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<!-- vis-timeline — timeline / Gantt views -->
<link  href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet">
<script src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
<!-- Mermaid — text-to-diagram (flowchart, sequence, ER, git…) -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<!-- JointJS — interactive editable flowcharts -->
<script src="https://cdn.jsdelivr.net/npm/@joint/core/dist/joint.js"></script>

<!-- ── 3D & CREATIVE CODING ───────────────────────────────── -->
<!-- Three.js r183 — 3D WebGL scenes (ES module + importmap — see threejs-3d skill) -->
<!-- p5.js v2 — generative art, creative coding, canvas sketches -->
<script src="https://cdn.jsdelivr.net/npm/p5@2.2.2/lib/p5.min.js"></script>
<!-- Konva.js 9 — 2D canvas editor, shapes, drawing, image annotation -->
<script src="https://cdn.jsdelivr.net/npm/konva@9/konva.min.js"></script>

<!-- ── ANIMATION ─────────────────────────────────────────── -->
<!-- Anime.js v4 — DOM/SVG timeline animations, stagger, scroll, draggable -->
<script src="https://cdn.jsdelivr.net/npm/animejs/dist/bundles/anime.umd.min.js"></script>
<!-- GSAP — professional-grade animation (alternative to Anime.js) -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>

<!-- ── PRESENTATIONS & CALENDARS ──────────────────────────── -->
<!-- Reveal.js 5 — slide decks / presentations -->
<link  rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
<link  rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/black.css">
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
<!-- FullCalendar 6 — calendar views, event scheduling -->
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@6/index.global.min.js"></script>
<!-- Recharts (UMD) — React charts in HTML artifacts -->
<script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/recharts@2/umd/Recharts.min.js"></script>

<!-- ── CSS FRAMEWORKS ─────────────────────────────────────── -->
<!-- Bulma v1 — pure CSS component framework with dark mode -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.4/css/bulma.min.css">
<!-- Tailwind v4 Play CDN (use <style type="text/tailwindcss"> for @theme) -->
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<!-- Font Awesome — icons (commonly paired with Bulma) -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">

<!-- ── UTILITIES ─────────────────────────────────────────── -->
<!-- Tone.js — audio synthesis and scheduling -->
<script src="https://cdn.jsdelivr.net/npm/tone@14.8.49/build/Tone.js"></script>
<!-- MathJax — LaTeX rendering -->
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.min.js"></script>
<!-- Prism.js — code syntax highlighting -->
<link  href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
```

### React artifact libraries (import in `.jsx`)

```jsx
// ── REACT CORE (always available) ─────────────────────────
import { useState, useEffect, useRef, useCallback, useMemo, useReducer } from "react";

// ── DATA VISUALISATION ─────────────────────────────────────
import { LineChart, BarChart, AreaChart, RadarChart, PieChart,
         Line, Bar, Area, Radar, Pie, Cell,
         XAxis, YAxis, CartesianGrid, Tooltip, Legend,
         ResponsiveContainer, ScatterChart, Scatter } from "recharts";
import * as d3 from "d3";

// ── UI COMPONENTS (shadcn/ui) ──────────────────────────────
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Tooltip as UITooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Skeleton } from "@/components/ui/skeleton";
import { Checkbox } from "@/components/ui/checkbox";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

// ── ICONS ──────────────────────────────────────────────────
import { Search, Star, Heart, ArrowRight, ChevronDown, X, Menu, Check,
         AlertCircle, Loader2, Play, Pause, RotateCcw, Settings, Trash2,
         Plus, Edit, Download, Upload, Copy, Eye, EyeOff, ChevronUp,
         ChevronLeft, ChevronRight, ExternalLink, Info, Zap } from "lucide-react";

// ── 3D & AUDIO ─────────────────────────────────────────────
import * as THREE from "three";   // r128 — no CapsuleGeometry, no OrbitControls via import
import * as Tone from "tone";

// ── CANVAS & CALENDAR ──────────────────────────────────────
import Konva from "konva";

// ── MATH & UTILITIES ───────────────────────────────────────
import * as math from "mathjs";
import _ from "lodash";
```

**Critical React artifact constraint:** `localStorage` and `sessionStorage` are NOT supported. Always use `useState` or `useReducer` for state.

---

## Step 6 — Encapsulation Rules (How to Build a Great Artifact)

These rules apply to every artifact regardless of which skill is used.

### 6.1 — Structure
- **One file, self-contained.** All CSS, JS, and HTML in a single file. No external file references except CDN libraries.
- **Libraries load before app code.** `<script>` tags for all CDN libraries come before your application `<script>` at the end of `<body>`.
- **CSS before JS.** All `<link>` stylesheet tags in `<head>`. JS `<script>` tags at end of `<body>`.
- **Explicit container heights.** Libraries like Leaflet, Tabulator, JointJS, vis-network, FullCalendar, Konva need an explicit CSS `height` on their container — never `auto`. Without this, they render as zero-height blank areas.

### 6.2 — Visual Presentation
- **Always dark theme by default.** Use `#0f1117` for page background unless the request explicitly asks for light mode.
- **Wrap content in a card.** Don't render raw components on a bare `<body>`. Always wrap in a centered `.card` or equivalent container with `border-radius`, `padding`, `background`, and `box-shadow`.
- **Provide a title and subtitle.** Every artifact has an `<h1>` (or `.title`) explaining what it is, and a brief subtitle explaining how to interact with it.
- **Add a hint line.** A small `<p>` below the title saying "Click to sort · Filter in header · Hover for details" — users need to know how to interact.

### 6.3 — Initialisation Order
Many libraries are async or need the DOM to be fully rendered. Always follow this order:
1. HTML markup (the containers / target divs)
2. CDN `<script>` tags (libraries)
3. Your app `<script>` at bottom of body
4. Inside your script: wait for `DOMContentLoaded` if needed, or initialise directly at script start (since scripts at end of body run after the DOM is ready)

### 6.4 — Interactivity
- **Every interactive element must have visible hover/focus states.** Buttons, table rows, map markers, graph nodes — all must respond visually to hover.
- **Error states are visible.** If data fails to load or a calculation errors, show a readable message — not a blank screen or console error.
- **Loading states exist.** If any initialization takes time (tile loading, large data), show a spinner or skeleton.
- **Actions have feedback.** Clicking "Copy", "Export", "Submit" must produce visible confirmation (a brief "Copied ✓" label, a success toast, a border flash).

### 6.5 — Performance
- **Cap pixel ratio at 2.** For canvas/WebGL: `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`.
- **Don't allocate in animation loops.** Pre-allocate all objects (`new THREE.Vector3()`, `createVector()`, etc.) outside the loop.
- **Virtual scrolling for large datasets.** Tabulator needs `height` set to enable virtual scrolling for >500 rows.
- **Cap at one animation frame request.** Never call `requestAnimationFrame` twice; cancel the previous before calling again.

---

## Step 7 — Universal Design System

Apply these tokens consistently across every artifact. Do not use browser defaults.

### Colour palette
```css
/* ── Surfaces (dark theme) ────────────────────────────── */
--bg-deep:      #0f1117   /* body / page background */
--bg-surface:   #1a1d27   /* card / panel */
--bg-elevated:  #1e2130   /* tooltip, dropdown, header */
--bg-overlay:   rgba(15,17,23,0.8)  /* modal backdrop, blurred HUD */

/* ── Borders & dividers ───────────────────────────────── */
--border:       rgba(255,255,255,0.08)
--border-hover: rgba(255,255,255,0.16)
--border-focus: rgba(99,102,241,0.5)

/* ── Text ─────────────────────────────────────────────── */
--text-primary: #f1f5f9   /* headings, important values */
--text-body:    #e2e8f0   /* body text */
--text-muted:   #94a3b8   /* labels, captions */
--text-faint:   #475569   /* placeholder, disabled */

/* ── Brand accent palette ─────────────────────────────── */
--indigo:   #6366f1    --indigo-light: #818cf8   --indigo-dim: rgba(99,102,241,0.15)
--violet:   #8b5cf6    --pink:         #ec4899
--cyan:     #06b6d4    --teal:         #14b8a6
--green:    #22c55e    --amber:        #eab308
--orange:   #f97316    --red:          #f43f5e
--blue:     #3b82f6
```

### Typography scale
```css
--text-xs:   0.72rem / 1.1   /* badge labels, captions, axis ticks */
--text-sm:   0.82rem / 1.4   /* table cells, secondary info */
--text-base: 1rem    / 1.5   /* body text */
--text-lg:   1.1rem  / 1.4   /* subheadings */
--text-xl:   1.3rem  / 1.3   /* card titles */
--text-2xl:  1.6rem  / 1.2   /* section headings */
--text-3xl:  2rem    / 1.1   /* hero text */
--text-hero: 2.8rem  / 1.0   /* stat values, big numbers */

font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
font-variant-numeric: tabular-nums;   /* for numbers/counters */
```

### Spacing grid (8px base unit)
```
4px   8px   12px   16px   24px   32px   48px   64px   96px
```
Use multiples of 4px for all padding, margin, and gap values.

### Elevation / shadow tokens
```css
--shadow-sm:  0 2px 8px rgba(0,0,0,0.3);
--shadow-md:  0 4px 20px rgba(0,0,0,0.4);
--shadow-lg:  0 8px 40px rgba(0,0,0,0.5);
--shadow-xl:  0 16px 60px rgba(0,0,0,0.6);
--shadow-glow-indigo: 0 0 20px rgba(99,102,241,0.35);
```

### Animation tokens
```css
--duration-fast:   150ms
--duration-normal: 250ms
--duration-slow:   400ms
--ease-out:        cubic-bezier(0.16, 1, 0.3, 1)  /* snappy deceleration */
--ease-in-out:     cubic-bezier(0.65, 0, 0.35, 1) /* smooth both ways */
```

### Micro-interaction rules
- **Hover lift:** `transform: translateY(-2px)` + `box-shadow` increase on cards and buttons
- **Hover glow:** `border-color` shift to `--border-focus` + optional `box-shadow` with brand color
- **Active press:** `transform: scale(0.97)` on click
- **Transition everything:** `transition: all 200ms cubic-bezier(0.16, 1, 0.3, 1)` on interactive elements
- **Badge/tag style:** `background: rgba(color, 0.15)`, `color: colorLight`, `border: 1px solid rgba(color, 0.3)`, `border-radius: 999px`

---

## Step 8 — Presentation Patterns

### The card wrapper (standard output container)
```html
<div style="
  background: #1a1d27;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.07);
  padding: 28px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.5);
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
">
  <div style="margin-bottom: 20px;">
    <h1 style="font-size:1.15rem; font-weight:600; color:#f1f5f9">Title</h1>
    <p style="font-size:0.8rem; color:#64748b; margin-top:3px">
      Hint · how to interact
    </p>
  </div>
  <!-- library container or content here -->
</div>
```

### The HUD overlay (for fullscreen canvas/WebGL artifacts)
```html
<div style="
  position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
  background: rgba(26,29,39,0.85); backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;
  padding: 10px 20px; color: #94a3b8; font-size: 12px;
  pointer-events: none; white-space: nowrap; z-index: 100;
">
  Drag to orbit · Scroll to zoom · Click to interact
</div>
```

### The stat strip (KPI row above a chart or table)
```html
<div style="display:flex; gap:24px; margin-bottom:20px; flex-wrap:wrap;">
  <div>
    <p style="font-size:0.72rem; color:#64748b; text-transform:uppercase; letter-spacing:0.05em">Revenue</p>
    <p style="font-size:1.8rem; font-weight:700; color:#f1f5f9; font-variant-numeric:tabular-nums">$48,295</p>
    <p style="font-size:0.75rem; color:#22c55e; margin-top:2px">↑ +12.5%</p>
  </div>
  <!-- more stats -->
</div>
```

### The action toolbar (above tables, below charts)
```html
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; flex-wrap:wrap; gap:10px;">
  <div style="display:flex; gap:8px;">
    <button style="/* primary button styles */">Export CSV</button>
    <button style="/* ghost button styles */">Clear filters</button>
  </div>
  <p id="status" style="font-size:12px; color:#64748b;">24 records shown</p>
</div>
```

### Button style tokens (copy-paste ready)
```css
/* Primary */
background: #6366f1; color: #fff; border: none;
border-radius: 8px; padding: 7px 16px; font-size: 13px; font-weight: 500;
cursor: pointer; transition: background 0.15s;
/* :hover → background: #5254cc */

/* Ghost */
background: rgba(255,255,255,0.06); color: #94a3b8;
border: 1px solid rgba(255,255,255,0.1);
border-radius: 8px; padding: 7px 16px; font-size: 13px;
cursor: pointer; transition: all 0.15s;
/* :hover → background: rgba(255,255,255,0.1); color: #f1f5f9 */

/* Destructive */
background: rgba(244,63,94,0.1); color: #f43f5e;
border: 1px solid rgba(244,63,94,0.2);
border-radius: 8px; padding: 7px 16px; font-size: 13px;
cursor: pointer;
```

---

## Step 9 — Creative Patterns by Category

### Entrance animations (use `animejs-animation` skill)
Every artifact should have an entrance animation. Minimum: fade + translateY on the main card.
```javascript
// With Anime.js v4
const { animate, stagger } = anime;
animate('.card', { opacity: [0, 1], y: [20, 0], duration: 600, ease: 'outExpo' });
animate('.stat', { opacity: [0, 1], y: [12, 0], delay: stagger(80), duration: 500, ease: 'outExpo' });

// Without Anime.js — pure CSS
.card { animation: fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) both; }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Generative art skeleton (use `p5js-creative-coding` skill)
```html
<script src="https://cdn.jsdelivr.net/npm/p5@2.2.2/lib/p5.min.js"></script>
<script>
  function setup() {
    createCanvas(windowWidth, windowHeight);
    colorMode(HSB, 360, 100, 100, 100);
  }
  function draw() { /* generative loop */ }
  function windowResized() { resizeCanvas(windowWidth, windowHeight); }
</script>
```

### 3D scene skeleton (use `threejs-3d` skill)
```html
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.183.2/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.183.2/examples/jsm/"}}</script>
<script type="module">
  import * as THREE from 'three';
  import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
  // scene + camera + renderer + controls + animate() loop
</script>
```

### Mini game loop
```javascript
let lastTime = 0;
function loop(timestamp) {
  const dt = Math.min((timestamp - lastTime) / 16.67, 3); // cap at 3× (tab hidden)
  lastTime = timestamp;
  update(dt);
  draw();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
```

### Presentation skeleton (use `reveal-slides` skill)
```html
<link  rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
<link  rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/black.css">
<div class="reveal"><div class="slides">
  <section>Slide 1</section>
  <section>Slide 2</section>
</div></div>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
<script>Reveal.initialize({ hash: true });</script>
```

### Calendar skeleton (use `fullcalendar` skill)
```html
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@6/index.global.min.js"></script>
<div id="calendar" style="max-width:900px; margin:auto;"></div>
<script>
  const cal = new FullCalendar.Calendar(document.getElementById('calendar'), {
    initialView: 'dayGridMonth', headerToolbar: { left:'prev,next today', center:'title', right:'dayGridMonth,timeGridWeek,listWeek' },
    events: []
  });
  cal.render();
</script>
```

### Audio synth skeleton (use `tone-audio` skill)
```html
<script src="https://cdn.jsdelivr.net/npm/tone@14.8.49/build/Tone.js"></script>
<script>
  const synth = new Tone.PolySynth(Tone.Synth).toDestination();
  document.getElementById('playBtn').addEventListener('click', async () => {
    await Tone.start();
    synth.triggerAttackRelease('C4', '8n');
  });
</script>
```

### Canvas editor skeleton (use `konva-canvas` skill)
```html
<script src="https://cdn.jsdelivr.net/npm/konva@9/konva.min.js"></script>
<div id="container" style="width:800px; height:500px;"></div>
<script>
  const stage = new Konva.Stage({ container: 'container', width: 800, height: 500 });
  const layer = new Konva.Layer();
  stage.add(layer);
  // Add shapes, Transformer, event handlers…
</script>
```

### GSAP scroll animation skeleton (use `gsap-animation` skill)
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<script>
  gsap.registerPlugin(ScrollTrigger);
  gsap.from('.section', {
    scrollTrigger: { trigger: '.section', start: 'top 80%' },
    opacity: 0, y: 60, duration: 0.8, stagger: 0.2
  });
</script>
```

### Animated counter
```javascript
// Pure JS animated counter (no library needed)
function animateCounter(el, from, to, duration = 1200, suffix = '') {
  const start = performance.now();
  const isFloat = (to % 1 !== 0);
  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - t, 3); // easeOutCubic
    const val = from + (to - from) * ease;
    el.textContent = (isFloat ? val.toFixed(2) : Math.round(val).toLocaleString()) + suffix;
    if (t < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
```

---

## Step 10 — Polish Checklist

Before delivering any artifact:

**Functionality**
- [ ] All interactive elements respond correctly
- [ ] No console errors (check edge cases, empty states, zero values)
- [ ] Loading/initialisation state is shown when needed
- [ ] Async operations have visible feedback

**Encapsulation**
- [ ] Single file, no external file references
- [ ] Libraries load before app script
- [ ] Container has explicit height if required by the library
- [ ] `const { ... } = libraryGlobal` destructuring at top of script (not inline)

**Design**
- [ ] Dark theme applied (`#0f1117` background, design system tokens used)
- [ ] Content wrapped in a card or equivalent — not bare on `<body>`
- [ ] Title + subtitle + interaction hint present
- [ ] Typography hierarchy is clear: heading > body > caption
- [ ] Sufficient contrast (≥ 4.5:1 body text, ≥ 3:1 large text)
- [ ] Hover/active states on every interactive element
- [ ] Spacing follows 8px grid
- [ ] Responsive (no overflow or breakage on narrow viewport)
- [ ] No raw `<form>` tags (React) — use event handlers

**Delight**
- [ ] At least one meaningful entrance animation or transition
- [ ] Micro-feedback on interactions (button press, copy confirm, selection)
- [ ] The artifact's purpose is immediately obvious on first look
- [ ] There is one design choice that goes beyond functional — something that makes the user pause and notice

---

## Step 11 — Creative Mandate

**The default output from this skill should be surprising.** When the request leaves room for creative interpretation:

- Choose a visual direction — commit to it, don't hedge with generic defaults
- Add an animation that wasn't asked for, if it elevates the result
- Pick a deliberate colour treatment — don't use browser defaults
- Include micro-interactions: hover lift, press feedback, transition
- If you're building a tool, make the output feel **designed**, not printed
- If you're building art, make it **move and breathe**
- If you're building a data view, make the **first number the user sees** feel significant

The question to ask before finalising: *"Would I be proud to show this to someone?"*

If the answer is "it works but looks generic", it's not done yet.
