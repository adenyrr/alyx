---
name: design-system
description: Système de design partagé pour tous les artifacts HTML d'Alyx (dev, presenter, mindmap, diagram). Définit les tokens (couleurs, typo, espacements, ombres), les composants de base (cards, boutons, badges), et les patterns d'animation. À INCLURE et SUIVRE EXACTEMENT par tout agent produisant un artifact HTML visible — c'est ce qui transforme un fragment fonctionnel mais sobre en quelque chose de soigné, moderne et accessible.
agents: [dev, presenter, mindmap, diagram]
---

# Alyx Design System — v1

Tous les artifacts HTML produits par Alyx doivent partager le même langage visuel : moderne, dark-first, accessible, légèrement vibrant sans surcharger. Ce skill est la **source unique de vérité** pour les tokens et les patterns.

---

## 1. Tokens de design (CSS variables — copier tels quels)

```css
:root,
[data-theme="dark"] {
  /* ─── Surfaces ─── */
  --bg:           #0b0d12;
  --bg-elevated:  #131722;
  --surface:      rgba(255, 255, 255, 0.04);
  --surface-hi:   rgba(255, 255, 255, 0.07);
  --border:       rgba(255, 255, 255, 0.08);
  --border-hi:    rgba(255, 255, 255, 0.14);

  /* ─── Texte ─── */
  --text:         #f1f5f9;
  --text-soft:    #cbd5e1;
  --text-muted:   #94a3b8;
  --text-dim:     #64748b;

  /* ─── Accents — palette riche ─── */
  --accent:       #818cf8;   /* indigo brillant */
  --accent-deep:  #6366f1;
  --accent-soft:  rgba(129, 140, 248, 0.18);
  --accent-glow:  rgba(129, 140, 248, 0.35);
  --success:      #34d399;   /* émeraude */
  --warning:      #fbbf24;   /* ambre */
  --danger:       #f87171;   /* corail */
  --info:         #60a5fa;   /* azur */

  /* ─── Gradients (utiliser parcimonieusement, pour titres/CTA) ─── */
  --grad-accent:  linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
  --grad-cool:    linear-gradient(135deg, #60a5fa 0%, #818cf8 100%);
  --grad-warm:    linear-gradient(135deg, #fbbf24 0%, #f87171 100%);

  /* ─── Ombres (élévation + lueur d'accent) ─── */
  --shadow-sm:    0 2px 8px rgba(0, 0, 0, 0.25);
  --shadow-md:    0 8px 24px rgba(0, 0, 0, 0.35);
  --shadow-lg:    0 16px 48px rgba(0, 0, 0, 0.45);
  --shadow-glow:  0 0 32px var(--accent-glow);

  /* ─── Spacing scale (multiples de 4px) ─── */
  --s-1: 4px;  --s-2: 8px;   --s-3: 12px;  --s-4: 16px;
  --s-5: 24px; --s-6: 32px;  --s-7: 48px;  --s-8: 64px;

  /* ─── Radius ─── */
  --r-sm: 6px;  --r-md: 10px;  --r-lg: 16px;  --r-xl: 24px;  --r-full: 9999px;

  /* ─── Easing & durées ─── */
  --ease:        cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out:    cubic-bezier(0.22, 1, 0.36, 1);
  --dur-fast:    140ms;
  --dur:         220ms;
  --dur-slow:    420ms;

  /* ─── Typographie ─── */
  --font-sans:   'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --font-mono:   'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace;
  --font-display:'Inter', sans-serif;
}

[data-theme="light"] {
  --bg:           #f8fafc;
  --bg-elevated:  #ffffff;
  --surface:      rgba(15, 23, 42, 0.03);
  --surface-hi:   rgba(15, 23, 42, 0.06);
  --border:       rgba(15, 23, 42, 0.08);
  --border-hi:    rgba(15, 23, 42, 0.14);
  --text:         #0f172a;
  --text-soft:    #1e293b;
  --text-muted:   #475569;
  --text-dim:     #64748b;
  --shadow-sm:    0 2px 8px rgba(15, 23, 42, 0.06);
  --shadow-md:    0 8px 24px rgba(15, 23, 42, 0.10);
  --shadow-lg:    0 16px 48px rgba(15, 23, 42, 0.14);
}
```

---

## 2. Reset + base (inclure dans tout `<style>` racine)

```css
* { box-sizing: border-box; margin: 0; padding: 0; }

html { font-size: 16px; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

body {
  font-family: var(--font-sans);
  font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  line-height: 1.6;
  padding: var(--s-5);
  /* Ambient gradient subtil — donne immédiatement plus de profondeur que le flat */
  background-image:
    radial-gradient(circle at 15% 20%, rgba(129, 140, 248, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 85% 80%, rgba(192, 132, 252, 0.06) 0%, transparent 40%);
}

::selection { background: var(--accent-soft); color: var(--text); }

/* Scrollbar fine et stylée */
*::-webkit-scrollbar { width: 8px; height: 8px; }
*::-webkit-scrollbar-track { background: transparent; }
*::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: var(--r-full); }
*::-webkit-scrollbar-thumb:hover { background: var(--text-dim); }
```

---

## 3. Charger les polices (CDN, à mettre dans `<head>`)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 4. Composant `card` (le shell par défaut de tout artifact)

```html
<main class="card">
  <header class="card__head">
    <h1 class="card__title">Titre de l'artifact</h1>
    <p class="card__sub">Sous-titre descriptif court (≤ 90 car.)</p>
  </header>
  <div class="card__body">
    <!-- contenu interactif ici -->
  </div>
</main>
```

```css
.card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: var(--s-6);
  max-width: 720px;
  margin: 0 auto;
  box-shadow: var(--shadow-md);
  /* Glassmorphism léger : laisse passer le gradient ambient du body */
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  /* Entrée animée subtile */
  animation: card-in var(--dur-slow) var(--ease) both;
}
@keyframes card-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card__head { margin-bottom: var(--s-5); }
.card__title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: var(--grad-accent);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: var(--s-1);
}
.card__sub {
  font-size: 0.875rem;
  color: var(--text-muted);
}
```

---

## 5. Boutons (primary, secondary, ghost)

```css
.btn {
  display: inline-flex; align-items: center; gap: var(--s-2);
  padding: var(--s-3) var(--s-5);
  border-radius: var(--r-md);
  font-family: var(--font-sans);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all var(--dur) var(--ease);
  user-select: none;
}
.btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* Primary : accent solid avec lueur au hover */
.btn--primary {
  background: var(--accent-deep);
  color: white;
  box-shadow: 0 4px 12px var(--accent-soft);
}
.btn--primary:hover {
  background: var(--accent);
  box-shadow: 0 6px 20px var(--accent-glow);
  transform: translateY(-1px);
}
.btn--primary:active { transform: translateY(0); }

/* Secondary : surface avec border */
.btn--secondary {
  background: var(--surface);
  color: var(--text);
  border-color: var(--border-hi);
}
.btn--secondary:hover { background: var(--surface-hi); border-color: var(--text-dim); }

/* Ghost : minimal, pour actions secondaires */
.btn--ghost {
  background: transparent;
  color: var(--text-muted);
}
.btn--ghost:hover { background: var(--surface); color: var(--text); }
```

---

## 6. Input + Select + Textarea

```css
.input, .select, .textarea {
  width: 100%;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: var(--s-3) var(--s-4);
  font-family: inherit;
  font-size: 0.9rem;
  transition: all var(--dur-fast) var(--ease);
}
.input:focus, .select:focus, .textarea:focus {
  outline: none;
  border-color: var(--accent);
  background: var(--bg-elevated);
  box-shadow: 0 0 0 3px var(--accent-soft);
}
.input::placeholder, .textarea::placeholder { color: var(--text-dim); }
```

---

## 7. Badges + chips

```css
.badge {
  display: inline-flex; align-items: center; gap: var(--s-1);
  padding: 2px 10px;
  border-radius: var(--r-full);
  font-size: 0.72rem;
  font-weight: 500;
  background: var(--surface);
  color: var(--text-muted);
  border: 1px solid var(--border);
}
.badge--accent  { background: var(--accent-soft);   color: var(--accent); border-color: transparent; }
.badge--success { background: rgba(52, 211, 153, 0.15); color: var(--success); border-color: transparent; }
.badge--warning { background: rgba(251, 191, 36, 0.15); color: var(--warning); border-color: transparent; }
.badge--danger  { background: rgba(248, 113, 113, 0.15); color: var(--danger);  border-color: transparent; }
```

---

## 8. Tableaux (clés pour data viz)

```css
.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
.table th {
  text-align: left;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.72rem;
  padding: var(--s-3) var(--s-4);
  border-bottom: 1px solid var(--border);
}
.table td {
  padding: var(--s-3) var(--s-4);
  border-bottom: 1px solid var(--border);
  transition: background var(--dur-fast);
}
.table tr:hover td { background: var(--surface); }
.table tr:last-child td { border-bottom: none; }
```

---

## 9. Animations utilitaires

```css
/* Fade-in d'élément (à appliquer à .fade) */
.fade { animation: fade-in var(--dur) var(--ease) both; }
@keyframes fade-in { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

/* Pulse de focus / état "attention" */
.pulse { animation: pulse 2s infinite; }
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--accent-soft); }
  50%      { box-shadow: 0 0 0 8px transparent; }
}

/* Hover lift utilisable sur n'importe quoi de cliquable */
.lift { transition: transform var(--dur) var(--ease), box-shadow var(--dur) var(--ease); }
.lift:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
```

---

## 10. Toggle theme dark/light (optionnel)

```html
<button class="btn btn--ghost" type="button" id="theme-toggle" aria-label="Basculer thème">
  <span aria-hidden="true">☀️</span>
</button>
<script>
  const tbtn = document.getElementById('theme-toggle');
  tbtn?.addEventListener('click', () => {
    const cur = document.body.dataset.theme || 'dark';
    document.body.dataset.theme = cur === 'dark' ? 'light' : 'dark';
    tbtn.firstElementChild.textContent = cur === 'dark' ? '🌙' : '☀️';
  });
</script>
```

---

## 11. Règles d'application

1. **Toujours partir du shell `<main class="card">`** sauf si l'artifact a sa propre structure (deck reveal.js, mindmap markmap, etc.) — dans ce cas, garder au moins les tokens (var(--bg), var(--accent), etc.) et l'ambient gradient sur `body`.
2. **Charger Inter + JetBrains Mono via Google Fonts** dans le `<head>` — c'est ce qui transforme immédiatement l'aspect « page brute » en « produit soigné ».
3. **Animer les entrées** : `card` fait son `card-in` automatiquement ; pour le contenu, ajouter `class="fade"` ou un délai `animation-delay`.
4. **Limiter les couleurs vives** : utiliser `--accent` pour 1-2 éléments hero, pas partout. Le reste = neutres + opacités sur l'accent (`--accent-soft`).
5. **Garder l'accessibilité** : `:focus-visible` toujours stylé, contrastes texte/bg vérifiés, `aria-label` sur les icônes seules.
6. **Pas de framework lourd inutile** : Tailwind/Bootstrap interdits dans le shell — uniquement CSS vanilla avec ces tokens. Si la lib de viz a son propre CSS (Chart.js, reveal.js), garder ses defaults mais OVERRIDE les couleurs principales avec nos `--accent` et `--text`.

---

## Exemple complet (artifact minimal mais polish)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mon artifact</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* TOKENS — copier intégralement la section 1 du design-system ici */
    :root, [data-theme="dark"] {
      --bg: #0b0d12; --bg-elevated: #131722; --surface: rgba(255,255,255,0.04);
      --surface-hi: rgba(255,255,255,0.07); --border: rgba(255,255,255,0.08);
      --border-hi: rgba(255,255,255,0.14); --text: #f1f5f9; --text-soft: #cbd5e1;
      --text-muted: #94a3b8; --text-dim: #64748b; --accent: #818cf8;
      --accent-deep: #6366f1; --accent-soft: rgba(129,140,248,0.18);
      --accent-glow: rgba(129,140,248,0.35);
      --grad-accent: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
      --shadow-md: 0 8px 24px rgba(0,0,0,0.35);
      --s-1: 4px; --s-2: 8px; --s-3: 12px; --s-4: 16px; --s-5: 24px; --s-6: 32px;
      --r-md: 10px; --r-lg: 16px;
      --ease: cubic-bezier(0.16, 1, 0.3, 1); --dur: 220ms; --dur-slow: 420ms;
      --font-sans: 'Inter', system-ui, sans-serif;
      --font-display: 'Inter', sans-serif;
    }
    /* RESET + BASE (cf. section 2) */
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:var(--font-sans);background:var(--bg);color:var(--text);min-height:100vh;
      padding:var(--s-5);line-height:1.6;-webkit-font-smoothing:antialiased;
      background-image:radial-gradient(circle at 15% 20%,rgba(129,140,248,0.08) 0%,transparent 40%),
                       radial-gradient(circle at 85% 80%,rgba(192,132,252,0.06) 0%,transparent 40%);}
    /* CARD (cf. section 4) */
    .card{background:var(--bg-elevated);border:1px solid var(--border);border-radius:var(--r-lg);
      padding:var(--s-6);max-width:720px;margin:0 auto;box-shadow:var(--shadow-md);
      backdrop-filter:blur(8px);animation:card-in var(--dur-slow) var(--ease) both;}
    @keyframes card-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
    .card__title{font-size:1.5rem;font-weight:700;letter-spacing:-0.02em;
      background:var(--grad-accent);-webkit-background-clip:text;background-clip:text;
      color:transparent;margin-bottom:var(--s-1);}
    .card__sub{font-size:0.875rem;color:var(--text-muted);margin-bottom:var(--s-5);}
  </style>
</head>
<body data-theme="dark">
  <main class="card">
    <h1 class="card__title">Artifact démonstratif</h1>
    <p class="card__sub">Contenu interactif rendu avec le design-system d'Alyx</p>
    <div class="card__body">
      <!-- contenu spécifique à l'artifact -->
    </div>
  </main>
</body>
</html>
```

---

## Anti-patterns à éviter

- ❌ Background plat sans le gradient ambient (rend l'artifact « page brute »)
- ❌ Couleurs custom hors palette (rouge HTML par défaut, bleu navigateur)
- ❌ Police système par défaut au lieu d'Inter (différence énorme sur le rendu)
- ❌ Pas d'animation d'entrée (l'artifact « apparaît » plat sans transition)
- ❌ Borders épais (≥ 2px) — on reste à 1px, l'élévation vient des ombres
- ❌ Border-radius mixés (4px + 8px + 12px sans logique) — tenir à l'échelle r-sm/md/lg/xl
- ❌ Texte muted sur fond muted (contraste insuffisant) — text-muted sur surface, text-soft sur bg-elevated
