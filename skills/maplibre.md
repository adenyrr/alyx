---
name: maplibre
description: Create high-performance, vector-tile interactive maps using MapLibre GL JS 4, delivered as self-contained HTML artifacts. Use this skill when the request involves large geographic datasets (10K+ features), custom cartographic styling, WebGL-accelerated rendering, 3D extrusions (buildings, terrain), data-driven styling via expressions, or smooth pitch/bearing/rotation interactions. Trigger on requests like "render 50K points on a map", "show 3D buildings", "animated fly-through over terrain", "choropleth with smooth zoom", "vector tile basemap", "GeoJSON with thousands of features", "custom map style", or "city explorer with 3D extrusions". Do NOT use for: simple marker-and-popup maps with < 100 points (→ leaflet-maps skill), schematic node-edge diagrams (→ vis-network skill), abstract geographic charts without tiles (→ d3-charting skill), or non-spatial data (→ chartjs / echarts skill).
agents: [dev]
---

# MapLibre GL JS Skill — v4

MapLibre GL JS is the open-source fork of Mapbox GL JS, rendering vector tiles via WebGL. It scales to hundreds of thousands of features, supports 3D building extrusions, terrain DEMs, hillshading, smooth pitch/bearing animations, and a declarative JSON style spec where every line/fill/symbol can be data-driven through expressions. It is the right tool when Leaflet's raster-tile rendering or canvas-based feature pipeline becomes a bottleneck.

---

## Artifact Presentation & Use Cases

Every MapLibre artifact is a self-contained HTML page with a dark theme by default. The visual structure follows the standard project pattern:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow, `overflow: hidden`) clips the map to rounded corners
- **Card header** (padding 22px, bottom border `rgba(255,255,255,0.07)`) carries the title
- **Title** (`h1`, 1.1rem, `#f1f5f9`) and **subtitle** (`p.sub`, 0.8rem, `#64748b`)
- **Map container** (`#map`, fixed height, transparent background) renders the WebGL map
- **Optional HUD or legend** floats over the map with `position: absolute` and a translucent surface

### Typical use cases

- **3D city explorers** — vector basemap + extruded buildings + camera fly-through
- **Choropleth at scale** — 5,000+ admin polygons styled via `interpolate` expressions
- **Animated point clouds** — 50K+ taxi pickups, sensor readings, or telemetry traces
- **Terrain visualization** — RGB-encoded DEM tiles with hillshade and exaggeration
- **Heatmaps & clusters** — built-in `heatmap` and `cluster` layer types, GPU-rendered
- **Custom cartography** — restyle every layer (water, roads, labels) to match brand palette
- **Geofence editors** — pair with `maplibre-gl-draw` for polygon authoring

### What the user sees

A buttery-smooth map: drag to pan, scroll to zoom, right-drag to pitch and rotate, double-click to zoom in. Buildings rise into 3D as you tilt the view. The dark vector basemap (Protomaps Dark) integrates seamlessly with the dark card. A HUD chip in the corner shows the active zoom level and feature count.

---

## When to Use MapLibre vs. Alternatives

| Use MapLibre when… | Use another library when… |
|---|---|
| Vector tiles, GPU rendering, > 10K features | < 100 markers, quick prototype → **Leaflet** |
| 3D building extrusions, pitch/bearing camera | Static thematic SVG map, no tiles → **D3 (d3-geo)** |
| Custom cartographic styling end-to-end | Marker clusters out-of-the-box with one plugin → **Leaflet + markercluster** |
| Terrain DEM + hillshade | Choropleth via simple GeoJSON polygons | Either works; MapLibre faster |
| Data-driven styling via `interpolate` / `match` | Schematic node-edge graphs → **vis-network** |
| Smooth animated camera (`flyTo`, `easeTo`) | Geographic plot inside a Plotly figure → **Plotly** |
| Free/open style providers (Protomaps, MapTiler free) | Raster-only basemap is fine → **Leaflet** |

> **Rule of thumb:** if you'd describe the map as "modern, fluid, dataset-heavy, possibly 3D", reach for MapLibre. If it's "a few pins on a map", Leaflet remains lighter and simpler.

---

## Step 1 — CDN Setup

MapLibre needs **both** a CSS file and a JS file, loaded in the right order.

```html
<!-- 1. CSS in <head> — BEFORE the JS -->
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css">

<!-- 2. JS — before your application script, at end of <body> -->
<script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
```

### Free vector-tile basemaps (no API key required)

| Provider | Style URL |
|---|---|
| **Protomaps dark** | `https://api.protomaps.com/styles/v4/dark/en.json?key=…` (free dev key from protomaps.com) |
| **Protomaps light** | `https://api.protomaps.com/styles/v4/light/en.json?key=…` |
| **MapTiler Cloud free tier** | `https://api.maptiler.com/maps/streets-v2/style.json?key=…` (free key from maptiler.com) |
| **OpenFreeMap** | `https://tiles.openfreemap.org/styles/liberty` (no key, fully free) |

For self-contained artifacts without a key, **OpenFreeMap** is the safest default; for custom dark cartography, point at Protomaps with a personal dev key.

> **Critical:** the `#map` container **must have an explicit CSS height**. WebGL needs a non-zero canvas — without an explicit height the map is invisible. This is the single most common MapLibre mistake.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Map</title>

  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css">

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
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px;
      overflow: hidden;     /* clip the map to the rounded corners */
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 22px 24px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
    }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }

    /* REQUIRED: explicit height */
    #map { width: 100%; height: 560px; position: relative; }

    /* MapLibre control overrides for dark theme */
    .maplibregl-ctrl-group {
      background: #1e2130 !important;
      border: 1px solid rgba(255,255,255,0.1) !important;
      box-shadow: 0 4px 16px rgba(0,0,0,0.4) !important;
    }
    .maplibregl-ctrl-group button {
      background-color: #1e2130 !important;
      filter: invert(0.85);    /* light icons on dark buttons */
    }
    .maplibregl-ctrl-group button:hover { background-color: #2d3148 !important; }
    .maplibregl-ctrl-attrib {
      background: rgba(15,17,23,0.75) !important;
      color: #475569 !important;
    }
    .maplibregl-ctrl-attrib a { color: #6366f1 !important; }
    .maplibregl-popup-content {
      background: #1e2130; color: #e2e8f0;
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 10px; padding: 12px 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    .maplibregl-popup-tip { border-top-color: #1e2130 !important; border-bottom-color: #1e2130 !important; }
  </style>
</head>
<body>
  <main class="card" role="region" aria-label="Interactive map">
    <div class="card-header">
      <h1>Map Title</h1>
      <p class="sub">Drag to pan · scroll to zoom · right-drag to pitch + rotate</p>
    </div>
    <div id="map" role="application" aria-label="Map of …" tabindex="0"></div>
  </main>

  <script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
  <script>
    // All MapLibre code here
  </script>
</body>
</html>
```

---

## Step 3 — Themes (dark default + light alternative)

MapLibre styles are JSON documents — to theme the UI you switch the style URL **and** retint the surrounding card chrome. Keep two palettes:

### Dark theme tokens (default)

```javascript
const DARK = {
  bg:      '#0f1117',
  card:    '#1a1d27',
  border:  'rgba(255,255,255,0.08)',
  text:    '#e2e8f0',
  muted:   '#94a3b8',
  accent:  '#6366f1',
  styleURL:'https://tiles.openfreemap.org/styles/positron'.replace('positron', 'dark'),  // OpenFreeMap "dark"
  // or: 'https://api.protomaps.com/styles/v4/dark/en.json?key=YOUR_KEY'
  building:{ color: '#2a2f3d', highlight: '#6366f1' },
  water:   '#0b0e16',
  land:    '#151823',
};
```

### Light theme tokens

```javascript
const LIGHT = {
  bg:      '#f8fafc',
  card:    '#ffffff',
  border:  'rgba(0,0,0,0.08)',
  text:    '#1e293b',
  muted:   '#475569',
  accent:  '#6366f1',
  styleURL:'https://tiles.openfreemap.org/styles/positron',
  // or: 'https://api.protomaps.com/styles/v4/light/en.json?key=YOUR_KEY'
  building:{ color: '#e2e8f0', highlight: '#6366f1' },
  water:   '#dbeafe',
  land:    '#f1f5f9',
};
```

### Theme switcher via `data-theme` + `prefers-color-scheme`

```html
<body data-theme="dark">
  <button id="themeToggle" aria-label="Switch theme">Toggle theme</button>
  <!-- … -->
</body>
<script>
  const themes = { dark: DARK, light: LIGHT };
  // Follow the OS by default, but allow override
  let current = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  document.body.dataset.theme = current;

  document.getElementById('themeToggle').addEventListener('click', () => {
    current = current === 'dark' ? 'light' : 'dark';
    document.body.dataset.theme = current;
    document.body.style.background = themes[current].bg;
    map.setStyle(themes[current].styleURL);
    // After the style swaps, your sources & layers need to be re-added — see Step 8
  });
</script>
```

> When you call `map.setStyle()` you replace the entire style document. Re-add your custom sources/layers in the `map.once('style.load', …)` callback.

---

## Step 4 — Initialisation

```javascript
const map = new maplibregl.Map({
  container: 'map',
  style:     DARK.styleURL,
  center:    [2.3522, 48.8566],   // [lng, lat] — MapLibre uses lng, lat (NOT lat, lng!)
  zoom:      12,
  pitch:     0,                   // 0 = top-down, 60 = strong tilt
  bearing:   0,                   // 0 = north up, 90 = east up
  minZoom:   1, maxZoom: 20,
  attributionControl: false,      // we add a styled one below
  cooperativeGestures: false,     // true forces ctrl+scroll on desktop
  hash: false,                    // sync zoom/center to URL hash
  antialias: true,                // smoother edges on 3D extrusions
});

// Built-in controls
map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'top-right');
map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-left');
map.addControl(new maplibregl.FullscreenControl(), 'top-right');
map.addControl(new maplibregl.GeolocateControl({ trackUserLocation: true }), 'top-right');
map.addControl(new maplibregl.AttributionControl({ compact: true }), 'bottom-right');

// Programmatic camera
map.flyTo({ center: [-0.09, 51.505], zoom: 13, pitch: 45, bearing: -20, duration: 2200, essential: true });
map.easeTo({ center: [2.35, 48.85], zoom: 14, duration: 800 });
map.fitBounds([[2.22, 48.80], [2.47, 48.90]], { padding: 60, pitch: 30, bearing: 0, duration: 1200 });
```

---

## Step 5 — The Style Spec at a Glance

A MapLibre style is a JSON document with three top-level keys you'll touch most:

```json
{
  "version": 8,
  "sources": { "my-data": { "type": "geojson", "data": { "type": "FeatureCollection", "features": [] } } },
  "layers":  [ { "id": "my-points", "type": "circle", "source": "my-data", "paint": { "circle-color": "#6366f1" } } ]
}
```

| Layer `type` | Renders |
|---|---|
| `background` | Solid fill across the whole map (the "land" color) |
| `fill` | Polygons (countries, neighbourhoods, choropleths) |
| `line` | LineStrings (roads, routes, borders) |
| `symbol` | Text labels and icons |
| `circle` | Point features as circles (cheap, GPU-rendered) |
| `heatmap` | Density visualisation of points |
| `fill-extrusion` | 3D extruded polygons (buildings) |
| `raster` | Image tiles (legacy basemaps, satellite) |
| `hillshade` | Terrain shading from RGB-encoded DEM |

Every `paint`/`layout` property accepts **expressions** — small JSON DSL programs that pull from feature properties or the zoom level (see Step 9).

---

## Step 6 — Sources & Layers (GeoJSON)

```javascript
map.on('load', () => {
  // 1. Add a source
  map.addSource('cities', {
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: [
        { type: 'Feature', properties: { name: 'Paris',  pop: 2161000 }, geometry: { type: 'Point', coordinates: [2.3522, 48.8566] } },
        { type: 'Feature', properties: { name: 'Lyon',   pop: 522969  }, geometry: { type: 'Point', coordinates: [4.8357, 45.7640] } },
        { type: 'Feature', properties: { name: 'Berlin', pop: 3669000 }, geometry: { type: 'Point', coordinates: [13.4050, 52.5200] } },
      ],
    },
  });

  // 2. Add a layer that reads from the source
  map.addLayer({
    id: 'city-points',
    type: 'circle',
    source: 'cities',
    paint: {
      'circle-radius': ['interpolate', ['linear'], ['get', 'pop'], 500000, 6, 4000000, 22],
      'circle-color':  '#6366f1',
      'circle-opacity': 0.85,
      'circle-stroke-color': '#a5b4fc',
      'circle-stroke-width': 1.5,
    },
  });

  map.addLayer({
    id: 'city-labels',
    type: 'symbol',
    source: 'cities',
    layout: {
      'text-field': ['get', 'name'],
      'text-font':  ['Noto Sans Regular'],
      'text-size':  12,
      'text-offset':[0, 1.4],
      'text-anchor':'top',
    },
    paint: {
      'text-color':         '#e2e8f0',
      'text-halo-color':    '#0f1117',
      'text-halo-width':    1.5,
    },
  });
});
```

> **GeoJSON coordinate order:** `[longitude, latitude]`. Same as the rest of MapLibre's API (`center: [lng, lat]`). This is the **opposite** of Leaflet — features in the ocean usually mean swapped coords.

---

## Step 7 — Markers & Popups

```javascript
// Default pin marker
new maplibregl.Marker({ color: '#6366f1' })
  .setLngLat([2.3522, 48.8566])
  .addTo(map);

// Custom HTML marker (most flexible, matches design system)
const el = document.createElement('div');
el.setAttribute('role', 'button');
el.setAttribute('aria-label', 'Paris office');
el.tabIndex = 0;
el.style.cssText = `
  width: 32px; height: 32px; border-radius: 50%;
  background: #6366f1; border: 2px solid #a5b4fc;
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 13px; cursor: pointer;
  box-shadow: 0 4px 14px rgba(99,102,241,0.6);
  transition: transform 200ms cubic-bezier(0.16,1,0.3,1);
`;
el.textContent = '42';
el.addEventListener('mouseenter', () => el.style.transform = 'scale(1.15)');
el.addEventListener('mouseleave', () => el.style.transform = 'scale(1)');

new maplibregl.Marker({ element: el, anchor: 'center' })
  .setLngLat([2.3522, 48.8566])
  .setPopup(
    new maplibregl.Popup({ offset: 24, closeButton: true, maxWidth: '260px' })
      .setHTML(`
        <div style="font-family:'Segoe UI',sans-serif;min-width:180px">
          <div style="font-weight:600;font-size:14px;color:#f1f5f9;margin-bottom:6px">Paris office</div>
          <div style="color:#94a3b8;font-size:12px">Headcount: <b style="color:#e2e8f0">42</b></div>
          <div style="color:#94a3b8;font-size:12px">Floor: <b style="color:#e2e8f0">3rd</b></div>
        </div>
      `)
  )
  .addTo(map);

// Bind popups to a whole layer (Step 6 city-points)
map.on('click', 'city-points', (e) => {
  const f = e.features[0];
  new maplibregl.Popup({ offset: 12 })
    .setLngLat(f.geometry.coordinates)
    .setHTML(`<b>${f.properties.name}</b><br>Pop: ${f.properties.pop.toLocaleString()}`)
    .addTo(map);
});
map.on('mouseenter', 'city-points', () => map.getCanvas().style.cursor = 'pointer');
map.on('mouseleave', 'city-points', () => map.getCanvas().style.cursor = '');
```

---

## Step 8 — Swapping Styles Without Losing Layers

```javascript
function applyTheme(theme) {
  const t = themes[theme];
  map.setStyle(t.styleURL);
  map.once('style.load', () => {
    // Re-add custom sources/layers because setStyle wipes them
    map.addSource('cities', { type: 'geojson', data: citiesGeoJSON });
    map.addLayer({ id: 'city-points', type: 'circle', source: 'cities', paint: { 'circle-color': t.accent } });
    // Recolour any background/water layers from the new style if you want a bespoke tint:
    if (map.getLayer('water')) map.setPaintProperty('water', 'fill-color', t.water);
    if (map.getLayer('background')) map.setPaintProperty('background', 'background-color', t.land);
  });
}
```

---

## Step 9 — Data-Driven Styling (Expressions)

Expressions are tiny JSON programs that compute paint/layout values from feature properties or the map state. They are the heart of MapLibre's power.

```javascript
// Choropleth: smoothly interpolate fill-color over `density`
'fill-color': [
  'interpolate', ['linear'], ['get', 'density'],
  0,    '#1e293b',
  50,   '#1e3a8a',
  200,  '#3b82f6',
  500,  '#a5b4fc',
  1000, '#ede9fe',
],

// Zoom-driven sizing
'circle-radius': [
  'interpolate', ['exponential', 1.5], ['zoom'],
  4,  2,
  10, 8,
  16, 24,
],

// Categorical match
'circle-color': [
  'match', ['get', 'type'],
  'flagship', '#6366f1',
  'standard', '#06b6d4',
  'outlet',   '#f97316',
  /* default */ '#94a3b8',
],

// Conditional opacity (hover highlight via feature-state)
'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], 0.9, 0.5],

// Filter a layer
filter: ['all', ['==', ['get', 'category'], 'park'], ['>', ['get', 'area'], 1000]],
```

**Choropleth with hover highlight**

```javascript
map.addSource('regions', { type: 'geojson', data: regionsGeoJSON, generateId: true });

map.addLayer({
  id: 'regions-fill',
  type: 'fill',
  source: 'regions',
  paint: {
    'fill-color': ['interpolate', ['linear'], ['get', 'gdp'],
      0,     '#1e293b',
      25000, '#1e3a8a',
      45000, '#3b82f6',
      65000, '#a5b4fc',
    ],
    'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], 0.92, 0.7],
  },
});

map.addLayer({ id: 'regions-line', type: 'line', source: 'regions',
  paint: { 'line-color': 'rgba(255,255,255,0.18)', 'line-width': 1 } });

let hovered = null;
map.on('mousemove', 'regions-fill', (e) => {
  if (!e.features.length) return;
  if (hovered !== null) map.setFeatureState({ source: 'regions', id: hovered }, { hover: false });
  hovered = e.features[0].id;
  map.setFeatureState({ source: 'regions', id: hovered }, { hover: true });
  map.getCanvas().style.cursor = 'pointer';
});
map.on('mouseleave', 'regions-fill', () => {
  if (hovered !== null) map.setFeatureState({ source: 'regions', id: hovered }, { hover: false });
  hovered = null;
  map.getCanvas().style.cursor = '';
});
```

---

## Step 10 — 3D Building Extrusions

Vector basemaps from Protomaps/MapTiler/OpenFreeMap usually expose a `building` source-layer with a `height` attribute. Add a `fill-extrusion` layer on top.

```javascript
map.on('load', () => {
  // Find the first symbol layer (labels) and insert buildings beneath it
  const labelLayer = map.getStyle().layers.find(l => l.type === 'symbol')?.id;

  map.addLayer({
    id: 'buildings-3d',
    type: 'fill-extrusion',
    source: 'openmaptiles',          // protomaps uses "protomaps"; OpenFreeMap uses "openmaptiles"
    'source-layer': 'building',
    minzoom: 14,
    paint: {
      'fill-extrusion-color': [
        'interpolate', ['linear'], ['get', 'render_height'],
        0,   '#2a2f3d',
        50,  '#3730a3',
        150, '#6366f1',
      ],
      'fill-extrusion-height': ['get', 'render_height'],
      'fill-extrusion-base':   ['get', 'render_min_height'],
      'fill-extrusion-opacity': 0.85,
      'fill-extrusion-vertical-gradient': true,
    },
  }, labelLayer);

  // Tilt the camera to show 3D
  map.easeTo({ pitch: 55, bearing: -22, duration: 1500 });
});
```

> The source name (`openmaptiles` vs `protomaps`) and the property names (`render_height`, `height`, `min_height`) depend on the basemap vendor. Inspect `map.getStyle().sources` after `load` to confirm.

---

## Step 11 — Clustering Large Point Datasets

Built into GeoJSON sources — no plugin needed.

```javascript
map.addSource('events', {
  type: 'geojson',
  data: eventsGeoJSON,           // tens of thousands of points
  cluster: true,
  clusterMaxZoom: 14,
  clusterRadius: 50,
});

map.addLayer({
  id: 'clusters', type: 'circle', source: 'events', filter: ['has', 'point_count'],
  paint: {
    'circle-color': ['step', ['get', 'point_count'], '#6366f1', 50, '#8b5cf6', 200, '#ec4899'],
    'circle-radius': ['step', ['get', 'point_count'], 18, 50, 24, 200, 32],
    'circle-stroke-color': 'rgba(99,102,241,0.4)', 'circle-stroke-width': 6,
  },
});

map.addLayer({
  id: 'cluster-count', type: 'symbol', source: 'events', filter: ['has', 'point_count'],
  layout: { 'text-field': '{point_count_abbreviated}', 'text-font': ['Noto Sans Bold'], 'text-size': 12 },
  paint:  { 'text-color': '#fff' },
});

map.addLayer({
  id: 'unclustered', type: 'circle', source: 'events', filter: ['!', ['has', 'point_count']],
  paint: { 'circle-color': '#6366f1', 'circle-radius': 6, 'circle-stroke-color': '#a5b4fc', 'circle-stroke-width': 1.5 },
});

// Click a cluster to expand
map.on('click', 'clusters', (e) => {
  const f = e.features[0];
  map.getSource('events').getClusterExpansionZoom(f.id, (err, zoom) => {
    if (err) return;
    map.easeTo({ center: f.geometry.coordinates, zoom });
  });
});
```

---

## Step 12 — Events Reference

```javascript
map.on('load',     () => {});         // first style + tiles ready
map.on('idle',     () => {});         // every layer drawn, no pending work
map.on('move',     () => {});         // continuous during pan
map.on('moveend',  () => console.log(map.getCenter(), map.getZoom()));
map.on('zoom',     () => {});
map.on('pitch',    () => {});
map.on('rotate',   () => {});
map.on('click',    (e) => console.log(e.lngLat));
map.on('contextmenu', (e) => { /* right-click */ });

// Per-layer events (only fire when the cursor is over a feature in that layer)
map.on('click',     'city-points', (e) => {});
map.on('mouseenter','city-points', () => map.getCanvas().style.cursor = 'pointer');
map.on('mouseleave','city-points', () => map.getCanvas().style.cursor = '');

// Query rendered features under a point
const hits = map.queryRenderedFeatures(e.point, { layers: ['city-points'] });
```

---

## Step 13 — Design, Performance & Accessibility

- **Always set an explicit container height.** No height → no map. This is the single biggest source of "blank screen" bugs.
- **Insert custom 3D layers beneath labels.** Pass the symbol layer id as the second arg to `addLayer()` so streets/POIs stay legible on top of buildings.
- **Use `generateId: true` on GeoJSON sources** when you want hover highlights via `feature-state` — otherwise features have no stable id.
- **Cluster anything > 1,000 points.** GPU-rendered circles are fast, but per-feature event handling and label rendering still cost.
- **Cap `pitch` at 60** to avoid awkward camera angles unless you specifically want a flyover effect.
- **Attribution is required.** OpenStreetMap-derived basemaps require attribution by license; keep `AttributionControl`.
- **Re-add sources/layers after `setStyle()`** in `map.once('style.load', …)`.
- **Throttle resize on layout changes.** Call `map.resize()` after the container changes size (tab shown, drawer opened, CSS transition ended).

### Accessibility

- `<div id="map" role="application" aria-label="…" tabindex="0">` makes the map keyboard-focusable.
- MapLibre supports `keyboard` interactions natively: arrow keys pan, `+`/`-` zoom, `shift+drag` rotate; document them in the subtitle so users know.
- Provide a **non-spatial alternative** for any critical info: a list of features below the map for screen-reader users.
- Maintain ≥ 3:1 contrast between feature colors and the basemap; the dark Protomaps/OpenFreeMap styles are tuned for this — verify if you swap palettes.

---

## Step 14 — Complete Example: City Explorer with 3D Buildings

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Paris — 3D Explorer</title>
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; padding: 24px; display: flex; flex-direction: column; align-items: center; }
    .card { width: 100%; max-width: 1100px; background: #1a1d27; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    .card-header { padding: 22px 24px 16px; border-bottom: 1px solid rgba(255,255,255,0.07); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.78rem; color: #64748b; margin-top: 3px; }
    .pills { display: flex; gap: 6px; flex-wrap: wrap; }
    .pill { background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); border-radius: 999px; padding: 6px 14px; font-size: 12px; cursor: pointer; transition: all 200ms cubic-bezier(0.16,1,0.3,1); }
    .pill:hover, .pill.active { background: rgba(99,102,241,0.2); border-color: rgba(99,102,241,0.5); color: #c7d2fe; transform: translateY(-1px); }
    #map { width: 100%; height: 560px; position: relative; }
    .hud {
      position: absolute; top: 16px; left: 16px; z-index: 1;
      background: rgba(26,29,39,0.85); backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
      padding: 10px 14px; font-size: 12px; color: #cbd5e1;
      box-shadow: 0 4px 16px rgba(0,0,0,0.4);
      pointer-events: none;
    }
    .hud b { color: #f1f5f9; font-variant-numeric: tabular-nums; }
    /* MapLibre dark UI */
    .maplibregl-ctrl-group { background: #1e2130 !important; border: 1px solid rgba(255,255,255,0.1) !important; }
    .maplibregl-ctrl-group button { background-color: #1e2130 !important; filter: invert(0.85); }
    .maplibregl-ctrl-group button:hover { background-color: #2d3148 !important; }
    .maplibregl-ctrl-attrib { background: rgba(15,17,23,0.75) !important; color: #475569 !important; font-size: 10px; }
    .maplibregl-ctrl-attrib a { color: #6366f1 !important; }
    .maplibregl-popup-content { background: #1e2130; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px 14px; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
    .maplibregl-popup-tip { border-top-color: #1e2130 !important; border-bottom-color: #1e2130 !important; }
  </style>
</head>
<body>
  <main class="card" role="region" aria-label="3D city explorer for Paris">
    <header class="card-header">
      <div>
        <h1>Paris — 3D Explorer</h1>
        <p class="sub">Drag · scroll-zoom · right-drag to tilt + rotate · click a landmark for details</p>
      </div>
      <nav class="pills" aria-label="Camera presets">
        <button class="pill active" data-target="eiffel">Eiffel Tower</button>
        <button class="pill" data-target="louvre">Louvre</button>
        <button class="pill" data-target="notredame">Notre-Dame</button>
        <button class="pill" data-target="defense">La Défense</button>
      </nav>
    </header>
    <div id="map" role="application" aria-label="Map of Paris with 3D buildings" tabindex="0">
      <div class="hud" id="hud">Zoom <b id="zoomLevel">15.0</b> · Pitch <b id="pitchLevel">55°</b></div>
    </div>
  </main>

  <script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
  <script>
    const ACCENT = '#6366f1';

    const LANDMARKS = {
      eiffel:    { center: [2.2945, 48.8584], zoom: 16, pitch: 60, bearing: -20, name: 'Eiffel Tower',     fact: 'Completed in 1889 — 330 m tall' },
      louvre:    { center: [2.3376, 48.8606], zoom: 16, pitch: 55, bearing: 18,  name: 'Musée du Louvre', fact: 'World\'s most-visited museum' },
      notredame: { center: [2.3499, 48.8530], zoom: 17, pitch: 55, bearing: -10, name: 'Notre-Dame',       fact: 'Gothic cathedral, 1163–1345' },
      defense:   { center: [2.2389, 48.8924], zoom: 15, pitch: 60, bearing: 30,  name: 'La Défense',       fact: 'Europe\'s largest business district' },
    };

    // Theme-aware style URLs — the basemap itself ships dark + light variants
    const STYLES = {
      dark:  'https://tiles.openfreemap.org/styles/dark',
      light: 'https://tiles.openfreemap.org/styles/positron',
      // or Protomaps: '…/styles/v4/dark/en.json?key=…' vs '…/styles/v4/light/en.json?key=…'
      // or MapTiler:  '…/maps/streets-dark-v2/style.json?key=…' vs '…/maps/streets-v2/style.json?key=…'
    };

    // Universal theme-detection pattern (CSS prefers-color-scheme + manual data-theme override)
    const themeQuery = window.matchMedia('(prefers-color-scheme: light)');
    function currentTheme() {
      return document.documentElement.dataset.theme
          || (themeQuery.matches ? 'light' : 'dark');
    }
    function onThemeChange(callback) {
      new MutationObserver(callback).observe(document.documentElement, {
        attributes: true, attributeFilter: ['data-theme'],
      });
      themeQuery.addEventListener('change', callback);
    }

    const map = new maplibregl.Map({
      container: 'map',
      style:     STYLES[currentTheme()],   // dark stays the default until OS/user says otherwise
      center:    LANDMARKS.eiffel.center,
      zoom:      LANDMARKS.eiffel.zoom,
      pitch:     LANDMARKS.eiffel.pitch,
      bearing:   LANDMARKS.eiffel.bearing,
      antialias: true,
      attributionControl: false,
    });

    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'top-right');
    map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-left');
    map.addControl(new maplibregl.AttributionControl({ compact: true, customAttribution: '© OpenFreeMap · OpenStreetMap' }), 'bottom-right');

    // Wrap layer additions so we can re-run them after setStyle() wipes them
    function addCustomLayers() {
      const labelLayer = map.getStyle().layers.find(l => l.type === 'symbol')?.id;

      map.addLayer({
        id: 'buildings-3d',
        type: 'fill-extrusion',
        source: 'openmaptiles',
        'source-layer': 'building',
        minzoom: 14,
        paint: {
          'fill-extrusion-color': [
            'interpolate', ['linear'], ['get', 'render_height'],
            0,   '#1f2330',
            20,  '#2a2f3d',
            50,  '#3730a3',
            120, '#6366f1',
            250, '#a5b4fc',
          ],
          'fill-extrusion-height': ['get', 'render_height'],
          'fill-extrusion-base':   ['get', 'render_min_height'],
          'fill-extrusion-opacity': 0.88,
          'fill-extrusion-vertical-gradient': true,
        },
      }, labelLayer);

      // Landmark markers
      const features = Object.entries(LANDMARKS).map(([id, l]) => ({
        type: 'Feature',
        properties: { id, name: l.name, fact: l.fact },
        geometry: { type: 'Point', coordinates: l.center },
      }));

      map.addSource('landmarks', { type: 'geojson', data: { type: 'FeatureCollection', features } });

      map.addLayer({
        id: 'landmark-glow', type: 'circle', source: 'landmarks',
        paint: { 'circle-radius': 22, 'circle-color': ACCENT, 'circle-opacity': 0.18, 'circle-blur': 0.6 },
      });
      map.addLayer({
        id: 'landmark-dots', type: 'circle', source: 'landmarks',
        paint: { 'circle-radius': 7, 'circle-color': ACCENT, 'circle-stroke-color': '#a5b4fc', 'circle-stroke-width': 2 },
      });

      map.on('click', 'landmark-dots', (e) => {
        const f = e.features[0];
        new maplibregl.Popup({ offset: 14, maxWidth: '240px' })
          .setLngLat(f.geometry.coordinates)
          .setHTML(`
            <div style="font-family:'Segoe UI',sans-serif;min-width:180px">
              <div style="font-weight:600;font-size:14px;color:#f1f5f9;margin-bottom:6px">${f.properties.name}</div>
              <div style="color:#94a3b8;font-size:12px">${f.properties.fact}</div>
            </div>`)
          .addTo(map);
      });
      map.on('mouseenter', 'landmark-dots', () => map.getCanvas().style.cursor = 'pointer');
      map.on('mouseleave', 'landmark-dots', () => map.getCanvas().style.cursor = '');
    }

    map.on('load', addCustomLayers);

    // Swap basemap whenever the page theme changes (data-theme attr or OS prefers-color-scheme)
    onThemeChange(() => {
      map.setStyle(STYLES[currentTheme()]);
      map.once('style.load', addCustomLayers);   // setStyle wipes custom sources/layers
    });

    // HUD live state
    const zoomEl  = document.getElementById('zoomLevel');
    const pitchEl = document.getElementById('pitchLevel');
    function syncHud() {
      zoomEl.textContent  = map.getZoom().toFixed(1);
      pitchEl.textContent = Math.round(map.getPitch()) + '°';
    }
    map.on('move',  syncHud);
    map.on('pitch', syncHud);

    // Preset pills
    document.querySelectorAll('.pill').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const t = LANDMARKS[btn.dataset.target];
        map.flyTo({ center: t.center, zoom: t.zoom, pitch: t.pitch, bearing: t.bearing, duration: 2200, essential: true, curve: 1.6 });
      });
    });

    // Keyboard shortcuts hint already in subtitle; ensure resize on container changes
    window.addEventListener('resize', () => map.resize());
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No height on `#map`** — without an explicit CSS height the WebGL canvas is 0px tall and you see a blank card
- **`[lat, lng]` instead of `[lng, lat]`** — MapLibre (and GeoJSON) use `[longitude, latitude]`. Coordinates that put markers in the ocean are almost always swapped
- **Forgetting to re-add layers after `setStyle()`** — `setStyle` replaces the whole style document; sources/layers must be re-added in the `style.load` callback
- **Loading the JS before the CSS** — markers and popups render unstyled / mis-positioned. Always put the CSS link in `<head>` before the script tag
- **Adding 3D extrusions on top of labels** — pass the first symbol layer id as the second argument of `addLayer()` so labels stay readable above buildings
- **Calling `map.addLayer()` before `load`** — until the style loads, the layer registry is unavailable. Wrap all initial layer code in `map.on('load', …)`
- **Missing `generateId: true` on GeoJSON for hover** — without a stable id, `setFeatureState` does nothing and hover highlight breaks silently
- **Using `MapLibre` capitalization or `mapboxgl` global** — the global is `maplibregl` (lowercase), not `MapLibre` or `mapboxgl`
- **Calling `map.resize()` never** — when the container is hidden then shown (tab, modal, CSS animation), you must call `map.resize()` or the canvas keeps its old size
- **Putting an API key in a shared artifact** — use a free, keyless basemap like OpenFreeMap, or a dev key with a strict origin allowlist
