---
name: tailwind-css
description: Build fast, responsive, utility-first interfaces using Tailwind CSS v4, delivered as self-contained HTML or React artifacts. Use this skill whenever someone needs a custom-styled UI without a pre-defined component vocabulary — layouts, landing pages, dashboards, cards, forms, or any interface where fine-grained control over every spacing, color, and typography decision is desired. Trigger on requests like "style this with Tailwind", "build a responsive layout", "create a dark landing page", "make a product card", "design a form", or any prompt that implies writing CSS inline through utility classes rather than component libraries. Tailwind excels at bespoke design systems. Do NOT use when the user wants pre-built components without touching classes (→ bulma-css or shadcn-ui), interactive 3D (→ threejs-3d), or generative art (→ p5js).
---

# Tailwind CSS Skill — v4

Tailwind CSS is a utility-first CSS framework: instead of writing CSS, you compose styles by applying small, single-purpose classes directly in HTML. Tailwind v4 (released January 2025) is a complete rewrite with a **CSS-first configuration** system, a new high-performance engine, and zero-config auto-detection of template files.

---

## Artifact Presentation & Use Cases

Every Tailwind artifact is a self-contained HTML page using the Play CDN for style generation. The visual structure follows:

- **Dark body** via `class="dark"` on `<html>` and `bg-[#0f1117]` on body
- **Custom theme** defined in `<style type="text/tailwindcss">` using `@theme { }` blocks
- **Utility-composed layouts** — every spacing, color, font, and layout decision is expressed as utility classes
- **Responsive design** via `sm:`, `md:`, `lg:`, `xl:` prefixes on utility classes
- **Dark mode** via `dark:` prefix on color utilities

### Typical use cases

- **Landing pages** — hero sections, feature grids, CTAs, testimonials with pixel-perfect custom design
- **Custom cards** — bespoke card layouts with exact spacing, colors, and typography
- **Forms** — styled inputs, selects, checkboxes with focus states and validation
- **Dashboard layouts** — sidebar + content + header patterns with responsive breakpoints
- **Product/pricing pages** — comparison grids, feature lists, pricing cards
- **Custom components** — any design that doesn’t fit a pre-built component vocabulary

### What the user sees

A clean, custom-designed page: consistent spacing, sharp typography, smooth hover/focus transitions. The Tailwind approach produces unique designs rather than “framework-looking” pages. Responsive layout reflows naturally across screen sizes.

---

## When to Use Tailwind vs. Alternatives

| Use Tailwind when… | Use another tool when… |
|---|---|
| Bespoke design, pixel-perfect control | Pre-built component library (navbar, modal, card) → **Bulma** |
| Utility-first workflow (classes in HTML) | React app with accessible components → **shadcn/ui** |
| Dark mode via `dark:` prefix | Data visualization charts → **Chart.js / Plotly / D3** |
| Custom spacing, colors, and typography | Data tables with sort/filter → **Tabulator** |
| Responsive layouts with breakpoint control | Interactive maps → **Leaflet** |
| Rapid prototyping without writing CSS files | Diagrams and flowcharts → **Mermaid** |

> **Rule of thumb:** if the design is custom and you want fine-grained control over every visual detail, use Tailwind. If you want pre-made components with minimal customization, use Bulma or shadcn/ui.

---

## Step 1 — CDN Setup (Play CDN)

For artifacts and browser-based prototypes, use the **Play CDN** — a single script tag that scans the page and generates CSS on the fly.

```html
<!-- In <head> — one line, no build step -->
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

> **⚠️ Play CDN is for development and prototypes only.** It is not intended for production. For production apps, use the Vite plugin (`@tailwindcss/vite`) or PostCSS plugin (`@tailwindcss/postcss`).

### Custom theme with `@theme`
In v4, there is no `tailwind.config.js`. All customization happens in CSS via the `@theme` directive. Use a `<style type="text/tailwindcss">` block so the Play CDN processes it:

```html
<style type="text/tailwindcss">
  @theme {
    --color-brand:     #6366f1;   /* creates bg-brand, text-brand, border-brand... */
    --color-accent:    #ec4899;
    --font-display:    'Inter', system-ui, sans-serif;
    --radius-card:     1rem;
    --spacing-18:      4.5rem;    /* creates p-18, m-18, w-18... */
  }
</style>
```

> Theme variables generate utility classes automatically. `--color-brand` → `bg-brand`, `text-brand`, `border-brand`, `ring-brand`, etc.

### Custom utilities and variants
```html
<style type="text/tailwindcss">
  /* Custom utility class */
  @utility card-shadow {
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
  }

  /* Class-based dark mode (instead of media query) */
  @custom-variant dark (&:where(.dark, .dark *));
</style>
```

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <style type="text/tailwindcss">
    @theme {
      --color-brand: #6366f1;
      --color-accent: #ec4899;
      --font-sans: 'Segoe UI', system-ui, sans-serif;
    }
    /* Custom CSS using Tailwind variables */
    @layer base {
      body { @apply bg-gray-950 text-gray-100 antialiased; }
    }
  </style>
</head>
<body class="min-h-screen">
  <!-- content -->
</body>
</html>
```

---

## Step 3 — Utility Class Reference

### Spacing (margin, padding, gap)
Every spacing utility uses a scale where 1 unit = 0.25rem (4px).

```
p-0   p-1   p-2   p-3   p-4   p-5   p-6   p-8   p-10  p-12  p-16  p-20  p-24
m-0   m-1   m-2   m-3   m-4   m-6   m-8   m-12  m-16  m-auto
gap-0 gap-1 gap-2 gap-4 gap-6 gap-8

Shorthand: px-4 py-2 (horizontal/vertical)
           mx-auto (center block horizontally)
           space-x-4 space-y-2 (gap between children via margin)
```

### Sizing
```
w-full    w-screen  w-auto    w-fit     w-1/2   w-1/3   w-2/3   w-1/4   w-3/4
h-full    h-screen  h-auto    h-fit
min-h-screen  max-w-xl  max-w-2xl  max-w-screen-lg
```

### Colors
Tailwind v4 includes a full palette: `slate`, `gray`, `zinc`, `neutral`, `stone`, `red`, `orange`, `amber`, `yellow`, `lime`, `green`, `emerald`, `teal`, `cyan`, `sky`, `blue`, `indigo`, `violet`, `purple`, `fuchsia`, `pink`, `rose`.

Each color has shades `50 100 200 300 400 500 600 700 800 900 950`.

```html
<div class="bg-indigo-600 text-white">                   <!-- background + text -->
<div class="bg-gray-900 text-gray-100">                  <!-- dark surface -->
<div class="border border-white/10">                     <!-- border with opacity -->
<div class="text-indigo-400">                            <!-- tinted text -->
<div class="ring-2 ring-indigo-500/50">                  <!-- focus ring -->

<!-- Opacity modifier (v4 syntax — replaces bg-opacity-*) -->
<div class="bg-black/20">                               <!-- 20% opacity -->
<div class="text-white/80">                             <!-- 80% opacity -->
```

### Typography
```
text-xs   text-sm   text-base  text-lg  text-xl  text-2xl  text-3xl  text-4xl  text-5xl  text-6xl
font-thin  font-light  font-normal  font-medium  font-semibold  font-bold  font-black
leading-none  leading-tight  leading-snug  leading-normal  leading-relaxed  leading-loose
tracking-tighter  tracking-tight  tracking-normal  tracking-wide  tracking-wider  tracking-widest
text-left  text-center  text-right  text-justify
uppercase  lowercase  capitalize  normal-case
truncate  line-clamp-2  line-clamp-3
```

### Borders & Radius
```
border  border-2  border-4        border-none
border-gray-700   border-white/10
rounded-none  rounded-sm  rounded  rounded-md  rounded-lg  rounded-xl  rounded-2xl  rounded-full
divide-y  divide-gray-700   (adds border-bottom between children)
outline-none  outline  outline-2  outline-indigo-500
ring-1  ring-2  ring-indigo-500   ring-offset-2
```

### Shadows
```
shadow-sm  shadow  shadow-md  shadow-lg  shadow-xl  shadow-2xl  shadow-none
shadow-indigo-500/30    (colored shadow)
drop-shadow-md  drop-shadow-lg
```

### Backgrounds
```
bg-transparent  bg-white  bg-black
bg-gradient-to-r  bg-gradient-to-b  bg-gradient-to-br   (direction)
from-indigo-600  via-purple-500  to-pink-500            (stops)
bg-no-repeat  bg-cover  bg-contain  bg-center
```

---

## Step 4 — Layout: Flexbox

```html
<!-- Flex row (default) -->
<div class="flex items-center justify-between gap-4">

<!-- Flex column -->
<div class="flex flex-col gap-6">

<!-- Center everything -->
<div class="flex items-center justify-center min-h-screen">

<!-- Wrap -->
<div class="flex flex-wrap gap-3">

<!-- Individual child -->
<div class="flex-1">    <!-- grow to fill -->
<div class="flex-none"> <!-- don't grow or shrink -->
<div class="shrink-0">  <!-- don't shrink (v4: was flex-shrink-0) -->
<div class="grow">      <!-- grow (v4: was flex-grow) -->
<div class="ml-auto">   <!-- push to the right -->
```

---

## Step 5 — Layout: Grid

```html
<!-- Equal columns -->
<div class="grid grid-cols-3 gap-6">

<!-- Responsive grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

<!-- Column span -->
<div class="col-span-2">

<!-- Named grid areas via arbitrary values -->
<div class="grid grid-cols-[250px_1fr] gap-0">   <!-- sidebar + main -->
<div class="grid grid-rows-[auto_1fr_auto] min-h-screen"> <!-- header + content + footer -->

<!-- Auto-fit responsive grid (no breakpoints needed) -->
<div class="grid gap-6" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))">
```

---

## Step 6 — Responsive Design

Tailwind is **mobile-first**: unprefixed classes apply at all sizes; prefixed classes apply at that breakpoint and above.

| Prefix | Min-width |
|---|---|
| *(none)* | 0px — applies everywhere |
| `sm:` | 40rem (640px) |
| `md:` | 48rem (768px) |
| `lg:` | 64rem (1024px) |
| `xl:` | 80rem (1280px) |
| `2xl:` | 96rem (1536px) |

```html
<!-- Stack on mobile, side-by-side on desktop -->
<div class="flex flex-col md:flex-row gap-6">

<!-- Responsive text sizes -->
<h1 class="text-2xl md:text-4xl lg:text-5xl font-bold">

<!-- Show/hide -->
<div class="hidden lg:block">Desktop only</div>
<div class="block lg:hidden">Mobile only</div>

<!-- Responsive padding -->
<div class="p-4 md:p-8 lg:p-12">

<!-- Responsive grid columns -->
<div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
```

---

## Step 7 — State Variants

```html
<!-- Hover -->
<button class="bg-indigo-600 hover:bg-indigo-500 transition-colors">

<!-- Focus -->
<input class="border border-gray-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30 outline-none">

<!-- Active (pressed) -->
<button class="active:scale-95 transition-transform">

<!-- Disabled -->
<button class="disabled:opacity-50 disabled:cursor-not-allowed">

<!-- Group hover — parent has group, children react to parent hover -->
<div class="group relative overflow-hidden rounded-xl">
  <div class="group-hover:scale-105 transition-transform duration-300">
  <div class="opacity-0 group-hover:opacity-100 transition-opacity">

<!-- Peer — sibling reacts to sibling state -->
<input class="peer" type="checkbox">
<span class="hidden peer-checked:block">Checked!</span>

<!-- Placeholder -->
<input class="placeholder:text-gray-500">

<!-- First/last child -->
<li class="border-b border-gray-800 last:border-0">

<!-- Odd/even rows -->
<tr class="even:bg-gray-900/50">
```

---

## Step 8 — Dark Mode

In v4, dark mode works automatically via `prefers-color-scheme` media query — no configuration needed. For a **class-controlled toggle**, add the `@custom-variant` setup:

```html
<style type="text/tailwindcss">
  /* Enable class-based dark mode */
  @custom-variant dark (&:where(.dark, .dark *));
</style>
```

Then toggle the `dark` class on `<html>` with JavaScript:
```javascript
document.documentElement.classList.toggle('dark');
```

Pattern for every dark mode pair:
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
<div class="border-gray-200 dark:border-gray-700">
<p class="text-gray-600 dark:text-gray-400">
<button class="bg-indigo-600 hover:bg-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-400">

<!-- Combine with responsive and state -->
<a class="text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400">
```

---

## Step 9 — Animations & Transitions

```html
<!-- Transition (apply before hover/focus variants) -->
<button class="transition-colors duration-200">         <!-- color transitions -->
<div   class="transition-all duration-300 ease-in-out"> <!-- all properties -->
<div   class="transition-transform duration-150">       <!-- transform only -->

<!-- Built-in animations -->
<div class="animate-spin">        <!-- infinite rotation (loading spinners) -->
<div class="animate-ping">        <!-- scale + fade pulse (notification badges) -->
<div class="animate-pulse">       <!-- opacity pulse (skeleton loaders) -->
<div class="animate-bounce">      <!-- bounce up/down -->

<!-- Transforms -->
<div class="hover:scale-105 transition-transform">        <!-- grow on hover -->
<div class="hover:-translate-y-1 transition-transform">  <!-- lift on hover -->
<div class="hover:rotate-3 transition-transform">        <!-- tilt on hover -->

<!-- Custom keyframe animation via arbitrary CSS -->
<style type="text/tailwindcss">
  @theme {
    --animate-fade-in: fade-in 0.4s ease-out;
  }
  @keyframes fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>
<div class="animate-fade-in">Fades in on mount</div>
```

---

## Step 10 — Arbitrary Values

When the theme scale isn't enough, use square brackets for one-off values:

```html
<div class="w-[372px]">                  <!-- exact pixel width -->
<div class="bg-[#6366f1]">              <!-- exact hex color -->
<div class="top-[117px]">              <!-- exact position -->
<div class="grid-cols-[1fr_2fr_1fr]">  <!-- custom grid template -->
<div class="text-[13px]">              <!-- exact font size -->
<div class="shadow-[0_4px_20px_rgba(99,102,241,0.4)]">  <!-- custom shadow -->
<div class="translate-y-[-50%]">       <!-- calc-like negative -->

<!-- CSS variables -->
<div class="bg-(--my-brand-color)">    <!-- shorthand for var() -->

<!-- Arbitrary properties (escape hatch for any CSS) -->
<div class="[clip-path:polygon(0_0,100%_0,100%_85%,0_100%)]">
<div class="[mask-image:linear-gradient(to_bottom,black,transparent)]">
```

---

## Step 11 — Component Patterns

### Card
```html
<div class="bg-gray-900 rounded-2xl border border-white/10 p-6 shadow-xl hover:-translate-y-1 transition-transform duration-200">
  <div class="flex items-center gap-3 mb-4">
    <div class="w-10 h-10 rounded-xl bg-indigo-500/20 flex items-center justify-center text-indigo-400">
      <!-- icon -->
    </div>
    <div>
      <h3 class="font-semibold text-white">Card Title</h3>
      <p class="text-sm text-gray-500">Subtitle</p>
    </div>
  </div>
  <p class="text-gray-400 text-sm leading-relaxed">Card content goes here.</p>
</div>
```

### Badge / Pill
```html
<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-500/15 text-indigo-400 ring-1 ring-indigo-500/30">
  Active
</span>
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-500/15 text-green-400">
  Success
</span>
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-500/15 text-red-400">
  Error
</span>
```

### Button variants
```html
<!-- Primary -->
<button class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-colors">
  Primary
</button>
<!-- Ghost -->
<button class="px-4 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 font-medium text-sm transition-colors">
  Ghost
</button>
<!-- Outline -->
<button class="px-4 py-2 rounded-lg border border-white/10 hover:border-white/25 text-gray-300 font-medium text-sm transition-colors">
  Outline
</button>
<!-- Destructive -->
<button class="px-4 py-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 font-medium text-sm border border-red-500/20 transition-colors">
  Delete
</button>
```

### Input
```html
<div class="space-y-1.5">
  <label class="block text-sm font-medium text-gray-300">Email</label>
  <input
    type="email"
    placeholder="you@example.com"
    class="w-full px-3 py-2 rounded-lg bg-gray-900 border border-white/10 text-gray-100 text-sm placeholder:text-gray-600
           focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-colors"
  >
</div>
```

### Stat card
```html
<div class="bg-gray-900/60 rounded-2xl border border-white/8 p-6 backdrop-blur">
  <p class="text-sm text-gray-500 font-medium mb-1">Total Revenue</p>
  <p class="text-3xl font-bold text-white">$48,295</p>
  <p class="mt-2 flex items-center gap-1.5 text-sm text-green-400">
    <svg class="w-4 h-4" ...>...</svg>
    +12.5% from last month
  </p>
</div>
```

---

## Step 12 — Important v4 API Changes from v3

| v3 class | v4 equivalent | Note |
|---|---|---|
| `bg-opacity-50` | `bg-black/50` | Opacity modifier syntax |
| `!flex` | `flex!` | Important modifier moves to end |
| `flex-grow` | `grow` | Renamed |
| `flex-shrink` | `shrink` | Renamed |
| `flex-shrink-0` | `shrink-0` | Renamed |
| `outline-none` | `outline-hidden` | `outline-none` now truly `outline: none` |
| `bg-gradient-to-t` | `bg-linear-to-t` | Gradient naming |
| `decoration-clone` | `box-decoration-clone` | Renamed |
| `shadow-sm` fill | Identical | No change |
| `tailwind.config.js` | `@theme { }` in CSS | Configuration moved to CSS |
| `@tailwind base` | `@import "tailwindcss"` | Import syntax (build tools only) |

---

## Step 13 — Design & Polish Guidelines

- **Dark theme tokens** — define custom colors in `@theme { }` and use them as utilities (`bg-body`, `text-title`, `border-subtle`) for consistency
- **Spacing rhythm** — stick to Tailwind’s 4px scale (`p-4` = 16px, `gap-6` = 24px); avoid arbitrary values unless necessary
- **Rounded corners** — `rounded-2xl` (16px) for cards, `rounded-lg` (8px) for buttons and inputs — consistent radius across the page
- **Shadows** — `shadow-lg` or `shadow-xl` for elevated cards on dark backgrounds; avoid `shadow-sm` which is invisible on dark themes
- **Focus states** — always include `focus:ring-2 focus:ring-indigo-500 focus:outline-none` on interactive elements for accessibility
- **Hover transitions** — add `transition-colors duration-200` to elements with `hover:` color changes for smooth feedback
- **Text hierarchy** — use `text-sm` for body, `text-xs` for labels/captions, `text-lg` or `text-xl` for headings; keep the scale tight
- **Responsive testing** — always test `sm:`, `md:`, `lg:` breakpoints; use `flex-col md:flex-row` for stack-to-row patterns
- **No `@apply` in artifacts** — the Play CDN doesn’t support `@apply`; use inline utilities only

---

## Step 14 — Complete Example: Landing Page Hero

```html
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nucleus — AI Platform</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <style type="text/tailwindcss">
    @theme {
      --color-brand:  #6366f1;
      --color-accent: #ec4899;
      --font-sans:    'Segoe UI', system-ui, sans-serif;
      --animate-fade-up: fade-up 0.5s ease-out both;
    }
    @keyframes fade-up {
      from { opacity: 0; transform: translateY(16px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @custom-variant dark (&:where(.dark, .dark *));
  </style>
</head>
<body class="bg-gray-950 text-gray-100 antialiased">

  <!-- Nav -->
  <nav class="fixed top-0 inset-x-0 z-50 border-b border-white/5 bg-gray-950/80 backdrop-blur-md">
    <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
      <span class="font-bold text-lg tracking-tight">⬡ Nucleus</span>
      <div class="hidden sm:flex items-center gap-6 text-sm text-gray-400">
        <a href="#" class="hover:text-white transition-colors">Docs</a>
        <a href="#" class="hover:text-white transition-colors">Pricing</a>
        <a href="#" class="hover:text-white transition-colors">Blog</a>
        <a href="#" class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium transition-colors">Sign up</a>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <main class="pt-32 pb-24 px-6">
    <div class="max-w-4xl mx-auto text-center">

      <!-- Badge -->
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-400 text-sm font-medium mb-8 animate-fade-up">
        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse"></span>
        Now in public beta
      </div>

      <!-- Headline -->
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight mb-6 animate-fade-up [animation-delay:100ms]">
        Build AI products
        <span class="bg-linear-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
          10× faster
        </span>
      </h1>

      <!-- Sub -->
      <p class="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed animate-fade-up [animation-delay:200ms]">
        Nucleus gives your team the infrastructure, APIs, and tooling to ship production-grade AI applications — without the DevOps overhead.
      </p>

      <!-- CTAs -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center animate-fade-up [animation-delay:300ms]">
        <a href="#" class="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition-colors shadow-lg shadow-indigo-500/25">
          Start free →
        </a>
        <a href="#" class="px-6 py-3 rounded-xl border border-white/10 hover:border-white/20 text-gray-300 hover:text-white font-semibold text-sm transition-colors">
          View docs
        </a>
      </div>

      <!-- Social proof -->
      <p class="mt-8 text-sm text-gray-600 animate-fade-up [animation-delay:400ms]">
        Trusted by <span class="text-gray-400 font-medium">2,400+</span> teams worldwide
      </p>
    </div>
  </main>

  <!-- Feature grid -->
  <section class="max-w-6xl mx-auto px-6 pb-24">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <!-- Feature card (repeated) -->
      <div class="group bg-gray-900/60 rounded-2xl border border-white/8 p-6 hover:border-indigo-500/30 hover:-translate-y-1 transition-all duration-200">
        <div class="w-10 h-10 rounded-xl bg-indigo-500/15 flex items-center justify-center mb-4 text-indigo-400 group-hover:bg-indigo-500/25 transition-colors">
          🧠
        </div>
        <h3 class="font-semibold text-white mb-2">Model Router</h3>
        <p class="text-sm text-gray-400 leading-relaxed">Automatically route requests to the optimal model based on task complexity and cost constraints.</p>
      </div>
      <div class="group bg-gray-900/60 rounded-2xl border border-white/8 p-6 hover:border-purple-500/30 hover:-translate-y-1 transition-all duration-200">
        <div class="w-10 h-10 rounded-xl bg-purple-500/15 flex items-center justify-center mb-4 text-purple-400 group-hover:bg-purple-500/25 transition-colors">
          ⚡
        </div>
        <h3 class="font-semibold text-white mb-2">Edge Inference</h3>
        <p class="text-sm text-gray-400 leading-relaxed">Deploy models to 300+ edge locations globally. Sub-50ms latency for any user, anywhere on earth.</p>
      </div>
      <div class="group bg-gray-900/60 rounded-2xl border border-white/8 p-6 hover:border-pink-500/30 hover:-translate-y-1 transition-all duration-200">
        <div class="w-10 h-10 rounded-xl bg-pink-500/15 flex items-center justify-center mb-4 text-pink-400 group-hover:bg-pink-500/25 transition-colors">
          🛡️
        </div>
        <h3 class="font-semibold text-white mb-2">Guardrails</h3>
        <p class="text-sm text-gray-400 leading-relaxed">Built-in prompt injection detection, PII filtering, and content moderation. Safe AI, by default.</p>
      </div>
    </div>
  </section>

</body>
</html>
```

---

## Common Mistakes to Avoid

- **Using Play CDN in production** — `@tailwindcss/browser@4` is a development tool that scans the DOM at runtime. For production, use the Vite plugin (`@tailwindcss/vite`) or CLI — they generate a static, optimized CSS file
- **Forgetting `type="text/tailwindcss"` on `<style>`** — without it, the Play CDN won't process `@theme`, `@utility`, or `@layer` — the block will be treated as raw CSS and `@theme` will cause a CSS parse error
- **Using v3 class names in v4** — key renames: `flex-grow → grow`, `flex-shrink → shrink`, `outline-none → outline-hidden`, `bg-opacity-50 → bg-black/50`, `bg-gradient-to-r → bg-linear-to-r`. The v4 Play CDN will silently ignore unknown classes
- **Dynamic class names** — Tailwind generates only classes it can detect statically. Never construct class names programmatically: `"text-" + color + "-500"` → the class `text-red-500` won't be generated. Write full class names: `text-red-500`
- **Important modifier order** — in v4, the important modifier moves to the **end**: `flex!` not `!flex`. Using the v3 syntax will be silently ignored
- **`@apply` not supported in Play CDN** — the browser CDN does not support `@apply`. Use component classes or `@utility` directives instead. `@apply` only works in build-tool setups
- **Relying on `container` class without configuration** — the `container` utility is fixed-width by breakpoint and NOT centered by default. Add `mx-auto` and `px-4` to center it: `<div class="container mx-auto px-4">`
- **Overriding with `@theme` instead of `extend`** — in v4, defining `--color-*` in `@theme` adds to the palette without removing defaults; but defining `--font-*` replaces the defaults. Be intentional about whether you're adding or replacing
