---
name: mermaid-diagrams
description: Create clear, well-structured diagrams using Mermaid syntax, rendered as self-contained HTML artifacts. Use this skill for flowcharts, process flows, decision trees, sequence diagrams (system interactions, API calls, auth flows), class diagrams (OOP, data models), entity-relationship diagrams, state machines, Gantt charts, Git branch graphs, architecture diagrams, C4 models, mindmaps, timelines, quadrant charts, pie charts, and XY charts. Trigger whenever someone asks to document a process, visualize a system, map relationships between entities, diagram an architecture, model a workflow, or describe interactions between components — even without explicit mention of Mermaid. Do NOT use for interactive network graphs (→ vis-network), data chart analytics (→ charting), or project roadmaps with drag-and-drop (→ vis-timeline).
---

# Mermaid Diagrams Skill

Mermaid turns text definitions into SVG diagrams. Diagrams live in plain text, version alongside code, and render instantly in the browser. This skill covers every diagram type, theming, the HTML rendering pattern, and common syntax pitfalls.

---

## Artifact Presentation & Use Cases

Every Mermaid artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius, soft shadow) centers the diagram(s)
- **Title** (`h1`, 1.15rem, `#f1f5f9`) describes the diagram
- **Subtitle** (`p.sub`, 0.82rem, `#64748b`) adds context
- **`.mermaid` div(s)** containing the text definition — Mermaid renders SVG inline

### Typical use cases

- **Process flows** — flowcharts for workflows, decision trees, approval processes
- **System interactions** — sequence diagrams for API calls, auth flows, microservice communication
- **Data models** — entity-relationship diagrams for databases, class diagrams for OOP
- **State machines** — state diagrams for UI states, order lifecycles, protocol states
- **Architecture** — C4 models, architecture diagrams, deployment topologies
- **Planning** — Gantt charts for project timelines, mindmaps for brainstorming, Git branch graphs

### What the user sees

Clean SVG diagrams rendered from text: crisp shapes, readable labels, dark-themed with custom colors. Multi-diagram pages show related views side by side. Diagrams are static (no drag/zoom) but pixel-perfect and export-ready.

---

## When to Use Mermaid vs. Alternatives

| Use Mermaid when… | Use another tool when… |
|---|---|
| Flowcharts, decision trees, process flows | Interactive node-edge graphs with drag/physics → **vis-network** |
| Sequence diagrams (API, auth, messaging) | Data-driven bar/line/pie charts → **Chart.js / Plotly** |
| ER diagrams, class diagrams | Geographic maps → **Leaflet** |
| Gantt charts (static view) | Interactive timelines with drag-and-drop → **vis-timeline** |
| Git branch visualization | Bespoke SVG visualizations → **D3.js** |
| Quick architecture diagrams | Animated DOM/SVG → **Anime.js** |
| Text-based, version-controllable diagrams | Complex, interactive UIs → **React + shadcn/ui** |

> **Rule of thumb:** if the diagram can be expressed as a text definition (nodes, edges, sequences) and doesn’t need interactivity, Mermaid is the fastest and most maintainable option.

---

## Step 1 — CDN Setup

Mermaid v11 ships as an ES module. The simplest pattern for single-file HTML artifacts uses the UMD build:

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',           // 'default' | 'dark' | 'neutral' | 'forest' | 'base'
    securityLevel: 'loose',  // allows HTML in labels
    fontFamily: "'Segoe UI', sans-serif",
  });
</script>
```

**Or with ESM** (needed when calling `mermaid.render()` programmatically):
```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'dark' });
</script>
```

Use the **UMD build + `startOnLoad: true`** for the vast majority of artifacts — it finds and renders all `.mermaid` divs automatically.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Diagram Title</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      min-height: 100vh;
      padding: 32px 24px;
    }
    .card {
      width: 100%;
      max-width: 960px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 28px; }

    /* Mermaid SVG fills its container */
    .mermaid { width: 100%; }
    .mermaid svg { max-width: 100%; height: auto; display: block; margin: 0 auto; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Diagram Title</h1>
    <p class="sub">Brief description</p>

    <div class="mermaid">
      %%{init: {'theme': 'dark', 'themeVariables': {'darkMode': true}}}%%
      flowchart TD
        A[Start] --> B{Decision}
        B -->|Yes| C[Result A]
        B -->|No| D[Result B]
    </div>
  </div>

  <!-- Scripts at end of body, AFTER the .mermaid divs -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({ startOnLoad: true, theme: 'dark', securityLevel: 'loose' });</script>
</body>
</html>
```

**Key rules:**
- Place `<script>` tags at the **end of `<body>`**, after all `.mermaid` divs
- The `%%{init: ...}%%` directive inside the diagram definition always wins over `mermaid.initialize()` — use it for per-diagram overrides
- Multiple diagrams on one page: each gets its own `.mermaid` div; `startOnLoad: true` renders all of them

---

## Step 3 — Themes and Custom Colors

### Built-in themes
| Theme | Description |
|---|---|
| `'dark'` | Dark background, light text — recommended for artifacts |
| `'default'` | Light background, classic Mermaid blue |
| `'neutral'` | Grayscale, minimal |
| `'forest'` | Green tones |
| `'base'` | Unstyled base — fully customizable via `themeVariables` |

### Per-diagram theme via directive (most reliable method)
```
%%{init: {'theme': 'dark'}}%%
flowchart LR
  ...
```

### Custom colors via `themeVariables` (use with `theme: 'base'`)
```
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor':       '#6366f1',
    'primaryTextColor':   '#f1f5f9',
    'primaryBorderColor': '#818cf8',
    'lineColor':          '#94a3b8',
    'secondaryColor':     '#1e293b',
    'tertiaryColor':      '#0f172a',
    'background':         '#0f1117',
    'mainBkg':            '#1a1d27',
    'nodeBorder':         '#6366f1',
    'clusterBkg':         '#1e293b',
    'titleColor':         '#f1f5f9',
    'edgeLabelBackground':'#1a1d27',
    'fontFamily':         'Segoe UI, sans-serif'
  }
}}%%
```

### Look and layout (flowcharts and stateDiagram only)
```
---
config:
  look: handDrawn    # 'classic' | 'handDrawn'
  layout: elk        # 'dagre' (default) | 'elk' (better for dense graphs)
  theme: dark
---
flowchart LR
  A --> B --> C
```

---

## Step 4 — Flowcharts

The most versatile diagram type. Used for processes, decision trees, system flows, algorithms.

### Syntax reference
```
flowchart TD   %%  TD=top-down  LR=left-right  RL  BT

  %% Node shapes
  A[Rectangle]
  B(Rounded rectangle)
  C([Stadium / pill])
  D[[Subroutine]]
  E[(Database / cylinder)]
  F((Circle))
  G>Asymmetric]
  H{Diamond / decision}
  I{{Hexagon}}
  J[/Parallelogram/]
  K[\Reverse parallelogram\]

  %% Edge types
  A --> B              %% Arrow
  A --- B              %% Open line (no arrow)
  A -.-> B             %% Dotted arrow
  A ==> B              %% Thick arrow
  A -- "label" --> B   %% Labelled arrow
  A -->|label| B       %% Label on arrow (alternative)
  A --o B              %% Circle end
  A --x B              %% Cross end
  A <--> B             %% Bidirectional

  %% Subgraphs (clusters)
  subgraph group1["Group Title"]
    direction LR
    X --> Y
  end

  %% Styling
  style A fill:#6366f1,stroke:#818cf8,color:#fff
  classDef highlight fill:#6366f1,stroke:#818cf8,color:#fff,rx:8
  class A,B highlight
  linkStyle 0 stroke:#f43f5e,stroke-width:2
```

### Best practices
- Use `LR` for pipelines and chains; `TD` for hierarchies and trees
- Keep to 15–20 nodes maximum before splitting into subgraphs or separate diagrams
- Wrap labels containing special characters in `"quotes"` — especially `end`, `(`, `)`, `{`, `}`
- Use `classDef` + `class` for consistent group styling instead of per-node `style`

---

## Step 5 — Sequence Diagrams

For interactions between actors, API calls, auth flows, message passing.

```
sequenceDiagram
  autonumber                         %% number each message

  actor U as User
  participant FE as Frontend
  participant API as API Gateway
  participant Auth as Auth Service
  participant DB as Database

  U->>FE: Submit login form
  FE->>API: POST /auth/login
  API->>Auth: validate(credentials)

  alt Valid credentials
    Auth-->>API: { token, userId }
    API->>DB: log_session(userId)
    DB-->>API: ok
    API-->>FE: 200 { token }
    FE-->>U: Redirect to dashboard
  else Invalid credentials
    Auth-->>API: 401 Unauthorized
    API-->>FE: 401 { error }
    FE-->>U: Show error message
  end

  Note over Auth,DB: Tokens expire in 1h

  loop Refresh token
    FE->>API: GET /auth/refresh
    API-->>FE: New token
  end
```

**Arrow types:**
| Syntax | Meaning |
|---|---|
| `A->>B` | Solid arrow (sync request) |
| `A-->>B` | Dashed arrow (async response) |
| `A-)B` | Async message (open arrowhead) |
| `A-xB` | Crossed end (error / rejection) |

---

## Step 6 — Class Diagrams

For object models, data structures, type hierarchies.

```
classDiagram
  direction TB

  class Animal {
    +String name
    +int age
    #String species
    -String _internal
    +speak() String
    +move(direction) void
  }

  class Dog {
    +String breed
    +fetch() void
    +speak() String
  }

  class ITrainable {
    <<interface>>
    +train(command) bool
  }

  Animal <|-- Dog : extends
  Dog ..|> ITrainable : implements

  class Owner {
    +String name
    +List~Animal~ pets
    +adopt(animal) void
  }

  Owner "1" --> "0..*" Animal : owns
```

**Relationship types:**
| Syntax | Type |
|---|---|
| `A <\|-- B` | Inheritance (B extends A) |
| `A *-- B` | Composition |
| `A o-- B` | Aggregation |
| `A --> B` | Association |
| `A ..> B` | Dependency |
| `A ..\|> B` | Realization / implements |

---

## Step 7 — Entity Relationship Diagrams

For database schemas, data models.

```
erDiagram
  USER {
    int id PK
    string email UK
    string name
    timestamp created_at
  }

  ORDER {
    int id PK
    int user_id FK
    decimal total
    string status
  }

  ORDER_ITEM {
    int id PK
    int order_id FK
    int product_id FK
    int quantity
    decimal unit_price
  }

  PRODUCT {
    int id PK
    string name
    decimal price
    int stock
  }

  USER ||--o{ ORDER : "places"
  ORDER ||--|{ ORDER_ITEM : "contains"
  PRODUCT ||--o{ ORDER_ITEM : "included in"
```

**Cardinality:** `||` exactly one · `o|` zero or one · `|{` one or more · `o{` zero or more

---

## Step 8 — State Diagrams

For state machines, lifecycle flows, status transitions.

```
stateDiagram-v2
  [*] --> Idle

  Idle --> Active : login
  Active --> Idle : logout / timeout

  state Active {
    [*] --> Browsing
    Browsing --> InCart : add to cart
    InCart --> Browsing : continue shopping
    InCart --> Checkout : proceed
    Checkout --> [*] : order placed
  }

  note right of Idle : Session cookie cleared
```

---

## Step 9 — Git Graphs

For branching strategies, release workflows.

```
gitGraph LR:
  commit id: "init"
  branch develop
  checkout develop
  commit id: "feature-A"

  branch feature/login
  checkout feature/login
  commit id: "login-ui"
  commit id: "login-api"

  checkout develop
  merge feature/login tag: "v1.1"

  checkout main
  merge develop tag: "v1.0" type: HIGHLIGHT

  checkout develop
  commit id: "hotfix" type: REVERSE
```

**Commit types:** `NORMAL` · `REVERSE` (hollow circle) · `HIGHLIGHT` (filled square)

---

## Step 10 — Other Diagram Types

### Gantt
```
gantt
  title Project Roadmap Q1 2025
  dateFormat YYYY-MM-DD
  excludes weekends

  section Design
  Research    :done,    d1, 2025-01-06, 7d
  Wireframes  :active,  d2, after d1, 5d

  section Development
  Backend API :crit,    dev1, 2025-01-13, 14d
  Frontend    :         dev2, after d2, 21d
  Integration :crit,    dev3, after dev1, 7d

  section Launch
  QA Testing  :         qa1, after dev3, 5d
  Deployment  :milestone, after qa1, 0d
```

### Mindmap
```
mindmap
  root((Product Vision))
    Users
      Personas
        Power User
        Casual User
    Features
      Core
        Auth
        Dashboard
      Premium
        Analytics
    Tech Stack
      Frontend: React
      Backend: Node.js
```

### Quadrant Chart
```
quadrantChart
  title Feature Prioritization Matrix
  x-axis Low Effort --> High Effort
  y-axis Low Impact --> High Impact
  quadrant-1 Quick Wins
  quadrant-2 Major Projects
  quadrant-3 Fill-ins
  quadrant-4 Thankless Tasks

  Search: [0.3, 0.6]
  Auth: [0.45, 0.85]
  Dark mode: [0.2, 0.35]
  Analytics: [0.7, 0.75]
```

### Architecture Diagram (v11+)
```
architecture-beta
  group api(cloud)[API Layer]

  service db(database)[Database] in api
  service cache(server)[Redis Cache] in api
  service server(server)[App Server] in api
  service client(internet)[Client]

  client:R --> L:server
  server:B --> T:db
  server:B --> T:cache
```

---

## Step 11 — Design & Polish Guidelines

- **Always use dark theme** — `theme: 'dark'` in `mermaid.initialize()` with custom `themeVariables` for consistency
- **Custom colors** — override `primaryColor`, `primaryTextColor`, `lineColor`, `secondaryColor` via `themeVariables` to match the design system
- **Font** — set `fontFamily: 'Segoe UI, system-ui, sans-serif'` in the initialize config for consistency
- **Keep diagrams readable** — limit flowcharts to 15–20 nodes; for complex systems, split into multiple diagrams on one page
- **Label brevity** — use short node labels (2–4 words); add detail in subgraphs or separate sequence diagrams
- **Subgraphs for grouping** — use `subgraph` in flowcharts to visually separate concerns (frontend, backend, database)
- **Direction** — `TB` (top-bottom) for vertical flows, `LR` (left-right) for horizontal processes; choose based on the natural reading direction of the data
- **Multi-diagram pages** — use a `.grid` CSS layout with multiple `.mermaid` divs for related diagrams side by side
- **Accessibility** — Mermaid renders SVG with embedded text; add an `aria-label` on the wrapper div for screen reader context

---

## Step 12 — Complete Example: Multi-Diagram Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>System Documentation</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; padding: 32px 24px; }
    .page { max-width: 980px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 32px; box-shadow: 0 4px 24px rgba(0,0,0,0.4); }
    h1 { font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: 4px; }
    h2 { font-size: 1rem; font-weight: 600; color: #a5b4fc; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 24px; }
    .mermaid svg { max-width: 100%; height: auto; display: block; margin: 0 auto; }
  </style>
</head>
<body>
<div class="page">

  <div class="card">
    <h1>E-Commerce System</h1>
    <p class="sub">Architecture & flow documentation</p>

    <h2>Order Flow</h2>
    <p class="sub">From cart to fulfillment</p>
    <div class="mermaid">
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor':'#6366f1','primaryTextColor':'#f1f5f9','primaryBorderColor':'#818cf8','lineColor':'#94a3b8','secondaryColor':'#1e293b','tertiaryColor':'#0f172a','mainBkg':'#1a1d27','edgeLabelBackground':'#1a1d27'}}}%%
flowchart LR
  Cart([Cart]) --> Checkout{Checkout}
  Checkout -->|Guest| GuestForm[Guest Details]
  Checkout -->|Logged in| Shipping[Shipping]
  GuestForm --> Shipping
  Shipping --> Payment[Payment]
  Payment -->|Card| Stripe[Stripe API]
  Payment -->|Wallet| PayPal[PayPal API]
  Stripe & PayPal --> Confirm{Confirm}
  Confirm -->|Success| Order[(Order Created)]
  Confirm -->|Failure| Payment
  Order --> Notify[Notify User]
  Order --> Fulfill[Fulfillment Queue]
    </div>
  </div>

  <div class="card">
    <h2>Authentication Sequence</h2>
    <p class="sub">OAuth2 with refresh token pattern</p>
    <div class="mermaid">
%%{init: {'theme': 'dark'}}%%
sequenceDiagram
  autonumber
  actor U as User
  participant App
  participant Auth as Auth Server
  participant API

  U->>App: Login with Google
  App->>Auth: Authorization Request
  Auth-->>U: Consent Screen
  U-->>Auth: Grant Access
  Auth-->>App: Authorization Code
  App->>Auth: Exchange for Tokens
  Auth-->>App: Access + Refresh Tokens
  App->>API: Request + Access Token
  API-->>App: Protected Resource
  Note over App,API: Token expires after 1h
  App->>Auth: Refresh Token Request
  Auth-->>App: New Access Token
    </div>
  </div>

</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, securityLevel: 'loose' });</script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **The word `end`** breaks flowcharts and sequence diagrams — always wrap it: `["end"]` or `("end")`
- **Special characters in labels** — `(`, `)`, `{`, `}`, `<`, `>` inside node labels must be wrapped in `"quotes"`: `A["price > 0 (required)"]`
- **`%%{init: ...}%%` must be the very first line** of the diagram definition — any blank line or comment before it breaks the directive
- **`startOnLoad: true` only scans elements present at parse time** — if `.mermaid` divs are injected dynamically via JS, call `mermaid.contentLoaded()` or `mermaid.init(undefined, document.querySelectorAll('.mermaid'))` after injection
- **YAML frontmatter (`---`) requires the triple dash alone on its own line** — any other character on that line breaks parsing
- **Deeply nested subgraphs** reduce readability fast — prefer flat diagrams with clear edge labels over 3+ nesting levels
- **Very long labels** push nodes off-screen — keep labels under ~30 characters; line breaks via `<br/>` require `securityLevel: 'loose'`
- **`theme` set in `initialize()` can silently lose to browser caching** — for reliable theming in artifacts, always use the `%%{init}%%` directive directly in the diagram definition
