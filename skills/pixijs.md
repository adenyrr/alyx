---
name: pixijs-webgl
description: Build high-performance 2D WebGL artifacts using Pixi.js v8, delivered as self-contained HTML pages with a polished dark theme. Use this skill whenever a scene needs thousands of sprites, particles, real-time motion, or GPU-accelerated 2D rendering: particle systems, sprite-heavy games, data-driven dot/glyph fields, generative art that needs > 100 moving objects, real-time data visualisations, interactive backgrounds, fluid mouse-reactive scenes, or shader-style effects on bitmap content. Trigger on phrases like "particle system", "thousands of sprites", "swarm", "interactive background", "WebGL 2D scene", "performance-heavy canvas", "real-time animation with many objects", or "GPU canvas". Do NOT use for: 3D scenes (→ threejs-3d skill), static generative art with < 100 objects (→ p5js-creative-coding skill), DOM/SVG animation (→ animejs-animation or gsap-animation), or vector drawing/annotation tools (→ konva-canvas skill).
agents: [dev]
---

# Pixi.js Skill — v8 (2D WebGL Renderer)

Pixi.js is the leading 2D WebGL renderer for the web. It draws sprites, graphics, particles, and text onto a hardware-accelerated canvas at 60 fps with thousands of objects. v8 modernised the API: `await PIXI.Application.init()`, `eventMode` replaces `interactive`, and `ParticleContainer` is now in `pixi.js` core. Bundle size is ~450 KB.

---

## Artifact Presentation & Use Cases

Every Pixi artifact is a self-contained HTML page with a dark theme. Two layout modes are typical:

**Mode A — Card-wrapped scene (data viz, demos, controlled stage)**
- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) frames the canvas
- **Title** (`h1`, 1.15rem, `#f1f5f9`) names the scene
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) shows interaction hints
- **Canvas container** (`#scene`, fixed pixel size) hosts Pixi

**Mode B — Fullscreen scene with HUD overlay (generative art, particle fields)**
- Fullscreen canvas, background colour matches the page (`#0f1117`)
- A blurred HUD overlay (`position: fixed`, `backdrop-filter: blur(12px)`) holds title and FPS counter
- Pointer-events disabled on the overlay so it does not block scene interaction

### Typical use cases

- **Particle systems** — fire, smoke, sparks, snow, confetti with thousands of particles
- **Sprite-heavy games** — top-down shooters, bullet hells, tower defense
- **Real-time data viz** — millions-of-points scatter, animated bubble swarms, force layouts on big graphs
- **Interactive backgrounds** — gradient orbs, flow fields, cursor-reactive dot grids
- **Generative art at scale** — Voronoi animations, agent-based simulations, life-like swarms
- **Tile maps** — isometric or top-down grids with thousands of tiles

### What the user sees

A buttery-smooth 60 fps canvas, often reactive to the mouse, scroll, or touch. Pixi handles all batching internally so 5 000 particles draw in a single GPU draw call. The dark theme integrates the scene visually into the artifact card or fullscreen overlay.

---

## When to Use Pixi vs. Alternatives

| Use Pixi when… | Use another library when… |
|---|---|
| > 100 moving objects on screen | < 100 objects, expressive sketch → **p5.js** |
| Need GPU-accelerated 2D batching | True 3D (depth, lighting, cameras) → **Three.js** |
| Particle systems, sprite-heavy games | DOM/SVG element animation → **Anime.js** / **GSAP** |
| Real-time canvas at 60 fps with many entities | Vector drawing / annotation editor → **Konva.js** |
| Custom shaders on bitmap content | Data charts (bar, line, pie) → **Chart.js** / **Plotly** |
| Pixel-perfect 2D rendering with filters | Tile-based geographic maps → **Leaflet** |

> **Rule of thumb:** if the scene has more than ~100 moving things at once, Pixi will outperform Canvas-2D and p5.js by an order of magnitude. For fewer objects or a sketch-y aesthetic, p5.js is friendlier.

---

## Step 1 — CDN Setup

```html
<!-- Pixi.js v8 — single UMD bundle exposing the global `PIXI` -->
<script src="https://cdn.jsdelivr.net/npm/pixi.js@8.6.6/dist/pixi.min.js"></script>
```

> **v8 vs v7:** `Application.init()` is now async. Always `await app.init({…})` instead of `new PIXI.Application({…})`. Old `interactive: true` is replaced by `eventMode: 'static'` (or `'dynamic'`).

> **No build step:** the UMD bundle works directly. No `import` required, no bundler, no Node tooling.

---

## Step 2 — HTML Artifact Shell (card-wrapped scene)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pixi Scene</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117; color: #e2e8f0;
      display: flex; flex-direction: column; align-items: center;
      min-height: 100vh; padding: 24px;
    }
    .card {
      width: 100%; max-width: 960px;
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 16px; overflow: hidden;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 22px 24px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
    }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }

    /* REQUIRED: explicit container size — Pixi reads it on init */
    #scene { width: 100%; height: 540px; background: #0b0d12; }
    #scene canvas { display: block; width: 100%; height: 100%; }
  </style>
</head>
<body>
  <main class="card" aria-labelledby="title">
    <header class="card-header">
      <h1 id="title">Interactive Scene</h1>
      <p class="sub">Move the cursor over the canvas · keyboard: R to reset, Space to pause</p>
    </header>
    <div id="scene" role="img" aria-label="Interactive Pixi.js scene"></div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/pixi.js@8.6.6/dist/pixi.min.js"></script>
  <script>
    // Pixi code here (Step 3+)
  </script>
</body>
</html>
```

---

## Step 3 — Themes (dark + light) and Scene Palette

Pixi colours can be set globally (`backgroundColor`) and per object (`tint`, fill colour, `Graphics.fill`). Define a palette object so themes swap in one line.

### Theme token reference

| Token | Dark | Light |
|---|---|---|
| Page background | `#0f1117` | `#f8fafc` |
| Card background | `#1a1d27` | `#ffffff` |
| Border | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` |
| Text | `#e2e8f0` | `#1e293b` |
| Muted | `#94a3b8` | `#475569` |
| Accent | `#6366f1` | `#6366f1` |
| Scene background | `0x0b0d12` | `0xf1f5f9` |
| Particle base    | `0x6366f1` | `0x6366f1` |
| Particle warm    | `0xec4899` | `0xec4899` |
| Particle cool    | `0x06b6d4` | `0x06b6d4` |

```javascript
const THEMES = {
  dark: {
    bg:        0x0b0d12,
    accent:    0x6366f1,
    accentAlt: 0xec4899,
    cool:      0x06b6d4,
    text:      0xe2e8f0,
    muted:     0x64748b,
  },
  light: {
    bg:        0xf1f5f9,
    accent:    0x6366f1,
    accentAlt: 0xec4899,
    cool:      0x0e7490,
    text:      0x1e293b,
    muted:     0x475569,
  },
};

let current = THEMES.dark;

function applyTheme(t) {
  current = t;
  app.renderer.background.color = t.bg;
  // Re-tint sprites that should follow the theme
  particles.forEach(p => p.tint = t.accent);
}
```

---

## Step 4 — Application Initialisation (v8)

```javascript
const container = document.getElementById('scene');

const app = new PIXI.Application();
await app.init({
  resizeTo:        container,        // auto-resize to the container
  background:      0x0b0d12,
  backgroundAlpha: 1,
  antialias:       true,
  resolution:      Math.min(window.devicePixelRatio, 2),  // cap at 2× for perf
  autoDensity:     true,             // CSS size stays logical, canvas scales
  preference:      'webgl',          // 'webgl' | 'webgpu' (v8 supports both)
});
container.appendChild(app.canvas);   // v8: `app.canvas` (was `app.view` in v7)

// Re-layout if the container changes size after init
const ro = new ResizeObserver(() => app.renderer.resize(container.clientWidth, container.clientHeight));
ro.observe(container);
```

> **Critical:** v8's `Application.init()` is async. Wrap your bootstrap in an `async` IIFE: `(async () => { await app.init({…}); /* setup */ })();`

---

## Step 5 — Sprites & Textures

```javascript
// Load a texture from a URL
const tex = await PIXI.Assets.load('https://pixijs.com/assets/bunny.png');

const sprite = new PIXI.Sprite(tex);
sprite.x = 200;            sprite.y = 150;
sprite.anchor.set(0.5);     // pivot at sprite centre
sprite.scale.set(1.5);
sprite.rotation = Math.PI / 6;
sprite.alpha = 0.9;
sprite.tint  = 0x6366f1;    // multiply the texture by this colour
app.stage.addChild(sprite);

// Procedural texture from a Graphics object — useful for particles
const g = new PIXI.Graphics()
  .circle(0, 0, 8)
  .fill({ color: 0xffffff });
const circleTex = app.renderer.generateTexture(g);
const dot = new PIXI.Sprite(circleTex);
dot.tint = 0x6366f1;

// Pre-load multiple assets with progress
PIXI.Assets.add({ alias: 'hero', src: '/hero.png' });
PIXI.Assets.add({ alias: 'tile', src: '/tile.png' });
const bundle = await PIXI.Assets.load(['hero', 'tile'], (p) => {
  loadingBar.style.width = (p * 100) + '%';
});
```

---

## Step 6 — Graphics API (Shapes, Lines, Fills)

`Graphics` in v8 uses a fluent, declarative API. Define a shape, then call `.fill()` or `.stroke()`.

```javascript
const g = new PIXI.Graphics();

// Rectangle
g.rect(20, 20, 200, 80)
 .fill({ color: 0x6366f1, alpha: 0.8 });

// Rounded rectangle
g.roundRect(250, 20, 200, 80, 12)
 .fill(0x1e2130)
 .stroke({ color: 0x6366f1, width: 2 });

// Circle
g.circle(120, 200, 60)
 .fill({ color: 0xec4899, alpha: 0.7 });

// Ellipse
g.ellipse(320, 200, 80, 40)
 .fill(0x06b6d4);

// Line / polyline
g.moveTo(40, 320).lineTo(200, 280).lineTo(360, 340)
 .stroke({ color: 0xe2e8f0, width: 2, alpha: 0.6, cap: 'round', join: 'round' });

// Polygon
g.poly([400, 200, 520, 260, 480, 360, 360, 320])
 .fill({ color: 0xf97316, alpha: 0.5 })
 .stroke({ color: 0xf97316, width: 2 });

// Arc / pie wedge
g.moveTo(600, 200)
 .arc(600, 200, 60, 0, Math.PI * 1.5)
 .lineTo(600, 200)
 .fill({ color: 0x22c55e, alpha: 0.6 });

// Bezier curve
g.moveTo(40, 420)
 .bezierCurveTo(120, 360, 240, 480, 360, 420)
 .stroke({ color: 0x818cf8, width: 3 });

app.stage.addChild(g);
```

---

## Step 7 — Container Hierarchy

Use containers to group, transform, and reorder objects. Transforms (position, rotation, scale, alpha) cascade to children.

```javascript
const world = new PIXI.Container();
app.stage.addChild(world);

const enemies = new PIXI.Container();
const player  = new PIXI.Container();
const ui      = new PIXI.Container();

world.addChild(enemies, player);
app.stage.addChild(ui);   // UI is on the stage, not in world — stays put when world scrolls

// Pan the world by moving its container
world.x = -camera.x;
world.y = -camera.y;

// Sort children by zIndex (per container)
world.sortableChildren = true;
sprite.zIndex = 5;

// Remove and destroy
const child = container.removeChildAt(0);
child.destroy({ children: true, texture: false });
```

---

## Step 8 — Ticker (Animation Loop)

Pixi has a built-in delta-aware ticker — never set up your own `requestAnimationFrame` when using Pixi.

```javascript
app.ticker.add((ticker) => {
  // ticker.deltaTime — frames since last tick (1 ≈ 60 fps)
  // ticker.deltaMS   — milliseconds since last tick
  // ticker.FPS       — measured frames per second
  // ticker.lastTime  — high-res timestamp

  sprite.rotation += 0.02 * ticker.deltaTime;
  sprite.x += velocity.x * ticker.deltaTime;
  sprite.y += velocity.y * ticker.deltaTime;
});

// Pause / resume
app.ticker.stop();
app.ticker.start();

// One-off / removable callbacks
const cb = (t) => {/* … */};
app.ticker.add(cb);
app.ticker.remove(cb);

// Cap framerate (useful for battery)
app.ticker.maxFPS = 30;
```

---

## Step 9 — Interaction (`eventMode: 'static'`)

v8 replaced `interactive: true` with explicit `eventMode` values:

| Mode | Use when |
|---|---|
| `'none'`     | Never receive events — fastest |
| `'passive'`  | Receive events, but only inside `hitArea` (default for Container) |
| `'auto'`     | Receive events only if ancestor has events enabled |
| `'static'`   | Always receive events at this object (best for buttons, fixed UI) |
| `'dynamic'`  | Receive events even when moving (best for game entities) |

```javascript
const btn = new PIXI.Graphics()
  .roundRect(0, 0, 160, 44, 10)
  .fill(0x6366f1);
btn.eventMode = 'static';
btn.cursor    = 'pointer';
btn.hitArea   = new PIXI.Rectangle(0, 0, 160, 44);   // explicit hit area

btn.on('pointerover',  (e) => btn.tint = 0x818cf8);
btn.on('pointerout',   (e) => btn.tint = 0xffffff);
btn.on('pointerdown',  (e) => btn.scale.set(0.96));
btn.on('pointerup',    (e) => btn.scale.set(1));
btn.on('pointertap',   (e) => console.log('Clicked at', e.global.x, e.global.y));

// Drag-and-drop pattern
let dragTarget = null;
sprite.eventMode = 'static';
sprite.cursor = 'grab';
sprite.on('pointerdown', (e) => { dragTarget = sprite; sprite.alpha = 0.7; });
app.stage.eventMode = 'static';
app.stage.hitArea   = app.screen;
app.stage.on('pointermove', (e) => {
  if (dragTarget) dragTarget.position.copyFrom(e.global);
});
app.stage.on('pointerup',     () => { if (dragTarget) { dragTarget.alpha = 1; dragTarget = null; } });
app.stage.on('pointerupoutside', () => { if (dragTarget) { dragTarget.alpha = 1; dragTarget = null; } });

// Global pointer tracking (no target required)
const pointer = { x: 0, y: 0 };
app.stage.on('globalpointermove', (e) => { pointer.x = e.global.x; pointer.y = e.global.y; });
```

---

## Step 10 — Particle Container (thousands of sprites)

`ParticleContainer` batches identical-texture sprites into a single GPU draw call — the right choice when you have > 1 000 things on screen.

```javascript
// 1. Create a texture once (procedural or loaded)
const dotTex = (() => {
  const g = new PIXI.Graphics().circle(0, 0, 6).fill(0xffffff);
  return app.renderer.generateTexture(g);
})();

// 2. Create the particle container
const particles = new PIXI.ParticleContainer({
  dynamicProperties: {
    position: true,   // particles move
    scale:    true,   // particles resize
    rotation: false,  // skip — not used
    color:    true,   // tint changes
  },
});
app.stage.addChild(particles);

// 3. Build particles — use PIXI.Particle, not PIXI.Sprite
const COUNT = 4000;
const particleList = [];
for (let i = 0; i < COUNT; i++) {
  const p = new PIXI.Particle({
    texture: dotTex,
    x: Math.random() * app.screen.width,
    y: Math.random() * app.screen.height,
    scaleX: 0.5 + Math.random() * 0.8,
    scaleY: 0.5 + Math.random() * 0.8,
    tint:   0x6366f1,
    anchorX: 0.5, anchorY: 0.5,
  });
  // Custom fields are fine — they live on the particle
  p.vx = (Math.random() - 0.5) * 1.2;
  p.vy = (Math.random() - 0.5) * 1.2;
  particles.addParticle(p);
  particleList.push(p);
}

// 4. Update in the ticker — direct field mutation, no transform tree
app.ticker.add((ticker) => {
  const dt = ticker.deltaTime;
  for (let i = 0; i < particleList.length; i++) {
    const p = particleList[i];
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    if (p.x < 0 || p.x > app.screen.width)  p.vx *= -1;
    if (p.y < 0 || p.y > app.screen.height) p.vy *= -1;
  }
});
```

> **Performance:** flag only the properties you actually mutate in `dynamicProperties`. Static fields skip per-frame upload to the GPU.

---

## Step 11 — Text (PIXI.Text and BitmapText)

```javascript
// PIXI.Text — vector text rasterised to a texture, smooth at any size
const label = new PIXI.Text({
  text: 'Hello, Alyx',
  style: new PIXI.TextStyle({
    fontFamily: 'Segoe UI, system-ui, sans-serif',
    fontSize:   28,
    fontWeight: '600',
    fill:       0xf1f5f9,
    align:      'center',
    dropShadow: {
      color: 0x000000, alpha: 0.4, blur: 4, distance: 2, angle: Math.PI / 4,
    },
  }),
});
label.anchor.set(0.5);
label.x = app.screen.width / 2;
label.y = 40;
app.stage.addChild(label);

// Update text live (re-rasterises — costly if done every frame)
label.text = 'FPS ' + app.ticker.FPS.toFixed(0);

// PIXI.BitmapText — pre-rasterised glyphs, ideal for HUDs that update every frame
PIXI.BitmapFont.install({
  name:  'HUDFont',
  style: { fontFamily: 'ui-monospace, monospace', fontSize: 18, fill: 0xa5b4fc },
});
const hud = new PIXI.BitmapText({ text: 'FPS 60', style: { fontFamily: 'HUDFont' } });
hud.x = 12; hud.y = 12;
app.stage.addChild(hud);

// Updating BitmapText is cheap — safe to call every frame
app.ticker.add(() => { hud.text = 'FPS ' + app.ticker.FPS.toFixed(0); });
```

> **Rule:** use `PIXI.Text` for occasional labels (smooth, anti-aliased). Use `BitmapText` for HUDs, score counters, and any text that changes every frame.

---

## Step 12 — Filters (post-process effects)

```javascript
const blur = new PIXI.BlurFilter({ strength: 6, quality: 4 });
const noise = new PIXI.NoiseFilter({ noise: 0.05 });
const colorMatrix = new PIXI.ColorMatrixFilter();
colorMatrix.saturate(0.6, false);

// Apply to an object — filters cascade to children
particles.filters = [blur];
app.stage.filters = [noise, colorMatrix];

// Cap filter cost — they re-render the affected subtree
container.filterArea = new PIXI.Rectangle(0, 0, 400, 200);
```

---

## Step 13 — Design & Polish Guidelines

- **Cap `resolution` at 2** — `Math.min(devicePixelRatio, 2)` keeps Retina screens crisp without paying for 3× pixels
- **Use `ParticleContainer` once you cross ~500 sprites** — single draw call vs one per sprite
- **Generate procedural textures once** outside the loop — `app.renderer.generateTexture(graphics)` and reuse for every particle
- **Pre-allocate vectors / temp objects** outside hot loops — `new PIXI.Point()` inside a 60 fps tick allocates 3 600 objects/min and triggers GC pauses
- **Use `BitmapText` for live counters** — `PIXI.Text` re-uploads a texture on every `.text =`
- **Hardware acceleration check** — Pixi falls back to Canvas-2D silently when WebGL is unavailable. Test with `app.renderer.type === PIXI.RendererType.WEBGL`
- **Pause when hidden** — `document.addEventListener('visibilitychange', () => document.hidden ? app.ticker.stop() : app.ticker.start())` saves battery
- **Destroy on unmount** — `app.destroy({ removeView: true }, { children: true, texture: true })` to free GPU memory if you remount
- **Accessibility** — Pixi paints to a canvas, which screen readers cannot inspect. Always provide `role="img"` + `aria-label` on the container, and ensure essential information is also rendered as HTML outside the canvas
- **Colour contrast** — when overlaying HUD text on the scene, give the text a subtle drop-shadow or backing panel; thin glyphs against busy particles vanish
- **Keyboard support** — Pixi does not implement keyboard navigation. Attach DOM listeners (`window.addEventListener('keydown', …)`) and act on Pixi state

---

## Step 14 — Complete Example: Interactive Particle Field

A cursor-reactive particle field where each particle is gently attracted to the mouse, with HUD, theme toggle, and pause control.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particle Field</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117; color: #e2e8f0;
      display: flex; flex-direction: column; align-items: center;
      min-height: 100vh; padding: 24px;
    }
    .card {
      width: 100%; max-width: 1000px;
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 16px; overflow: hidden;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 20px 24px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;
    }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }

    .actions { display: flex; gap: 8px; }
    .btn {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1);
      color: #e2e8f0; border-radius: 8px;
      padding: 7px 14px; font-size: 12px; font-weight: 500;
      font-family: inherit; cursor: pointer; transition: all 0.15s;
    }
    .btn:hover  { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.18); }
    .btn:active { transform: scale(0.97); }

    #scene {
      position: relative;
      width: 100%; height: 560px;
      background: #0b0d12;
      overflow: hidden;
    }
    #scene canvas { display: block; }

    .hud {
      position: absolute; top: 14px; left: 14px;
      padding: 8px 14px;
      background: rgba(15,17,23,0.6);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 10px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 11.5px; color: #94a3b8;
      pointer-events: none;
      font-variant-numeric: tabular-nums;
    }
    .hud strong { color: #a5b4fc; font-weight: 600; }
  </style>
</head>
<body>
  <main class="card" aria-labelledby="title">
    <header class="card-header">
      <div>
        <h1 id="title">Particle Field</h1>
        <p class="sub">Move the cursor over the canvas · Space to pause · T to toggle theme · R to reset</p>
      </div>
      <div class="actions">
        <button class="btn" id="themeBtn"  aria-pressed="false">Light theme</button>
        <button class="btn" id="pauseBtn"  aria-pressed="false">Pause</button>
        <button class="btn" id="resetBtn">Reset</button>
      </div>
    </header>

    <div id="scene" role="img" aria-label="Interactive particle field that follows the mouse cursor">
      <div class="hud" id="hud" aria-live="off">
        <strong>FPS</strong> 60 · <strong>PARTICLES</strong> 4000 · <strong>MODE</strong> attract
      </div>
    </div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/pixi.js@8.6.6/dist/pixi.min.js"></script>
  <script>
    (async () => {
      const THEMES = {
        dark: { bg: 0x0b0d12, palette: [0x6366f1, 0x818cf8, 0xec4899, 0x06b6d4] },
        light:{ bg: 0xf1f5f9, palette: [0x4338ca, 0x6366f1, 0xbe185d, 0x0e7490] },
      };
      let theme = THEMES.dark;

      const sceneEl = document.getElementById('scene');
      const hudEl   = document.getElementById('hud');

      const app = new PIXI.Application();
      await app.init({
        resizeTo:    sceneEl,
        background:  theme.bg,
        antialias:   true,
        resolution:  Math.min(window.devicePixelRatio, 2),
        autoDensity: true,
      });
      sceneEl.appendChild(app.canvas);

      // Procedural circle texture for every particle
      const dotTex = (() => {
        const g = new PIXI.Graphics()
          .circle(0, 0, 6).fill({ color: 0xffffff, alpha: 0.95 });
        return app.renderer.generateTexture(g);
      })();

      const container = new PIXI.ParticleContainer({
        dynamicProperties: { position: true, scale: true, color: true, rotation: false },
      });
      app.stage.addChild(container);

      const COUNT  = 4000;
      const list   = [];
      const pointer = { x: app.screen.width / 2, y: app.screen.height / 2, active: false };

      function spawn() {
        for (let i = list.length - 1; i >= 0; i--) container.removeParticle(list[i]);
        list.length = 0;
        for (let i = 0; i < COUNT; i++) {
          const p = new PIXI.Particle({
            texture: dotTex,
            x: Math.random() * app.screen.width,
            y: Math.random() * app.screen.height,
            scaleX: 0.25 + Math.random() * 0.55,
            scaleY: 0.25 + Math.random() * 0.55,
            tint:   theme.palette[i % theme.palette.length],
            anchorX: 0.5, anchorY: 0.5,
          });
          p.vx = (Math.random() - 0.5) * 0.4;
          p.vy = (Math.random() - 0.5) * 0.4;
          p.baseScale = p.scaleX;
          container.addParticle(p);
          list.push(p);
        }
      }
      spawn();

      // Mouse / touch tracking on the stage
      app.stage.eventMode = 'static';
      app.stage.hitArea   = app.screen;
      app.stage.on('globalpointermove', (e) => {
        pointer.x = e.global.x; pointer.y = e.global.y; pointer.active = true;
      });
      sceneEl.addEventListener('pointerleave', () => { pointer.active = false; });

      // FPS HUD update — throttled to 4×/s
      let hudAcc = 0;
      app.ticker.add((ticker) => {
        const dt = ticker.deltaTime;

        // Update particles — gentle attraction to pointer when active
        const px = pointer.x, py = pointer.y;
        const W  = app.screen.width, H = app.screen.height;
        for (let i = 0; i < list.length; i++) {
          const p = list[i];
          if (pointer.active) {
            const dx = px - p.x, dy = py - p.y;
            const d2 = dx * dx + dy * dy + 50;
            const f  = 6 / d2;
            p.vx += dx * f * dt;
            p.vy += dy * f * dt;
          }
          // Damping + integration
          p.vx *= 0.97;
          p.vy *= 0.97;
          p.x  += p.vx * dt;
          p.y  += p.vy * dt;

          // Soft wall bounce
          if (p.x < 0)  { p.x = 0;  p.vx *= -0.6; }
          if (p.x > W)  { p.x = W;  p.vx *= -0.6; }
          if (p.y < 0)  { p.y = 0;  p.vy *= -0.6; }
          if (p.y > H)  { p.y = H;  p.vy *= -0.6; }

          // Speed-modulated scale for a subtle "alive" effect
          const speed = Math.hypot(p.vx, p.vy);
          const s = p.baseScale * (1 + Math.min(speed * 0.5, 1.2));
          p.scaleX = s; p.scaleY = s;
        }

        // HUD throttle
        hudAcc += ticker.deltaMS;
        if (hudAcc > 250) {
          hudAcc = 0;
          hudEl.innerHTML =
            `<strong>FPS</strong> ${app.ticker.FPS.toFixed(0)} · ` +
            `<strong>PARTICLES</strong> ${list.length} · ` +
            `<strong>MODE</strong> ${pointer.active ? 'attract' : 'drift'}`;
        }
      });

      // Controls
      const pauseBtn = document.getElementById('pauseBtn');
      const themeBtn = document.getElementById('themeBtn');
      const resetBtn = document.getElementById('resetBtn');

      let paused = false;
      function togglePause() {
        paused = !paused;
        paused ? app.ticker.stop() : app.ticker.start();
        pauseBtn.textContent = paused ? 'Resume' : 'Pause';
        pauseBtn.setAttribute('aria-pressed', String(paused));
      }
      pauseBtn.addEventListener('click', togglePause);

      let dark = true;
      function toggleTheme() {
        dark = !dark;
        theme = dark ? THEMES.dark : THEMES.light;
        app.renderer.background.color = theme.bg;
        sceneEl.style.background = '#' + theme.bg.toString(16).padStart(6, '0');
        list.forEach((p, i) => p.tint = theme.palette[i % theme.palette.length]);
        themeBtn.textContent = dark ? 'Light theme' : 'Dark theme';
        themeBtn.setAttribute('aria-pressed', String(!dark));
      }
      themeBtn.addEventListener('click', toggleTheme);

      resetBtn.addEventListener('click', spawn);

      // Keyboard shortcuts
      window.addEventListener('keydown', (e) => {
        if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
        if (e.code === 'Space') { e.preventDefault(); togglePause(); }
        if (e.code === 'KeyT')  { toggleTheme(); }
        if (e.code === 'KeyR')  { spawn(); }
      });

      // Pause when the tab is hidden
      document.addEventListener('visibilitychange', () => {
        if (paused) return;
        document.hidden ? app.ticker.stop() : app.ticker.start();
      });
    })();
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **`new PIXI.Application({…})` without `await app.init({…})`** — v8 is async. The old v7 constructor signature creates an empty app with no renderer
- **Using `app.view` instead of `app.canvas`** — renamed in v8. `app.view` is undefined
- **`interactive: true`** — replaced by `eventMode: 'static'` (or `'dynamic'`). The old property is ignored silently
- **Adding 5 000 `PIXI.Sprite` to a regular `Container`** — every sprite is a draw call. Use `PIXI.ParticleContainer` + `PIXI.Particle` for batching
- **Allocating in the ticker** — `new PIXI.Point()`, `new PIXI.Rectangle()`, or even `arr.push()` every frame at 60 fps causes GC pauses. Pre-allocate
- **Not capping `resolution`** — Retina screens give `devicePixelRatio = 3`; uncapped, the canvas renders 9× the pixels. Always `Math.min(devicePixelRatio, 2)`
- **Generating textures from `Graphics` every frame** — `generateTexture` is expensive. Generate once outside the loop, reuse the texture for every particle
- **Updating `PIXI.Text.text` every frame** — re-rasterises a texture on every change. Use `PIXI.BitmapText` for HUDs and counters
- **No explicit container height** — Pixi reads its parent's size on `resizeTo` init. A `height: auto` container yields a 0 px canvas
- **Forgetting `app.stage.hitArea = app.screen`** — `globalpointermove` only fires inside the hit area; without it you get no events when the cursor is over the background
- **No `role`/`aria-label` on the canvas container** — canvases are invisible to assistive tech. Always describe the scene in HTML for screen readers
- **Not destroying on unmount** — `app.destroy()` is required to release GPU textures and event listeners when you swap out the artifact
