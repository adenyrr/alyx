---
name: animejs-animation
description: Create precise, timeline-driven DOM and SVG animations using Anime.js v4, delivered as self-contained HTML artifacts. Use this skill whenever someone needs controlled, choreographed animation on HTML elements — entrance sequences, staggered reveals, interactive micro-animations, SVG morphing, scroll-triggered effects, draggable elements with physics, or any animation that requires exact timing, sequencing, and easing control over DOM/SVG. Trigger on requests like "animate these cards appearing one by one", "make this SVG morph", "create a staggered entrance animation", "animate a loading sequence", "add scroll-triggered animations", "make this draggable with spring physics", or any request for choreographed multi-element animation. Anime.js excels where CSS transitions are too simple and Three.js / p5.js would be overkill — the sweet spot is precise, beautiful DOM animation. Do NOT use for generative art / canvas (→ p5js), 3D WebGL scenes (→ threejs-3d), or static diagrams (→ mermaid-diagrams).
---

# Anime.js Animation Skill — v4

Anime.js v4 is a complete ESM-first rewrite of the library. The API changed fundamentally from v3: `animate(targets, params)` replaces `anime({ targets, ... })`, easing names are shortened, and major new systems (Timeline, Scroll, Draggable, SVG, Text) are now first-class modules.

> **⚠️ v3 syntax will silently break in v4.** If you find v3 examples online (`anime({ targets: '.el', easing: 'easeOutExpo' })`), they are wrong for v4. Always use v4 syntax as documented here.

---

## Artifact Presentation & Use Cases

Every Anime.js artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the animated content
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the animation
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context or interaction hints
- **Animated elements** — DOM elements, SVG paths, or cards that Anime.js manipulates

### Typical use cases

- **Entrance animations** — staggered card reveals, fade-in sequences, slide-up lists
- **Micro-interactions** — button hover effects, toggle animations, loading spinners
- **SVG morphing** — path transitions, stroke drawing (dashoffset), shape morphing
- **Scroll-triggered effects** — elements animate in as the user scrolls via `onScroll()`
- **Timeline choreography** — multi-step animation sequences with precise timing control
- **Draggable elements** — drag-and-drop with spring physics via `createDraggable()`

### What the user sees

Smooth, choreographed animations: elements entrance with staggered timing, SVG paths draw themselves, cards slide in on scroll. Animations feel polished and intentional — the dark theme provides clean contrast for motion.

---

## When to Use Anime.js vs. Alternatives

| Use Anime.js when… | Use another tool when… |
|---|---|
| Precise DOM/SVG animation timing | Simple hover/transition effects → **CSS transitions** |
| Staggered reveal sequences | Generative art, particle systems → **p5.js / Canvas** |
| SVG path morphing and drawing | 3D WebGL scenes → **Three.js** |
| Scroll-triggered animation | Data-driven transitions on SVG → **D3** (built-in transitions) |
| Draggable elements with physics | Complex gesture handling → **GSAP / Framer Motion** |
| Timeline-based choreography | React component animations → **Framer Motion / React Spring** |

> **Rule of thumb:** if you need choreographed, multi-element DOM/SVG animation with exact timing control, Anime.js is the right choice. For simple transitions, CSS suffices. For canvas/WebGL, use dedicated libraries.

---

## Step 1 — CDN Setup

### Option A — UMD bundle (simplest for HTML artifacts)
```html
<!-- In <body>, before your script -->
<script src="https://cdn.jsdelivr.net/npm/animejs/dist/bundles/anime.umd.min.js"></script>
<script>
  // Destructure from the global `anime` object
  const { animate, createTimeline, createTimer, stagger, onScroll,
          createDraggable, createAnimatable, createScope,
          utils, svg, eases } = anime;
</script>
```

### Option B — ES Module (importmap, cleaner)
```html
<script type="importmap">
{
  "imports": {
    "animejs": "https://cdn.jsdelivr.net/npm/animejs/dist/modules/index.js"
  }
}
</script>
<script type="module">
  import { animate, createTimeline, stagger, onScroll, createDraggable, utils, svg } from 'animejs';
</script>
```

> Use **Option A (UMD)** for simplicity in artifacts. The UMD bundle exposes everything via the global `anime` object — no import map required.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Animation</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    /* Elements to animate — define their initial state in CSS */
    .card {
      opacity: 0;             /* initial state — Anime will animate TO opacity: 1 */
      transform: translateY(24px); /* Anime animates FROM here */
    }
  </style>
</head>
<body>

  <!-- Markup -->

  <!-- Anime.js UMD LAST, before your script -->
  <script src="https://cdn.jsdelivr.net/npm/animejs/dist/bundles/anime.umd.min.js"></script>
  <script>
    const { animate, createTimeline, stagger, utils } = anime;

    // All animation code here
  </script>
</body>
</html>
```

> **Pattern:** Define the visual *start state* of elements in CSS (`opacity: 0`, `transform: translateY(24px)`). Anime.js animates them to their natural/final state. This prevents a flash of content before the animation starts.

---

## Step 3 — Core: `animate()`

`animate()` is the primary function. Unlike v3, **targets are the first argument**, not a property inside the params object.

```javascript
const anim = animate(targets, parameters);

// targets can be:
animate('.card', { ... })          // CSS selector (all matching elements)
animate('#hero', { ... })          // single ID
animate(document.querySelector('.el'), { ... })  // DOM element
animate([el1, el2, el3], { ... })  // array of elements
animate({ value: 0 }, { value: 100, onUpdate: self => console.log(self.targets[0].value) }) // JS object
```

### Animatable properties
```javascript
// CSS transforms (use camelCase shorthand — preferred over transform string)
animate('.el', {
  x:        100,         // translateX in px
  y:        '50%',       // translateY (unit auto-detected)
  rotate:   '1turn',     // rotate (deg, turn, rad)
  scale:    1.5,
  scaleX:   0.8,
  scaleY:   1.2,
  skewX:    10,
  skewZ:    5,
});

// CSS properties (camelCase)
animate('.el', {
  opacity:         0,
  backgroundColor: '#6366f1',
  width:           '200px',
  borderRadius:    '50%',
  fontSize:        '2rem',
  color:           'rgb(99, 102, 241)',
});

// CSS custom properties (CSS variables)
animate('.el', {
  '--progress': '100%',
  '--hue':      360,
});

// SVG attributes
animate('circle', {
  r:    50,
  cx:   200,
  fill: '#6366f1',
});

// JavaScript object properties (no DOM required)
const obj = { count: 0 };
animate(obj, {
  count:    100,
  duration: 1000,
  onUpdate: () => display.textContent = Math.round(obj.count),  // animated counter
});
```

### Tween parameters (per-property control)
```javascript
animate('.el', {
  // Simple value — animates from current CSS value to this
  x: 200,

  // Object with explicit from/to
  opacity: { from: 0, to: 1 },

  // Object with per-property timing
  y: {
    to:       100,
    delay:    200,      // ms delay before this property starts
    duration: 800,      // ms for this property only
    ease:     'outBounce',
  },

  // Relative values (+=, -=, *=)
  x: '+=100',    // add 100 to current value
  scale: '*=2',  // multiply current value by 2
  rotate: '-=45',

  // Array = keyframes shorthand
  x: [0, 100, 50, 200],   // visits each value in sequence

  // Function-based (called once per element, receives element + index + total)
  x: (el, i) => i * 80,         // stagger by index
  delay: (el, i) => i * 100,    // custom delay per element
  duration: (el, i) => 400 + i * 50,
});
```

---

## Step 4 — Playback Settings

```javascript
animate('.el', {
  x:             300,
  duration:      1200,    // ms (default: 1000)
  delay:         500,     // ms before animation starts
  loopDelay:     200,     // ms between loop iterations
  ease:          'outQuad',  // easing function (see Step 6)
  loop:          true,    // infinite loop
  loop:          3,       // loop 3 times then stop
  alternate:     true,    // reverse direction on each loop (ping-pong)
  reversed:      true,    // play in reverse
  autoplay:      true,    // start immediately (default: true)
  playbackRate:  0.5,     // 0.5 = half speed, 2 = double speed
  playbackEase:  'inOutSine',  // ease applied to the entire animation's progress
});
```

---

## Step 5 — Playback Methods & Callbacks

```javascript
const anim = animate('.el', { x: 200, autoplay: false });

// Methods — chainable
anim.play()       // start / resume
anim.pause()      // pause
anim.restart()    // go to beginning and play
anim.reverse()    // reverse direction and play
anim.seek(500)    // jump to 500ms (does not change play state)
anim.complete()   // jump to end
anim.revert()     // restore original CSS values and stop
anim.cancel()     // stop without reverting
anim.then(cb)     // promise — resolves when animation completes

// Callbacks (receive the animation instance)
animate('.el', {
  x: 200,
  onBegin:   (anim) => console.log('started'),
  onUpdate:  (anim) => console.log(anim.currentTime, 'ms'),
  onComplete:(anim) => console.log('done'),
  onLoop:    (anim) => console.log('looped'),
  onPause:   (anim) => console.log('paused'),
});

// Await pattern
await animate('.el', { x: 200, duration: 800 });
console.log('animation complete');
// Or: animate(...).then(() => console.log('done'));
```

---

## Step 6 — Easing Reference

v4 uses shortened easing names (no more `easeOutQuad` — just `outQuad`).

```javascript
// Basic easings
ease: 'linear'
ease: 'inSine'   | 'outSine'   | 'inOutSine'
ease: 'inQuad'   | 'outQuad'   | 'inOutQuad'
ease: 'inCubic'  | 'outCubic'  | 'inOutCubic'
ease: 'inQuart'  | 'outQuart'  | 'inOutQuart'
ease: 'inQuint'  | 'outQuint'  | 'inOutQuint'
ease: 'inExpo'   | 'outExpo'   | 'inOutExpo'
ease: 'inCirc'   | 'outCirc'   | 'inOutCirc'
ease: 'inBack'   | 'outBack'   | 'inOutBack'     // slight overshoot
ease: 'inElastic'| 'outElastic'| 'inOutElastic'  // springy
ease: 'inBounce' | 'outBounce' | 'inOutBounce'   // bouncing

// Spring physics (most natural-feeling)
import { createSpring } from 'animejs';  // or destructure from anime object
ease: createSpring({ stiffness: 100, damping: 10, mass: 1 })
// stiffness: 1–1000 (higher = snappier), damping: 1–100 (higher = less oscillation)
// Note: spring ignores duration — it plays until it settles

// Cubic bezier (like CSS transition-timing-function)
ease: eases.cubicBezier(0.25, 0.1, 0.25, 1)

// Steps (discrete jumps)
ease: eases.steps(5)    // 5 equal steps
```

**Quick guide:**
| Effect | Use |
|---|---|
| Natural UI motion | `outCubic` or `outQuint` |
| Entrance (flies in) | `outExpo` or `outBack` |
| Emphasize / pop | `outElastic` or `createSpring` |
| Bounce landing | `outBounce` |
| Smooth loop | `inOutSine` |
| Suspense / emphasis | `inOutQuint` |

---

## Step 7 — `stagger()` Utility

`stagger` applies a progressively increasing value across multiple elements — the cleanest way to create cascade/ripple/wave effects.

```javascript
const { animate, stagger } = anime;

// Basic stagger — each element starts 100ms after the previous
animate('.card', {
  opacity: [0, 1],
  y:       [20, 0],
  delay:   stagger(100),         // 0ms, 100ms, 200ms, 300ms…
  duration: 600,
  ease:    'outExpo',
});

// stagger(value, options)
delay: stagger(100, {
  start:    200,          // start offset — first element starts at 200ms
  from:     'center',     // distribute from center outward (instead of start→end)
  from:     2,            // distribute from index 2 outward
  reversed: true,         // start delay from last element instead of first
  ease:     'outQuad',    // apply easing to the delay distribution itself
  grid:     [4, 3],       // 2D grid stagger (for elements in a grid layout)
  axis:     'x',          // 'x' | 'y' (with grid)
})

// stagger a value (not just delay)
animate('.dot', {
  x:     stagger('2rem'),          // 0rem, 2rem, 4rem, 6rem…
  scale: stagger([0.5, 1.5]),     // range: first=0.5, last=1.5, interpolated between
  delay: stagger(50, { from: 'center' }),
});
```

---

## Step 8 — `createTimeline()`

A timeline sequences multiple `animate()` calls with precise time positioning. Each `.add()` call adds an animation at the specified time offset.

```javascript
const { createTimeline, stagger } = anime;

const tl = createTimeline({
  // Playback options (same as animate)
  loop:      false,
  alternate: false,
  autoplay:  true,
  defaults: {                    // shared defaults for all child animations
    duration: 600,
    ease:     'outExpo',
  },
  // Callbacks
  onComplete: () => console.log('sequence done'),
});

// .add(targets, params, timePosition?)
tl
  .add('.hero-title',    { opacity: [0, 1], y: [30, 0] })          // starts at 0ms (after previous)
  .add('.hero-subtitle', { opacity: [0, 1], y: [20, 0] })          // starts when previous ends
  .add('.hero-cta',      { opacity: [0, 1], scale: [0.8, 1] })     // chained
  .add('.nav-item',      { opacity: [0, 1], x: [-20, 0],
                           delay: stagger(80) }, '-=200')           // overlap previous by 200ms
  .add('.background',    { opacity: [0, 0.5] }, 0)                 // absolute position: at 0ms
  .add('.badge',         { scale: [0, 1], opacity: [0, 1] }, '<')  // at same time as previous
  .add('.badge',         { rotate: ['0turn', '1turn'] }, '+=100'); // 100ms after previous END

// Time position shortcuts
// '<'       → same start time as previous animation
// '<100'    → 100ms after start of previous animation
// '-=200'   → 200ms before end of previous animation (overlap)
// '+=200'   → 200ms after end of previous animation (gap)
// 1500      → absolute time in ms
// 'myLabel' → jump to a named label

// Labels
tl.label('cards-start');
tl.add('.card', { ... }, 'cards-start');
tl.add('.card-detail', { ... }, 'cards-start+=200');

// Set an instant value (no animation, just set)
tl.set('.el', { opacity: 0, x: -100 });

// Call a function at a specific time
tl.call(() => updateUI(), 1200);

// Playback control
tl.play();
tl.pause();
tl.seek(800);    // jump to 800ms
tl.reverse();
tl.restart();
tl.revert();     // restore all animated elements to initial state
```

---

## Step 9 — `onScroll()` — Scroll-Triggered Animations

`onScroll` replaces `autoplay: true` to link an animation's playback to scroll position.

```javascript
const { animate, createTimeline, onScroll } = anime;

// Simplest form — animation plays as you scroll through the element
animate('.card', {
  opacity: [0, 1],
  y:       [40, 0],
  duration: 800,
  ease:    'outExpo',
  autoplay: onScroll(),   // links to the element's own scroll visibility
});

// Full options
animate('.section', {
  x: ['-100%', '0%'],
  autoplay: onScroll({
    target:    '.section',    // element whose visibility controls the animation
    container: '.scroll-box', // scroll container (default: window)
    enter:     'top bottom',  // when target's TOP enters viewport BOTTOM
    leave:     'bottom top',  // when target's BOTTOM leaves viewport TOP
    sync:      true,          // scrub — animation progress = scroll progress (no playback)
    sync:      'outQuad',     // scrub with easing
    repeat:    true,          // replay every time element enters viewport
    onEnter:   (obs) => console.log('entered', obs.progress),
    onLeave:   (obs) => console.log('left'),
    onUpdate:  (obs) => console.log('scroll progress:', obs.progress),
  }),
});

// Scrub animation — progress tied directly to scroll position
animate('.progress-bar', {
  width: ['0%', '100%'],
  autoplay: onScroll({ sync: true }),  // 0% at top, 100% at bottom of page
});

// Timeline on scroll
createTimeline({
  autoplay: onScroll({ target: '.section', sync: true }),
})
.add('.step-1', { opacity: [0, 1] })
.add('.step-2', { opacity: [0, 1] })
.add('.step-3', { opacity: [0, 1] });
```

---

## Step 10 — `createDraggable()` — Physics Dragging

```javascript
const { createDraggable, createSpring } = anime;

// Simple draggable
const draggable = createDraggable('.circle');

// Full options
const draggable = createDraggable('.card', {
  // Constraints
  x:            { min: 0, max: 400 },    // constrain X axis
  y:            false,                   // disable Y axis (horizontal only)
  container:    '.bounds',              // constrain to container element

  // Snapping
  snap:         100,                     // snap to every 100px
  snap:         [0, 100, 200, 300],      // snap to specific positions
  snapX:        50,
  snapY:        50,

  // Release physics
  releaseEase:  createSpring({ stiffness: 120, damping: 6 }),  // spring to snap point
  releaseVelocity: 0.8,                 // velocity multiplier on release

  // Drag thresholds
  dragThreshold: 3,                    // px before drag starts (default 3)
  velocityMultiplier: 0.8,

  // Callbacks
  onGrab:      (drag) => console.log('grabbed at', drag.x, drag.y),
  onDrag:      (drag) => console.log('dragging', drag.x, drag.y),
  onRelease:   (drag) => console.log('released at velocity', drag.velocity),
  onSettle:    (drag) => console.log('settled at', drag.x, drag.y),
});

// Programmatic control
draggable.enable();
draggable.disable();
draggable.x;           // current X position
draggable.y;           // current Y position
draggable.velocity;    // current velocity magnitude
```

---

## Step 11 — SVG Utilities

```javascript
const { animate, svg } = anime;

// Shape morphing — animate between two SVG path shapes
animate('#shape1', {
  d: svg.morphTo('#shape2'),              // morph to shape2's path
  d: svg.morphTo('#shape2', 2),           // precision level (higher = smoother, more points)
  duration: 1000,
  ease:     'inOutQuad',
  alternate: true,
  loop:      true,
});

// Motion path — move an element along an SVG path
const motionPath = svg.createMotionPath('#my-path');
animate('.rocket', {
  ...motionPath,          // spreads x, y, rotate properties tied to path
  duration: 2000,
  ease:    'inOutSine',
  loop:    true,
});

// SVG drawing — animate a path being drawn (like a signature effect)
const drawable = svg.createDrawable('#my-line');
animate('#my-line', {
  ...drawable,            // animates stroke-dashoffset
  duration: 1500,
  ease:    'outExpo',
});
```

---

## Step 12 — `utils` Module

```javascript
const { utils } = anime;

// utils.$() — like querySelectorAll but returns a real Array
const els = utils.$('.card');   // Array of DOM elements

// utils.set() — instantly set values without animation (no tween)
utils.set('.card', { opacity: 0, x: -20 });   // set initial state
utils.set(el, { scale: 1, rotate: 0 });        // reset after animation

// utils.get() — read current animated value
const currentX = utils.get('.card', 'x');         // returns numeric value
const currentOp = utils.get('.card', 'opacity');

// utils.random(min, max, decimals?)
const x = utils.random(0, 500);       // integer
const y = utils.random(0, 1, 2);     // float with 2 decimals

// utils.lerp(a, b, t) — linear interpolation
const mid = utils.lerp(0, 100, 0.5);  // 50

// utils.clamp(value, min, max)
const safe = utils.clamp(mouseX, 0, 800);

// utils.mapRange(value, fromLow, fromHigh, toLow, toHigh)
const mapped = utils.mapRange(mouseX, 0, innerWidth, -1, 1);

// utils.snap(value, snapPoints)
const snapped = utils.snap(75, 50);      // → 100 (nearest multiple of 50)
const snapped2 = utils.snap(35, [0, 50, 100]);  // → 50
```

---

## Step 13 — v3 → v4 Migration Reference

| v3 pattern | v4 equivalent |
|---|---|
| `anime({ targets: '.el', x: 100 })` | `animate('.el', { x: 100 })` |
| `easing: 'easeOutExpo'` | `ease: 'outExpo'` |
| `direction: 'alternate'` | `alternate: true` |
| `direction: 'reverse'` | `reversed: true` |
| `anime.timeline()` | `createTimeline()` |
| `tl.add({ targets: '.el', ... })` | `tl.add('.el', { ... })` |
| `tl.add({...}, '-=300')` | `tl.add('.el', {...}, '-=300')` (same) |
| `anime.stagger(100)` | `stagger(100)` (imported separately) |
| `anime.setDashoffset` | `svg.createDrawable('#path')` |
| `anime.set('.el', {x: 0})` | `utils.set('.el', {x: 0})` |
| `anime.get('.el', 'x')` | `utils.get('.el', 'x')` |
| `stagger({ direction: 'reversed' })` | `stagger(100, { reversed: true })` |

---

## Step 14 — Design & Polish Guidelines

- **Duration sweet spot** — 300–800ms for most UI animations; shorter feels snappy, longer feels cinematic
- **Easing matters** — `out(3)` (cubic out) is the most natural deceleration; `inOut(3)` for symmetric transitions; avoid linear for UI
- **Stagger direction** — stagger from the element closest to the user’s attention (top-left for cards, center-out for grids)
- **Don’t animate layout properties** — prefer `translate`, `scale`, `opacity` over `width`, `height`, `top`, `left` for GPU-accelerated performance
- **Respect reduced motion** — wrap animations in `if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) { ... }`
- **SVG drawing** — always set `stroke-dasharray` and `stroke-dashoffset` to the path’s total length first, then animate `dashoffset` to 0
- **Scroll triggers** — use `enter: 'bottom'` threshold so elements animate before the user scrolls past them
- **Cleanup** — call `animation.pause()` or `animation.revert()` when removing animated elements to prevent memory leaks
- **Layer animated elements** — use `will-change: transform, opacity` CSS on animated elements for GPU compositing

---

## Step 15 — Complete Example: Staggered Card Entrance + Scroll

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Entrance Animation</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; padding: 48px 24px; }

    .page-title {
      text-align: center; margin-bottom: 48px;
      opacity: 0; transform: translateY(-20px); /* initial state */
    }
    .page-title h1 { font-size: 2.2rem; font-weight: 700; color: #f1f5f9; }
    .page-title p  { color: #64748b; margin-top: 8px; font-size: 0.95rem; }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 20px;
      max-width: 1100px;
      margin: 0 auto;
    }

    .card {
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 16px;
      padding: 24px;
      cursor: pointer;
      opacity: 0;               /* start invisible */
      transform: translateY(32px); /* start below */
      transition: border-color 0.2s;
    }
    .card:hover { border-color: rgba(99,102,241,0.4); }

    .card-icon {
      font-size: 2rem; margin-bottom: 14px; display: block;
      transform: scale(0);  /* start collapsed */
    }
    .card h2  { font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 6px; }
    .card p   { font-size: 0.82rem; color: #64748b; line-height: 1.5; }
    .card-bar {
      margin-top: 18px; height: 3px; border-radius: 2px;
      background: rgba(255,255,255,0.06); overflow: hidden;
    }
    .card-bar-fill { height: 100%; width: 0; border-radius: 2px; }

    .counter-section {
      max-width: 600px; margin: 64px auto 0;
      display: flex; justify-content: center; gap: 48px;
    }
    .counter {
      text-align: center; opacity: 0;
    }
    .counter-val { font-size: 2.8rem; font-weight: 800; color: #6366f1; font-variant-numeric: tabular-nums; }
    .counter-label { font-size: 0.8rem; color: #64748b; margin-top: 4px; }
  </style>
</head>
<body>

  <div class="page-title">
    <h1>Our Platform</h1>
    <p>Everything you need to ship faster</p>
  </div>

  <div class="grid" id="grid"></div>

  <div class="counter-section" id="counters">
    <div class="counter"><div class="counter-val" id="c1">0</div><div class="counter-label">Projects</div></div>
    <div class="counter"><div class="counter-val" id="c2">0</div><div class="counter-label">Users</div></div>
    <div class="counter"><div class="counter-val" id="c3">0</div><div class="counter-label">Uptime %</div></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/animejs/dist/bundles/anime.umd.min.js"></script>
  <script>
    const { animate, createTimeline, createSpring, stagger, onScroll, utils } = anime;

    // ── Build cards ───────────────────────────────────────────
    const cards = [
      { icon:'🧠', title:'AI Router',      desc:'Route requests to the optimal model automatically.',       color:'#6366f1', value:78 },
      { icon:'⚡', title:'Edge Inference', desc:'300+ edge locations. Sub-50ms globally.',                  color:'#06b6d4', value:92 },
      { icon:'🛡️', title:'Guardrails',     desc:'Built-in safety filters and PII detection.',              color:'#22c55e', value:65 },
      { icon:'📊', title:'Analytics',      desc:'Real-time dashboards for all your model calls.',           color:'#eab308', value:84 },
      { icon:'🔗', title:'Integrations',   desc:'Works with OpenAI, Anthropic, Mistral, and more.',        color:'#ec4899', value:71 },
      { icon:'🚀', title:'Deploy',         desc:'One-click deployments with zero config required.',         color:'#f97316', value:90 },
    ];

    const grid = document.getElementById('grid');
    cards.forEach(c => {
      grid.innerHTML += `
        <div class="card" data-value="${c.value}">
          <span class="card-icon">${c.icon}</span>
          <h2>${c.title}</h2>
          <p>${c.desc}</p>
          <div class="card-bar">
            <div class="card-bar-fill" style="background:${c.color}"></div>
          </div>
        </div>`;
    });

    // ── Main entrance sequence ────────────────────────────────
    const tl = createTimeline({ defaults: { ease: 'outExpo' } });

    tl
      // 1. Page title drops in
      .add('.page-title', {
        opacity: [0, 1],
        y:       [-20, 0],
        duration: 700,
      })
      // 2. Cards stagger up simultaneously
      .add('.card', {
        opacity:  [0, 1],
        y:        [32, 0],
        duration: 700,
        delay:    stagger(80, { from: 'first' }),
      }, '-=200')
      // 3. Icons pop in after cards
      .add('.card-icon', {
        scale:    [0, 1],
        duration: 500,
        ease:     createSpring({ stiffness: 280, damping: 18 }),
        delay:    stagger(60),
      }, '-=500')
      // 4. Progress bars fill
      .add('.card-bar-fill', {
        width:    (el) => el.closest('.card').dataset.value + '%',
        duration: 900,
        ease:     'inOutQuart',
        delay:    stagger(60),
      }, '-=300');

    // ── Hover animation on each card ─────────────────────────
    document.querySelectorAll('.card').forEach(card => {
      const icon = card.querySelector('.card-icon');
      card.addEventListener('mouseenter', () => {
        animate(icon, { rotate: '1turn', scale: 1.2, duration: 400, ease: 'outBack' });
      });
      card.addEventListener('mouseleave', () => {
        animate(icon, { rotate: '0turn', scale: 1, duration: 300, ease: 'outQuad' });
      });
    });

    // ── Scroll-triggered counter animation ───────────────────
    const targets = [
      { el: document.getElementById('c1'), end: 1240 },
      { el: document.getElementById('c2'), end: 24800 },
      { el: document.getElementById('c3'), end: 99.97 },
    ];

    animate('.counter', {
      opacity: [0, 1],
      y:       [24, 0],
      duration: 600,
      ease:    'outExpo',
      delay:   stagger(120),
      autoplay: onScroll({ target: '#counters', enter: 'top 85%', repeat: false }),
    });

    targets.forEach(({ el, end }) => {
      const isFloat = end % 1 !== 0;
      const obj = { val: 0 };
      animate(obj, {
        val:      end,
        duration: 1600,
        ease:     'outExpo',
        autoplay: onScroll({ target: '#counters', enter: 'top 85%', repeat: false }),
        onUpdate: () => {
          el.textContent = isFloat ? obj.val.toFixed(2) : Math.round(obj.val).toLocaleString();
        },
      });
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Using v3 syntax** — `anime({ targets: '.el', easing: 'easeOutExpo' })` will NOT work in v4. Use `animate('.el', { ease: 'outExpo' })`. There is no backward compatibility shim
- **Forgetting to destructure from `anime` (UMD)** — with the UMD build, `animate` is not a global — it lives on `window.anime`. Always destructure: `const { animate, stagger } = anime`
- **Animating from CSS class state without setting initial values** — if an element starts at `opacity: 1` in CSS and you animate `opacity: [0, 1]`, the `from: 0` resets the element before animating. Use `utils.set('.el', { opacity: 0 })` before the timeline starts, or set the initial CSS state directly
- **Spring easing ignores `duration`** — `createSpring()` easing determines its own duration based on physics. Passing `duration` alongside a spring ease has no effect. Let the spring settle naturally
- **`revert()` vs `cancel()`** — `revert()` removes all animated values and restores original CSS; `cancel()` stops the animation but leaves elements in their current animated state. Use `revert()` when dismounting or resetting a scene
- **`onScroll` without `repeat: false`** — by default, scroll-triggered animations replay every time the element enters the viewport. Set `repeat: false` if you only want the animation to run once (typical for entrance animations)
- **`stagger` with a single element** — `stagger` is a no-op when targeting a single element (there's no second element to offset). This is not a bug but can be confusing when testing
- **Mixing `autoplay: onScroll(...)` with manual `play()`** — once `autoplay` is set to a scroll observer, the animation's playback is owned by the observer. Calling `play()` manually may conflict. Use `onScroll` OR manual control, not both
- **Morphing SVG paths with different point counts** — `svg.morphTo` works best when both paths have the same number of points. For different point counts, increase the precision parameter: `svg.morphTo('#shape2', 4)` — higher values interpolate more intermediate points at the cost of performance
