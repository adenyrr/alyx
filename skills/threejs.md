---
name: threejs-3d
description: Create immersive, interactive 3D scenes and animations using Three.js r183, delivered as self-contained HTML artifacts. Use this skill whenever someone needs real-time 3D graphics in the browser: rotating objects, particle systems, procedural geometry, abstract 3D art, product visualisations, interactive 3D data visualisation, physics-like simulations, shader effects, or any scene requiring depth, lighting, and perspective. Trigger on requests like "create a 3D scene", "make a spinning object", "build a particle system", "generate 3D abstract art", "visualise data in 3D", or any prompt that evokes spatial depth and real-time rendering. Do NOT use for flat 2D canvas art (→ p5.js skill), geographic maps (→ leaflet skill), or charts and graphs (→ charting skill).
---

# Three.js 3D Skill — r183

Three.js is the leading WebGL library for real-time 3D in the browser. It abstracts away raw WebGL complexity and exposes a clean scene graph of objects, lights, cameras, and materials. Since r171, **WebGPU is fully production-ready** via `WebGPURenderer` — with automatic WebGL fallback on older browsers.

---

## Artifact Presentation & Use Cases

Every Three.js artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport — often the scene itself is fullscreen
- **WebGL canvas** renders the 3D scene, filling the card or the entire viewport
- **HUD overlay** (optional, fixed-position, translucent) shows interaction hints and controls
- **Card wrapper** (`#1a1d27`, only for non-fullscreen scenes) centers a contained 3D view
- **OrbitControls** provides drag-to-orbit, scroll-to-zoom, right-click-to-pan

### Typical use cases

- **Abstract 3D art** — particle galaxies, procedural geometry, generative landscapes
- **Product visualizations** — rotating objects with realistic materials and lighting
- **Data visualization in 3D** — 3D scatter plots, network graphs, terrain data
- **Interactive simulations** — physics demos, solar systems, architectural walkthroughs
- **Shader effects** — custom GLSL shaders for water, fire, glow, and post-processing
- **Games and demos** — simple 3D games, interactive toys, creative experiences

### What the user sees

An immersive 3D scene: drag to orbit around objects, scroll to zoom, watch particles flow or objects rotate. Post-processing effects (bloom, ambient occlusion) add cinematic polish. The dark background integrates seamlessly with the scene.

---

## When to Use Three.js vs. Alternatives

| Use Three.js when… | Use another library when… |
|---|---|
| Real-time 3D scenes with depth, lighting, perspective | 2D canvas art, generative patterns → **p5.js** |
| Particle systems with thousands of points in 3D | 2D particle systems without depth → **p5.js** |
| Product/object visualization with materials | Data charts (bar, line, pie) → **Chart.js / Plotly** |
| GLTF/GLB model loading and display | 3D scatter/surface plots only → **Plotly** (simpler) |
| Custom GLSL shaders and post-processing | Geographic maps → **Leaflet** |
| WebGPU rendering for next-gen performance | DOM/SVG animation → **Anime.js / GSAP** |
| InstancedMesh for massive object counts | Diagrams and flowcharts → **Mermaid / JointJS** |

> **Rule of thumb:** if the visualization needs depth, lighting, perspective, or real-time 3D interaction, use Three.js. For anything flat (2D canvas, SVG, DOM), use a more appropriate 2D library.

---

## Step 1 — CDN Setup

Three.js r134+ ships exclusively as ES modules. The recommended CDN pattern for artifacts uses an **import map**, which lets `<script type="module">` code use bare specifiers like `'three'` and `'three/addons/'`.

```html
<!-- In <head> — BEFORE any module scripts -->
<script type="importmap">
{
  "imports": {
    "three":          "https://cdn.jsdelivr.net/npm/three@0.183.2/build/three.module.js",
    "three/addons/":  "https://cdn.jsdelivr.net/npm/three@0.183.2/examples/jsm/"
  }
}
</script>

<!-- Your code — must be type="module" -->
<script type="module">
  import * as THREE from 'three';
  import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
  // ...
</script>
```

> **⚠️ All files and addons must use the same version.** Never mix `three@0.183.2` core with addons from a different version — silent breakage guaranteed.

### Key addons (import on demand)
```javascript
import { OrbitControls }    from 'three/addons/controls/OrbitControls.js';     // mouse orbit/zoom/pan
import { TransformControls } from 'three/addons/controls/TransformControls.js'; // drag to move/scale/rotate objects
import { GLTFLoader }        from 'three/addons/loaders/GLTFLoader.js';          // load .glb / .gltf models
import { RGBELoader }        from 'three/addons/loaders/RGBELoader.js';          // HDR environment maps
import { EffectComposer }    from 'three/addons/postprocessing/EffectComposer.js'; // post-processing pipeline
import { RenderPass }        from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass }   from 'three/addons/postprocessing/UnrealBloomPass.js'; // glow effect
import { FontLoader }        from 'three/addons/loaders/FontLoader.js';           // 3D text
import { TextGeometry }      from 'three/addons/geometries/TextGeometry.js';      // 3D text geometry
```

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>3D Scene</title>

  <script type="importmap">
  {
    "imports": {
      "three":         "https://cdn.jsdelivr.net/npm/three@0.183.2/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.183.2/examples/jsm/"
    }
  }
  </script>

  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #0f1117; overflow: hidden; font-family: 'Segoe UI', sans-serif; }

    /* Canvas fills the viewport */
    canvas { display: block; width: 100vw; height: 100vh; }

    /* Optional HUD overlay */
    #hud {
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      background: rgba(26,29,39,0.85); backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
      padding: 10px 20px; color: #94a3b8; font-size: 12px;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <div id="hud">Drag to orbit · Scroll to zoom</div>

  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

    // All Three.js code here
  </script>
</body>
</html>
```

---

## Step 3 — The Scene/Camera/Renderer Trinity

Every Three.js scene requires exactly these three objects, set up in this order:

```javascript
// 1. Scene — the container for all objects, lights, and fog
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0f1117);   // dark background
// scene.fog = new THREE.Fog(0x0f1117, 10, 50);  // optional depth fog

// 2. Camera — defines what we see and from where
const camera = new THREE.PerspectiveCamera(
  60,                                // FOV in degrees (45–75 is natural; wider = more dramatic)
  window.innerWidth / window.innerHeight,  // aspect ratio — update on resize
  0.1,                               // near clipping plane
  1000                               // far clipping plane
);
camera.position.set(0, 2, 6);       // x, y, z — move back to see objects at origin
camera.lookAt(0, 0, 0);             // point camera at scene origin

// 3. Renderer — draws the scene to a <canvas>
const renderer = new THREE.WebGLRenderer({
  antialias: true,                   // smooth edges
  alpha:     false,                  // transparent background (set true for overlay on HTML)
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));  // cap at 2x for performance
renderer.shadowMap.enabled = true;
renderer.shadowMap.type    = THREE.PCFSoftShadowMap;
renderer.outputColorSpace   = THREE.SRGBColorSpace;            // correct gamma
renderer.toneMapping        = THREE.ACESFilmicToneMapping;     // cinematic tone map
renderer.toneMappingExposure = 1.0;
document.body.appendChild(renderer.domElement);

// Responsive resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});
```

---

## Step 4 — Geometries

```javascript
// Standard primitives
new THREE.BoxGeometry(w, h, d)                          // cube / cuboid
new THREE.SphereGeometry(radius, widthSegs, heightSegs) // sphere (min 32, 32 for smooth)
new THREE.PlaneGeometry(w, h, wSegs, hSegs)             // flat plane / ground
new THREE.CylinderGeometry(rTop, rBottom, height, segs) // cylinder / cone (rTop=0)
new THREE.TorusGeometry(radius, tube, radialSegs, tubularSegs)  // donut ring
new THREE.TorusKnotGeometry(radius, tube, tubularSegs, radialSegs, p, q)  // knot
new THREE.IcosahedronGeometry(radius, detail)           // low-poly sphere (detail 0=20 faces)
new THREE.OctahedronGeometry(radius)                    // diamond shape
new THREE.TetrahedronGeometry(radius)                   // 4-face pyramid
new THREE.ConeGeometry(radius, height, segs)            // cone
new THREE.RingGeometry(innerR, outerR, segs)            // flat ring
new THREE.CircleGeometry(radius, segs)                  // flat disc
new THREE.TubeGeometry(path, tubularSegs, radius, radialSegs, closed)  // tube along a path

// Custom geometry from vertex positions
const geo = new THREE.BufferGeometry();
const vertices = new Float32Array([
   0,  1, 0,   // vertex 0
  -1, -1, 0,   // vertex 1
   1, -1, 0,   // vertex 2
]);
geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
// Optional: add normals, UVs, indices

// Geometry modifiers
geo.computeVertexNormals();   // auto-calculate normals (needed for lighting)
geo.center();                 // center geometry at its bounding box center
```

---

## Step 5 — Materials

```javascript
// MeshStandardMaterial — physically-based (PBR), responds to lights — use by default
const mat = new THREE.MeshStandardMaterial({
  color:       0x6366f1,     // base color (hex or THREE.Color)
  metalness:   0.3,          // 0 = plastic, 1 = metal
  roughness:   0.4,          // 0 = mirror, 1 = matte
  emissive:    0x220044,     // self-illumination (adds to lit color)
  emissiveIntensity: 0.5,
  wireframe:   false,
  transparent: false,
  opacity:     1.0,
  side:        THREE.FrontSide,   // THREE.BackSide | THREE.DoubleSide
});

// MeshPhongMaterial — cheaper, non-PBR, good for stylised renders
new THREE.MeshPhongMaterial({ color: 0x6366f1, shininess: 100, specular: 0xffffff })

// MeshBasicMaterial — unlit, ignores all lights — useful for helpers and wireframes
new THREE.MeshBasicMaterial({ color: 0x6366f1, wireframe: true })

// MeshDepthMaterial — renders depth map (white=near, black=far)
new THREE.MeshDepthMaterial()

// MeshNormalMaterial — colors by surface normal (great for debugging)
new THREE.MeshNormalMaterial()

// MeshToonMaterial — cel-shaded, cartoon look
new THREE.MeshToonMaterial({ color: 0x6366f1 })

// PointsMaterial — for particle systems
new THREE.PointsMaterial({ color: 0x6366f1, size: 0.05, sizeAttenuation: true })

// ShaderMaterial — raw GLSL shaders for complete control
new THREE.ShaderMaterial({
  uniforms: { uTime: { value: 0 }, uColor: { value: new THREE.Color(0x6366f1) } },
  vertexShader:   `/* GLSL */`,
  fragmentShader: `/* GLSL */`,
  transparent: true,
})

// LineBasicMaterial — for wireframe lines drawn with THREE.Line
new THREE.LineBasicMaterial({ color: 0x6366f1, linewidth: 1 })
```

---

## Step 6 — Lights

```javascript
// AmbientLight — flat, omnidirectional fill (no shadows, no directionality)
const ambient = new THREE.AmbientLight(0xffffff, 0.4);  // (color, intensity)
scene.add(ambient);

// DirectionalLight — parallel rays, like the sun. Casts shadows.
const sun = new THREE.DirectionalLight(0xffffff, 2.0);
sun.position.set(5, 10, 5);
sun.castShadow = true;
sun.shadow.mapSize.width  = 2048;  // shadow resolution
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far  = 50;
sun.shadow.camera.left = sun.shadow.camera.bottom = -10;
sun.shadow.camera.right = sun.shadow.camera.top  =  10;
scene.add(sun);

// PointLight — omnidirectional, radiates from a point (like a bulb). Casts shadows.
const bulb = new THREE.PointLight(0xffa0ff, 3.0, 20, 2);  // (color, intensity, distance, decay)
bulb.position.set(-3, 3, -3);
scene.add(bulb);

// SpotLight — cone of light (like a stage light). Casts shadows.
const spot = new THREE.SpotLight(0xffffff, 5.0);
spot.position.set(0, 8, 0);
spot.angle   = Math.PI / 6;   // cone half-angle
spot.penumbra = 0.3;           // 0 = hard edge, 1 = soft
spot.castShadow = true;
scene.add(spot);

// HemisphereLight — sky color from above, ground color from below (great atmosphere fill)
const hemi = new THREE.HemisphereLight(0x4488ff, 0x223311, 0.6);
scene.add(hemi);

// RectAreaLight — emits from a rectangular surface (studio softbox look)
const rect = new THREE.RectAreaLight(0x6366f1, 4, 3, 2);  // (color, intensity, width, height)
rect.position.set(-3, 2, 3);
rect.lookAt(0, 0, 0);
scene.add(rect);
```

---

## Step 7 — Building the Scene (Mesh)

```javascript
// A Mesh = Geometry + Material
const mesh = new THREE.Mesh(
  new THREE.IcosahedronGeometry(1, 1),
  new THREE.MeshStandardMaterial({ color: 0x6366f1, metalness: 0.3, roughness: 0.4 })
);
mesh.position.set(0, 0, 0);
mesh.castShadow    = true;
mesh.receiveShadow = true;
scene.add(mesh);

// Group — parent container to transform multiple objects together
const group = new THREE.Group();
group.add(meshA, meshB, meshC);
group.rotation.y = Math.PI / 4;
scene.add(group);

// Clone a mesh cheaply (shares geometry and material)
const clone = mesh.clone();
clone.position.x = 3;
scene.add(clone);

// Key transform properties
mesh.position.set(x, y, z);
mesh.rotation.set(rx, ry, rz);      // Euler angles in radians
mesh.scale.set(sx, sy, sz);
mesh.visible = false;
mesh.name = 'myMesh';               // find later with scene.getObjectByName('myMesh')
```

---

## Step 8 — Animation Loop

```javascript
// OrbitControls — mouse orbit/pan/zoom (load from addons)
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;          // smooth inertia
controls.dampingFactor = 0.05;
controls.autoRotate    = false;
controls.minDistance   = 2;
controls.maxDistance   = 20;

// Clock for frame-rate-independent animation
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);

  const elapsed = clock.getElapsedTime();  // total seconds since start
  const delta   = clock.getDelta();        // seconds since last frame ← call ONCE per frame

  // Example: rotate and pulse
  mesh.rotation.y = elapsed * 0.5;
  mesh.position.y = Math.sin(elapsed) * 0.3;

  // Update uniforms for ShaderMaterial
  // shaderMat.uniforms.uTime.value = elapsed;

  controls.update();          // required when enableDamping is true
  renderer.render(scene, camera);
}
animate();
```

> **⚠️ `clock.getDelta()` resets the internal timer on each call.** Call it exactly **once per frame** at the top of your loop. Calling it multiple times in the same frame gives 0 on subsequent calls.

---

## Step 9 — Particles (Points System)

```javascript
const COUNT    = 5000;
const positions = new Float32Array(COUNT * 3);
const colors    = new Float32Array(COUNT * 3);
const color     = new THREE.Color();

for (let i = 0; i < COUNT; i++) {
  // Random sphere distribution
  const theta = Math.random() * Math.PI * 2;
  const phi   = Math.acos(2 * Math.random() - 1);
  const r     = 2 + Math.random() * 3;
  positions[i * 3]     = r * Math.sin(phi) * Math.cos(theta);
  positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
  positions[i * 3 + 2] = r * Math.cos(phi);

  // Color gradient by height
  color.setHSL(0.6 + positions[i * 3 + 1] * 0.05, 0.8, 0.6);
  colors[i * 3]     = color.r;
  colors[i * 3 + 1] = color.g;
  colors[i * 3 + 2] = color.b;
}

const geo = new THREE.BufferGeometry();
geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geo.setAttribute('color',    new THREE.BufferAttribute(colors, 3));

const mat = new THREE.PointsMaterial({
  size:            0.04,
  sizeAttenuation: true,           // particles shrink with distance
  vertexColors:    true,           // use per-vertex color attribute
  transparent:     true,
  opacity:         0.85,
  blending:        THREE.AdditiveBlending,  // particles add their color (glow effect)
  depthWrite:      false,          // required for correct transparency with AdditiveBlending
});

const particles = new THREE.Points(geo, mat);
scene.add(particles);

// Animate in loop:
// particles.rotation.y = elapsed * 0.1;
```

---

## Step 10 — Raycasting (Mouse Interaction)

```javascript
const raycaster = new THREE.Raycaster();
const mouse     = new THREE.Vector2();
let   hovered   = null;

window.addEventListener('mousemove', (e) => {
  // Normalize to [-1, +1]
  mouse.x = (e.clientX / window.innerWidth)  * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
});

// In animate(), before renderer.render():
function checkHover() {
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children, true);  // true = recursive

  if (intersects.length > 0) {
    const hit = intersects[0].object;
    if (hovered !== hit) {
      if (hovered) hovered.material.emissiveIntensity = 0;   // reset old
      hovered = hit;
      hovered.material.emissiveIntensity = 0.5;              // highlight new
    }
  } else {
    if (hovered) hovered.material.emissiveIntensity = 0;
    hovered = null;
  }
}

window.addEventListener('click', () => {
  if (hovered) console.log('Clicked:', hovered.name, hovered.userData);
});
```

---

## Step 11 — Shadows, Fog, Helpers

```javascript
// Shadows — enable on renderer, set castShadow/receiveShadow on objects
renderer.shadowMap.enabled = true;
mesh.castShadow    = true;
groundPlane.receiveShadow = true;

// Fog
scene.fog = new THREE.Fog(0x0f1117, 8, 30);      // linear fog (near, far)
scene.fog = new THREE.FogExp2(0x0f1117, 0.05);   // exponential fog (density)

// Grid helper (floor grid reference)
const grid = new THREE.GridHelper(20, 20, 0x444455, 0x2a2a3a);
scene.add(grid);

// Axes helper (red=X, green=Y, blue=Z)
const axes = new THREE.AxesHelper(3);
scene.add(axes);

// Point light sphere helper (shows light position)
const lightHelper = new THREE.PointLightHelper(bulb, 0.3);
scene.add(lightHelper);

// Bounding box helper
const bbox = new THREE.BoxHelper(mesh, 0x6366f1);
scene.add(bbox);
```

---

## Step 12 — Design & Polish Guidelines

- **Pixel ratio cap** — always `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`; 4× on retina displays is a massive performance hit
- **Responsive resize** — listen to `window.resize`, update `camera.aspect` and `renderer.setSize()`, never hardcode pixel dimensions
- **OrbitControls defaults** — set `controls.enableDamping = true` and `controls.dampingFactor = 0.05` for smooth, inertial orbiting
- **Lighting setup** — minimum: one `AmbientLight(0x404040)` + one `DirectionalLight(0xffffff, 1)` — pure ambient looks flat, pure directional creates harsh shadows
- **Transparent backgrounds** — `renderer = new THREE.WebGLRenderer({ alpha: true })` + `renderer.setClearColor(0x000000, 0)` lets the HTML background show through
- **Memory cleanup** — always `geometry.dispose()`, `material.dispose()`, `texture.dispose()` when removing objects; Three.js does NOT garbage-collect GPU resources
- **Pre-allocate** — never create `new THREE.Vector3()` or `new THREE.Matrix4()` inside the animation loop; allocate once outside
- **InstancedMesh** — for 100+ identical objects, use `InstancedMesh` instead of individual `Mesh` objects (one draw call vs hundreds)
- **Post-processing** — `UnrealBloomPass` adds cinematic glow; use sparingly (`strength: 0.5–1.5`, `radius: 0.4`, `threshold: 0.6`)
- **HUD overlay** — for fullscreen scenes, add a fixed-position translucent hint bar: "Drag to orbit · Scroll to zoom"

---

## Step 13 — Performance Patterns

```javascript
// Object pooling — reuse geometries and materials, avoid creating in animation loop
const sharedGeo = new THREE.SphereGeometry(0.5, 16, 16);
const sharedMat = new THREE.MeshStandardMaterial({ color: 0x6366f1 });
for (let i = 0; i < 100; i++) {
  const m = new THREE.Mesh(sharedGeo, sharedMat);  // geometry and material are shared
  m.position.set(Math.random() * 10 - 5, Math.random() * 5, Math.random() * 10 - 5);
  scene.add(m);
}

// Memory cleanup — call when removing objects
function disposeMesh(mesh) {
  mesh.geometry.dispose();
  if (Array.isArray(mesh.material)) mesh.material.forEach(m => m.dispose());
  else mesh.material.dispose();
  scene.remove(mesh);
}

// InstancedMesh — render thousands of identical objects in one draw call
const instancedMesh = new THREE.InstancedMesh(sharedGeo, sharedMat, 1000);
const matrix = new THREE.Matrix4();
for (let i = 0; i < 1000; i++) {
  matrix.setPosition(Math.random() * 20 - 10, Math.random() * 10, Math.random() * 20 - 10);
  instancedMesh.setMatrixAt(i, matrix);
}
instancedMesh.instanceMatrix.needsUpdate = true;
scene.add(instancedMesh);
```

**Performance rules:**
- Keep draw calls low: use `InstancedMesh` for many identical objects, merge static geometry with `BufferGeometryUtils.mergeGeometries()`
- `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` — cap at 2× (4K screens at 4× are brutal)
- Set `depthWrite: false` on transparent objects with `AdditiveBlending`
- Call `geometry.dispose()` and `material.dispose()` when removing objects
- Avoid creating new `THREE.Vector3`, `THREE.Color`, etc. inside `animate()` — pre-allocate them outside

---

## Step 14 — Complete Example: Interactive Particle Galaxy

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Galaxy</title>
  <script type="importmap">
  {
    "imports": {
      "three":         "https://cdn.jsdelivr.net/npm/three@0.183.2/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.183.2/examples/jsm/"
    }
  }
  </script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #030508; overflow: hidden; }
    canvas { display: block; }
    #ui {
      position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
      background: rgba(15,17,23,0.8); backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.06); border-radius: 10px;
      padding: 10px 20px; color: #475569; font-size: 12px; font-family: 'Segoe UI', sans-serif;
      pointer-events: none; white-space: nowrap;
    }
  </style>
</head>
<body>
  <div id="ui">Drag to orbit · Scroll to zoom · Double-click to pulse</div>
  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

    // ── Renderer ──────────────────────────────────────
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    document.body.appendChild(renderer.domElement);

    // ── Scene & Camera ────────────────────────────────
    const scene  = new THREE.Scene();
    scene.fog    = new THREE.FogExp2(0x030508, 0.035);

    const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 200);
    camera.position.set(0, 4, 12);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.04;
    controls.minDistance   = 3;
    controls.maxDistance   = 30;
    controls.maxPolarAngle = Math.PI * 0.75;

    // ── Galaxy generator ──────────────────────────────
    function generateGalaxy(params) {
      const { count, radius, branches, spin, randomness, randomPow, insideColor, outsideColor } = params;

      const positions = new Float32Array(count * 3);
      const colors    = new Float32Array(count * 3);
      const cIn  = new THREE.Color(insideColor);
      const cOut = new THREE.Color(outsideColor);

      for (let i = 0; i < count; i++) {
        const r       = Math.random() * radius;
        const branch  = (i % branches) / branches * Math.PI * 2;
        const spinAng = r * spin;
        const angle   = branch + spinAng;

        const rx = (Math.random() ** randomPow) * (Math.random() < 0.5 ? 1 : -1) * randomness * r;
        const ry = (Math.random() ** randomPow) * (Math.random() < 0.5 ? 1 : -1) * randomness * r * 0.3;
        const rz = (Math.random() ** randomPow) * (Math.random() < 0.5 ? 1 : -1) * randomness * r;

        positions[i*3]   = Math.cos(angle) * r + rx;
        positions[i*3+1] = ry;
        positions[i*3+2] = Math.sin(angle) * r + rz;

        const mixed = cIn.clone().lerp(cOut, r / radius);
        colors[i*3]   = mixed.r;
        colors[i*3+1] = mixed.g;
        colors[i*3+2] = mixed.b;
      }

      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geo.setAttribute('color',    new THREE.BufferAttribute(colors, 3));

      const mat = new THREE.PointsMaterial({
        size:            0.025,
        sizeAttenuation: true,
        vertexColors:    true,
        blending:        THREE.AdditiveBlending,
        depthWrite:      false,
        transparent:     true,
        opacity:         0.9,
      });

      return new THREE.Points(geo, mat);
    }

    const galaxy = generateGalaxy({
      count:        80000,
      radius:       8,
      branches:     5,
      spin:         1.2,
      randomness:   0.4,
      randomPow:    3,
      insideColor:  '#ff8844',
      outsideColor: '#2244ff',
    });
    scene.add(galaxy);

    // ── Pulse on double-click ─────────────────────────
    let pulseStart = -999;
    renderer.domElement.addEventListener('dblclick', () => { pulseStart = clock.getElapsedTime(); });

    // ── Animate ───────────────────────────────────────
    const clock = new THREE.Clock();

    function animate() {
      requestAnimationFrame(animate);
      const t  = clock.getElapsedTime();
      const dt = clock.getDelta();

      // Slow galaxy spin
      galaxy.rotation.y = t * 0.05;

      // Pulse scale on double-click
      const pAge = t - pulseStart;
      if (pAge < 1.5) {
        const pulse = 1 + Math.sin(pAge * Math.PI / 1.5) * 0.15;
        galaxy.scale.setScalar(pulse);
      } else {
        galaxy.scale.setScalar(1);
      }

      controls.update();
      renderer.render(scene, camera);
    }
    animate();

    // ── Resize ────────────────────────────────────────
    window.addEventListener('resize', () => {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    });
  </script>
</body>
</html>
```

---

## Step 15 — Common Mistakes to Avoid

- **Old UMD `<script src="three.min.js">` pattern** — Three.js dropped the UMD build as the primary distribution after r134. Use the importmap + ES module pattern. The old `THREE.OrbitControls` (not from addons) no longer exists
- **Missing `type="module"` on the script tag** — import maps only work with `<script type="module">`. A plain `<script>` tag will fail with a syntax error on `import` statements
- **Version mismatch between core and addons** — always pin to the same version: `three@0.183.2` core and `three@0.183.2` in the addons path
- **`clock.getDelta()` called multiple times per frame** — it resets its internal timer on each call; always call it exactly once, at the very start of `animate()`
- **Forgetting `controls.update()` when `enableDamping: true`** — without this call in the animation loop, damping won't work and the camera will freeze
- **Creating objects inside `animate()`** — `new THREE.Vector3()`, `new THREE.Color()`, `new THREE.Matrix4()` inside the loop trigger garbage collection every frame; declare and reuse them outside
- **Not setting `depthWrite: false` on additive/transparent particles** — without it, particles incorrectly occlude each other and the blending breaks
- **No `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`** — on Retina/HiDPI displays the canvas will be blurry; on 4K screens without the cap, performance will tank
- **`geometry.dispose()` and `material.dispose()` neglected** — GPU memory is not freed automatically when you remove meshes from the scene; always call dispose on cleanup
- **`scene.background = new THREE.Color(...)` conflicts with `renderer.setClearColor`** — use one or the other, not both; `scene.background` takes priority
