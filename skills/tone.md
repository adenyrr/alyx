---
name: tone-audio
description: Create interactive audio synthesis and music applications using Tone.js, delivered as self-contained HTML artifacts. Use this skill whenever someone needs audio synthesis, sound effects, sequencing, musical instruments, beat machines, audio visualizers, or any interactive sound experience in the browser. Trigger on requests like "make a synthesizer", "create a drum machine", "build a piano", "generate audio in the browser", "make a music sequencer", or any prompt involving real-time audio generation. Do NOT use for audio file playback only (→ plain HTML <audio>), data visualizations (→ chartjs/d3 skill), or animation without sound (→ animejs/gsap skill).
---

# Tone.js Audio Skill

Tone.js is a Web Audio framework that provides synths, effects, scheduling (Transport), sequencers, and audio analysis. It abstracts the Web Audio API into a musician-friendly interface—create oscillators, chain effects, schedule patterns, and build interactive instruments all from JavaScript. Everything runs in the browser with no backend required.

---

## Artifact Presentation & Use Cases

Every Tone.js artifact is a self-contained HTML page with a dark theme and interactive audio controls. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius) centers the instrument/controls
- **Title** (1.15rem, `#f1f5f9`) names the audio experience
- **Subtitle** (0.82rem, `#64748b`) explains interaction ("Click to start audio · tap keys to play")
- **Start Audio button** — mandatory first interaction (AudioContext user-gesture requirement)
- **Interactive controls** — keyboard buttons, sliders, pads, or visualizer canvas

### Typical use cases

- **Virtual piano/keyboard** — clickable/keyable notes with realistic or synth sounds
- **Drum machine** — grid sequencer with kick, snare, hi-hat patterns
- **Synthesizer** — oscillators with filter, envelope, reverb, and delay controls
- **Ambient soundscapes** — generative audio with layered drones and textures
- **Sound effects generator** — UI for creating game/notification sounds
- **Audio visualizer** — FFT or waveform display synced to audio output
- **Metronome/tempo tools** — click track with adjustable BPM
- **Music sequencer** — step sequencer for melodic or rhythmic patterns

### What the user sees

An interactive audio instrument with a "Start Audio" button that must be clicked first (browser requirement). After that, the user interacts via clicking pads, pressing keyboard keys, adjusting sliders, or starting playback—hearing synthesized audio in real-time.

---

## When to Use Tone.js vs. Alternatives

| Use Tone.js when… | Use another tool when… |
|---|---|
| Synthesis: create sounds from oscillators | Just play an MP3/WAV file → plain `<audio>` element |
| Effects chains: reverb, delay, distortion | Visual-only animation → **Anime.js / GSAP** |
| Scheduling: loops, sequences, transport | Data sonification with charts → **D3 + Web Audio** |
| Interactive instruments (piano, drums) | Music notation rendering → **VexFlow** (not in stack) |
| Real-time audio analysis (FFT, waveform) | 3D audio spatialization → **Three.js + Web Audio** |
| Pattern sequencing (step sequencer) | MIDI file playback → consider native Web MIDI API |

> **Rule of thumb:** if the user wants to generate, synthesize, or sequence sound in the browser, use Tone.js. If they just want to play a pre-recorded file, use `<audio>`.

---

## Step 1 — CDN Setup

```html
<!-- Tone.js -->
<script src="https://cdn.jsdelivr.net/npm/tone@14.8.49/build/Tone.js"></script>
```

> Tone.js exposes the `Tone` global object. No CSS required—it's audio-only.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Audio Instrument</title>
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
      max-width: 700px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }
    .btn {
      background: #6366f1;
      color: #fff;
      border: none;
      border-radius: 10px;
      padding: 10px 24px;
      font-size: 14px;
      cursor: pointer;
      transition: background 0.15s;
    }
    .btn:hover { background: #818cf8; }
    .btn:disabled { opacity: 0.5; cursor: not-allowed; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Instrument Name</h1>
    <p class="sub">Click "Start Audio" to enable sound · then interact with controls</p>
    <button class="btn" id="start-btn">Start Audio</button>
    <div id="controls" style="margin-top:20px; display:none;">
      <!-- Interactive controls here -->
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/tone@14.8.49/build/Tone.js"></script>
  <script>
    document.getElementById('start-btn').addEventListener('click', async () => {
      await Tone.start();
      document.getElementById('start-btn').disabled = true;
      document.getElementById('start-btn').textContent = 'Audio Active ✓';
      document.getElementById('controls').style.display = 'block';
      // Initialize instruments here
    });
  </script>
</body>
</html>
```

---

## Step 3 — AudioContext User-Gesture Requirement

**Critical:** Browsers require a user gesture (click/tap) before audio can play.

```javascript
// ALWAYS start with this pattern
document.getElementById('start-btn').addEventListener('click', async () => {
  await Tone.start();  // Resumes AudioContext
  console.log('Audio is ready');
  // Now safe to create synths, start transport, etc.
});
```

> Never create synths or start the Transport before `Tone.start()` resolves.

---

## Step 4 — Synths

```javascript
// Basic synth (oscillator + envelope)
const synth = new Tone.Synth().toDestination();
synth.triggerAttackRelease('C4', '8n');  // note, duration

// Polyphonic synth (multiple simultaneous notes)
const poly = new Tone.PolySynth(Tone.Synth).toDestination();
poly.triggerAttackRelease(['C4', 'E4', 'G4'], '4n');  // chord

// FM synth
const fm = new Tone.FMSynth().toDestination();
fm.triggerAttackRelease('A3', '2n');

// AM synth
const am = new Tone.AMSynth().toDestination();

// Membrane synth (drums, kicks)
const kick = new Tone.MembraneSynth().toDestination();
kick.triggerAttackRelease('C1', '8n');

// Metal synth (hi-hats, cymbals)
const hat = new Tone.MetalSynth().toDestination();
hat.triggerAttackRelease('16n');

// Noise synth (snares, white noise)
const noise = new Tone.NoiseSynth().toDestination();
noise.triggerAttackRelease('8n');

// Pluck synth (guitar-like)
const pluck = new Tone.PluckSynth().toDestination();
pluck.triggerAttack('E3');
```

---

## Step 5 — Effects Chain

```javascript
// Create effects
const reverb = new Tone.Reverb({ decay: 3, wet: 0.4 }).toDestination();
const delay = new Tone.FeedbackDelay({ delayTime: '8n', feedback: 0.3, wet: 0.3 }).toDestination();
const distortion = new Tone.Distortion({ distortion: 0.4, wet: 0.3 }).toDestination();
const chorus = new Tone.Chorus({ frequency: 1.5, depth: 0.7, wet: 0.3 }).toDestination().start();
const filter = new Tone.Filter({ frequency: 800, type: 'lowpass' }).toDestination();

// Chain synth through effects
const synth = new Tone.Synth().chain(delay, reverb);
// or
const synth2 = new Tone.PolySynth(Tone.Synth).connect(filter);
filter.connect(reverb);

// Available effects: AutoFilter, AutoPanner, AutoWah, BitCrusher, Chebyshev,
// Chorus, Compressor, Distortion, EQ3, FeedbackDelay, Filter, Freeverb,
// JCReverb, Phaser, PingPongDelay, Reverb, StereoWidener, Tremolo, Vibrato
```

---

## Step 6 — Transport & Scheduling

```javascript
// Set tempo
Tone.getTransport().bpm.value = 120;

// Schedule repeating events
Tone.getTransport().scheduleRepeat((time) => {
  synth.triggerAttackRelease('C4', '8n', time);
}, '4n');  // repeat every quarter note

// Start/stop transport
Tone.getTransport().start();
Tone.getTransport().stop();
Tone.getTransport().toggle();
```

---

## Step 7 — Sequences & Patterns

```javascript
// Sequence: play notes in order
const seq = new Tone.Sequence((time, note) => {
  synth.triggerAttackRelease(note, '8n', time);
}, ['C4', 'E4', 'G4', 'B4'], '4n');
seq.start(0);
Tone.getTransport().start();

// Pattern: play notes with a pattern type
const pattern = new Tone.Pattern((time, note) => {
  synth.triggerAttackRelease(note, '8n', time);
}, ['C4', 'D4', 'E4', 'F4', 'G4'], 'upDown');
pattern.start(0);

// Loop
const loop = new Tone.Loop((time) => {
  kick.triggerAttackRelease('C1', '8n', time);
}, '4n');
loop.start(0);
```

---

## Step 8 — Audio Analysis (FFT / Waveform)

```javascript
// Analyser for visualization
const analyser = new Tone.Analyser('fft', 256);  // or 'waveform'
synth.connect(analyser);

// Read data in animation loop
function draw() {
  const values = analyser.getValue();  // Float32Array
  // Draw bars / waveform on canvas
  requestAnimationFrame(draw);
}
draw();
```

### Canvas visualizer example:
```javascript
const canvas = document.getElementById('visualizer');
const ctx = canvas.getContext('2d');

function drawFFT() {
  const data = analyser.getValue();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const barWidth = canvas.width / data.length;
  
  data.forEach((val, i) => {
    const height = ((val + 140) / 140) * canvas.height;  // normalize dB to pixels
    const x = i * barWidth;
    ctx.fillStyle = `hsl(${240 + i * 0.5}, 70%, 60%)`;
    ctx.fillRect(x, canvas.height - height, barWidth - 1, height);
  });
  
  requestAnimationFrame(drawFFT);
}
```

---

## Step 9 — Keyboard Mapping

```javascript
const NOTE_MAP = {
  'a': 'C4', 's': 'D4', 'd': 'E4', 'f': 'F4',
  'g': 'G4', 'h': 'A4', 'j': 'B4', 'k': 'C5',
  'w': 'C#4', 'e': 'D#4', 't': 'F#4', 'y': 'G#4', 'u': 'A#4',
};

document.addEventListener('keydown', (e) => {
  if (e.repeat) return;  // prevent key repeat
  const note = NOTE_MAP[e.key.toLowerCase()];
  if (note) synth.triggerAttack(note);
});

document.addEventListener('keyup', (e) => {
  const note = NOTE_MAP[e.key.toLowerCase()];
  if (note) synth.triggerRelease();
});
```

---

## Step 10 — Sampler (Custom Sounds)

```javascript
// Load audio samples
const sampler = new Tone.Sampler({
  urls: {
    C4: 'C4.mp3',
    'D#4': 'Ds4.mp3',
    'F#4': 'Fs4.mp3',
    A4: 'A4.mp3',
  },
  baseUrl: 'https://tonejs.github.io/audio/salamander/',
  onload: () => console.log('Samples loaded'),
}).toDestination();

// Play once loaded
sampler.triggerAttackRelease('C4', '4n');
```

---

## Step 11 — Design & Polish Guidelines

- **"Start Audio" button is mandatory** — always begin with a user gesture that calls `await Tone.start()`; this is a browser requirement, not optional
- **Visual feedback** — highlight keys/pads when they produce sound; use CSS transitions or class toggling for active states
- **Keyboard mapping legend** — show a small legend of which keys map to which notes
- **Slider controls** — for parameters like BPM, reverb wet, filter frequency; use `<input type="range">` styled with the dark theme
- **Canvas visualizer** — pair audio with an FFT or waveform canvas for visual engagement; match canvas background to `#0f1117`
- **Latency** — keep the signal chain short; too many chained effects increase latency perceptibly
- **Dispose** — call `synth.dispose()` when removing instruments to free Web Audio nodes and prevent memory leaks
- **Transport state UI** — show play/pause/stop buttons that reflect `Tone.getTransport().state`
- **Mobile touch** — use `touchstart` events alongside `click` for responsive mobile play; prevent double-firing with `{ passive: false }`
- **Volume control** — provide a master volume: `Tone.getDestination().volume.value = -6;` (in dB, 0 = max, -Infinity = mute)

---

## Step 12 — Complete Example: Mini Synth Keyboard

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mini Synth</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 28px; width: 100%; max-width: 700px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 16px; }
    .btn { background: #6366f1; color: #fff; border: none; border-radius: 10px; padding: 10px 24px; font-size: 14px; cursor: pointer; }
    .btn:hover { background: #818cf8; }
    .btn:disabled { opacity: 0.5; }
    #controls { display: none; margin-top: 20px; }
    .keyboard { display: flex; gap: 4px; margin-bottom: 20px; position: relative; height: 140px; }
    .key { flex: 1; border-radius: 0 0 8px 8px; cursor: pointer; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 10px; font-size: 11px; transition: all 0.1s; user-select: none; }
    .key.white { background: #2a2d3a; color: #94a3b8; height: 100%; min-width: 40px; }
    .key.white:hover, .key.white.active { background: #6366f1; color: #fff; }
    .key.black { background: #0f1117; color: #64748b; height: 60%; min-width: 30px; position: absolute; z-index: 2; border: 1px solid #2a2d3a; }
    .key.black:hover, .key.black.active { background: #4f46e5; color: #fff; }
    .sliders { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .slider-group label { font-size: 12px; color: #94a3b8; display: block; margin-bottom: 4px; }
    .slider-group input[type=range] { width: 100%; accent-color: #6366f1; }
    canvas { width: 100%; height: 60px; border-radius: 8px; margin-bottom: 16px; background: #0f1117; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Mini Synth</h1>
    <p class="sub">Click "Start Audio" · play with on-screen keys or keyboard (A S D F G H J K)</p>
    <button class="btn" id="start-btn">Start Audio</button>
    <div id="controls">
      <canvas id="viz" height="60"></canvas>
      <div class="keyboard" id="keyboard"></div>
      <div class="sliders">
        <div class="slider-group">
          <label>Reverb: <span id="rev-val">0.3</span></label>
          <input type="range" id="reverb" min="0" max="1" step="0.05" value="0.3">
        </div>
        <div class="slider-group">
          <label>Delay: <span id="del-val">0.2</span></label>
          <input type="range" id="delay" min="0" max="0.8" step="0.05" value="0.2">
        </div>
        <div class="slider-group">
          <label>Filter: <span id="flt-val">2000</span> Hz</label>
          <input type="range" id="filter" min="100" max="8000" step="50" value="2000">
        </div>
        <div class="slider-group">
          <label>Volume: <span id="vol-val">-6</span> dB</label>
          <input type="range" id="volume" min="-30" max="0" step="1" value="-6">
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/tone@14.8.49/build/Tone.js"></script>
  <script>
    const NOTES = [
      { note: 'C4',  type: 'white', key: 'a' },
      { note: 'C#4', type: 'black', key: 'w', offset: 28 },
      { note: 'D4',  type: 'white', key: 's' },
      { note: 'D#4', type: 'black', key: 'e', offset: 72 },
      { note: 'E4',  type: 'white', key: 'd' },
      { note: 'F4',  type: 'white', key: 'f' },
      { note: 'F#4', type: 'black', key: 't', offset: 160 },
      { note: 'G4',  type: 'white', key: 'g' },
      { note: 'G#4', type: 'black', key: 'y', offset: 204 },
      { note: 'A4',  type: 'white', key: 'h' },
      { note: 'A#4', type: 'black', key: 'u', offset: 248 },
      { note: 'B4',  type: 'white', key: 'j' },
      { note: 'C5',  type: 'white', key: 'k' },
    ];

    let synth, reverb, delay, filter, analyser, ctx, canvas;

    // Build keyboard
    const kb = document.getElementById('keyboard');
    NOTES.forEach(n => {
      const el = document.createElement('div');
      el.className = `key ${n.type}`;
      el.dataset.note = n.note;
      el.textContent = n.key.toUpperCase();
      if (n.type === 'black' && n.offset !== undefined) {
        el.style.left = n.offset + 'px';
        el.style.width = '30px';
      }
      kb.appendChild(el);
    });

    document.getElementById('start-btn').addEventListener('click', async () => {
      await Tone.start();
      document.getElementById('start-btn').disabled = true;
      document.getElementById('start-btn').textContent = 'Audio Active ✓';
      document.getElementById('controls').style.display = 'block';

      filter = new Tone.Filter(2000, 'lowpass').toDestination();
      reverb = new Tone.Reverb({ decay: 2.5, wet: 0.3 }).connect(filter);
      delay = new Tone.FeedbackDelay({ delayTime: '8n', feedback: 0.2, wet: 0.2 }).connect(reverb);
      synth = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: 'triangle8' },
        envelope: { attack: 0.02, decay: 0.3, sustain: 0.4, release: 0.8 },
      }).connect(delay);

      analyser = new Tone.Analyser('waveform', 256);
      synth.connect(analyser);

      Tone.getDestination().volume.value = -6;

      canvas = document.getElementById('viz');
      ctx = canvas.getContext('2d');
      canvas.width = canvas.offsetWidth * 2;
      canvas.height = 120;
      drawWaveform();
    });

    function drawWaveform() {
      if (!analyser) return;
      const data = analyser.getValue();
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.beginPath();
      ctx.strokeStyle = '#6366f1';
      ctx.lineWidth = 2;
      const step = canvas.width / data.length;
      data.forEach((val, i) => {
        const y = ((val + 1) / 2) * canvas.height;
        i === 0 ? ctx.moveTo(0, y) : ctx.lineTo(i * step, y);
      });
      ctx.stroke();
      requestAnimationFrame(drawWaveform);
    }

    function playNote(note) {
      if (!synth) return;
      synth.triggerAttackRelease(note, '8n');
      const el = kb.querySelector(`[data-note="${note}"]`);
      if (el) { el.classList.add('active'); setTimeout(() => el.classList.remove('active'), 200); }
    }

    // Click/touch
    kb.addEventListener('pointerdown', (e) => {
      const note = e.target.dataset.note;
      if (note) playNote(note);
    });

    // Keyboard
    const keyMap = {};
    NOTES.forEach(n => keyMap[n.key] = n.note);
    document.addEventListener('keydown', (e) => {
      if (e.repeat) return;
      const note = keyMap[e.key.toLowerCase()];
      if (note) playNote(note);
    });

    // Sliders
    document.getElementById('reverb').addEventListener('input', (e) => {
      if (reverb) reverb.wet.value = +e.target.value;
      document.getElementById('rev-val').textContent = e.target.value;
    });
    document.getElementById('delay').addEventListener('input', (e) => {
      if (delay) delay.wet.value = +e.target.value;
      document.getElementById('del-val').textContent = e.target.value;
    });
    document.getElementById('filter').addEventListener('input', (e) => {
      if (filter) filter.frequency.value = +e.target.value;
      document.getElementById('flt-val').textContent = e.target.value;
    });
    document.getElementById('volume').addEventListener('input', (e) => {
      Tone.getDestination().volume.value = +e.target.value;
      document.getElementById('vol-val').textContent = e.target.value;
    });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **No `await Tone.start()` before playing** — the AudioContext is suspended until a user gesture triggers `Tone.start()`; audio will silently fail without it
- **Creating synths before `Tone.start()`** — create instruments after the AudioContext is active, not at page load
- **Not calling `.toDestination()`** — synths and effects must be connected to the destination (speakers); without it, no sound plays
- **Key repeat flooding** — always check `if (e.repeat) return;` in `keydown` handlers to prevent rapid-fire note triggering
- **Forgetting `.dispose()`** — unused synths leak Web Audio nodes; dispose when switching instruments or cleaning up
- **Wrong note format** — Tone.js uses scientific notation: `'C4'`, `'F#3'`, `'Bb5'` (uppercase note + optional sharp/flat + octave number)
- **Transport not started** — sequences and loops only play after `Tone.getTransport().start()`
- **FFT values in dB** — `analyser.getValue()` returns dB values (negative numbers); normalize to `[0, 1]` for canvas drawing
- **Effect order matters** — chain effects in signal-flow order: `synth → delay → reverb → filter → destination`
- **Mobile audio policies** — on iOS, audio only works after a touchstart/click event; the "Start Audio" button pattern handles this
