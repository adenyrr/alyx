---
name: vis-timeline
description: Create interactive, fully customizable timeline visualizations using vis-timeline, delivered as self-contained HTML artifacts. Use this skill whenever someone needs to display events, milestones, project schedules, historical data, or any data series positioned along a time axis — with or without groups/lanes. Trigger on any request mentioning timelines, Gantt-like charts, chronologies, project planning views, event sequences, historical visualizations, or roadmaps. Prefer this skill over generic charting tools whenever the primary axis is time and items need to be placed, dragged, or explored interactively.
---

# vis-timeline Skill

vis-timeline renders interactive timelines in the browser using HTML DOM (not Canvas), making items fully styleable with CSS. It supports point events, ranged blocks, background bands, grouping into lanes, custom HTML content, drag-and-drop editing, zooming, and a custom time marker.

---

## Artifact Presentation & Use Cases

Every vis-timeline artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the timeline
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the timeline
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context and interaction hints
- **Timeline container** (`#timeline`, fixed height) renders the interactive timeline with CSS-styled items
- **Optional legend or controls** for filtering groups or toggling views

### Typical use cases

- **Project schedules** — task bars grouped by team/phase with start and end dates
- **Historical timelines** — events placed chronologically with descriptions and images
- **Roadmaps** — milestones and features across multiple tracks/workstreams
- **Event sequences** — log entries, incidents, or activities along a time axis
- **Gantt-like views** — resource allocation with grouped lanes and overlapping ranges
- **Process timelines** — step-by-step workflows with duration visualization

### What the user sees

An interactive timeline: scroll horizontally to move through time, scroll vertically to see groups, drag items to reschedule, zoom in/out for different time granularity. Items are styled DOM elements (not canvas) so they support rich HTML content and CSS hover effects.

---

## When to Use vis-timeline vs. Alternatives

| Use vis-timeline when… | Use another tool when… |
|---|---|
| Time-based data with start/end dates | Static, text-based Gantt charts → **Mermaid** (simpler syntax) |
| Grouped lanes (teams, categories) | Node-edge relationship graphs → **vis-network** |
| Drag-and-drop item editing | Data charts (bar, line, pie) → **Chart.js / Plotly** |
| Zoomable time navigation | Geographic maps → **Leaflet** |
| Custom HTML content in items | SVG-based custom timeline visualizations → **D3** |
| Interactive project planning views | Tabular schedule data → **Tabulator** |

> **Rule of thumb:** if the primary axis is time and items need to be placed, explored, or edited along that axis, vis-timeline is the right choice. For static Gantt charts in documentation, Mermaid is simpler.

---

## Step 1 — CDN Setup (CRITICAL: two files required)

vis-timeline **always** requires both a JS file and a CSS file. Missing the CSS produces a broken, unstyled layout.

```html
<!-- Standalone build: self-contained, no extra dependencies -->
<script src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
<link  href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet" />
```

The standalone build bundles all dependencies (including Moment.js). Use it for single-file artifacts. The `vis` global is available after loading.

---

## Step 2 — HTML Artifact Shell

The timeline container **must have an explicit height**. It will fill the available width automatically.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Timeline</title>

  <!-- vis-timeline: JS + CSS both required -->
  <script src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
  <link  href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet" />

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
      max-width: 1000px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }

    /* Container: MUST have explicit height */
    #timeline { width: 100%; height: 300px; }

    /* ── Dark theme overrides ───────────────────────────── */
    .vis-timeline { border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 8px; background: #1a1d27; }
    .vis-time-axis .vis-text { color: #94a3b8 !important; }
    .vis-time-axis .vis-grid.vis-minor { border-color: rgba(255,255,255,0.05) !important; }
    .vis-time-axis .vis-grid.vis-major { border-color: rgba(255,255,255,0.1) !important; }
    .vis-panel.vis-center,
    .vis-panel.vis-left,
    .vis-panel.vis-right { border-color: rgba(255,255,255,0.08) !important; }
    .vis-label { color: #94a3b8 !important; background: #1a1d27 !important; border-right: 1px solid rgba(255,255,255,0.08) !important; }
    .vis-current-time { background: #f43f5e !important; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Project Timeline</h1>
    <p class="sub">Interactive — scroll to zoom, drag to pan</p>
    <div id="timeline"></div>
  </div>

  <script>
    // All vis-timeline code here
  </script>
</body>
</html>
```

---

## Step 3 — Data Format

### Items (required)

```javascript
const items = new vis.DataSet([
  // Point event — single moment
  { id: 1, content: 'Kickoff',      start: '2025-01-10' },

  // Range — start + end block
  { id: 2, content: 'Development',  start: '2025-01-15', end: '2025-03-01' },

  // Range with group (lane)
  { id: 3, content: 'Testing',      start: '2025-02-20', end: '2025-03-15', group: 1 },

  // Background band — colors the entire time range behind items
  { id: 4, content: '',             start: '2025-02-01', end: '2025-02-28', type: 'background', className: 'sprint-bg' },

  // HTML content inside an item
  { id: 5, content: '<b>🚀 Launch</b>', start: '2025-04-01', type: 'point' },

  // Individual style override
  { id: 6, content: 'Blocked',      start: '2025-01-20', end: '2025-01-25', style: 'background-color: #ef4444; border-color: #b91c1c; color: white;' },

  // Custom CSS class
  { id: 7, content: 'Milestone',    start: '2025-03-20', className: 'milestone-item' },

  // Tooltip on hover
  { id: 8, content: 'Review',       start: '2025-03-10', end: '2025-03-15', title: 'Peer review session — 3 reviewers assigned' },
]);
```

**Item type reference:**

| `type`        | `start` | `end`    | Renders as                         |
|--------------|---------|----------|------------------------------------|
| `'box'`      | ✓       | —        | Vertical line + label box (default)|
| `'point'`    | ✓       | —        | Dot on the axis                    |
| `'range'`    | ✓       | ✓        | Horizontal block bar               |
| `'background'| ✓       | ✓        | Full-height colored band (no label)|

### Groups (optional — creates swim lanes)

```javascript
const groups = new vis.DataSet([
  { id: 1, content: 'Frontend' },
  { id: 2, content: 'Backend' },
  { id: 3, content: 'QA',        style: 'color: #6366f1; font-weight: 600;' },

  // Nested groups
  { id: 4, content: 'Engineering', nestedGroups: [1, 2] },

  // Hidden group (collapsible)
  { id: 5, content: 'Infra', visible: true, showNested: false },
]);
```

---

## Step 4 — Constructor & Initialization

```javascript
const container = document.getElementById('timeline');

// With items only
const timeline = new vis.Timeline(container, items, options);

// With groups
const timeline = new vis.Timeline(container, items, groups, options);
```

---

## Step 5 — Key Configuration Options

```javascript
const options = {
  // ── Time window ──────────────────────────────────────────
  start:          '2025-01-01',     // initial visible start (Date, string, or timestamp)
  end:            '2025-06-01',     // initial visible end
  min:            '2024-01-01',     // hard pan limit (cannot scroll before this)
  max:            '2027-01-01',     // hard pan limit (cannot scroll after this)
  zoomMin:        1000 * 60 * 60,   // min zoom = 1 hour (ms)
  zoomMax:        1000 * 60 * 60 * 24 * 365 * 2, // max zoom = 2 years

  // ── Layout ───────────────────────────────────────────────
  height:         '350px',          // or number (px); null = auto-fit content
  minHeight:      '200px',
  maxHeight:      '600px',
  orientation:    { axis: 'top' },  // 'top' | 'bottom' | 'both' — axis position
  align:          'center',         // item label alignment: 'auto'|'center'|'left'|'right'
  stack:          true,             // stack overlapping items (disable for Gantt feel)
  stackSubgroups: true,
  showMajorLabels: true,            // e.g. "January 2025"
  showMinorLabels: true,            // e.g. "Mon 6"
  showCurrentTime: true,            // red "now" line

  // ── Item styling ─────────────────────────────────────────
  margin: {
    item:  { horizontal: 10, vertical: 5 },
    axis:  5,
  },

  // ── Interaction ──────────────────────────────────────────
  selectable:     true,
  multiselect:    false,
  moveable:       true,             // allow panning
  zoomable:       true,             // allow scrolling to zoom
  horizontalScroll: false,
  verticalScroll:   false,
  clickToUse:     false,            // set true to prevent page scroll conflicts

  // ── Editing ──────────────────────────────────────────────
  editable: false,
  // or granular:
  editable: {
    add:         false,   // double-click empty space to create item
    updateTime:  true,    // drag item left/right
    updateGroup: true,    // drag item between groups
    remove:      true,    // click delete button on selected item
    overrideItems: false, // item-level editable overrides this when false
  },

  // ── Custom time axis labels ───────────────────────────────
  format: {
    minorLabels: {
      minute: 'HH:mm',
      hour:   'HH:mm',
      day:    'D',
      week:   'w',
      month:  'MMM',
      year:   'YYYY',
    },
    majorLabels: {
      hour:    'ddd D MMM',
      day:     'MMMM YYYY',
      week:    'MMMM YYYY',
      month:   'YYYY',
    },
  },

  // ── Groups ───────────────────────────────────────────────
  groupOrder:      'order',         // field name or sort function
  groupHeightMode: 'auto',          // 'auto' | 'fixed' | 'fitItems'

  // ── Tooltip ──────────────────────────────────────────────
  tooltip: {
    followMouse:    true,
    overflowMethod: 'cap',          // 'cap' | 'flip'
  },
};
```

---

## Step 6 — Methods Reference

```javascript
// ── Window control ───────────────────────────────────────────
timeline.setWindow('2025-02-01', '2025-04-01');                    // pan to range
timeline.setWindow('2025-02-01', '2025-04-01', { animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
timeline.moveTo('2025-03-15');                                      // center on date
timeline.fit();                                                     // fit all items in view
timeline.zoomIn(0.5);                                              // zoom in by 50%
timeline.zoomOut(0.5);

const { start, end } = timeline.getWindow();                       // get current window

// ── Data ─────────────────────────────────────────────────────
timeline.setItems(newItemsDataSet);
timeline.setGroups(newGroupsDataSet);
timeline.setOptions({ stack: false });                             // live option update

// ── Selection ────────────────────────────────────────────────
timeline.setSelection([2, 3]);                                     // select by id(s)
const sel = timeline.getSelection();                               // returns [id, ...]
timeline.focus(3);                                                 // scroll to item id

// ── Custom time marker ────────────────────────────────────────
timeline.addCustomTime(new Date(), 'deadline');                    // add marker with id
timeline.setCustomTime(new Date('2025-05-01'), 'deadline');        // move marker
timeline.removeCustomTime('deadline');

// ── Misc ─────────────────────────────────────────────────────
timeline.redraw();
timeline.destroy();                                                // remove from DOM + cleanup
```

---

## Step 7 — Events

```javascript
// Click on an item
timeline.on('click', (props) => {
  // props: { event, item (id or null), group, time, snappedTime, what, pageX, pageY }
  if (props.item !== null) {
    console.log('Clicked item:', props.item);
  }
});

// Double-click (create item when editable.add is true)
timeline.on('doubleClick', (props) => { ... });

// Selection changed
timeline.on('select', ({ items }) => {
  console.log('Selected ids:', items);
});

// View window changed (pan or zoom)
timeline.on('rangechange',  ({ start, end, byUser }) => { ... });
timeline.on('rangechanged', ({ start, end, byUser }) => { ... });  // after interaction ends

// Item dragged to a new time (editable.updateTime = true)
timeline.on('itemover',  ({ item, time }) => { ... });
timeline.on('itemout',   ({ item, time }) => { ... });

// Custom time marker dragged
timeline.on('timechange',  ({ id, time }) => { ... });
timeline.on('timechanged', ({ id, time }) => { ... });

// Remove event listener
timeline.off('click', handler);

// Editing callbacks (via options)
const options = {
  onAdd:    (item, callback) => { callback(item); },          // confirm/reject add
  onUpdate: (item, callback) => { callback(item); },          // confirm/reject update
  onMove:   (item, callback) => { callback(item); },          // confirm/reject move (return null to reject)
  onRemove: (item, callback) => { callback(item); },          // confirm/reject remove
  onMoving: (item, callback) => { callback(item); },          // called while dragging (modify item live)
};
```

---

## Step 8 — DataSet Live Updates (Two-Way Binding)

When items are stored in a `vis.DataSet`, updating the dataset instantly updates the rendered timeline — no `.setItems()` needed.

```javascript
// Add
items.add({ id: 10, content: 'New Sprint', start: '2025-05-01', end: '2025-05-14' });

// Update
items.update({ id: 2, content: 'Development v2', end: '2025-03-10' });

// Remove
items.remove(3);

// Batch update
items.update([
  { id: 1, style: 'background: #22c55e; color: white;' },
  { id: 2, className: 'completed' },
]);
```

---

## Step 9 — CSS Theming & Custom Styles

vis-timeline is styled entirely with CSS. All important selectors:

```css
/* ── Item types ───────────────────────────────── */
.vis-item                    { /* all items */ }
.vis-item.vis-box            { /* point/box items */ }
.vis-item.vis-range          { /* range items */ }
.vis-item.vis-background     { /* background bands */ }
.vis-item.vis-selected       { /* selected state */ }
.vis-item.vis-editable       { /* when draggable */ }

/* Default vis item colors (override to theme) */
.vis-item {
  border-color:       rgba(99,102,241,0.6);
  background-color:   rgba(99,102,241,0.2);
  color:              #f1f5f9;
  border-radius:      6px;
  font-size:          13px;
}
.vis-item.vis-selected {
  border-color:       #6366f1;
  background-color:   rgba(99,102,241,0.5);
}

/* ── Time axis ────────────────────────────────── */
.vis-time-axis .vis-text            { color: #94a3b8; font-size: 11px; }
.vis-time-axis .vis-grid.vis-minor  { border-color: rgba(255,255,255,0.05); }
.vis-time-axis .vis-grid.vis-major  { border-color: rgba(255,255,255,0.1); }

/* ── Group labels (left panel) ───────────────── */
.vis-label                          { color: #94a3b8; background: #1a1d27; padding: 0 12px; }
.vis-label.vis-nesting-group        { font-weight: 600; color: #e2e8f0; }

/* ── "Now" line ──────────────────────────────── */
.vis-current-time                   { background-color: #f43f5e; width: 2px; }

/* ── Custom time marker ──────────────────────── */
.vis-custom-time                    { background-color: #f97316; width: 2px; }
.vis-custom-time > .vis-custom-time-marker { background: #f97316; color: white; border-radius: 4px; padding: 2px 6px; font-size: 11px; }

/* ── Per-item custom class ───────────────────── */
.vis-item.milestone-item {
  background-color: rgba(234,179,8,0.25);
  border-color: #eab308;
  color: #fef08a;
  border-radius: 50%;
}
.vis-item.sprint-bg.vis-background {
  background-color: rgba(99,102,241,0.05);
}
```

---

## Step 10 — Templates (HTML content in items/groups)

```javascript
const options = {
  // Custom item content via template function
  template: (item, element, data) => {
    return `
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="width:8px;height:8px;border-radius:50%;background:${data.color || '#6366f1'};flex-shrink:0;"></span>
        <span>${item.content}</span>
      </div>
    `;
  },

  // Custom group label
  groupTemplate: (group, element) => {
    return `<div style="font-weight:600;color:#a5b4fc;">${group.content}</div>`;
  },
};
```

---

## Step 11 — Design & Polish Guidelines

- **Dark CSS overrides** — always include the full dark theme CSS from Step 9; missing overrides leave white backgrounds on the time axis, group labels, or item text
- **Item colors** — use the design system accent colors (`#6366f1`, `#8b5cf6`, `#22c55e`) as item backgrounds with `rgba()` for transparency
- **Group styling** — style `.vis-label` for group sidebar labels; use subtle borders between groups for visual separation
- **Time axis** — style `.vis-time-axis .vis-text` with `color: #94a3b8` for readable axis labels on dark backgrounds
- **Zoom constraints** — use `zoomMin` / `zoomMax` to prevent users from zooming into milliseconds or out to centuries
- **Initial window** — always set `start` and `end` in options (or `fit()` after adding items) to show a meaningful default view
- **Tooltips** — use `title` property on items for lightweight tooltips, or `template` for rich HTML content inside items
- **Stack optimization** — `stack: true` prevents item overlap; disable only for background items or when density is intentional
- **Accessibility** — add descriptive `<h1>` and `aria-label` on the timeline container; vis-timeline items are DOM elements and inherit focus management

---

## Step 12 — Complete Example: Multi-Group Project Timeline

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Project Timeline</title>
  <script src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
  <link  href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet" />
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 32px; width: 100%; max-width: 1000px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
    #timeline { width: 100%; height: 320px; }

    /* Dark theme */
    .vis-timeline { border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 8px; background: #1a1d27 !important; }
    .vis-time-axis .vis-text { color: #94a3b8 !important; font-size: 11px; }
    .vis-time-axis .vis-grid.vis-minor { border-color: rgba(255,255,255,0.04) !important; }
    .vis-time-axis .vis-grid.vis-major { border-color: rgba(255,255,255,0.1) !important; }
    .vis-panel.vis-center, .vis-panel.vis-left, .vis-panel.vis-right, .vis-panel.vis-top, .vis-panel.vis-bottom { border-color: rgba(255,255,255,0.08) !important; }
    .vis-label { color: #94a3b8 !important; background: #161923 !important; border-right: 1px solid rgba(255,255,255,0.08) !important; font-size: 13px; padding: 0 12px; }
    .vis-current-time { background: rgba(244,63,94,0.8) !important; }

    /* Item styles */
    .vis-item { border-radius: 5px !important; font-size: 12px !important; }
    .vis-item.vis-range { padding: 3px 8px !important; }
    .vis-item.vis-selected { box-shadow: 0 0 0 2px #6366f1 !important; }

    /* Per-group colors via className */
    .vis-item.frontend  { background: rgba(99,102,241,0.25) !important; border-color: #6366f1 !important; color: #a5b4fc !important; }
    .vis-item.backend   { background: rgba(139,92,246,0.25) !important; border-color: #8b5cf6 !important; color: #c4b5fd !important; }
    .vis-item.qa        { background: rgba(34,197,94,0.2)  !important; border-color: #22c55e !important; color: #86efac !important; }
    .vis-item.milestone { background: rgba(234,179,8,0.2)  !important; border-color: #eab308 !important; color: #fef08a !important; border-radius: 12px !important; }
    .vis-item.sprint-bg.vis-background { background: rgba(255,255,255,0.02) !important; border: none !important; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Q1–Q2 2025 Roadmap</h1>
    <p class="sub">Scroll to zoom · Drag to pan · Click to select</p>
    <div id="timeline"></div>
  </div>
  <script>
    const groups = new vis.DataSet([
      { id: 1, content: 'Frontend' },
      { id: 2, content: 'Backend'  },
      { id: 3, content: 'QA'       },
    ]);

    const items = new vis.DataSet([
      // Background sprints
      { id: 10, type: 'background', start: '2025-01-06', end: '2025-01-19', className: 'sprint-bg', content: '' },
      { id: 11, type: 'background', start: '2025-01-20', end: '2025-02-02', className: 'sprint-bg', content: '' },
      { id: 12, type: 'background', start: '2025-02-03', end: '2025-02-16', className: 'sprint-bg', content: '' },

      // Frontend lane
      { id: 1, group: 1, content: 'UI Design',       start: '2025-01-06', end: '2025-01-17', className: 'frontend' },
      { id: 2, group: 1, content: 'Component Build',  start: '2025-01-20', end: '2025-02-14', className: 'frontend' },
      { id: 3, group: 1, content: 'Integration',      start: '2025-02-17', end: '2025-03-07', className: 'frontend' },

      // Backend lane
      { id: 4, group: 2, content: 'API Design',       start: '2025-01-06', end: '2025-01-12', className: 'backend' },
      { id: 5, group: 2, content: 'Core Services',    start: '2025-01-13', end: '2025-02-21', className: 'backend' },
      { id: 6, group: 2, content: 'Auth & Security',  start: '2025-02-10', end: '2025-03-01', className: 'backend' },

      // QA lane
      { id: 7, group: 3, content: 'Test Planning',    start: '2025-01-20', end: '2025-01-31', className: 'qa' },
      { id: 8, group: 3, content: 'Regression Suite', start: '2025-02-17', end: '2025-03-07', className: 'qa' },

      // Milestones
      { id: 9,  type: 'box', content: '🚀 Beta', start: '2025-03-10', className: 'milestone', title: 'Beta release to staging' },
      { id: 13, type: 'box', content: '✅ Launch', start: '2025-04-01', className: 'milestone', title: 'Public launch' },
    ]);

    const timeline = new vis.Timeline(
      document.getElementById('timeline'),
      items,
      groups,
      {
        start:          '2025-01-01',
        end:            '2025-04-15',
        min:            '2024-11-01',
        max:            '2026-01-01',
        zoomMin:        1000 * 60 * 60 * 24 * 7,
        stack:          true,
        showCurrentTime: true,
        margin:         { item: { horizontal: 8, vertical: 4 }, axis: 4 },
        orientation:    { axis: 'top' },
        tooltip:        { followMouse: true },
      }
    );

    // Click interaction
    timeline.on('click', ({ item }) => {
      if (item) timeline.focus(item, { animation: { duration: 400, easingFunction: 'easeInOutQuad' } });
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Missing CSS file** — the most frequent issue; the timeline renders broken without `vis-timeline-graph2d.min.css`
- **No explicit height on container** — the `#timeline` div must have a CSS height set; `height: auto` renders nothing
- **Passing plain Arrays instead of DataSet** — both work for initial load, but only `vis.DataSet` supports live `.add()` / `.update()` / `.remove()`
- **Date strings without timezone** — use ISO format `'2025-03-15'` (date only) or `'2025-03-15T09:00:00'` to avoid timezone offset bugs
- **`content` is HTML** — sanitize any user-provided strings before passing to `content` to prevent XSS
- **Forgetting `.destroy()`** — on SPA route changes, call `timeline.destroy()` to remove event listeners and DOM nodes
- **CSS specificity fights** — vis-timeline uses inline styles for some elements; use `!important` in custom CSS when overriding doesn't work
