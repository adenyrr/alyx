---
name: tabulator
description: Create beautiful, interactive data tables and grids using Tabulator.js v6, delivered as self-contained HTML artifacts. Use this skill whenever someone needs to display, sort, filter, search, paginate, group, or edit tabular data in the browser — even without explicit mention of Tabulator. Trigger on requests like "display this data in a table", "make a sortable list", "create a data grid", "build an editable table", "show this dataset with filters", "make a spreadsheet-like view", or any request to present rows and columns of data with interactivity. Do NOT use for static HTML tables (plain CSS suffices), data charts or graphs (→ charting skill), or network/relational visualizations (→ vis-network skill).
---

# Tabulator Skill — Interactive Data Tables

Tabulator turns any JavaScript array or JSON into a fully interactive data grid: sortable, filterable, paginated, editable, exportable — with zero dependencies.

---

## Artifact Presentation & Use Cases

Every Tabulator artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the table
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the dataset
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context and interaction hints
- **Tabulator container** renders the fully interactive data grid (dark-themed headers, rows, pagination controls)

### Typical use cases

- **Data exploration** — display any dataset with instant sorting, filtering, and searching
- **CRUD interfaces** — inline editable cells for user-managed data (inventories, contacts, settings)
- **Dashboards** — paginated data grids with grouped rows and summary calculations
- **Report tables** — formatted columns (currency, dates, progress bars, stars) with export to CSV/XLSX
- **API data display** — load remote JSON endpoints with Ajax and display results interactively
- **Comparison tables** — frozen columns, multi-column sorting, and row selection for side-by-side analysis

### What the user sees

A polished data grid: click column headers to sort, type in header filters to search, navigate pages at the bottom, click rows to select them. Columns resize and align automatically. The dark theme blends seamlessly with the card wrapper.

---

## When to Use Tabulator vs. Alternatives

| Use Tabulator when… | Use another tool when… |
|---|---|
| Displaying rows & columns of structured data | Visualizing data as charts or graphs → **Chart.js / Plotly** |
| Need sorting, filtering, pagination, editing | Simple static table with < 20 rows → **plain HTML/CSS** |
| Inline editing (text, select, autocomplete) | Spreadsheet-level formulas and cell references → **dedicated spreadsheet** |
| 10,000+ rows via virtual DOM scrolling | Complex relational data + node-edge graph → **vis-network** |
| Export to CSV, XLSX, JSON, PDF | Timeline or Gantt display → **vis-timeline** |
| Ajax / remote data loading | Layout and design (not tabular data) → **Tailwind / Bulma** |

> **Rule of thumb:** if the data is naturally rows and columns and users need to sort, filter, or edit it, Tabulator is the right choice. For anything visual (charts, diagrams, maps), use a dedicated visualization skill.

---

## Step 1 — CDN Setup

Tabulator requires **both** a CSS file and a JS file. The CSS is not optional — without it the table renders as unstyled HTML.

```html
<!-- CSS first, in <head> -->
<link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css" rel="stylesheet">

<!-- JS before your script, at end of <body> -->
<script src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>
```

> **⚠️ Critical:** Tabulator uses an **asynchronous initialization process**. Do not call table methods (`.setData()`, `.setFilter()`, etc.) before the `tableBuilt` event fires. Always wrap post-init logic in that callback.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Data Table</title>

  <!-- 1. Tabulator CSS -->
  <link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css" rel="stylesheet">

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

    /* Dark theme overrides — see Step 3 for full theming */
    .tabulator {
      background: transparent;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      overflow: hidden;
      font-size: 13px;
    }
    .tabulator .tabulator-header { background: #1e2130; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .tabulator .tabulator-header .tabulator-col { background: transparent; border-right: 1px solid rgba(255,255,255,0.06); color: #94a3b8; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }
    .tabulator .tabulator-header .tabulator-col:hover { background: rgba(255,255,255,0.04); }
    .tabulator-row { background: transparent; border-bottom: 1px solid rgba(255,255,255,0.05); color: #e2e8f0; }
    .tabulator-row:hover { background: rgba(255,255,255,0.04) !important; }
    .tabulator-row.tabulator-selectable:hover { background: rgba(99,102,241,0.08) !important; }
    .tabulator-row.tabulator-selected { background: rgba(99,102,241,0.15) !important; }
    .tabulator .tabulator-footer { background: #1e2130; border-top: 1px solid rgba(255,255,255,0.08); color: #94a3b8; }
    .tabulator-page { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; border-radius: 4px; margin: 0 2px; }
    .tabulator-page.active { background: #6366f1; border-color: #6366f1; color: #fff; }
    .tabulator-page:hover:not(.active) { background: rgba(255,255,255,0.06); color: #f1f5f9; }
    .tabulator-col-sorter .tabulator-arrow { border-bottom-color: #475569; }
    .tabulator-col.tabulator-sortable.tabulator-col-sorter-element .tabulator-arrow { border-bottom-color: #6366f1; }
    .tabulator-header-filter input, .tabulator-header-filter select { background: #0f1117; border: 1px solid rgba(255,255,255,0.1); color: #e2e8f0; border-radius: 4px; padding: 3px 6px; font-size: 12px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Table Title</h1>
    <p class="sub">Brief description · click headers to sort · filter in column headers</p>

    <!-- The table container — Tabulator fills this -->
    <div id="data-table"></div>
  </div>

  <!-- 2. Tabulator JS -->
  <script src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>
  <script>
    // All Tabulator code here
  </script>
</body>
</html>
```

---

## Step 3 — Dark Theme Reference

The CSS overrides in the shell above cover the essentials. Key selectors to know:

```css
/* Table shell */
.tabulator { }
.tabulator .tabulator-header { }
.tabulator .tabulator-header .tabulator-col { }     /* each header cell */
.tabulator .tabulator-header .tabulator-col:hover { }

/* Rows */
.tabulator-row { }
.tabulator-row:nth-child(even) { }                  /* striped rows */
.tabulator-row:hover { }
.tabulator-row.tabulator-selected { }               /* selected row */

/* Cells */
.tabulator-cell { }
.tabulator-cell.tabulator-editing { }               /* cell being edited */

/* Footer & pagination */
.tabulator .tabulator-footer { }
.tabulator-page { }
.tabulator-page.active { }

/* Filters in header */
.tabulator-header-filter input { }
.tabulator-header-filter select { }
```

Built-in themes (apply by swapping the CSS file):
```html
<!-- Default -->
<link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css" rel="stylesheet">
<!-- Midnight (dark, pre-built) -->
<link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_midnight.min.css" rel="stylesheet">
<!-- Modern -->
<link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_modern.min.css" rel="stylesheet">
<!-- Bootstrap 5 -->
<link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_bootstrap5.min.css" rel="stylesheet">
```

> Use `tabulator_midnight.min.css` as a starting point for dark themes, then override with your own CSS on top.

---

## Step 4 — Minimal Setup

```javascript
const table = new Tabulator('#data-table', {
  height:      '400px',      // fixed height → enables virtual scrolling (essential for large datasets)
  layout:      'fitColumns', // 'fitColumns' | 'fitData' | 'fitDataFill' | 'fitDataStretch'
  data:        tableData,    // array of row objects
  columns: [
    { title: 'Name',   field: 'name',   sorter: 'string', width: 180 },
    { title: 'Age',    field: 'age',    sorter: 'number', hozAlign: 'right' },
    { title: 'Status', field: 'status' },
  ],
});
```

---

## Step 5 — Column Definition Reference

Every column is an object in the `columns` array. The most useful properties:

```javascript
{
  // Core
  title:       'Column Label',   // header text (required)
  field:       'dataKey',        // key in the row data object (required)
  width:       150,              // px — omit to let layout mode decide
  minWidth:    80,
  maxWidth:    300,
  frozen:      true,             // freeze column to left (or right with hozAlign)
  visible:     false,            // hide column initially

  // Alignment
  hozAlign:    'left',           // 'left' | 'center' | 'right'
  vertAlign:   'middle',         // 'top' | 'middle' | 'bottom'
  headerHozAlign: 'center',

  // Sorting
  sorter:      'string',         // see Step 6
  sorterParams: {},
  headerSort:  true,             // default true; set false to disable

  // Filtering
  headerFilter:       true,      // show filter input in header
  headerFilterPlaceholder: 'Search…',
  headerFilterFunc:   '=',       // comparison function or custom function

  // Formatting
  formatter:   'progress',      // see Step 7
  formatterParams: { min: 0, max: 100, color: '#6366f1' },

  // Editing
  editor:      'input',         // see Step 8
  editorParams: {},
  editable:    true,            // or function(cell) { return bool }

  // Events
  cellClick:   (e, cell) => {},
  cellDblClick:(e, cell) => {},
  headerClick: (e, col) => {},

  // Display
  tooltip:     true,            // show cell value as tooltip
  cssClass:    'my-col',        // add CSS class to header + cells
  resizable:   true,            // allow user to resize (default true)
}
```

---

## Step 6 — Sorters

```javascript
sorter: 'string'     // alphabetical, case-insensitive
sorter: 'number'     // numeric
sorter: 'alphanum'   // alphanumeric (natural sort: "item2" < "item10")
sorter: 'boolean'    // true/false
sorter: 'date'       // requires sorterParams: { format: 'DD/MM/YYYY' }
sorter: 'time'       // requires sorterParams: { format: 'HH:mm' }
sorter: 'array'      // array length
sorter: 'exists'     // whether value exists (not null/undefined)

// Custom sorter
sorter: (a, b, aRow, bRow, col, dir, params) => a - b,

// Initial sort on load
initialSort: [
  { column: 'age',  dir: 'asc' },
  { column: 'name', dir: 'desc' },
]
```

---

## Step 7 — Formatters

```javascript
// Built-in formatters
formatter: 'plaintext'             // raw text (default, sanitizes HTML)
formatter: 'html'                  // renders HTML in cell value
formatter: 'textarea'              // wraps text with newlines
formatter: 'money'                 // 1234 → "$1,234.00"
  formatterParams: { symbol: '€', symbolAfter: true, precision: 2 }
formatter: 'email'                 // renders as mailto link
formatter: 'link'                  // renders as anchor
  formatterParams: { urlPrefix: 'https://', labelField: 'name', target: '_blank' }
formatter: 'image'                 // renders <img>
  formatterParams: { height: '40px', width: '40px', urlPrefix: '/img/' }
formatter: 'progress'              // colored progress bar
  formatterParams: { min: 0, max: 100, color: ['#f43f5e','#eab308','#22c55e'], legendColor: '#e2e8f0' }
formatter: 'star'                  // star rating (value = count of filled stars)
  formatterParams: { stars: 5 }
formatter: 'tickCross'             // ✓ or ✗ based on truthy/falsy
  formatterParams: { tickElement: '<span style="color:#22c55e">✓</span>', crossElement: '<span style="color:#f43f5e">✗</span>' }
formatter: 'toggle'                // toggle button (edit mode)
formatter: 'rownum'                // auto-incrementing row number
formatter: 'rowSelection'          // checkbox for row selection
formatter: 'color'                 // renders cell background as the color value
formatter: 'datetime'              // format date with luxon
  formatterParams: { inputFormat: 'yyyy-MM-dd', outputFormat: 'dd/MM/yyyy', invalidPlaceholder: '–' }
formatter: 'badge'                 // pill badge (v6+)
  formatterParams: { color: '#6366f1', backgroundColor: 'rgba(99,102,241,0.15)' }

// Custom formatter — most powerful pattern
formatter: (cell, formatterParams, onRendered) => {
  const value = cell.getValue();
  const row   = cell.getRow().getData();
  return `<span class="badge" style="background:${value > 80 ? '#22c55e' : '#f43f5e'}">${value}</span>`;
}

// Row-level formatting (applies to entire row)
rowFormatter: (row) => {
  if (row.getData().status === 'critical') {
    row.getElement().style.borderLeft = '3px solid #f43f5e';
  }
}
```

---

## Step 8 — Editors (inline editing)

```javascript
editor: 'input'          // plain text
editor: 'number'         // numeric input
  editorParams: { min: 0, max: 100, step: 1 }
editor: 'textarea'       // multiline
editor: 'select'
  editorParams: { values: ['Active', 'Inactive', 'Pending'], defaultValue: 'Active' }
editor: 'autocomplete'
  editorParams: { values: ['Paris', 'London', 'Berlin'], freetext: true }
editor: 'star'           // star rating editor
editor: 'toggle'         // boolean toggle
editor: 'date'
  editorParams: { format: 'YYYY-MM-DD', min: '2020-01-01', max: '2030-12-31' }
editor: 'list'           // dropdown list (v6+)
  editorParams: { values: [{ label: 'High', value: 'high' }, { label: 'Low', value: 'low' }] }

// Make specific cells editable conditionally
editable: (cell) => cell.getRow().getData().locked !== true,

// Trigger editing on double-click instead of click
editTriggerEvent: 'dblclick',
```

---

## Step 9 — Filtering

```javascript
// Header filter in each column (user-visible search box)
{ field: 'name', headerFilter: true, headerFilterPlaceholder: 'Search name…' }

// Built-in filter functions for headerFilterFunc
// '='  '!='  '<'  '<='  '>'  '>='  'like'  'keywords'  'starts'  'ends'  'in'  'regex'

// Programmatic filters (applied in code, invisible to user)
table.setFilter('age', '>', 18);
table.setFilter('status', 'in', ['active', 'pending']);
table.setFilter([                              // multiple filters at once
  { field: 'age',    type: '>',    value: 18 },
  { field: 'status', type: '=',    value: 'active' },
]);

// Custom filter function
table.setFilter((data, params) => data.score >= params.min && data.score <= params.max, { min: 40, max: 90 });

// Clear filters
table.clearFilter(true);  // true = also clear header filters
```

---

## Step 10 — Pagination

```javascript
// Local pagination (all data loaded, then paginated client-side)
{
  pagination:         true,        // enable
  paginationSize:     10,          // rows per page
  paginationSizeSelector: [5, 10, 25, 50, true],  // true = "all"
  paginationCounter:  'rows',      // show "x–y of z rows"
}

// Remote pagination (server returns one page at a time)
{
  pagination:     true,
  paginationMode: 'remote',
  ajaxURL:        'https://api.example.com/data',
  ajaxParams:     { token: 'abc123' },
  // Server must return: { "last_page": 15, "data": [...] }
}
```

---

## Step 11 — Row Selection

```javascript
{
  selectableRows: true,              // enable row selection
  selectableRowsRangeMode: 'click',  // shift-click for range
  rowHeader: {                       // add checkbox column
    formatter:      'rowSelection',
    titleFormatter: 'rowSelection',
    titleFormatterParams: { rowRange: 'active' },
    hozAlign:  'center',
    headerSort: false,
    width:      40,
  },
}

// Get selected data
const selected = table.getSelectedData();

// Events
table.on('rowSelectionChanged', (data, rows) => {
  console.log(`${data.length} rows selected`);
});
```

---

## Step 12 — Grouping

```javascript
{
  groupBy:        'department',              // group by field value
  groupStartOpen: true,                     // expand groups by default
  groupHeader: (value, count, data, group) =>
    `<span style="color:#a5b4fc">${value}</span> <span style="color:#475569">(${count})</span>`,
  groupToggleElement: 'header',             // click header to toggle
}

// Multiple group levels
groupBy: ['department', 'role'],
```

---

## Step 13 — Data Loading & Methods

```javascript
// Load data directly
const table = new Tabulator('#table', { data: myArray, columns: [...] });

// From URL (AJAX)
const table = new Tabulator('#table', {
  ajaxURL:    'https://api.example.com/users',
  ajaxConfig: 'GET',
  columns:    [...],
});

// Auto-generate columns from data shape (no columns array needed)
const table = new Tabulator('#table', {
  data:        myArray,
  autoColumns: true,
});

// Key methods (call after tableBuilt event)
table.setData(newArray);             // replace all data
table.addRow({ name: 'Alice' }, true); // true = add to top
table.deleteRow(3);                  // delete row by index
table.updateRow(1, { name: 'Bob' }); // update row data
table.getSelectedData();             // returns array of selected row data
table.getData();                     // all data (respects current filter/sort)
table.getData('active');             // filtered data only
table.clearData();                   // remove all rows
table.setSort('name', 'asc');        // sort programmatically
table.clearSort();
table.getPage();                     // current page number
table.setPage(2);
table.nextPage();
table.download('csv', 'export.csv'); // 'csv' | 'json' | 'xlsx' | 'pdf'
table.print();
```

---

## Step 14 — Events

```javascript
// Table lifecycle
table.on('tableBuilt',     ()     => { /* safe to call methods now */ });
table.on('dataLoaded',     (data) => {});
table.on('renderComplete', ()     => {});

// Row interactions
table.on('rowClick',        (e, row) => { console.log(row.getData()); });
table.on('rowDblClick',     (e, row) => {});
table.on('rowContext',      (e, row) => { e.preventDefault(); /* context menu */ });
table.on('rowMoved',        (row)    => {});
table.on('rowSelectionChanged', (data, rows) => {});

// Cell interactions
table.on('cellClick',       (e, cell) => {});
table.on('cellEdited',      (cell)    => {
  console.log('New value:', cell.getValue());
  console.log('Old value:', cell.getOldValue());
  console.log('Row data:', cell.getRow().getData());
});
table.on('cellEditCancelled', (cell) => {});

// Sorting & filtering
table.on('dataSorted',   (sorters, rows) => {});
table.on('dataFiltered', (filters, rows) => {});

// Pagination
table.on('pageLoaded', (pageNum) => {});
```

---

## Step 15 — Design & Polish Guidelines

- **Always set `height`** — enables virtual DOM scrolling for performance; without it, large datasets render all rows and lag
- **Use `layout: 'fitColumns'`** — columns fill the container width; switch to `fitData` only for narrow tables with few columns
- **Dark theme CSS overrides** — always include the full set from the Shell (Step 2); missing overrides leave white backgrounds on headers, footers, or filters
- **Frozen columns** — freeze identifier columns (name, ID) so users can scroll horizontally without losing context
- **Header filters** — add `headerFilter: true` for searchable columns; use `headerFilter: 'select'` for categorical data
- **Number formatting** — use `formatter: 'money'` with appropriate `formatterParams` for currency; `formatter: 'progress'` for visual bars
- **Pagination size** — 15–25 rows is optimal; fewer feels empty, more requires scrolling
- **Row selection** — enable `selectable: true` with `tabulator-selectable:hover` CSS for clear affordance
- **Accessibility** — Tabulator adds ARIA roles automatically; ensure your card has a descriptive `<h1>` for screen readers
- **Responsive fallback** — on narrow screens, use `responsiveLayout: 'collapse'` to hide lower-priority columns

---

## Step 16 — Complete Example: Employee Directory

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Employee Directory</title>
  <link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_midnight.min.css" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 24px; }
    .card { width: 100%; max-width: 1100px; background: #1a1d27; border-radius: 16px; padding: 28px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }
    .actions { display: flex; gap: 8px; }
    button { background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.35); color: #a5b4fc; border-radius: 6px; padding: 6px 14px; font-size: 12px; cursor: pointer; transition: background 0.15s; }
    button:hover { background: rgba(99,102,241,0.3); }
    #stats { font-size: 12px; color: #64748b; margin-top: 14px; }

    /* Fine-tuning on top of midnight theme */
    .tabulator { border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 10px !important; font-size: 13px; }
    .tabulator .tabulator-header .tabulator-col { font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; color: #64748b !important; }
    .tabulator-row:hover { background: rgba(255,255,255,0.04) !important; }
    .tabulator-row.tabulator-selected { background: rgba(99,102,241,0.18) !important; }
    .tabulator-page.active { background: #6366f1 !important; border-color: #6366f1 !important; }
    .tabulator-header-filter input { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #e2e8f0; border-radius: 4px; }
  </style>
</head>
<body>
<div class="card">
  <div class="header">
    <div>
      <h1>Employee Directory</h1>
      <p class="sub">Click headers to sort · Filter in column headers · Select rows</p>
    </div>
    <div class="actions">
      <button id="btn-csv">Export CSV</button>
      <button id="btn-clear">Clear filters</button>
    </div>
  </div>
  <div id="table"></div>
  <div id="stats"></div>
</div>

<script src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>
<script>
  const data = [
    { id:1, name:'Alice Martin',   dept:'Engineering', role:'Senior Dev',   salary:92000, score:88, active:true,  joined:'2021-03-15' },
    { id:2, name:'Bob Chen',       dept:'Design',      role:'UI Lead',      salary:78000, score:92, active:true,  joined:'2020-07-01' },
    { id:3, name:'Carla Ruiz',     dept:'Engineering', role:'Backend Dev',  salary:85000, score:74, active:false, joined:'2019-11-22' },
    { id:4, name:'David Kim',      dept:'Marketing',   role:'Growth Mgr',   salary:70000, score:65, active:true,  joined:'2022-01-10' },
    { id:5, name:'Emma Johnson',   dept:'Engineering', role:'CTO',          salary:145000,score:97, active:true,  joined:'2018-06-01' },
    { id:6, name:'Frank Müller',   dept:'Design',      role:'Junior Des.',  salary:55000, score:58, active:true,  joined:'2023-04-20' },
    { id:7, name:'Grace Lee',      dept:'Marketing',   role:'Content Str.', salary:62000, score:81, active:false, joined:'2020-09-14' },
    { id:8, name:'Henry Dubois',   dept:'Engineering', role:'DevOps Eng.',  salary:98000, score:86, active:true,  joined:'2021-08-03' },
    { id:9, name:'Isabelle Costa', dept:'Design',      role:'Design Mgr',   salary:88000, score:91, active:true,  joined:'2019-02-28' },
    { id:10,name:'James Park',     dept:'Marketing',   role:'CMO',          salary:130000,score:95, active:true,  joined:'2017-05-15' },
  ];

  const scoreColor = v => v >= 90 ? '#22c55e' : v >= 70 ? '#eab308' : '#f43f5e';

  const table = new Tabulator('#table', {
    data,
    height:         '420px',
    layout:         'fitColumns',
    pagination:     true,
    paginationSize: 8,
    paginationSizeSelector: [5, 8, 10, true],
    paginationCounter: 'rows',
    movableColumns: true,
    selectableRows: true,
    initialSort:    [{ column: 'score', dir: 'desc' }],

    rowHeader: {
      formatter: 'rowSelection', titleFormatter: 'rowSelection',
      titleFormatterParams: { rowRange: 'active' },
      hozAlign: 'center', headerSort: false, width: 40,
    },

    rowFormatter: (row) => {
      if (!row.getData().active) {
        row.getElement().style.opacity = '0.5';
      }
    },

    columns: [
      {
        title: 'Name', field: 'name', sorter: 'string', width: 160, frozen: true,
        headerFilter: true, headerFilterPlaceholder: 'Search…',
        formatter: (cell) => `<span style="font-weight:500;color:#f1f5f9">${cell.getValue()}</span>`,
      },
      {
        title: 'Department', field: 'dept', sorter: 'string', width: 130,
        headerFilter: 'select',
        headerFilterParams: { values: { '': 'All', Engineering: 'Engineering', Design: 'Design', Marketing: 'Marketing' } },
        formatter: (cell) => {
          const colors = { Engineering:'#6366f1', Design:'#ec4899', Marketing:'#06b6d4' };
          const c = colors[cell.getValue()] || '#475569';
          return `<span style="background:${c}22;color:${c};padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600">${cell.getValue()}</span>`;
        },
      },
      { title: 'Role', field: 'role', sorter: 'string', headerFilter: true, headerFilterPlaceholder: 'Filter…' },
      {
        title: 'Salary', field: 'salary', sorter: 'number', hozAlign: 'right', width: 110,
        formatter: 'money', formatterParams: { symbol: '$', thousand: ',', precision: 0 },
      },
      {
        title: 'Score', field: 'score', sorter: 'number', hozAlign: 'center', width: 130,
        formatter: 'progress',
        formatterParams: { min: 0, max: 100, color: (val) => scoreColor(val), legendColor: '#94a3b8' },
      },
      {
        title: 'Active', field: 'active', sorter: 'boolean', hozAlign: 'center', width: 80,
        formatter: 'tickCross',
        formatterParams: {
          tickElement:  '<span style="color:#22c55e;font-size:16px">✓</span>',
          crossElement: '<span style="color:#f43f5e;font-size:16px">✗</span>',
        },
      },
      {
        title: 'Joined', field: 'joined', sorter: 'date',
        sorterParams: { format: 'YYYY-MM-DD' }, hozAlign: 'center', width: 110,
      },
    ],
  });

  table.on('tableBuilt', () => updateStats());
  table.on('dataFiltered', () => updateStats());
  table.on('rowSelectionChanged', (selectedData) => {
    document.getElementById('stats').innerHTML =
      selectedData.length ? `<span style="color:#a5b4fc">${selectedData.length} row(s) selected</span>` : updateStats() || '';
  });

  function updateStats() {
    const d = table.getData('active');
    document.getElementById('stats').innerHTML =
      `<span style="color:#475569">${d.length} employees shown</span>`;
  }

  document.getElementById('btn-csv').onclick   = () => table.download('csv', 'employees.csv');
  document.getElementById('btn-clear').onclick = () => { table.clearFilter(true); updateStats(); };
</script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Missing CSS file** — the JS alone produces an unstyled, broken layout. Always load `tabulator.min.css` (or a theme variant) in `<head>`
- **Calling methods before `tableBuilt`** — Tabulator initializes asynchronously. Wrap any post-creation logic in `table.on('tableBuilt', () => { ... })`
- **`height` not set for large datasets** — without a fixed `height`, Tabulator renders all rows at once (no virtual scrolling) and can freeze on 10 000+ rows; always set `height` for large data
- **`layout: 'fitColumns'` with fixed widths on all columns** — if all columns have `width`, there's nothing to distribute and the layout breaks on resize; leave at least one column without a fixed width, or use `layout: 'fitData'`
- **Filtering `null`/`undefined` values** — Tabulator's built-in sorters and filters handle `null` poorly; normalize data before loading (`null → ''` or `null → 0`)
- **Remote pagination without server-side implementation** — `paginationMode: 'remote'` requires the server to return `{ "last_page": N, "data": [...] }`; if the server returns a plain array, use `pagination: true` (local mode)
- **`autoColumns: true` on mixed-type data** — Tabulator infers types from the first row only; if your data has inconsistent types, define columns explicitly instead
