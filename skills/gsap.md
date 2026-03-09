---
name: gsap-animation
description: Create scroll-driven animations, parallax effects, and rich motion storytelling using GSAP (GreenSock Animation Platform) with ScrollTrigger, delivered as self-contained HTML artifacts. Use this skill whenever someone needs scroll-triggered animations, parallax scrolling, pinned section reveals, text split/stagger animations, SVG morphing, timeline-based sequenced motion, or cinematic scrollytelling. Trigger on requests like "make a parallax landing page", "animate sections on scroll", "create a scroll-driven story", "build an animated timeline on scroll", or any prompt requiring scroll-aware animations. Do NOT use for simple micro-interactions (→ animejs-animation skill), data visualizations (→ d3/chartjs/plotly), or 3D scenes (→ threejs-3d).
---

# GSAP Animation Skill

GSAP (GreenSock Animation Platform) is the industry-standard JavaScript animation library. Combined with ScrollTrigger, it enables scroll-driven animations, parallax effects, pinned sections, scrubbing (tying animation progress to scroll position), and complex timeline choreography. It works on any DOM element, SVG, or CSS property with buttery-smooth 60fps performance.

---

## Artifact Presentation & Use Cases

Every GSAP artifact is a self-contained HTML page with a dark theme and scroll-enabled content. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Hero section** with animated headline and subtitle that fade/slide in
- **Scrollable sections** — each section triggers its own animation as the user scrolls
- **Pinned panels** — sections that stick while content animates within them
- **Smooth typography** and accent colors (`#6366f1`) for highlights

### Typical use cases

- **Parallax landing pages** — layered backgrounds scrolling at different speeds
- **Scrollytelling** — data stories or narratives that unfold as the user scrolls
- **Section reveals** — elements slide, fade, or scale into view on scroll
- **Text split animations** — headlines where each character/word animates independently
- **Pinned infographics** — a section stays fixed while stats or charts animate in sequence
- **SVG path animations** — drawing SVG strokes on scroll, morphing shapes
- **Hero transitions** — full-screen hero that shrinks/transforms into a header on scroll

### What the user sees

A scrollable page with elements that come alive as they enter the viewport — sliding, fading, scaling, rotating, or morphing in choreographed sequences tied to scroll position.

---

## When to Use GSAP vs. Alternatives

| Use GSAP + ScrollTrigger when… | Use another tool when… |
|---|---|
| Animation must be tied to scroll position | Simple hover/click micro-animations → **Anime.js** |
| Parallax effects with multiple layers | Data-driven animated charts → **D3** |
| Pinned sections with scrubbed timelines | CSS-only transitions are sufficient → **plain CSS** |
| Complex choreographed motion sequences | 3D WebGL scenes → **Three.js** |
| SVG path drawing / morphing on scroll | Physics-based spring animations → **Anime.js** |
| Text split + stagger reveals | Presentation slides → **Reveal.js** |
| Page-level cinematic storytelling | Component-level UI animation → **CSS / Anime.js** |

> **Rule of thumb:** if the animation should respond to scroll position (scrubbing, triggering, pinning), use GSAP + ScrollTrigger. For isolated micro-interactions on click/hover, Anime.js is lighter and sufficient.

---

## Step 1 — CDN Setup

```html
<!-- GSAP Core -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<!-- ScrollTrigger Plugin -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
```

Optional plugins (load only when needed):
```html
<!-- Text splitting (SplitText is Club only — use alternative below) -->
<!-- SVG morphing -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/MotionPathPlugin.min.js"></script>
```

> **Note:** SplitText is a GSAP Club plugin (paid). For free text splitting, manually wrap characters/words in `<span>` elements.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Scroll Animation</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117;
      color: #e2e8f0;
    }
    section {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 60px 24px;
    }
    h1 { font-size: 2.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: 12px; }
    h2 { font-size: 1.6rem; font-weight: 600; color: #f1f5f9; margin-bottom: 8px; }
    p { font-size: 1rem; color: #94a3b8; max-width: 600px; text-align: center; line-height: 1.7; }
    .accent { color: #6366f1; }
    .card {
      background: #1a1d27;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
      max-width: 600px;
      width: 100%;
    }
  </style>
</head>
<body>
  <section class="hero"> ... </section>
  <section class="content"> ... </section>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
  <script>
    gsap.registerPlugin(ScrollTrigger);
    // All GSAP code here
  </script>
</body>
</html>
```

---

## Step 3 — Register Plugins

Always register plugins before using them:

```javascript
gsap.registerPlugin(ScrollTrigger);
// gsap.registerPlugin(MotionPathPlugin); // if using motion paths
```

---

## Step 4 — Basic Tweens

```javascript
// Single property animation
gsap.to('.box', { x: 200, duration: 1 });

// From a starting state
gsap.from('.box', { opacity: 0, y: 50, duration: 0.8 });

// From-to explicit control
gsap.fromTo('.box', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.8 });

// Set (instant, no animation)
gsap.set('.box', { opacity: 0, y: 50 });
```

### Common properties
```javascript
{
  x: 100,              // translateX (px)
  y: -50,              // translateY (px)
  xPercent: -50,       // translateX (%)
  yPercent: -50,       // translateY (%)
  rotation: 45,        // rotate (degrees)
  scale: 1.2,          // scale
  opacity: 0,          // opacity
  duration: 1,         // seconds
  delay: 0.5,          // seconds
  ease: 'power2.out',  // easing
  stagger: 0.1,        // delay between each element in a set
}
```

---

## Step 5 — Timelines

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.8, ease: 'power2.out' } });

tl.from('.title', { opacity: 0, y: 40 })
  .from('.subtitle', { opacity: 0, y: 30 }, '-=0.4')   // overlap by 0.4s
  .from('.card', { opacity: 0, scale: 0.9 }, '-=0.3')
  .from('.btn', { opacity: 0, y: 20 }, '-=0.2');
```

Position shortcuts:
```javascript
tl.to(el, {}, '+=0.5')    // 0.5s after previous ends
tl.to(el, {}, '-=0.3')    // 0.3s before previous ends (overlap)
tl.to(el, {}, '<')         // same start as previous
tl.to(el, {}, '<0.2')      // 0.2s after previous starts
tl.to(el, {}, 2)            // at absolute 2s on the timeline
```

---

## Step 6 — ScrollTrigger (Core)

```javascript
gsap.from('.card', {
  scrollTrigger: {
    trigger: '.card',       // element to watch
    start: 'top 80%',       // trigger when top of .card hits 80% of viewport
    end: 'bottom 20%',      // end when bottom of .card hits 20% of viewport
    toggleActions: 'play none none reverse', // onEnter onLeave onEnterBack onLeaveBack
    // markers: true,       // DEBUG: show start/end markers
  },
  opacity: 0,
  y: 60,
  duration: 0.8,
  ease: 'power2.out',
});
```

### toggleActions values: `play`, `pause`, `resume`, `reverse`, `restart`, `reset`, `complete`, `none`

---

## Step 7 — Scrubbing (Scroll-Linked Progress)

```javascript
// Animation progress tied 1:1 to scroll position
gsap.to('.progress-bar', {
  scaleX: 1,
  ease: 'none',
  scrollTrigger: {
    trigger: 'body',
    start: 'top top',
    end: 'bottom bottom',
    scrub: true,          // true = smooth, number = seconds of lag (e.g., 0.5)
  },
});
```

---

## Step 8 — Pinning

```javascript
// Pin a section while its content animates
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.pinned-section',
    pin: true,              // pin the section
    start: 'top top',
    end: '+=2000',          // pin for 2000px of scroll
    scrub: 1,               // smooth scrubbing
  },
});

tl.from('.step-1', { opacity: 0, x: -100 })
  .from('.step-2', { opacity: 0, x: 100 })
  .from('.step-3', { opacity: 0, y: 50 });
```

---

## Step 9 — Stagger Animations

```javascript
// Stagger children entering view
gsap.from('.grid-item', {
  scrollTrigger: { trigger: '.grid', start: 'top 80%' },
  opacity: 0,
  y: 40,
  duration: 0.6,
  stagger: {
    each: 0.1,       // delay between each
    from: 'start',   // 'start', 'end', 'center', 'edges', 'random', or index
  },
});
```

---

## Step 10 — Text Split Animation (Free Approach)

```javascript
// Split text into <span> per character (no Club plugin needed)
function splitText(selector) {
  const el = document.querySelector(selector);
  el.innerHTML = el.textContent.split('').map(
    (ch, i) => ch === ' ' ? ' ' : `<span style="display:inline-block">${ch}</span>`
  ).join('');
  return el.querySelectorAll('span');
}

const chars = splitText('.hero-title');
gsap.from(chars, {
  opacity: 0, y: 30, rotationX: -90,
  duration: 0.6, stagger: 0.03, ease: 'back.out(1.7)',
});
```

---

## Step 11 — Parallax Effect

```javascript
// Multi-layer parallax
gsap.to('.bg-layer', {
  y: -200,
  ease: 'none',
  scrollTrigger: { trigger: '.parallax-section', start: 'top bottom', end: 'bottom top', scrub: true },
});

gsap.to('.mid-layer', {
  y: -100,
  ease: 'none',
  scrollTrigger: { trigger: '.parallax-section', start: 'top bottom', end: 'bottom top', scrub: true },
});

gsap.to('.fg-layer', {
  y: -30,
  ease: 'none',
  scrollTrigger: { trigger: '.parallax-section', start: 'top bottom', end: 'bottom top', scrub: true },
});
```

---

## Step 12 — Easing Reference

```javascript
// Built-in eases
'none'            // linear
'power1.out'      // gentle ease-out
'power2.out'      // moderate ease-out (most common)
'power3.out'      // strong ease-out
'power4.out'      // extreme ease-out
'back.out(1.7)'   // slight overshoot
'elastic.out(1, 0.3)' // bouncy elastic
'bounce.out'      // bouncing ball
'circ.out'        // circular
'expo.out'        // exponential

// directions: .in, .out, .inOut
```

---

## Step 13 — Design & Polish Guidelines

- **Start hidden** — use `gsap.set()` or CSS to hide elements before scroll triggers them; prevents flash-of-visible-content
- **Smooth scrub** — use `scrub: 1` (1 second lag) rather than `scrub: true` (instant) for a smoother feel
- **Performance** — animate `transform` and `opacity` only; avoid animating `width`, `height`, `top`, `left` (triggers layout reflow)
- **will-change** — GSAP auto-manages GPU layers; do NOT manually add `will-change: transform` (GSAP handles it)
- **ScrollTrigger.refresh()** — call after dynamic content changes height (e.g., images loading, accordions opening)
- **Mobile caution** — pinning on mobile can be janky in WebViews; test thoroughly or disable pinning on small screens with `ScrollTrigger.matchMedia()`
- **Easing consistency** — use `power2.out` as default ease across the project; only deviate for emphasis
- **Stagger moderation** — keep stagger values between `0.03` and `0.15`; too high makes the animation feel sluggish
- **Cleanup** — call `ScrollTrigger.killAll()` or individual `trigger.kill()` when removing sections dynamically
- **Markers for dev** — enable `markers: true` during development to see trigger start/end points; remove for production

---

## Step 14 — Complete Example: Scrollytelling Landing Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Scroll Story</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; overflow-x: hidden; }
    section { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 24px; position: relative; }
    .hero h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 700; color: #f1f5f9; text-align: center; }
    .hero p { font-size: 1.1rem; color: #94a3b8; margin-top: 12px; text-align: center; }
    .accent { color: #6366f1; }

    .progress-bar { position: fixed; top: 0; left: 0; height: 3px; width: 100%; background: #6366f1; transform-origin: left; transform: scaleX(0); z-index: 100; }

    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; max-width: 900px; width: 100%; }
    .card { background: #1a1d27; border-radius: 16px; padding: 28px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    .card h3 { font-size: 1rem; color: #f1f5f9; margin-bottom: 8px; }
    .card p { font-size: 0.85rem; color: #94a3b8; line-height: 1.6; text-align: left; }

    .stat-section { gap: 40px; }
    .stats { display: flex; gap: 40px; flex-wrap: wrap; justify-content: center; }
    .stat { text-align: center; }
    .stat .num { font-size: 2.5rem; font-weight: 700; color: #6366f1; }
    .stat .label { font-size: 0.82rem; color: #64748b; margin-top: 4px; }

    .pinned-section { overflow: hidden; }
    .pin-content { max-width: 600px; text-align: center; }
    .pin-content h2 { font-size: 1.8rem; color: #f1f5f9; margin-bottom: 12px; }
    .pin-content p { font-size: 0.95rem; color: #94a3b8; line-height: 1.7; }
    .step { opacity: 0; }
  </style>
</head>
<body>
  <div class="progress-bar"></div>

  <section class="hero">
    <h1>The Future of <span class="accent">Animation</span></h1>
    <p>Scroll down to explore</p>
  </section>

  <section class="stat-section">
    <h2 style="color:#f1f5f9; font-size:1.4rem;">By the Numbers</h2>
    <div class="stats">
      <div class="stat"><div class="num" data-val="60">0</div><div class="label">Frames/sec</div></div>
      <div class="stat"><div class="num" data-val="300">0</div><div class="label">Plugins</div></div>
      <div class="stat"><div class="num" data-val="11">0</div><div class="label">Million+ Users</div></div>
    </div>
  </section>

  <section>
    <div class="cards">
      <div class="card"><h3>Scroll Driven</h3><p>Tie any animation to scroll position. Scrub through complex timelines as the user scrolls.</p></div>
      <div class="card"><h3>Pinned Panels</h3><p>Pin sections to the viewport while content animates — perfect for step-by-step reveals.</p></div>
      <div class="card"><h3>Stagger Effects</h3><p>Animate lists, grids, and sets of elements with elegant cascading delays.</p></div>
    </div>
  </section>

  <section class="pinned-section">
    <div class="pin-content">
      <div class="step step-a"><h2>Step 1: Observe</h2><p>ScrollTrigger watches the viewport and fires animations when elements enter view.</p></div>
      <div class="step step-b"><h2>Step 2: Animate</h2><p>GSAP handles the math, timing, and GPU acceleration for silky-smooth motion.</p></div>
      <div class="step step-c"><h2>Step 3: Deliver</h2><p>Users experience a polished, interactive story that feels native and responsive.</p></div>
    </div>
  </section>

  <section class="hero">
    <h1>Built with <span class="accent">GSAP</span></h1>
  </section>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
  <script>
    gsap.registerPlugin(ScrollTrigger);

    /* ── Progress bar ── */
    gsap.to('.progress-bar', {
      scaleX: 1, ease: 'none',
      scrollTrigger: { trigger: 'body', start: 'top top', end: 'bottom bottom', scrub: true },
    });

    /* ── Hero entrance ── */
    const heroTl = gsap.timeline({ defaults: { duration: 0.8, ease: 'power2.out' } });
    heroTl.from('.hero h1', { opacity: 0, y: 40 })
          .from('.hero p', { opacity: 0, y: 20 }, '-=0.4');

    /* ── Stat counters ── */
    document.querySelectorAll('.num[data-val]').forEach(el => {
      const target = +el.dataset.val;
      gsap.fromTo(el, { innerText: 0 }, {
        innerText: target,
        duration: 1.5,
        ease: 'power1.out',
        snap: { innerText: 1 },
        scrollTrigger: { trigger: el, start: 'top 85%' },
      });
    });

    /* ── Cards stagger ── */
    gsap.from('.card', {
      scrollTrigger: { trigger: '.cards', start: 'top 80%' },
      opacity: 0, y: 50, duration: 0.7, stagger: 0.15, ease: 'power2.out',
    });

    /* ── Pinned section ── */
    const pinTl = gsap.timeline({
      scrollTrigger: {
        trigger: '.pinned-section',
        pin: true,
        start: 'top top',
        end: '+=2000',
        scrub: 1,
      },
    });
    pinTl.to('.step-a', { opacity: 1, duration: 1 })
         .to('.step-a', { opacity: 0, duration: 0.5 }, '+=0.5')
         .to('.step-b', { opacity: 1, duration: 1 })
         .to('.step-b', { opacity: 0, duration: 0.5 }, '+=0.5')
         .to('.step-c', { opacity: 1, duration: 1 });

    /* ── Final hero ── */
    gsap.from('section:last-child h1', {
      scrollTrigger: { trigger: 'section:last-child', start: 'top 80%' },
      opacity: 0, scale: 0.8, duration: 1, ease: 'power2.out',
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Forgetting `gsap.registerPlugin(ScrollTrigger)`** — ScrollTrigger won't work without registration; call this once before any ScrollTrigger usage
- **Animating layout properties** — `width`, `height`, `top`, `left` trigger layout reflow; use `x`, `y`, `scale`, `opacity` instead
- **`scrub: true` feels jittery** — use `scrub: 0.5` or `scrub: 1` for smoother scroll-linked motion
- **Pinning inside a flex/grid container** — pinning creates a placeholder element; wrap pinned sections in a static parent to avoid layout shifts
- **Not refreshing after async content** — call `ScrollTrigger.refresh()` after images load or content height changes
- **Overusing pinning** — more than 2-3 pinned sections overwhelms users; use sparingly for maximum impact
- **Text split without `display:inline-block`** — split spans must be `inline-block` for transform animations to work
- **Missing `ease: 'none'` on scrubbed tweens** — scrubbed animations with easing feel wrong; use linear (`'none'`) when scrubbing
- **Leaving `markers: true`** — remove debug markers before shipping; they render as visible colored lines
