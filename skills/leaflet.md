---
name: leaflet-maps
description: Create beautiful, interactive geographic maps using Leaflet.js v1.9, delivered as self-contained HTML artifacts. Use this skill whenever someone needs to display locations, draw routes or zones, visualize geographic data, build a store locator, map data points by region, show a choropleth, cluster markers, or render any spatial visualization on a real-world map — even without explicit mention of Leaflet. Trigger on requests like "show these locations on a map", "map this data by country", "draw this route", "create a heatmap of these coordinates", "build a store finder", or any request involving latitude/longitude, addresses, countries, or geographic distributions. Do NOT use for abstract network diagrams (→ vis-network), purely schematic flowcharts (→ mermaid-diagrams), or data charts without geographic context (→ charting skill).
---

# Leaflet Maps Skill — Interactive Geographic Maps

Leaflet is the leading open-source JavaScript mapping library. It is lightweight (~42KB), mobile-friendly, and extensible via a rich plugin ecosystem. It renders maps from any tile provider (OpenStreetMap, CartoDB, Esri…) and handles markers, popups, polygons, GeoJSON, clustering, heatmaps, and more.

---

## Artifact Presentation & Use Cases

Every Leaflet artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the map
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the map
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context and interaction hints
- **Map container** (`#map`, fixed height, rounded corners) renders the interactive tile-based map
- **Optional sidebar or legend** for filtering, search, or data display

### Typical use cases

- **Store/office locators** — markers with popups showing address, hours, and contact info
- **Choropleth maps** — GeoJSON regions colored by data values (population, GDP, scores)
- **Route visualization** — polylines showing paths, delivery routes, or hiking trails
- **Heatmaps** — density visualization of coordinate-based data (incidents, check-ins)
- **Cluster maps** — thousands of markers grouped dynamically by zoom level
- **Geofencing** — draw polygons, circles, or rectangles to define areas of interest

### What the user sees

An interactive map: drag to pan, scroll to zoom, click markers for detailed popups, toggle layer controls to switch between data views. The dark tile set (CartoDB Dark Matter) integrates seamlessly with the dark card wrapper.

---

## When to Use Leaflet vs. Alternatives

| Use Leaflet when… | Use another library when… |
|---|---|
| Tile-based maps with real-world geography | Abstract node-edge network graphs → **vis-network** |
| Markers, popups, polygons, GeoJSON | Schematic diagrams or flowcharts → **Mermaid** |
| Choropleth maps from GeoJSON data | Geographic choropleths via Plotly’s built-in geo → **Plotly** (simpler but less flexible) |
| 100+ interactive markers with clustering | Data charts (bar, line, pie) → **Chart.js / Plotly** |
| Route polylines, heatmaps, custom tile layers | Timeline or Gantt views → **vis-timeline** |
| Need full control: custom layers, projections | Quick thematic map without tile servers → **D3** (with `d3-geo`) |

> **Rule of thumb:** if the visualization involves real-world coordinates and the user needs to pan/zoom on a base map, use Leaflet. For abstract geographic projections without tiles, D3 may be simpler.

---

## Step 1 — CDN Setup

Leaflet requires **both** a CSS file and a JS file, loaded in the right order.

```html
<!-- 1. CSS in <head> — BEFORE the JS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">

<!-- 2. Leaflet JS — before your script, at end of <body> -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
```

### Optional plugins (load after leaflet.js)
```html
<!-- Marker clustering — group nearby markers automatically -->
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

<!-- Heatmap layer -->
<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
```

> **⚠️ Critical:** The `#map` container **must have an explicit CSS height** (e.g., `height: 500px`). If the container has `height: 0` or `height: auto`, the map renders as a blank space. This is the most common Leaflet mistake.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Map</title>

  <!-- 1. Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">

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
      max-width: 1000px;
      background: #1a1d27;
      border-radius: 16px;
      overflow: hidden;       /* clips the map to rounded corners */
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 22px 24px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
    }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }

    /* REQUIRED: map container must have explicit height */
    #map { width: 100%; height: 520px; }

    /* Leaflet UI dark overrides */
    .leaflet-control-zoom a { background: #1e2130 !important; color: #e2e8f0 !important; border-color: rgba(255,255,255,0.15) !important; }
    .leaflet-control-zoom a:hover { background: #2d3148 !important; }
    .leaflet-control-attribution { background: rgba(15,17,23,0.7) !important; color: #475569 !important; }
    .leaflet-control-attribution a { color: #6366f1 !important; }
    .leaflet-popup-content-wrapper { background: #1e2130; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 20px rgba(0,0,0,0.5); border-radius: 10px; }
    .leaflet-popup-tip { background: #1e2130; }
  </style>
</head>
<body>
  <div class="card">
    <div class="card-header">
      <h1>Map Title</h1>
      <p class="sub">Brief description</p>
    </div>
    <div id="map"></div>
  </div>

  <!-- 2. Leaflet JS — after the #map div -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
  <script>
    // All Leaflet code here
  </script>
</body>
</html>
```

---

## Step 3 — Map Initialization

```javascript
const map = L.map('map', {
  center:    [48.8566, 2.3522],  // [lat, lng] — Paris
  zoom:      12,                 // 0 (world) → 19 (street level)
  minZoom:   2,
  maxZoom:   18,
  zoomControl: true,             // show +/- buttons
  scrollWheelZoom: true,         // zoom with mouse wheel
  dragging:  true,               // pan by dragging
  doubleClickZoom: true,
});

// Programmatic navigation
map.setView([51.505, -0.09], 13);   // move to London, zoom 13
map.setZoom(10);
map.panTo([48.85, 2.35]);
map.flyTo([48.85, 2.35], 13, { duration: 1.5 });   // animated fly-to
map.fitBounds([[51.5, -0.09], [48.85, 2.35]]);      // fit view to bbox
```

---

## Step 4 — Tile Providers

Every map needs a tile layer. Always include an attribution string.

```javascript
// OpenStreetMap — free, no key required (most common)
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom:     19,
  attribution: '© <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// CartoDB Positron — light, minimal, great for data overlays
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '© <a href="https://carto.com">CARTO</a>',
  subdomains:  'abcd',
  maxZoom:     19,
}).addTo(map);

// CartoDB Dark Matter — dark theme, elegant for night maps
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '© <a href="https://carto.com">CARTO</a>',
  subdomains:  'abcd',
  maxZoom:     19,
}).addTo(map);

// CartoDB Voyager — colorful, readable labels
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
  attribution: '© <a href="https://carto.com">CARTO</a>',
  subdomains:  'abcd',
  maxZoom:     19,
}).addTo(map);

// OpenTopoMap — terrain/topographic
L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
  attribution: '© <a href="https://opentopomap.org">OpenTopoMap</a>',
  maxZoom:     17,
}).addTo(map);
```

**Tile provider choice guide:**
| Context | Recommended tile |
|---|---|
| Data visualization, clean background | CartoDB Positron (light) or Dark Matter |
| Dark-themed artifact | CartoDB Dark Matter |
| General reference map | OpenStreetMap |
| Outdoor / hiking | OpenTopoMap |
| City/transit detail | OpenStreetMap |

---

## Step 5 — Markers, Popups & Tooltips

```javascript
// Default blue marker
const marker = L.marker([48.8566, 2.3522]).addTo(map);

// With popup (opens on click)
marker.bindPopup('<b>Paris</b><br>Capital of France').openPopup();

// With tooltip (shows on hover)
marker.bindTooltip('Paris', { direction: 'top', offset: [0, -10] });

// Custom DivIcon (HTML/CSS marker — most flexible)
const customIcon = L.divIcon({
  className: '',   // remove default white square
  html: `
    <div style="
      background:#6366f1; color:#fff; border-radius:50%;
      width:32px; height:32px; display:flex; align-items:center;
      justify-content:center; font-weight:700; font-size:13px;
      box-shadow: 0 2px 8px rgba(99,102,241,0.6);
    ">42</div>`,
  iconSize:   [32, 32],
  iconAnchor: [16, 16],   // center bottom of icon aligns to lat/lng
  popupAnchor:[0, -16],
});
L.marker([48.85, 2.35], { icon: customIcon }).addTo(map)
  .bindPopup('<b>Custom marker</b>');

// Draggable marker
const draggable = L.marker([48.86, 2.34], { draggable: true }).addTo(map);
draggable.on('dragend', (e) => {
  const pos = e.target.getLatLng();
  console.log(`Dropped at ${pos.lat.toFixed(4)}, ${pos.lng.toFixed(4)}`);
});

// Rich HTML popup
marker.bindPopup(`
  <div style="font-family:'Segoe UI',sans-serif;min-width:160px">
    <div style="font-weight:600;font-size:14px;margin-bottom:6px">Location Name</div>
    <div style="color:#94a3b8;font-size:12px">Category: Retail</div>
    <div style="color:#94a3b8;font-size:12px">Revenue: $1.2M</div>
    <a href="#" style="color:#6366f1;font-size:12px;display:block;margin-top:8px">View details →</a>
  </div>
`, { maxWidth: 240 });

// Programmatic popup (no marker)
L.popup()
  .setLatLng([48.87, 2.33])
  .setContent('<p>A standalone popup</p>')
  .openOn(map);
```

---

## Step 6 — Shapes: Circles, Polylines, Polygons

```javascript
// Circle (radius in meters)
L.circle([48.85, 2.35], {
  radius:      500,
  color:       '#6366f1',
  weight:      2,
  fillColor:   '#6366f1',
  fillOpacity: 0.2,
}).addTo(map).bindPopup('500m radius');

// Polyline (route / path)
const route = L.polyline([
  [48.8566, 2.3522],
  [48.8606, 2.3376],
  [48.8738, 2.2950],
], {
  color:     '#6366f1',
  weight:    4,
  opacity:   0.85,
  dashArray: null,       // '5,10' for dashed line
  lineCap:   'round',
  lineJoin:  'round',
}).addTo(map);

map.fitBounds(route.getBounds(), { padding: [40, 40] });

// Polygon (zone / region)
const zone = L.polygon([
  [48.87, 2.30],
  [48.87, 2.40],
  [48.82, 2.40],
  [48.82, 2.30],
], {
  color:       '#f97316',
  weight:      2,
  fillColor:   '#f97316',
  fillOpacity: 0.15,
}).addTo(map).bindPopup('Zone A');

// Rectangle
L.rectangle([[48.82, 2.30], [48.87, 2.40]], {
  color: '#06b6d4', weight: 2, fillOpacity: 0.1,
}).addTo(map);
```

---

## Step 7 — GeoJSON Layers

GeoJSON is the standard format for geographic features. Leaflet renders it natively.

```javascript
const geojsonData = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [2.3522, 48.8566] }, // lng, lat (GeoJSON is lon/lat!)
      properties: { name: 'Paris', population: 2161000, country: 'FR' },
    },
    {
      type: 'Feature',
      geometry: {
        type: 'Polygon',
        coordinates: [[[2.22, 48.90], [2.47, 48.90], [2.47, 48.80], [2.22, 48.80], [2.22, 48.90]]],
      },
      properties: { name: 'Île-de-France', density: 1021 },
    },
  ],
};

L.geoJSON(geojsonData, {

  // Style polygons/lines
  style: (feature) => ({
    color:       '#6366f1',
    weight:      2,
    fillOpacity: feature.properties.density > 500 ? 0.5 : 0.2,
    fillColor:   feature.properties.density > 500 ? '#6366f1' : '#94a3b8',
  }),

  // Custom marker for point features
  pointToLayer: (feature, latlng) => {
    return L.circleMarker(latlng, {
      radius:      8,
      fillColor:   '#6366f1',
      color:       '#818cf8',
      weight:      2,
      fillOpacity: 0.9,
    });
  },

  // Bind popup to each feature
  onEachFeature: (feature, layer) => {
    if (feature.properties) {
      layer.bindPopup(`<b>${feature.properties.name}</b>`);
      layer.on('mouseover', () => layer.openPopup());
      layer.on('mouseout',  () => layer.closePopup());
    }
  },

}).addTo(map);
```

> **GeoJSON coordinate order:** GeoJSON uses `[longitude, latitude]`, which is the **opposite** of Leaflet's `[latitude, longitude]`. This is a very common source of bugs.

---

## Step 8 — Choropleth Maps (color by value)

A choropleth colors regions based on a data value — the most common geographic data viz.

```javascript
// Color scale function
function getColor(value) {
  return value > 1000 ? '#1e3a8a'
       : value > 500  ? '#1d4ed8'
       : value > 200  ? '#3b82f6'
       : value > 100  ? '#60a5fa'
       : value > 50   ? '#93c5fd'
                      : '#dbeafe';
}

L.geoJSON(countriesGeoJSON, {
  style: (feature) => ({
    fillColor:   getColor(feature.properties.value),
    weight:      1,
    opacity:     1,
    color:       'rgba(255,255,255,0.3)',
    fillOpacity: 0.8,
  }),
  onEachFeature: (feature, layer) => {
    // Highlight on hover
    layer.on({
      mouseover: (e) => {
        e.target.setStyle({ weight: 2, fillOpacity: 1, color: '#fff' });
        e.target.bringToFront();
      },
      mouseout: (e) => {
        geoJsonLayer.resetStyle(e.target);
      },
      click: (e) => {
        map.fitBounds(e.target.getBounds(), { padding: [40, 40] });
        e.target.bindPopup(`<b>${feature.properties.name}</b><br>Value: ${feature.properties.value}`).openPopup();
      },
    });
  },
}).addTo(map);

// Legend control
const legend = L.control({ position: 'bottomright' });
legend.onAdd = () => {
  const div = L.DomUtil.create('div');
  div.style.cssText = 'background:#1e2130;padding:12px 16px;border-radius:8px;color:#e2e8f0;font-size:12px;line-height:1.6';
  div.innerHTML = '<strong style="display:block;margin-bottom:8px">Value</strong>';
  [1000, 500, 200, 100, 50, 0].forEach(grade => {
    div.innerHTML += `<span style="display:inline-block;width:14px;height:14px;background:${getColor(grade + 1)};border-radius:2px;margin-right:6px;vertical-align:middle"></span>${grade}+<br>`;
  });
  return div;
};
legend.addTo(map);
```

---

## Step 9 — Marker Clustering

When displaying many markers, clustering groups nearby ones to avoid visual overload. Requires the `leaflet.markercluster` plugin.

```javascript
// CDN (loaded in <head>):
// <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
// <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">
// <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

const clusters = L.markerClusterGroup({
  maxClusterRadius:      60,    // px — max radius for a cluster
  showCoverageOnHover:   false, // don't show cluster bounds on hover
  zoomToBoundsOnClick:   true,  // zoom in to cluster on click
  disableClusteringAtZoom: 15,  // stop clustering at high zoom
  iconCreateFunction: (cluster) => {
    const count = cluster.getChildCount();
    const size  = count > 100 ? 44 : count > 10 ? 38 : 32;
    return L.divIcon({
      className: '',
      html: `<div style="
        background:#6366f1; color:#fff; border-radius:50%;
        width:${size}px; height:${size}px;
        display:flex; align-items:center; justify-content:center;
        font-weight:700; font-size:${size > 38 ? 14 : 12}px;
        box-shadow:0 2px 12px rgba(99,102,241,0.5);
      ">${count}</div>`,
      iconSize: [size, size],
      iconAnchor: [size/2, size/2],
    });
  },
});

// Add markers to the cluster group (not directly to map)
points.forEach(pt => {
  L.marker([pt.lat, pt.lng])
    .bindPopup(`<b>${pt.name}</b>`)
    .addTo(clusters);
});

clusters.addTo(map);
```

---

## Step 10 — Heatmap Layer

Renders density/intensity of point data as a smooth heatmap. Requires `leaflet.heat`.

```javascript
// CDN: <script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>

// Data format: [lat, lng, intensity]  (intensity 0.0–1.0)
const heatData = [
  [48.87, 2.35, 0.9],
  [48.86, 2.34, 0.7],
  [48.85, 2.33, 0.5],
  // ... hundreds of points
];

const heat = L.heatLayer(heatData, {
  radius:   25,     // each point's influence radius (px)
  blur:     15,     // blur amount
  maxZoom:  17,     // zoom at which points reach max intensity
  max:      1.0,    // max intensity value
  gradient: {       // custom color scale (value → color)
    0.0: '#0f172a',
    0.3: '#1d4ed8',
    0.6: '#7c3aed',
    0.8: '#ec4899',
    1.0: '#fbbf24',
  },
}).addTo(map);

// Update data live
heat.setLatLngs(newHeatData);
heat.redraw();
```

---

## Step 11 — Layer Control (toggle layers)

```javascript
// Base layers — mutually exclusive (radio buttons)
const osm   = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',   { attribution: '© OpenStreetMap', maxZoom: 19 });
const carto = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { attribution: '© CARTO', subdomains: 'abcd' });
carto.addTo(map);   // default

// Overlay layers — toggleable (checkboxes)
const markersLayer = L.layerGroup([/* markers */]);
const zonesLayer   = L.layerGroup([/* polygons */]);
markersLayer.addTo(map);
zonesLayer.addTo(map);

// Layer control widget
L.control.layers(
  { 'OpenStreetMap': osm, 'CartoDB Dark': carto },                        // base layers
  { 'Locations': markersLayer, 'Zones': zonesLayer },                      // overlays
  { position: 'topright', collapsed: false }
).addTo(map);
```

---

## Step 12 — Events

```javascript
// Map events
map.on('click',    (e) => console.log(e.latlng));
map.on('dblclick', (e) => map.setZoom(map.getZoom() + 1));
map.on('zoom',     ()  => console.log('Zoom:', map.getZoom()));
map.on('moveend',  ()  => {
  const center = map.getCenter();
  const bounds = map.getBounds();
});
map.on('contextmenu', (e) => {
  e.originalEvent.preventDefault();
  L.popup().setLatLng(e.latlng).setContent('Right-clicked!').openOn(map);
});

// Marker events
marker.on('click',    (e) => {});
marker.on('mouseover',(e) => marker.openPopup());
marker.on('mouseout', (e) => marker.closePopup());
marker.on('dragend',  (e) => console.log(e.target.getLatLng()));

// Useful map methods
map.getCenter();          // LatLng of map center
map.getZoom();            // current zoom level
map.getBounds();          // LatLngBounds of visible area
map.latLngToLayerPoint([lat, lng]);   // convert to pixel coordinates
map.layerPointToLatLng(point);        // convert from pixel coordinates
map.invalidateSize();     // call if map container was resized
```

---

## Step 13 — Design & Polish Guidelines

- **Always call `map.invalidateSize()`** after the map container changes size (e.g., tab shown, modal opened, CSS transition ends) — otherwise tiles don't load for the new size
- **Fit bounds instead of hardcoding center/zoom** — use `map.fitBounds(layer.getBounds(), { padding: [40, 40] })` so the map auto-centers on the data
- **Use `L.layerGroup()` or `L.featureGroup()`** to manage multiple markers/shapes as a unit; you can then call `.clearLayers()` to remove all at once
- **GeoJSON coordinate order** — `[longitude, latitude]` in GeoJSON, `[latitude, longitude]` in Leaflet. Never confuse them. Tip: if the map is blank or markers appear in the ocean, the coords are probably swapped
- **Clustering for >50 markers** — `leaflet.markercluster` prevents visual overload and dramatically improves performance
- **Attribution is required** — OpenStreetMap, CartoDB, and most tile providers require attribution in the map. Omitting it violates their terms of service
- **Use `L.divIcon()` for custom markers** — custom icons via `L.icon()` require image files; `L.divIcon()` is pure HTML/CSS and works in self-contained artifacts
- **Avoid `zIndexOffset` on many markers** — managing z-index across hundreds of markers degrades performance; use layerGroups and `bringToFront()` on individual layers instead

---

## Step 14 — Complete Example: Interactive Store Locator

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Store Locator</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 24px; }
    .card { width: 100%; max-width: 1000px; background: #1a1d27; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    .card-header { padding: 22px 24px 16px; border-bottom: 1px solid rgba(255,255,255,0.07); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.78rem; color: #64748b; margin-top: 3px; }
    .filters { display: flex; gap: 8px; }
    .filter-btn { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; border-radius: 6px; padding: 5px 12px; font-size: 12px; cursor: pointer; transition: all 0.15s; }
    .filter-btn:hover, .filter-btn.active { background: rgba(99,102,241,0.2); border-color: rgba(99,102,241,0.5); color: #a5b4fc; }
    #map { width: 100%; height: 520px; }
    /* Leaflet dark overrides */
    .leaflet-control-zoom a { background: #1e2130 !important; color: #e2e8f0 !important; border-color: rgba(255,255,255,0.12) !important; }
    .leaflet-control-zoom a:hover { background: #2d3148 !important; }
    .leaflet-control-attribution { background: rgba(15,17,23,0.75) !important; color: #475569 !important; }
    .leaflet-control-attribution a { color: #6366f1 !important; }
    .leaflet-popup-content-wrapper { background: #1e2130; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 8px 32px rgba(0,0,0,0.5); border-radius: 10px; }
    .leaflet-popup-tip { background: #1e2130; }
    .leaflet-popup-content { margin: 14px 16px; }
  </style>
</head>
<body>
<div class="card">
  <div class="card-header">
    <div>
      <h1>European Store Network</h1>
      <p class="sub" id="sub">Loading stores…</p>
    </div>
    <div class="filters">
      <button class="filter-btn active" data-type="all">All</button>
      <button class="filter-btn" data-type="flagship">Flagship</button>
      <button class="filter-btn" data-type="standard">Standard</button>
      <button class="filter-btn" data-type="outlet">Outlet</button>
    </div>
  </div>
  <div id="map"></div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
<script>
  const stores = [
    { name:'Paris Flagship',    lat:48.8723, lng:2.3325,  type:'flagship', revenue:'€4.2M', staff:48 },
    { name:'Paris Outlet',      lat:48.8280, lng:2.3780,  type:'outlet',   revenue:'€1.1M', staff:12 },
    { name:'Lyon Standard',     lat:45.7640, lng:4.8357,  type:'standard', revenue:'€2.1M', staff:24 },
    { name:'Marseille Flagship',lat:43.2965, lng:5.3698,  type:'flagship', revenue:'€3.8M', staff:42 },
    { name:'Berlin Flagship',   lat:52.5200, lng:13.4050, type:'flagship', revenue:'€5.1M', staff:55 },
    { name:'Berlin Outlet',     lat:52.4770, lng:13.4020, type:'outlet',   revenue:'€1.4M', staff:15 },
    { name:'Munich Standard',   lat:48.1351, lng:11.5820, type:'standard', revenue:'€2.8M', staff:28 },
    { name:'Amsterdam Flagship',lat:52.3676, lng:4.9041,  type:'flagship', revenue:'€3.2M', staff:36 },
    { name:'Brussels Standard', lat:50.8503, lng:4.3517,  type:'standard', revenue:'€1.7M', staff:19 },
    { name:'Madrid Flagship',   lat:40.4168, lng:-3.7038, type:'flagship', revenue:'€4.7M', staff:50 },
    { name:'Barcelona Standard',lat:41.3851, lng:2.1734,  type:'standard', revenue:'€2.5M', staff:26 },
    { name:'Rome Standard',     lat:41.9028, lng:12.4964, type:'standard', revenue:'€2.2M', staff:22 },
  ];

  const TYPE_STYLES = {
    flagship: { bg: '#6366f1', border: '#818cf8', label: 'Flagship' },
    standard: { bg: '#06b6d4', border: '#67e8f9', label: 'Standard' },
    outlet:   { bg: '#f97316', border: '#fdba74', label: 'Outlet'   },
  };

  const map = L.map('map').setView([48.5, 7.5], 5);

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '© <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors, © <a href="https://carto.com">CARTO</a>',
    subdomains: 'abcd', maxZoom: 19,
  }).addTo(map);

  function makeIcon(type) {
    const s = TYPE_STYLES[type];
    return L.divIcon({
      className: '',
      html: `<div style="background:${s.bg};border:2px solid ${s.border};border-radius:50%;width:28px;height:28px;box-shadow:0 2px 8px ${s.bg}88"></div>`,
      iconSize: [28, 28], iconAnchor: [14, 14], popupAnchor: [0, -14],
    });
  }

  function makePopup(store) {
    const s = TYPE_STYLES[store.type];
    return `
      <div style="min-width:170px">
        <span style="background:${s.bg}22;color:${s.bg};padding:2px 8px;border-radius:999px;font-size:10px;font-weight:700;text-transform:uppercase">${s.label}</span>
        <div style="font-weight:600;font-size:14px;margin:8px 0 4px">${store.name}</div>
        <div style="color:#94a3b8;font-size:12px">Revenue: <b style="color:#e2e8f0">${store.revenue}</b></div>
        <div style="color:#94a3b8;font-size:12px">Staff: <b style="color:#e2e8f0">${store.staff}</b></div>
      </div>`;
  }

  let clusterGroup = null;

  function renderStores(filter) {
    if (clusterGroup) map.removeLayer(clusterGroup);

    clusterGroup = L.markerClusterGroup({
      showCoverageOnHover: false,
      maxClusterRadius:    50,
      iconCreateFunction: (cluster) => {
        const n = cluster.getChildCount();
        return L.divIcon({
          className: '',
          html: `<div style="background:#6366f1;color:#fff;border-radius:50%;width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;box-shadow:0 2px 12px rgba(99,102,241,0.5)">${n}</div>`,
          iconSize: [36, 36], iconAnchor: [18, 18],
        });
      },
    });

    const visible = stores.filter(s => filter === 'all' || s.type === filter);
    visible.forEach(store => {
      L.marker([store.lat, store.lng], { icon: makeIcon(store.type) })
        .bindPopup(makePopup(store), { maxWidth: 220 })
        .addTo(clusterGroup);
    });

    clusterGroup.addTo(map);
    document.getElementById('sub').textContent = `${visible.length} store${visible.length !== 1 ? 's' : ''} shown`;
  }

  // Filter buttons
  let activeFilter = 'all';
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeFilter = btn.dataset.type;
      renderStores(activeFilter);
    });
  });

  renderStores('all');
</script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No height on the map container** — `<div id="map">` with no CSS height renders as 0px: the map is invisible. Always set an explicit `height` in CSS
- **GeoJSON lon/lat reversal** — GeoJSON uses `[longitude, latitude]`; Leaflet uses `[latitude, longitude]`. A marker in the ocean or Atlantic is almost always a swapped coordinate
- **Loading plugins before leaflet.js** — `leaflet.markercluster` and `leaflet.heat` must be loaded **after** `leaflet.js`; they extend the `L` global which must already exist
- **`map.invalidateSize()` not called on resize** — if the map container changes size after init (tab switch, modal, layout change), call `map.invalidateSize()` or tiles won't fill the new area
- **Adding markers directly to map when clustering** — with `markerClusterGroup`, add markers to the **cluster group**, not to the map directly: `marker.addTo(clusters)` not `marker.addTo(map)`
- **Missing attribution** — OpenStreetMap and CartoDB require attribution by their licenses. The `attribution` option in `L.tileLayer()` is not optional
- **`L.icon()` with image URLs in self-contained artifacts** — use `L.divIcon()` for pure HTML/CSS icons that work without external image files
- **Not destroying the map on re-render** — if recreating the map in the same container, call `map.remove()` first, otherwise Leaflet throws "Map container is already initialized"
