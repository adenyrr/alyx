---
name: p5js-creative-coding
description: Create expressive, generative, and interactive 2D/3D sketches using p5.js v2, delivered as self-contained HTML artifacts. Use this skill whenever someone needs creative coding, generative art, algorithmic drawing, interactive animations, simulations, educational math/physics visualisations, particle systems, Perlin noise landscapes, fractal patterns, or any sketch where the pleasure is in the process of drawing rather than in a static result. Trigger on requests like "generate abstract art", "make a particle simulation", "draw a fractal", "animate this mathematical concept", "create a generative pattern", "build an interactive drawing tool", or any prompt that combines creativity, code, and animation. Do NOT use for data charts (→ charting skill), 3D scenes with complex lighting and models (→ threejs-3d skill), or static SVG diagrams (→ mermaid-diagrams skill).
---

# p5.js Creative Coding Skill — v2

p5.js is a JavaScript library that re-imagines Processing for the web. It provides a simple, expressive API for drawing, animating, and interacting — a blank canvas that runs at 60 fps. p5.js v2 is the current major version (CDN: `p5@2.x`), with improved async support and WebGPU readiness.

---

## Artifact Presentation & Use Cases

Every p5.js artifact is a self-contained HTML page. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport — the canvas typically covers the full window
- **Canvas element** created by `createCanvas()` — p5.js manages it automatically
- **Optional HUD overlay** (fixed-position, translucent) for interaction hints or controls
- **Optional card wrapper** (`#1a1d27`) for smaller, contained sketches
- **60 fps draw loop** runs continuously, creating smooth animation

### Typical use cases

- **Generative art** — algorithmic patterns, Perlin noise landscapes, fractal trees, mandalas
- **Particle systems** — flow fields, flocking simulations, explosions, rain/snow effects
- **Interactive drawing tools** — paint programs, procedural brushes, sketch pads
- **Math/physics visualizations** — pendulums, wave interference, Lorenz attractors, orbital mechanics
- **Educational animations** — sorting algorithms, pathfinding, cellular automata, signal processing
- **Creative toys** — interactive musical visualizers, sound-reactive patterns, mouse-following art

### What the user sees

A living canvas: shapes emerge, particles flow, patterns evolve in real time. Mouse interaction affects the scene — hover creates ripples, clicks spawn elements, drag leaves trails. The dark background provides clean contrast for colorful generative output.

---

## When to Use p5.js vs. Alternatives

| Use p5.js when… | Use another library when… |
|---|---|
| Generative art, algorithmic drawing | 3D scenes with lighting, models → **Three.js** |
| 2D particle systems, simulations | Data charts (bar, line, pie) → **Chart.js / Plotly** |
| Educational math/physics animations | DOM/SVG choreographed animations → **Anime.js** |
| Interactive drawing/painting tools | Geographic maps → **Leaflet** |
| Creative coding explorations | Diagrams (flowcharts, sequences) → **Mermaid** |
| Perlin noise, fractals, cellular automata | Interactive data tables → **Tabulator** |
| Quick prototypes with `setup()`/`draw()` | Scroll-driven storytelling → **GSAP** |

> **Rule of thumb:** if the output is visual art, a simulation, or an interactive canvas experience driven by a draw loop, use p5.js. For structured data or UI components, use a purpose-built library.

---

## Step 1 — CDN Setup

p5.js is a single script file. No CSS required, no import maps.

```html
<!-- p5.js v2 — stable release -->
<script src="https://cdn.jsdelivr.net/npm/p5@2.2.2/lib/p5.min.js"></script>

<!-- Or: p5.js v1 — legacy stable (still widely used) -->
<script src="https://cdn.jsdelivr.net/npm/p5@1.11.3/lib/p5.min.js"></script>
```

**v1 vs v2:**
| | p5.js v1 | p5.js v2 |
|---|---|---|
| CDN | `p5@1.11.3` | `p5@2.2.2` |
| Async setup | No | Yes (`async function setup()`) |
| WebGPU | No | Yes (with `p5.webgpu.js` addon) |
| API | Stable, widely documented | Mostly compatible, some breaking changes |
| Recommended for | Existing sketches, tutorials | New projects |

Use **v2 for new projects**, v1 if following existing tutorials or examples that haven't been updated.

---

## Step 2 — Two Programming Modes

### Global mode (simpler — functions in global scope)
```html
<script src="https://cdn.jsdelivr.net/npm/p5@2.2.2/lib/p5.min.js"></script>
<script>
  function setup() {
    createCanvas(800, 600);   // creates and attaches canvas
  }
  function draw() {
    background(15, 17, 23);   // clears canvas each frame
    // drawing commands here
  }
</script>
```

### Instance mode (isolated — no global pollution, multiple sketches)
```html
<script src="https://cdn.jsdelivr.net/npm/p5@2.2.2/lib/p5.min.js"></script>
<script>
  const sketch = (p) => {
    p.setup = () => {
      p.createCanvas(800, 600);
    };
    p.draw = () => {
      p.background(15, 17, 23);
      p.circle(p.mouseX, p.mouseY, 40);
    };
  };
  new p5(sketch, document.getElementById('canvas-container'));
</script>
```

**Use global mode for standalone artifacts (simpler). Use instance mode when embedding multiple sketches in one page, or when integrating with other frameworks.**

---

## Step 3 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sketch</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0f1117;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      font-family: 'Segoe UI', sans-serif;
      overflow: hidden;
    }
    /* p5 appends canvas to body — style it here */
    canvas {
      display: block;
      border-radius: 12px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.6);
    }
    /* Optional caption below canvas */
    #caption {
      margin-top: 14px;
      color: #475569;
      font-size: 12px;
      letter-spacing: 0.04em;
    }
  </style>
</head>
<body>
  <div id="caption">Move mouse to interact · Click to reset</div>

  <script src="https://cdn.jsdelivr.net/npm/p5@2.2.2/lib/p5.min.js"></script>
  <script>
    function setup() {
      const cnv = createCanvas(800, 600);
      cnv.parent(document.body);  // explicit parent (cleaner than default)
      colorMode(HSB, 360, 100, 100, 100);  // or RGB (default)
      frameRate(60);
    }

    function draw() {
      background(220, 15, 9, 20);  // dark with low alpha = trail effect
      // drawing commands here
    }

    // Resize canvas to window (fullscreen sketches)
    // function windowResized() {
    //   resizeCanvas(windowWidth, windowHeight);
    // }
  </script>
</body>
</html>
```

---

## Step 4 — The Draw Loop

p5.js runs `setup()` once, then calls `draw()` in a loop at the target frame rate (default 60 fps).

```javascript
function setup() {
  createCanvas(800, 600);  // canvas dimensions
  // background(0);         // in setup = only drawn once (leave trails)
}

function draw() {
  background(15, 17, 23);  // in draw = redraws each frame (clean animation)

  // frameCount: total frames elapsed since start
  // millis():   milliseconds since start
  // frameRate():actual FPS (call with no args to read)
  // frameRate(30): set target FPS
}

// Pause / resume
noLoop();    // stop the draw loop
loop();      // resume it
redraw();    // trigger one more frame while paused
```

**Trail effect:** calling `background()` with a 4th argument (alpha) in draw creates a fade-out trail:
```javascript
background(15, 17, 23, 20);  // RGBA: near-transparent background each frame → ghost trails
```

---

## Step 5 — Colour System

```javascript
// Default: RGB mode
background(15, 17, 23);            // r, g, b
background(15, 17, 23, 200);       // r, g, b, alpha (0–255)
background('#0f1117');              // hex string
background(128);                   // grayscale

fill(99, 102, 241);                 // r, g, b
fill(99, 102, 241, 180);            // with alpha
fill('#6366f1');
noFill();                           // transparent fill

stroke(148, 163, 184);             // outline color
strokeWeight(2);                   // outline width in pixels
noStroke();                        // no outline

// HSB mode (much more intuitive for generative art)
colorMode(HSB, 360, 100, 100, 100); // hue 0–360, saturation 0–100, brightness 0–100, alpha 0–100
background(220, 80, 9);             // dark blue-ish
fill(280, 80, 90, 80);              // purple, 80% alpha
stroke(300 + sin(frameCount * 0.02) * 60, 90, 95); // animated hue

// Interpolate between colors
const c1 = color(99, 102, 241);
const c2 = color(236, 72, 153);
const mid = lerpColor(c1, c2, 0.5);  // 0 = c1, 1 = c2
fill(mid);
```

---

## Step 6 — Shapes

```javascript
// 2D primitives
point(x, y);
line(x1, y1, x2, y2);
rect(x, y, w, h);                  // top-left corner by default
rect(x, y, w, h, r);               // uniform rounded corners
rect(x, y, w, h, tl, tr, br, bl); // per-corner radius
ellipse(x, y, w, h);               // center by default
circle(x, y, d);                   // shorthand ellipse with equal w/h
triangle(x1,y1, x2,y2, x3,y3);
quad(x1,y1, x2,y2, x3,y3, x4,y4);
arc(x, y, w, h, start, stop);     // angles in radians (or use degrees() + angleMode(DEGREES))
arc(x, y, w, h, start, stop, PIE);      // pie slice
arc(x, y, w, h, start, stop, CHORD);   // chord

// Custom shapes — beginShape / endShape
beginShape();
  vertex(x1, y1);
  vertex(x2, y2);
  vertex(x3, y3);
  // curveVertex(x, y);   Catmull-Rom spline
  // bezierVertex(cp1x, cp1y, cp2x, cp2y, x, y);  cubic Bézier
endShape(CLOSE);  // CLOSE connects last to first vertex

// Text
textSize(24);
textAlign(CENTER, CENTER);  // horizontal: LEFT|CENTER|RIGHT, vertical: TOP|CENTER|BOTTOM|BASELINE
textStyle(BOLD);            // NORMAL | ITALIC | BOLD | BOLDITALIC
text('Hello World', x, y);
text('Multiline\nText', x, y, maxWidth, maxHeight);

// Alignment modes (affect rect and ellipse position)
rectMode(CENTER);      // x,y = center (default is CORNER)
ellipseMode(CORNER);   // x,y = top-left corner (default is CENTER)
```

---

## Step 7 — Transforms

p5.js uses a state machine for transforms. Use `push()` / `pop()` to isolate them.

```javascript
push();                        // save current transform + style state
  translate(200, 300);         // move origin to (200, 300)
  rotate(PI / 4);              // rotate 45° around new origin
  scale(2);                    // scale by 2
  rect(0, 0, 50, 50);          // drawn at transformed position
pop();                         // restore saved state

// Chaining transforms accumulate:
translate(width / 2, height / 2);   // move origin to center
rotate(frameCount * 0.01);           // rotate each frame

// Angle modes
angleMode(RADIANS);   // default — use PI, TWO_PI, HALF_PI
angleMode(DEGREES);   // 0–360
```

---

## Step 8 — Perlin Noise

`noise()` generates smooth, organic pseudo-randomness (0.0–1.0). Unlike `random()`, adjacent calls return similar values — ideal for flowing motion, terrain, textures.

```javascript
// 1D noise — smooth signal over time
let t = 0;
function draw() {
  const n = noise(t);       // 0.0–1.0
  const y = map(n, 0, 1, 0, height);
  circle(width / 2, y, 20);
  t += 0.01;                // increment slowly for smooth motion
}

// 2D noise — spatial texture (terrain, clouds)
for (let x = 0; x < cols; x++) {
  for (let y = 0; y < rows; y++) {
    const n = noise(x * 0.05, y * 0.05);   // scale down for smoother result
    fill(map(n, 0, 1, 0, 255));
    rect(x * cellSize, y * cellSize, cellSize, cellSize);
  }
}

// 3D noise — 2D texture animated over time
let zOff = 0;
function draw() {
  let xOff = 0;
  for (let x = 0; x < cols; x++) {
    let yOff = 0;
    for (let y = 0; y < rows; y++) {
      const n = noise(xOff, yOff, zOff);   // 3rd arg = time slice
      // use n...
      yOff += 0.05;
    }
    xOff += 0.05;
  }
  zOff += 0.005;   // animate slowly
}

// Flow field — noise as vector angles
function draw() {
  for (let x = 0; x < width; x += 10) {
    for (let y = 0; y < height; y += 10) {
      const angle = noise(x * 0.003, y * 0.003, frameCount * 0.003) * TWO_PI * 2;
      const v = p5.Vector.fromAngle(angle, 5);
      push();
        translate(x, y);
        rotate(angle);
        line(0, 0, 5, 0);
      pop();
    }
  }
}

// Noise tuning
noiseSeed(42);          // reproducible results
noiseDetail(4, 0.5);   // octaves (more = detail), falloff (less = smoother)
```

---

## Step 9 — Math & Vectors

```javascript
// map — re-range a value (essential function in p5)
const y = map(mouseX, 0, width, 0, height);     // mouseX in 0–width → 0–height
const v = map(sin(t), -1, 1, 50, 200);          // sine wave → 50–200

// constrain
const clamped = constrain(mouseX, 0, 400);       // clamp to [0, 400]

// lerp — linear interpolation
const x = lerp(start, end, 0.1);                 // move 10% toward end each frame (easing)

// Trig
sin(angle), cos(angle), tan(angle)               // input in radians by default
atan2(y, x)                                      // angle of a vector (radians)
degrees(radians), radians(degrees)               // convert

// dist
const d = dist(x1, y1, x2, y2);                 // 2D distance

// p5.Vector — 2D/3D vector math
const v = createVector(3, 4);
v.add(createVector(1, 0));
v.normalize();                                   // unit vector (length 1)
v.mult(speed);                                   // scale
v.limit(maxSpeed);                               // cap magnitude
v.heading();                                     // angle of vector (radians)
const angle = p5.Vector.angleBetween(v1, v2);

// Random
random(0, 100);                                  // float in [0, 100)
random(['red', 'blue', 'green']);                // random element from array
int(random(10));                                 // random int 0–9
randomGaussian(mean, sd);                        // Gaussian distribution
randomSeed(42);                                  // reproducible random
```

---

## Step 10 — Input & Events

```javascript
// ── Mouse ──────────────────────────────────────────────────────
// System variables (update automatically each frame)
mouseX, mouseY         // current mouse position relative to canvas
pmouseX, pmouseY       // previous frame position (→ velocity = mouseX - pmouseX)
mouseIsPressed         // boolean, true while any button held
mouseButton            // LEFT | RIGHT | CENTER

// Event functions (called once per event)
function mousePressed()  { }   // button down
function mouseReleased() { }   // button up
function mouseClicked()  { }   // complete click (down + up)
function mouseMoved()    { }   // move without button
function mouseDragged()  { }   // move with button held
function mouseWheel(event) {   // scroll
  const delta = event.delta;   // positive = down, negative = up
}

// ── Keyboard ──────────────────────────────────────────────────
key         // last key pressed as string ('a', ' ', 'Enter'…)
keyCode     // last key as code (UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW, BACKSPACE, DELETE, ENTER, ESCAPE, SHIFT, CONTROL, ALT, TAB)
keyIsPressed  // boolean

function keyPressed()  { }
function keyReleased() { }
function keyIsDown(keyCode) { }  // check specific key in draw()

// ── Touch ────────────────────────────────────────────────────
touches         // array of {x, y, id} for each touch point
touchStarted()  // first touch
touchMoved()    // drag
touchEnded()    // lift
```

---

## Step 11 — WEBGL Mode (3D)

```javascript
function setup() {
  createCanvas(800, 600, WEBGL);   // add WEBGL as third argument
  // Origin is now at CENTER of canvas (not top-left corner)
}

function draw() {
  background(15, 17, 23);
  orbitControl();                  // add mouse orbit in WEBGL mode

  // Lights
  ambientLight(60);
  directionalLight(255, 255, 255, 0.5, -0.5, -1);
  pointLight(100, 150, 255, 200, -100, 200);

  // 3D primitives (all centered at origin)
  box(100, 80, 60);                  // width, height, depth
  sphere(80, 32, 32);               // radius, detailX, detailY
  cylinder(50, 150);                // radius, height
  cone(60, 120);
  torus(100, 30);
  plane(300, 200);                   // flat plane

  // Materials
  ambientMaterial(99, 102, 241);     // uniform lit color
  specularMaterial(255, 255, 255);   // shiny highlights
  shininess(100);
  emissiveMaterial(30, 0, 80);       // self-illuminating

  // 3D transforms (same push/pop pattern)
  push();
    translate(0, -100, 0);
    rotateX(frameCount * 0.01);
    rotateY(frameCount * 0.02);
    box(60);
  pop();

  // Camera control (manual, overrides orbitControl)
  camera(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ);
  perspective(fov, aspect, near, far);
}
```

> **WEBGL coordinate system:** origin at canvas center, Y axis points **up** (opposite of 2D mode). In 2D, `y` increases downward; in WEBGL, `y` increases upward.

---

## Step 12 — Pixel Manipulation

```javascript
// Save pixel array to memory
loadPixels();
for (let x = 0; x < width; x++) {
  for (let y = 0; y < height; y++) {
    const i = (x + y * width) * 4;   // RGBA index
    pixels[i]     = 255;              // R
    pixels[i + 1] = 0;               // G
    pixels[i + 2] = 128;             // B
    pixels[i + 3] = 255;             // A
  }
}
updatePixels();   // write back to canvas

// Read a pixel color
loadPixels();
const r = pixels[(x + y * width) * 4];

// get() — read pixel(s) as color or p5.Image
const col = get(mouseX, mouseY);   // color at mouse
const img = get(x, y, w, h);       // sub-region as p5.Image

// set() — write pixels without loadPixels/updatePixels overhead for small operations
set(x, y, color(255, 0, 0));
updatePixels();
```

---

## Step 13 — Design & Polish Guidelines

- **Dark background** — `background(15, 17, 23)` matches `#0f1117`; call it in `draw()` to clear each frame, or omit for trail effects
- **Color modes** — use `colorMode(HSB, 360, 100, 100, 100)` for intuitive color manipulation; HSB makes gradients, rainbows, and palettes much easier
- **Frame rate** — `frameRate(60)` is default; lower to 30 for complex scenes, or use `noLoop()` + `redraw()` for event-driven sketches
- **Responsive canvas** — always add `function windowResized() { resizeCanvas(windowWidth, windowHeight); }` for fullscreen sketches
- **Noise seed** — call `noiseSeed(42)` in `setup()` for reproducible Perlin noise patterns; change the seed for variation
- **Performance** — for 10K+ particles, avoid `fill()`/`stroke()` per particle; use `loadPixels()` → write to `pixels[]` → `updatePixels()` for raw pixel access
- **Alpha trails** — instead of clearing with `background()`, use `background(15, 17, 23, 20)` for a fading trail effect (the alpha value controls trail length)
- **Mouse interaction** — `mouseX`/`mouseY` are always available; use `dist(mouseX, mouseY, x, y)` for distance-based effects
- **Instance mode** — for embedding alongside other content, use `new p5(sketch, containerElement)` to avoid global namespace conflicts
- **Accessibility** — call `describe('Description of the visual')` in `setup()` for screen reader support

---

## Step 14 — Complete Example: Flow Field Particles

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flow Field</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #0f1117; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
    canvas { border-radius: 12px; box-shadow: 0 8px 40px rgba(0,0,0,0.7); }
    #info { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); color: #475569; font-size: 12px; font-family: 'Segoe UI', sans-serif; pointer-events: none; }
  </style>
</head>
<body>
  <div id="info">Click to clear · Move mouse to interact</div>

  <script src="https://cdn.jsdelivr.net/npm/p5@2.2.2/lib/p5.min.js"></script>
  <script>
    const W = 900, H = 600;
    const COLS = 60, ROWS = 40;
    const CELL_W = W / COLS, CELL_H = H / ROWS;
    const NUM_PARTICLES = 600;

    let field = [];       // angle at each grid cell
    let particles = [];
    let zOff = 0;

    function setup() {
      const cnv = createCanvas(W, H);
      cnv.parent(document.body);
      colorMode(HSB, 360, 100, 100, 100);
      background(220, 20, 7);
      noiseDetail(2, 0.5);

      for (let i = 0; i < NUM_PARTICLES; i++) particles.push(new Particle());
    }

    function draw() {
      // Rebuild flow field each frame
      field = [];
      for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
          const angle = noise(col * 0.12, row * 0.12, zOff) * TWO_PI * 2.5;
          field[row * COLS + col] = angle;
        }
      }
      zOff += 0.004;

      // Draw semi-transparent background for trail
      background(220, 20, 7, 6);

      // Update & draw all particles
      for (const p of particles) {
        p.follow();
        p.update();
        p.edges();
        p.show();
      }
    }

    function mousePressed() {
      background(220, 20, 7);   // clear trails on click
    }

    class Particle {
      constructor() {
        this.reset();
        this.age = random(200);   // stagger ages
      }
      reset() {
        this.pos = createVector(random(W), random(H));
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);
        this.hue = random(180, 300);
        this.age = 0;
        this.maxAge = random(100, 250);
        this.speed = random(1.5, 3.5);
        this.weight = random(0.6, 1.8);
      }
      follow() {
        // Influence from mouse (attract/repel)
        const toMouse = createVector(mouseX - this.pos.x, mouseY - this.pos.y);
        const d = toMouse.mag();
        if (d < 120) {
          toMouse.normalize().mult(map(d, 0, 120, mouseIsPressed ? 2 : -0.8, 0));
          this.acc.add(toMouse);
        }

        // Follow flow field
        const col = floor(this.pos.x / CELL_W);
        const row = floor(this.pos.y / CELL_H);
        const idx = row * COLS + col;
        if (idx >= 0 && idx < field.length) {
          const force = p5.Vector.fromAngle(field[idx], this.speed);
          this.acc.add(force);
        }
      }
      update() {
        this.vel.add(this.acc);
        this.vel.limit(this.speed + 1);
        this.pos.add(this.vel);
        this.acc.mult(0);
        this.age++;
        if (this.age > this.maxAge) this.reset();
      }
      edges() {
        if (this.pos.x < 0) this.pos.x = W;
        if (this.pos.x > W) this.pos.x = 0;
        if (this.pos.y < 0) this.pos.y = H;
        if (this.pos.y > H) this.pos.y = 0;
      }
      show() {
        const alpha = map(this.age, 0, this.maxAge, 0, 70);
        stroke(this.hue + sin(this.age * 0.05) * 30, 75, 90, alpha);
        strokeWeight(this.weight);
        point(this.pos.x, this.pos.y);
      }
    }
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Calling `getDelta()` or time tracking inside `draw()` incorrectly** — p5.js does not have a built-in delta-time function; use `millis()` or `frameCount` for time-based animation, or track `let lastTime = millis()` manually
- **Creating objects inside `draw()`** — `createVector()`, `color()`, `createImage()` inside the draw loop allocate new objects every frame. Pre-allocate them in `setup()` or at module level and reuse them
- **Forgetting `push()` / `pop()` around transforms** — `translate()`, `rotate()`, `scale()` accumulate; without push/pop, every frame's transform stacks onto the previous, causing objects to drift or spiral out of control
- **`background()` in `setup()` only** — if you want to clear the canvas each frame, call `background()` inside `draw()`. In `setup()`, it only clears once, which is intentional only for painting-style sketches
- **WEBGL origin confusion** — in 2D, `(0,0)` is the top-left corner; in WEBGL mode, `(0,0,0)` is the center of the canvas and `y` points upward. `text()` in WEBGL also requires a preloaded font
- **`noise()` with large arguments** — `noise(x * 1.0, y * 1.0)` will be very chaotic and grid-like; scale inputs down by 0.002–0.05 for smooth, organic results
- **Multiple `colorMode()` calls without resetting** — `colorMode(HSB)` affects all color functions globally from that point forward; switching modes mid-sketch without being aware of it breaks all color values
- **`loadPixels()` / `updatePixels()` on every frame unnecessarily** — pixel manipulation is slow; call it only when needed, not every frame unless you're doing per-pixel animation
- **`mouseX` / `mouseY` are 0 before the mouse enters the canvas** — don't use them for initial placement without a conditional; use `width/2, height/2` as defaults
- **Global mode variable naming conflicts** — p5.js exposes many global names (`width`, `height`, `mouseX`, `mouseY`, `color`, `image`, `text`, `key`, `random`, `min`, `max`, `abs`…); avoid using these as your own variable names in global mode, or use instance mode instead
