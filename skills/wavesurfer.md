---
name: wavesurfer-audio
description: Build polished, interactive audio waveform visualisations using wavesurfer.js v7, delivered as self-contained HTML artifacts. Use this skill whenever someone needs to display, scrub, or annotate audio in the browser: podcast players, music players, audio editors, voice-note review, clip selection, region annotation, speech-to-text alignment, spectrograms, or any waveform UI — even without explicit mention of wavesurfer. Trigger on phrases like "audio player", "podcast player", "waveform", "music visualiser", "audio annotation", "trim audio", "select clip", "spectrogram", "audio scrubber", or anything involving mp3/wav/ogg/m4a/blob audio playback with a visual representation. Do NOT use for: pure synthesis or instruments (→ tone-audio skill), video playback (use the native `<video>` element), or non-audio time-series charts (→ chartjs / plotly skills).
agents: [dev]
---

# wavesurfer.js Skill — v7 (Audio Waveform Player & Editor)

wavesurfer.js v7 is a modern, dependency-free audio-waveform library built on the Web Audio API and Canvas. It renders waveforms, scrubs frame-perfectly, supports plugins for regions / timeline / minimap / spectrogram, and ships as a single ES module from UNPKG.

---

## Artifact Presentation & Use Cases

Every wavesurfer artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) frames the player
- **Title** (`h1`, 1.15rem, `#f1f5f9`) names the track or session
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) shows artist / duration / interaction hints
- **Waveform container** (`#waveform`, fixed height, transparent background) hosts the canvas
- **Optional timeline strip** above or below the waveform
- **Transport bar** with Play/Pause, Skip, time read-out, and a volume control

### Typical use cases

- **Podcast players** — waveform scrubber with chapter regions and current time
- **Music visualisers** — waveform + minimap for navigating long tracks
- **Audio annotation tools** — draggable regions to mark phrases, errors, or beats
- **Voice-note review** — speed control, looped regions, comment markers
- **Audio editors (UI-only)** — region selection, zoom, marker creation
- **Speech / transcript alignment** — synchronised highlight as audio plays
- **Spectrogram analyzers** — frequency view stacked with the waveform

### What the user sees

A polished waveform with a coloured progress overlay, a draggable progress cursor, clickable timeline ticks, optional regions in transparent colour swatches, and a transport bar. Click anywhere on the wave to jump; drag a region edge to resize; scroll horizontally on the minimap.

---

## When to Use wavesurfer vs. Alternatives

| Use wavesurfer when… | Use another library when… |
|---|---|
| You need to **render** a waveform from audio | You only need to **play** audio → `<audio controls>` |
| Scrub / seek by clicking the waveform | Synthesise sounds or instruments → **Tone.js** |
| Mark regions, chapters, comments on audio | Multi-track sequencer / DAW UI → custom + **Tone.js** |
| Show spectrogram or minimap | Real-time microphone visualiser only → raw Web Audio + Canvas |
| Audio annotation / transcript alignment | Plot generic time-series data → **Chart.js** |
| Podcast / music player UI | Video player → native `<video>` |

> **Rule of thumb:** if the artifact contains a visible waveform of recorded audio, use wavesurfer. If it produces sound rather than visualising it, use Tone.js.

---

## Step 1 — CDN Setup (ES Module)

wavesurfer v7 ships only as ESM. Use a `<script type="module">` with named imports.

```html
<script type="module">
  import WaveSurfer       from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js';
  import RegionsPlugin    from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/regions.esm.js';
  import TimelinePlugin   from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/timeline.esm.js';
  import MinimapPlugin    from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/minimap.esm.js';
  import SpectrogramPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/spectrogram.esm.js';

  // App code here…
</script>
```

> **Critical:** v7 is ESM-only. The legacy `<script src="…wavesurfer.min.js">` UMD tag does **not** work — you will get `WaveSurfer is not defined`. Always use `type="module"` and `import`.

> **Autoplay policy:** Most browsers block audio until the user interacts. Bind playback to a click / keypress rather than calling `wavesurfer.play()` automatically on load.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Audio Player</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117; color: #e2e8f0;
      display: flex; flex-direction: column; align-items: center;
      min-height: 100vh; padding: 24px;
    }
    .card {
      width: 100%; max-width: 900px;
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 16px; overflow: hidden;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 20px 24px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
    }
    h1 { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
    p.sub { font-size: 0.8rem; color: #64748b; margin-top: 3px; }

    /* REQUIRED: waveform container needs height */
    #waveform { width: 100%; height: 128px; padding: 12px 20px; }
    #timeline { padding: 0 20px; }
  </style>
</head>
<body>
  <main class="card" aria-labelledby="title">
    <header class="card-header">
      <h1 id="title">Track Title</h1>
      <p class="sub">Artist · Click waveform to scrub · Space to play/pause</p>
    </header>
    <div id="waveform" role="slider" aria-label="Audio waveform — click to scrub" aria-valuemin="0" aria-valuemax="100"></div>
    <div id="timeline"></div>
  </main>

  <script type="module">
    // wavesurfer code here
  </script>
</body>
</html>
```

---

## Step 3 — Themes (dark + light)

wavesurfer accepts colour options directly. Define both palettes once and switch them at runtime via `setOptions`.

### Theme token reference

| Token | Dark | Light |
|---|---|---|
| Page background | `#0f1117` | `#f8fafc` |
| Card background | `#1a1d27` | `#ffffff` |
| Border | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` |
| Text | `#e2e8f0` | `#1e293b` |
| Muted | `#94a3b8` | `#475569` |
| Accent | `#6366f1` | `#6366f1` |
| `waveColor`       | `#475569` | `#cbd5e1` |
| `progressColor`   | `#6366f1` | `#6366f1` |
| `cursorColor`     | `#f1f5f9` | `#1e293b` |

```javascript
const THEMES = {
  dark: {
    waveColor:     '#475569',
    progressColor: '#6366f1',
    cursorColor:   '#f1f5f9',
  },
  light: {
    waveColor:     '#cbd5e1',
    progressColor: '#6366f1',
    cursorColor:   '#1e293b',
  },
};

// Live switch
let dark = true;
themeBtn.addEventListener('click', () => {
  dark = !dark;
  ws.setOptions(dark ? THEMES.dark : THEMES.light);
  document.body.style.background = dark ? '#0f1117' : '#f8fafc';
  document.body.style.color      = dark ? '#e2e8f0' : '#1e293b';
  themeBtn.setAttribute('aria-pressed', String(!dark));
});
```

---

## Step 4 — Creating an Instance

```javascript
import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js';

const ws = WaveSurfer.create({
  container:     '#waveform',
  url:           'https://example.com/audio.mp3',
  waveColor:     '#475569',
  progressColor: '#6366f1',
  cursorColor:   '#f1f5f9',
  cursorWidth:   2,

  barWidth:    2,         // 0 = solid wave, > 0 = bar style
  barGap:      2,
  barRadius:   2,
  height:      120,
  normalize:   true,      // scale peaks to fill height
  fillParent:  true,      // stretch to container width
  minPxPerSec: 50,        // zoom factor (px per second)

  autoplay:    false,
  mediaControls: false,   // hide native HTML5 controls
  interact:    true,      // allow click-to-seek
  hideScrollbar: false,
});

// Re-emit when the audio is ready (peaks computed)
ws.on('ready', () => console.log('Duration:', ws.getDuration().toFixed(2), 's'));
ws.on('error', (err) => console.error('Load error:', err));
```

### Useful events

```javascript
ws.on('ready',     ()        => {});                          // peaks computed
ws.on('play',      ()        => {});
ws.on('pause',     ()        => {});
ws.on('finish',    ()        => {});                          // playback reached end
ws.on('audioprocess', (t)    => updateTimeDisplay(t));        // current time during playback
ws.on('seeking',   (t)       => {});                          // user clicked / dragged
ws.on('interaction', (t)     => {});                          // click on waveform
ws.on('decode',    (duration)=> {});                          // audio decoded
ws.on('loading',   (percent) => loaderBar.style.width = percent + '%');
ws.on('zoom',      (px)      => {});

// Cleanup
ws.destroy();
```

---

## Step 5 — Loading Audio (URL, File, or Blob)

```javascript
// 1. URL (CORS-enabled host) — easiest
ws.load('https://example.com/track.mp3');

// 2. URL + pre-computed peaks — fast, no decode required
ws.load('https://example.com/track.mp3', [[/* normalized peaks 0..1 */]], duration);

// 3. Blob from a file input
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  const blobUrl = URL.createObjectURL(file);
  ws.load(blobUrl);
});

// 4. Drag-and-drop
dropZone.addEventListener('dragover', e => e.preventDefault());
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  ws.load(URL.createObjectURL(e.dataTransfer.files[0]));
});

// 5. Recorded MediaStream blob
ws.loadBlob(audioBlob);
```

> **CORS:** `wavesurfer.load(url)` fetches the file to compute peaks. If the audio host does not send `Access-Control-Allow-Origin`, decoding fails. Use a CORS-enabled CDN (e.g. `https://www.mfiles.co.uk/`, your own bucket), or supply pre-computed peaks.

---

## Step 6 — Playback Controls

```javascript
ws.play();
ws.pause();
ws.playPause();          // toggle
ws.stop();               // pause + seek to 0
ws.isPlaying();          // → boolean

ws.setTime(15.5);        // seek to 15.5s (absolute seconds)
ws.seekTo(0.5);          // seek to 50 % of duration (0..1)
ws.skip(5);              // skip +5s (negative for backward)

ws.getCurrentTime();     // → seconds
ws.getDuration();        // → seconds

ws.setVolume(0.6);       // 0..1
ws.setMuted(true);
ws.setPlaybackRate(1.5); // 0.25..4 — playback speed (1 = normal)

// Zoom (px per second)
ws.zoom(150);
```

### Keyboard shortcuts (recommended)

```javascript
document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT') return;
  if (e.code === 'Space')      { e.preventDefault(); ws.playPause(); }
  if (e.code === 'ArrowLeft')  { ws.skip(-5); }
  if (e.code === 'ArrowRight') { ws.skip(5); }
  if (e.code === 'KeyM')       { ws.setMuted(!ws.getMuted()); }
});
```

---

## Step 7 — Regions Plugin (clip selection, chapters, annotations)

```javascript
import RegionsPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/regions.esm.js';

const regions = ws.registerPlugin(RegionsPlugin.create());

ws.on('decode', () => {
  // Static regions / chapters
  regions.addRegion({
    start:   12, end: 38,
    content: 'Intro',
    color:   'rgba(99,102,241,0.18)',
    drag:    false, resize: false,
  });
  regions.addRegion({
    start:   42, end: 78,
    content: 'Chorus',
    color:   'rgba(236,72,153,0.18)',
    drag:    true,  resize: true,
  });

  // Single marker
  regions.addRegion({
    start: 100, content: 'Drop ▼', color: '#f97316',
  });
});

// Click-and-drag to draw new regions
regions.enableDragSelection({ color: 'rgba(34,197,94,0.18)' });

// Region events
regions.on('region-created',     (r) => console.log('Created', r.id));
regions.on('region-updated',     (r) => console.log('Updated', r.start, r.end));
regions.on('region-clicked',     (r, e) => { e.stopPropagation(); r.play(); });
regions.on('region-double-clicked', (r) => r.remove());
regions.on('region-in',          (r) => console.log('Entered', r.content));
regions.on('region-out',         (r) => console.log('Left', r.content));

// Loop a region
let loopRegion = null;
regions.on('region-clicked', (r) => { loopRegion = r; r.play(); });
ws.on('timeupdate', (t) => {
  if (loopRegion && t >= loopRegion.end) ws.setTime(loopRegion.start);
});
```

---

## Step 8 — Timeline Plugin

```javascript
import TimelinePlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/timeline.esm.js';

ws.registerPlugin(TimelinePlugin.create({
  container:        '#timeline',     // empty div under the waveform
  height:           20,
  timeInterval:     5,                // major tick every 5 s
  primaryLabelInterval: 30,           // big label every 30 s
  secondaryLabelInterval: 5,
  style: {
    fontSize:   '10px',
    color:      '#64748b',
    fontFamily: 'ui-monospace, monospace',
  },
}));
```

---

## Step 9 — Minimap Plugin

A miniature overview rendered below the main waveform — drag to navigate long tracks.

```javascript
import MinimapPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/minimap.esm.js';

ws.registerPlugin(MinimapPlugin.create({
  height:        30,
  waveColor:     '#334155',
  progressColor: '#6366f1',
  cursorColor:   'transparent',
  insertPosition: 'afterend',
}));
```

---

## Step 10 — Spectrogram Plugin

Renders a frequency-vs-time heatmap above the waveform. Heavy on CPU at first load.

```javascript
import SpectrogramPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/spectrogram.esm.js';

ws.registerPlugin(SpectrogramPlugin.create({
  labels:    true,
  height:    160,
  fftSamples: 1024,                // 256 / 512 / 1024 / 2048
  frequencyMax: 8000,              // Hz — cap top of display
  splitChannels: false,
  colorMap: 'roseus',              // 'gray' | 'igray' | 'roseus'
}));
```

---

## Step 11 — Design & Polish Guidelines

- **Always set an explicit `height`** on the waveform container — without it the canvas renders 0px high and the wave is invisible
- **Use `barWidth: 2` + `barGap: 2`** for a modern Soundcloud-style waveform; omit them for a solid filled wave
- **`normalize: true`** scales every track to fill the height — quiet recordings will not look like flat lines
- **Pre-compute peaks for large files** — pass `[peaksArray]` as the second arg of `load()` to skip decode on the client
- **Show a loading indicator** — bind `'loading'` and update a progress bar; decoding a 30 min podcast can take seconds
- **Respect autoplay policy** — never call `ws.play()` before a user gesture; bind to the Play button instead
- **Keyboard support** — Space, arrows, M. Tab to focus the waveform, then arrows for fine seek
- **Accessibility** — set `role="slider"`, `aria-label`, `aria-valuemin/max/now` on the waveform container; mirror current time into `aria-valuenow`
- **Colour contrast** — `waveColor` and `progressColor` should have ≥ 3:1 contrast against each other so progress is visible
- **Destroy on unmount** — call `ws.destroy()` before recreating in the same container or you leak audio nodes and canvases
- **Mobile** — touch events work out of the box; consider `dragToSeek: true` for a more obvious affordance on touchscreens

---

## Step 12 — Complete Example: Podcast Player with Regions and Timeline

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Podcast Player</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117; color: #e2e8f0;
      display: flex; flex-direction: column; align-items: center;
      min-height: 100vh; padding: 24px;
    }
    .card {
      width: 100%; max-width: 920px;
      background: #1a1d27;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 16px; overflow: hidden;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .card-header {
      padding: 22px 24px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
      display: flex; justify-content: space-between; align-items: flex-end; gap: 16px; flex-wrap: wrap;
    }
    .meta h1   { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; }
    .meta p.sub{ font-size: 0.82rem; color: #64748b; margin-top: 3px; }
    .chapters  { display: flex; gap: 6px; flex-wrap: wrap; }
    .chip {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.08);
      color: #94a3b8; padding: 4px 10px;
      border-radius: 999px; font-size: 11px; cursor: pointer;
      transition: all 0.15s;
    }
    .chip:hover { background: rgba(99,102,241,0.15); color: #a5b4fc; border-color: rgba(99,102,241,0.35); }

    #waveform { padding: 18px 20px 4px; }
    #timeline { padding: 0 20px 12px; }

    .transport {
      display: flex; align-items: center; gap: 14px;
      padding: 14px 22px 18px;
      border-top: 1px solid rgba(255,255,255,0.06);
      background: #14171f;
    }
    .btn {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1);
      color: #e2e8f0; border-radius: 10px;
      width: 38px; height: 38px;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer; transition: all 0.15s;
    }
    .btn:hover  { background: rgba(255,255,255,0.1); transform: translateY(-1px); }
    .btn:active { transform: scale(0.96); }
    .btn.primary {
      background: #6366f1; border-color: #6366f1; color: #fff;
      width: 46px; height: 46px;
      box-shadow: 0 4px 14px rgba(99,102,241,0.35);
    }
    .btn.primary:hover { background: #5254cc; }

    .time {
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-variant-numeric: tabular-nums;
      font-size: 13px; color: #94a3b8;
      min-width: 100px;
    }
    .time strong { color: #f1f5f9; }

    .spacer { flex: 1; }

    .rate {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1);
      color: #e2e8f0; border-radius: 8px;
      padding: 6px 10px; font-size: 12px; cursor: pointer;
      font-family: inherit;
    }
    .volume {
      width: 90px; accent-color: #6366f1;
    }

    .loader {
      height: 2px; background: rgba(255,255,255,0.05);
    }
    .loader > div {
      height: 100%; width: 0%;
      background: #6366f1;
      transition: width 0.2s ease;
    }

    /* Pure CSS icons (no font dependency) */
    .icon { width: 14px; height: 14px; fill: currentColor; }
  </style>
</head>
<body>
  <main class="card" aria-labelledby="title">
    <header class="card-header">
      <div class="meta">
        <h1 id="title">Episode 42 — Building with Alyx</h1>
        <p class="sub">Audio Demo · Click waveform to scrub · Space to play · Arrows to ±5s · M to mute</p>
      </div>
      <div class="chapters" role="toolbar" aria-label="Chapters">
        <button class="chip" data-jump="0">Intro</button>
        <button class="chip" data-jump="20">Topic</button>
        <button class="chip" data-jump="40">Discussion</button>
        <button class="chip" data-jump="60">Q&A</button>
      </div>
    </header>

    <div class="loader" aria-hidden="true"><div id="loader"></div></div>
    <div id="waveform" role="slider"
         aria-label="Audio waveform — click to scrub"
         aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"
         tabindex="0"></div>
    <div id="timeline"></div>

    <div class="transport">
      <button class="btn" id="back"   aria-label="Skip backward 10 seconds">
        <svg class="icon" viewBox="0 0 24 24"><path d="M12 5V1L7 6l5 5V7c3.3 0 6 2.7 6 6s-2.7 6-6 6-6-2.7-6-6H4c0 4.4 3.6 8 8 8s8-3.6 8-8-3.6-8-8-8z"/></svg>
      </button>
      <button class="btn primary" id="play" aria-label="Play / Pause">
        <svg class="icon" viewBox="0 0 24 24" id="playIcon"><path d="M8 5v14l11-7z"/></svg>
      </button>
      <button class="btn" id="fwd"    aria-label="Skip forward 10 seconds">
        <svg class="icon" viewBox="0 0 24 24"><path d="M12 5V1l5 5-5 5V7c-3.3 0-6 2.7-6 6s2.7 6 6 6 6-2.7 6-6h2c0 4.4-3.6 8-8 8s-8-3.6-8-8 3.6-8 8-8z"/></svg>
      </button>

      <span class="time"><strong id="cur">0:00</strong> / <span id="dur">0:00</span></span>

      <span class="spacer"></span>

      <button class="rate" id="rate" aria-label="Playback speed">1.0×</button>
      <input class="volume" id="vol" type="range" min="0" max="1" step="0.01" value="0.85" aria-label="Volume">
    </div>
  </main>

  <script type="module">
    import WaveSurfer     from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js';
    import RegionsPlugin  from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/regions.esm.js';
    import TimelinePlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/timeline.esm.js';

    const fmt = (s) => {
      if (!isFinite(s)) return '0:00';
      const m = Math.floor(s / 60), r = Math.floor(s % 60);
      return `${m}:${r.toString().padStart(2, '0')}`;
    };

    const ws = WaveSurfer.create({
      container:     '#waveform',
      url:           'https://www.mfiles.co.uk/mp3-downloads/brahms-st-anthony-chorale-theme-two-pianos.mp3',
      waveColor:     '#475569',
      progressColor: '#6366f1',
      cursorColor:   '#f1f5f9',
      cursorWidth:   2,
      barWidth:      2,
      barGap:        2,
      barRadius:     2,
      height:        120,
      normalize:     true,
      dragToSeek:    true,
    });

    const regions = ws.registerPlugin(RegionsPlugin.create());
    ws.registerPlugin(TimelinePlugin.create({
      container:    '#timeline',
      height:       18,
      timeInterval: 5,
      primaryLabelInterval: 30,
      style: { fontSize: '10px', color: '#64748b', fontFamily: 'ui-monospace, monospace' },
    }));

    // Chapter regions added once the audio is decoded
    ws.on('decode', () => {
      const dur = ws.getDuration();
      const chapters = [
        { start: 0,           end: dur * 0.20, content: 'Intro',     color: 'rgba(99,102,241,0.18)' },
        { start: dur * 0.20,  end: dur * 0.50, content: 'Topic',     color: 'rgba(236,72,153,0.18)' },
        { start: dur * 0.50,  end: dur * 0.80, content: 'Discussion',color: 'rgba(6,182,212,0.18)'  },
        { start: dur * 0.80,  end: dur,        content: 'Q&A',       color: 'rgba(34,197,94,0.18)'  },
      ];
      chapters.forEach(c => regions.addRegion({ ...c, drag: false, resize: false }));
      document.getElementById('dur').textContent = fmt(dur);
    });

    // Loading bar
    const loader = document.getElementById('loader');
    ws.on('loading', (p) => loader.style.width = p + '%');
    ws.on('ready',   ()  => loader.style.width = '100%');

    // Time + a11y value
    const waveformEl = document.getElementById('waveform');
    ws.on('timeupdate', (t) => {
      document.getElementById('cur').textContent = fmt(t);
      const dur = ws.getDuration();
      waveformEl.setAttribute('aria-valuenow', dur ? Math.round((t / dur) * 100) : 0);
    });

    // Region playback — click a chapter to jump
    regions.on('region-clicked', (r, e) => { e.stopPropagation(); ws.setTime(r.start); ws.play(); });

    // Transport
    const playBtn  = document.getElementById('play');
    const playIcon = document.getElementById('playIcon');
    const PLAY  = 'M8 5v14l11-7z';
    const PAUSE = 'M6 4h4v16H6zM14 4h4v16h-4z';

    playBtn.addEventListener('click', () => ws.playPause());
    ws.on('play',  () => playIcon.setAttribute('d', PAUSE));
    ws.on('pause', () => playIcon.setAttribute('d', PLAY));

    document.getElementById('back').addEventListener('click', () => ws.skip(-10));
    document.getElementById('fwd' ).addEventListener('click', () => ws.skip(10));

    document.querySelectorAll('[data-jump]').forEach(btn => {
      btn.addEventListener('click', () => {
        const pct = parseInt(btn.dataset.jump, 10) / 100;
        ws.seekTo(pct);
      });
    });

    // Playback rate
    const rates = [0.75, 1, 1.25, 1.5, 2];
    let rateIdx = 1;
    const rateBtn = document.getElementById('rate');
    rateBtn.addEventListener('click', () => {
      rateIdx = (rateIdx + 1) % rates.length;
      ws.setPlaybackRate(rates[rateIdx]);
      rateBtn.textContent = rates[rateIdx].toFixed(2) + '×';
    });

    // Volume
    document.getElementById('vol').addEventListener('input', (e) => {
      ws.setVolume(parseFloat(e.target.value));
    });

    // Keyboard
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') return;
      if (e.code === 'Space')      { e.preventDefault(); ws.playPause(); }
      if (e.code === 'ArrowLeft')  { e.preventDefault(); ws.skip(-5); }
      if (e.code === 'ArrowRight') { e.preventDefault(); ws.skip(5); }
      if (e.code === 'KeyM')       { ws.setMuted(!ws.getMuted()); }
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Using a UMD `<script>` tag** — v7 is ESM-only. Always use `<script type="module">` and `import` from the `.esm.js` URLs
- **No height on the waveform container** — wavesurfer renders a 0px canvas and the waveform is invisible. Use `height` in CSS *and* in the constructor options
- **Calling `ws.play()` on `ready` without user gesture** — browsers block autoplay and throw `NotAllowedError`. Bind play to a button click
- **Loading audio from a non-CORS host** — decoding fails silently. Use a host that sends `Access-Control-Allow-Origin`, or pre-compute peaks
- **Mixing v6 plugin imports with v7 core** — plugin URLs must come from the matching v7 path under `dist/plugins/`
- **Forgetting to `registerPlugin`** — importing a plugin module does nothing; you must call `ws.registerPlugin(Plugin.create({…}))`
- **Adding regions before `decode`** — `ws.addRegion` before the audio finishes loading silently does nothing. Listen to the `decode` event first
- **Not destroying before recreating** — recreating in the same container without `ws.destroy()` leaks Web Audio nodes and detached canvases
- **Reading `getDuration()` immediately after `create`** — duration is only valid after `'ready'` or `'decode'`. Use those events to gate UI updates
- **Spectrogram with a long file at full FFT** — `fftSamples: 2048` on a 1 hour file freezes the tab. Use 512 or 1024 and consider lazy-mount
