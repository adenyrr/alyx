---
name: bulma-css
description: Build clean, responsive, component-rich interfaces using Bulma v1 CSS framework, delivered as self-contained HTML artifacts. Use this skill whenever someone needs a well-structured UI page with ready-made components and no JavaScript dependency — landing pages, dashboards, forms, admin panels, marketing pages, documentation layouts, or any multi-component page where visual consistency and responsiveness matter. Trigger on requests like "build a page with a navbar and cards", "create a responsive layout", "make a clean form with sections", "design a dashboard with columns", or any request for structured multi-component HTML pages. Bulma is pure CSS — use it when you want a polished result fast without framework overhead. Do NOT use for pixel-perfect custom animations (→ creative-artifacts), data tables (→ tabulator), charts (→ charting), or complex interactive React apps (→ shadcn-ui or creative-artifacts).
---

# Bulma CSS Skill — v1.0.4

Bulma is a modern CSS framework based on Flexbox and Sass. It is **pure CSS — no JavaScript included or required**. Every interactive behavior (modals, dropdowns, hamburger menus) must be toggled via custom JS by adding/removing `is-active`. Bulma v1 introduced native dark mode, a new CSS-variable theme system, and the CSS Grid layout alongside the Flexbox columns system.

---

## Artifact Presentation & Use Cases

Every Bulma artifact is a self-contained HTML page using Bulma’s built-in dark mode. The visual structure follows:

- **Dark body** via `data-theme="dark"` on `<html>` — Bulma v1 natively supports dark mode
- **Card wrappers** (`.card`, `.box`) with Bulma’s built-in dark-themed backgrounds and borders
- **Navbar** (`.navbar`) for navigation, toggled via JS `is-active` class
- **Columns** (`.columns > .column`) for responsive grid layouts
- **Components** (modals, forms, tabs, dropdowns) all styled consistently by the framework

### Typical use cases

- **Landing pages** — hero sections, feature grids, pricing tables, call-to-action forms
- **Admin dashboards** — KPI cards, sidebar navigation, summary tables, status indicators
- **Forms and settings pages** — clean form layouts with validation styling, grouped inputs, file uploads
- **Documentation layouts** — sidebar + content area with breadcrumbs and section navigation
- **Marketing pages** — testimonials, team sections, timeline content, FAQ accordions
- **Multi-component UIs** — any page requiring consistent, responsive design without JS frameworks

### What the user sees

A polished, responsive page: columns reflow on mobile, components follow consistent spacing and typography, dark mode colors are coherent throughout. No JavaScript is needed for layout — only for toggling interactive components (modals, menus).

---

## When to Use Bulma vs. Alternatives

| Use Bulma when… | Use another tool when… |
|---|---|
| Ready-made UI components (navbar, card, modal, form) | Utility-first custom designs → **Tailwind CSS** |
| Pure CSS, no JS framework needed | React-based SPA with state management → **shadcn/ui** |
| Semantic class names (`is-primary`, `is-large`) | Highly custom animations → **Anime.js** |
| Quick responsive layouts with Flexbox columns | Data tables with sort/filter/edit → **Tabulator** |
| Native dark mode via `data-theme="dark"` | Charts and data visualization → **Chart.js / Plotly / D3** |
| CSS Grid via `.fixed-grid` (v1) | Interactive maps → **Leaflet** |

> **Rule of thumb:** if you need a multi-component page (navbar, cards, forms, modals) with consistent styling and minimal effort, Bulma is the fastest path. For pixel-level utility control, use Tailwind.

---

## Step 1 — CDN Setup

Bulma is a single CSS file. No JavaScript file.

```html
<!-- In <head> — this is all you need -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.4/css/bulma.min.css">
```

> **⚠️ Bulma contains zero JavaScript.** Toggling interactive components (modals, mobile navbar, dropdowns) requires you to add or remove the `is-active` class yourself via vanilla JS or Alpine.js.

Optional: Font Awesome icons (commonly paired with Bulma)
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
```

---

## Step 2 — Dark Mode

Bulma v1 has first-class dark mode support via CSS variables. Three activation methods:

```html
<!-- Method 1: Respect system preference (automatic) -->
<!-- No class or attribute needed — uses prefers-color-scheme media query -->

<!-- Method 2: Force dark mode on an element and its children -->
<html data-theme="dark">    <!-- entire page dark -->
<div data-theme="dark">     <!-- only this section dark -->

<!-- Method 3: Class-based (same result as attribute) -->
<html class="theme-dark">

<!-- Force light mode explicitly -->
<html data-theme="light">
```

For artifacts, always add `data-theme="dark"` on `<html>` to match the default dark aesthetic.

---

## Step 3 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.4/css/bulma.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
  <style>
    /* Optional custom overrides — Bulma CSS variables are available here */
    :root {
      --bulma-primary-h: 243deg;   /* shift primary color hue to indigo */
      --bulma-primary-s: 75%;
      --bulma-primary-l: 59%;
    }
  </style>
</head>
<body>
  <!-- navbar, sections, footer -->

  <script>
    // Toggle logic for interactive Bulma components (add as needed)
    document.querySelectorAll('.navbar-burger').forEach(burger => {
      burger.addEventListener('click', () => {
        const target = document.getElementById(burger.dataset.target);
        burger.classList.toggle('is-active');
        target.classList.toggle('is-active');
      });
    });
  </script>
</body>
</html>
```

---

## Step 4 — Modifier System

Bulma's entire API is built on two modifier prefixes:

| Prefix | Purpose | Examples |
|---|---|---|
| `is-` | State, size, color, style | `is-primary`, `is-large`, `is-active`, `is-rounded` |
| `has-` | Content or child property | `has-text-white`, `has-background-dark`, `has-icon` |

### Colors (apply to any component)
```
is-primary    is-link       is-info
is-success    is-warning    is-danger
is-white      is-light      is-dark     is-black
```

### Sizes
```
is-small    is-normal    is-medium    is-large
```

### Text helpers
```
has-text-centered   has-text-left   has-text-right   has-text-justified
has-text-primary    has-text-success  has-text-danger  has-text-grey
has-text-white      has-text-dark

has-text-weight-light    has-text-weight-normal
has-text-weight-semibold has-text-weight-bold
```

### Spacing helpers (v1+)
```
mt-0 … mt-6    mb-0 … mb-6    ml-0 … ml-6    mr-0 … mr-6
pt-0 … pt-6    pb-0 … pb-6    pl-0 … pl-6    pr-0 … pr-6
mx-auto        my-auto        px-4            py-5
```

---

## Step 5 — Layout: Container, Section, Hero

```html
<!-- Container — centers content, responsive max-width -->
<div class="container">              <!-- max-width at each breakpoint -->
<div class="container is-fluid">    <!-- full width with padding -->
<div class="container is-max-desktop"> <!-- capped at desktop width -->

<!-- Section — adds vertical padding (the standard page wrapper) -->
<section class="section">
  <div class="container">
    <h1 class="title">Page Title</h1>
    <p class="subtitle">Subtitle text</p>
  </div>
</section>

<!-- Hero — large introductory banner -->
<section class="hero is-primary is-medium">  <!-- is-small | is-medium | is-large | is-fullheight -->
  <div class="hero-body">
    <p class="title">Hero Title</p>
    <p class="subtitle">Hero subtitle</p>
  </div>
</section>

<!-- Footer -->
<footer class="footer">
  <div class="container has-text-centered">
    <p>Footer content</p>
  </div>
</footer>
```

---

## Step 6 — Columns (Flexbox Grid)

```html
<!-- Basic columns — equal width by default -->
<div class="columns">
  <div class="column">One</div>
  <div class="column">Two</div>
  <div class="column">Three</div>
</div>

<!-- Sized columns (12-column grid) -->
<div class="columns">
  <div class="column is-4">4/12 wide</div>
  <div class="column is-8">8/12 wide</div>
</div>

<!-- Named fractions -->
<!-- is-half  is-one-third  is-two-thirds  is-one-quarter  is-three-quarters  is-full -->

<!-- Offset -->
<div class="column is-6 is-offset-3">Centered third</div>

<!-- Multiline (wrap when full) -->
<div class="columns is-multiline">
  <div class="column is-4"> … </div>
  <div class="column is-4"> … </div>
  <div class="column is-4"> … </div>
  <div class="column is-4"> … </div>  <!-- wraps to next row -->
</div>

<!-- Gap control -->
<div class="columns is-gapless">   <!-- no gap -->
<div class="columns is-variable is-2">  <!-- small gap -->
<div class="columns is-variable is-8">  <!-- large gap -->

<!-- Responsive: columns stack on mobile by default, use is-mobile to keep horizontal -->
<div class="columns is-mobile">    <!-- always horizontal, even on phone -->

<!-- Responsive sizes per breakpoint -->
<div class="column is-full-mobile is-half-tablet is-one-third-desktop">
```

---

## Step 7 — CSS Grid (Bulma v1+)

```html
<!-- Smart Grid — auto-responsive without breakpoint classes -->
<div class="grid">
  <div class="cell">Cell 1</div>
  <div class="cell">Cell 2</div>
  <div class="cell">Cell 3</div>
</div>

<!-- Fixed Grid — explicit rows × columns -->
<div class="fixed-grid has-3-cols">  <!-- has-1-cols … has-12-cols -->
  <div class="grid">
    <div class="cell">A</div>
    <div class="cell">B</div>
    <div class="cell is-col-span-2">C spanning 2</div>
  </div>
</div>

<!-- Responsive column count -->
<div class="fixed-grid has-2-cols-mobile has-3-cols-tablet has-4-cols-desktop">
```

---

## Step 8 — Elements

### Buttons
```html
<button class="button">Default</button>
<button class="button is-primary">Primary</button>
<button class="button is-success is-outlined">Outlined success</button>
<button class="button is-danger is-rounded">Rounded danger</button>
<button class="button is-info is-loading">Loading</button>
<button class="button is-large">Large</button>
<button class="button is-small">Small</button>
<button class="button" disabled>Disabled</button>

<!-- Group of buttons -->
<div class="buttons">
  <button class="button is-primary">Save</button>
  <button class="button">Cancel</button>
</div>
<div class="buttons has-addons">  <!-- attached together -->
  <button class="button">Left</button>
  <button class="button is-active">Middle</button>
  <button class="button">Right</button>
</div>
```

### Typography
```html
<h1 class="title is-1">Heading 1</h1>          <!-- is-1 … is-6 -->
<h2 class="title is-3">Heading 3</h2>
<p class="subtitle is-4">Subtitle</p>
<span class="tag is-primary">Label</span>
<span class="tag is-warning is-rounded">Pill</span>
<span class="tag is-danger is-large">Large tag</span>

<!-- Notification banner -->
<div class="notification is-info">ℹ️ Informational message</div>
<div class="notification is-danger is-light">⚠️ Error with light variant</div>

<!-- Progress bar -->
<progress class="progress is-primary" value="65" max="100">65%</progress>
```

### Table
```html
<table class="table is-fullwidth is-striped is-hoverable is-bordered">
  <thead>
    <tr>
      <th>Name</th>
      <th>Status</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Alice</td>
      <td><span class="tag is-success">Active</span></td>
      <td>92</td>
    </tr>
  </tbody>
</table>
```

---

## Step 9 — Components

### Navbar
```html
<nav class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="#">
      <strong>Brand</strong>
    </a>
    <!-- Hamburger (toggle with JS) -->
    <a role="button" class="navbar-burger" data-target="mainNav"
       aria-label="menu" aria-expanded="false">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="mainNav" class="navbar-menu">
    <div class="navbar-start">
      <a class="navbar-item">Home</a>
      <a class="navbar-item">About</a>
      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">More</a>
        <div class="navbar-dropdown">
          <a class="navbar-item">Settings</a>
          <hr class="navbar-divider">
          <a class="navbar-item">Logout</a>
        </div>
      </div>
    </div>
    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a class="button is-primary">Sign Up</a>
          <a class="button is-light">Log in</a>
        </div>
      </div>
    </div>
  </div>
</nav>
```

### Card
```html
<div class="card">
  <div class="card-image">
    <figure class="image is-4by3">
      <img src="https://picsum.photos/400/300" alt="Card image">
    </figure>
  </div>
  <div class="card-content">
    <div class="media">
      <div class="media-content">
        <p class="title is-4">Card Title</p>
        <p class="subtitle is-6">@username</p>
      </div>
    </div>
    <div class="content">
      Card body text here.
    </div>
  </div>
  <footer class="card-footer">
    <a href="#" class="card-footer-item">Save</a>
    <a href="#" class="card-footer-item">Edit</a>
    <a href="#" class="card-footer-item has-text-danger">Delete</a>
  </footer>
</div>
```

### Modal
```html
<!-- Trigger button -->
<button class="button is-primary" id="openModal">Open Modal</button>

<!-- Modal structure -->
<div class="modal" id="myModal">
  <div class="modal-background"></div>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Modal Title</p>
      <button class="delete" aria-label="close" id="closeModal"></button>
    </header>
    <section class="modal-card-body">
      Modal content here.
    </section>
    <footer class="modal-card-foot">
      <div class="buttons">
        <button class="button is-success">Confirm</button>
        <button class="button">Cancel</button>
      </div>
    </footer>
  </div>
</div>

<script>
  // Modal must be toggled manually — Bulma provides no JS
  document.getElementById('openModal').onclick  = () => document.getElementById('myModal').classList.add('is-active');
  document.getElementById('closeModal').onclick = () => document.getElementById('myModal').classList.remove('is-active');
  document.querySelector('#myModal .modal-background').onclick = () => document.getElementById('myModal').classList.remove('is-active');
</script>
```

### Form
```html
<div class="field">
  <label class="label">Name</label>
  <div class="control has-icons-left">
    <input class="input" type="text" placeholder="Your name">
    <span class="icon is-left"><i class="fas fa-user"></i></span>
  </div>
</div>

<div class="field">
  <label class="label">Message</label>
  <div class="control">
    <textarea class="textarea is-info" placeholder="Write something…" rows="4"></textarea>
  </div>
</div>

<div class="field">
  <label class="label">Status</label>
  <div class="control">
    <div class="select is-fullwidth">
      <select>
        <option>Active</option>
        <option>Inactive</option>
      </select>
    </div>
  </div>
</div>

<div class="field">
  <div class="control">
    <label class="checkbox"><input type="checkbox"> I agree to the terms</label>
  </div>
</div>

<div class="field is-grouped">
  <div class="control">
    <button class="button is-primary">Submit</button>
  </div>
  <div class="control">
    <button class="button is-light">Reset</button>
  </div>
</div>
```

### Tabs
```html
<div class="tabs is-boxed">
  <ul>
    <li class="is-active"><a>Overview</a></li>
    <li><a>Analytics</a></li>
    <li><a>Settings</a></li>
  </ul>
</div>
<!-- Tabs do not auto-switch content — toggle with JS -->
```

### Level (horizontal toolbar / stats row)
```html
<nav class="level">
  <div class="level-item has-text-centered">
    <div>
      <p class="heading">Users</p>
      <p class="title">12,480</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
      <p class="heading">Revenue</p>
      <p class="title">$48K</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
      <p class="heading">Uptime</p>
      <p class="title">99.9%</p>
    </div>
  </div>
</nav>
```

---

## Step 10 — Responsive Breakpoints

| Suffix | Viewport |
|---|---|
| *(none)* | All sizes |
| `-mobile` | ≤ 768px |
| `-tablet` | ≥ 769px |
| `-desktop` | ≥ 1024px |
| `-widescreen` | ≥ 1216px |
| `-fullhd` | ≥ 1408px |

```html
<!-- Show/hide at breakpoints -->
<div class="is-hidden-mobile">Hidden on mobile</div>
<div class="is-hidden-tablet-only">Hidden only on tablet</div>
<div class="is-hidden-desktop">Hidden on desktop+</div>

<!-- Responsive column sizes -->
<div class="column is-12-mobile is-6-tablet is-4-desktop">
```

---

## Step 11 — Design & Polish Guidelines

- **Always use `data-theme="dark"`** on `<html>` — this activates Bulma v1’s native dark mode; all components inherit correct dark colors
- **Override CSS variables** — customize `--bulma-body-background-color`, `--bulma-card-background-color`, etc. to match the project’s design system
- **Column responsiveness** — always specify mobile breakpoint sizes (`is-12-mobile is-6-tablet is-4-desktop`) for predictable reflow
- **Semantic modifiers** — use `is-primary`, `is-link`, `is-info`, `is-success`, `is-warning`, `is-danger` consistently for color semantics
- **Spacing** — use Bulma’s spacing helpers (`mb-4`, `mt-6`, `px-3`) instead of custom CSS margins
- **JS for interactivity** — always add toggle scripts for navbar hamburger, modals, and dropdowns — Bulma has no built-in JS
- **Accessibility** — use `aria-label` on buttons, `role="navigation"` on navbars, `aria-modal="true"` on modals
- **Card consistency** — use `.card-header`, `.card-content`, `.card-footer` structure rather than custom divs inside `.card`
- **Font stack** — Bulma defaults to system fonts; this is already optimal for performance and consistency

---

## Step 12 — Complete Example: SaaS Dashboard

```html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.4/css/bulma.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
  <style>
    .stat-card { transition: transform 0.15s; }
    .stat-card:hover { transform: translateY(-3px); }
    .stat-value { font-size: 2rem; font-weight: 700; }
  </style>
</head>
<body>

<!-- Navbar -->
<nav class="navbar is-dark" role="navigation">
  <div class="container">
    <div class="navbar-brand">
      <a class="navbar-item" href="#">
        <strong class="has-text-primary">⬡ Nucleus</strong>
      </a>
      <a role="button" class="navbar-burger" data-target="navMenu" aria-label="menu">
        <span></span><span></span><span></span>
      </a>
    </div>
    <div id="navMenu" class="navbar-menu">
      <div class="navbar-start">
        <a class="navbar-item is-active">Dashboard</a>
        <a class="navbar-item">Projects</a>
        <a class="navbar-item">Team</a>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a class="button is-primary is-small">New Project</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</nav>

<!-- Hero -->
<section class="hero is-small">
  <div class="hero-body">
    <div class="container">
      <h1 class="title">Good morning, Alex 👋</h1>
      <p class="subtitle has-text-grey">Here's what's happening with your projects today.</p>
    </div>
  </div>
</section>

<!-- Stats row -->
<section class="section pt-0">
  <div class="container">
    <div class="columns is-multiline">

      <!-- Stat cards -->
      <div class="column is-6-tablet is-3-desktop">
        <div class="box stat-card">
          <p class="heading"><span class="icon-text"><span class="icon has-text-info"><i class="fas fa-users"></i></span><span>Total Users</span></span></p>
          <p class="stat-value has-text-info">24,831</p>
          <p class="has-text-success is-size-7"><span class="icon"><i class="fas fa-arrow-up"></i></span> +12% this month</p>
        </div>
      </div>

      <div class="column is-6-tablet is-3-desktop">
        <div class="box stat-card">
          <p class="heading"><span class="icon-text"><span class="icon has-text-success"><i class="fas fa-dollar-sign"></i></span><span>Revenue</span></span></p>
          <p class="stat-value has-text-success">$98,420</p>
          <p class="has-text-success is-size-7"><span class="icon"><i class="fas fa-arrow-up"></i></span> +8% this month</p>
        </div>
      </div>

      <div class="column is-6-tablet is-3-desktop">
        <div class="box stat-card">
          <p class="heading"><span class="icon-text"><span class="icon has-text-warning"><i class="fas fa-clock"></i></span><span>Avg Session</span></span></p>
          <p class="stat-value has-text-warning">4m 32s</p>
          <p class="has-text-danger is-size-7"><span class="icon"><i class="fas fa-arrow-down"></i></span> -3% this month</p>
        </div>
      </div>

      <div class="column is-6-tablet is-3-desktop">
        <div class="box stat-card">
          <p class="heading"><span class="icon-text"><span class="icon has-text-primary"><i class="fas fa-server"></i></span><span>Uptime</span></span></p>
          <p class="stat-value has-text-primary">99.97%</p>
          <p class="has-text-grey is-size-7">Last 30 days</p>
        </div>
      </div>

      <!-- Recent projects table -->
      <div class="column is-8-desktop">
        <div class="box">
          <p class="title is-5 mb-4">Recent Projects</p>
          <table class="table is-fullwidth is-hoverable">
            <thead>
              <tr>
                <th>Project</th>
                <th>Status</th>
                <th>Team</th>
                <th>Progress</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Redesign v3</strong></td>
                <td><span class="tag is-warning is-light">In Progress</span></td>
                <td>Design</td>
                <td><progress class="progress is-warning is-small" value="65" max="100">65%</progress></td>
              </tr>
              <tr>
                <td><strong>API Migration</strong></td>
                <td><span class="tag is-success is-light">Complete</span></td>
                <td>Backend</td>
                <td><progress class="progress is-success is-small" value="100" max="100">100%</progress></td>
              </tr>
              <tr>
                <td><strong>Mobile App</strong></td>
                <td><span class="tag is-info is-light">Review</span></td>
                <td>Mobile</td>
                <td><progress class="progress is-info is-small" value="88" max="100">88%</progress></td>
              </tr>
              <tr>
                <td><strong>Analytics Dashboard</strong></td>
                <td><span class="tag is-danger is-light">Blocked</span></td>
                <td>Frontend</td>
                <td><progress class="progress is-danger is-small" value="32" max="100">32%</progress></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Quick actions -->
      <div class="column is-4-desktop">
        <div class="box">
          <p class="title is-5 mb-4">Quick Actions</p>
          <div class="buttons is-flex-direction-column" style="align-items:stretch">
            <button class="button is-primary is-outlined mb-2"><span class="icon"><i class="fas fa-plus"></i></span><span>New Project</span></button>
            <button class="button is-info is-outlined mb-2"><span class="icon"><i class="fas fa-user-plus"></i></span><span>Invite Member</span></button>
            <button class="button is-warning is-outlined mb-2"><span class="icon"><i class="fas fa-chart-bar"></i></span><span>View Reports</span></button>
            <button class="button is-light is-outlined"><span class="icon"><i class="fas fa-cog"></i></span><span>Settings</span></button>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<script>
  // Navbar hamburger toggle
  document.querySelectorAll('.navbar-burger').forEach(b =>
    b.addEventListener('click', () => {
      b.classList.toggle('is-active');
      document.getElementById(b.dataset.target).classList.toggle('is-active');
    })
  );
</script>

</body>
</html>
```

---

## Common Mistakes to Avoid

- **Expecting Bulma to handle JS interactions** — Bulma is pure CSS. Modals, dropdowns, hamburger menus, and tabs do nothing until you add/remove `is-active` via JavaScript. There is no Bulma JS file
- **Forgetting the navbar burger script** — `navbar-burger` renders a hamburger icon on mobile but clicks do nothing without at least 3 lines of JS to toggle `is-active` on the burger and `#navbarMenu`
- **Using v0.9 CDN for v1 features** — dark mode (`data-theme`), CSS Grid (`grid` / `cell`), and the new color palette are v1-only. Always use `bulma@1.0.4` (or `bulma@1` for latest)
- **Columns outside a `columns` wrapper** — `<div class="column">` must always be a direct child of `<div class="columns">`. Columns nested outside this relationship will not layout correctly
- **Missing `is-mobile` on horizontal mobile columns** — by default, `.columns` stacks vertically on mobile. Add `is-mobile` to the `columns` div to keep them horizontal on phones
- **Conflicting custom CSS specificity** — Bulma uses BEM-like classes with low specificity. Custom styles on the same selectors (e.g., `.button`) can be overridden by Bulma's `!important` on helper classes; use the CSS variable system (`--bulma-*`) for theme overrides instead
- **Using `is-fullwidth` on inline elements** — `is-fullwidth` uses `width: 100%` which works on block elements; apply it to the wrapper, not to inline elements like `<a>` or `<span>`
