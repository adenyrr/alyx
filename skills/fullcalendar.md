---
name: fullcalendar
description: Create interactive calendar views using FullCalendar, delivered as self-contained HTML artifacts. Use this skill whenever someone needs a calendar display — month, week, day, or list views — with events that can be clicked, dragged, resized, or loaded from data. Trigger on requests like "make a calendar", "create a schedule view", "build an event calendar", "display events on a calendar", "show a weekly planner", or any prompt needing temporal event visualization. Do NOT use for Gantt charts or timeline ranges (→ vis-timeline skill), date pickers (→ plain HTML input), or data charts over time (→ chartjs/d3 skill).
---

# FullCalendar Skill

FullCalendar is a full-featured JavaScript calendar library that renders interactive month, week, day, and list views. It supports event creation, drag-and-drop, resizing, recurring events, date navigation, JSON event sources, and custom rendering—all in a responsive, mobile-friendly interface.

---

## Artifact Presentation & Use Cases

Every FullCalendar artifact is a self-contained HTML page with a dark theme. The visual structure follows:

- **Dark body** (`#0f1117`) fills the viewport
- **Card wrapper** (`#1a1d27`, 16px radius) centers the calendar
- **Title** (1.15rem, `#f1f5f9`) names the calendar
- **Subtitle** (0.82rem, `#64748b`) explains interaction hints
- **Calendar container** (explicit height) renders the interactive calendar
- **Dark-themed overrides** for FullCalendar's default CSS (toolbar, cells, events, popover)

### Typical use cases

- **Event calendars** — team schedules, meeting rooms, personal planners
- **Booking systems** — appointment slots with available/booked states
- **Project timelines** — task blocks spanning multiple days (month/week view)
- **Content calendars** — editorial or social media publish schedules
- **Availability displays** — show when people or resources are free/busy
- **Academic schedules** — class timetables in week/day views
- **Dashboard widgets** — embedded mini-calendar showing upcoming events

### What the user sees

An interactive calendar with clickable/draggable events, navigation arrows for month/week/day, and responsive layout. Events display with colored backgrounds, can span multiple days, and show details on click.

---

## When to Use FullCalendar vs. Alternatives

| Use FullCalendar when… | Use another tool when… |
|---|---|
| Calendar grid (month/week/day views) | Gantt chart or range timeline → **vis-timeline** |
| Drag-and-drop event scheduling | Simple date picker → plain `<input type="date">` |
| Recurring events (RRULE) | Data time series charts → **Chart.js / D3** |
| Multiple event sources (JSON) | Kanban board layout → custom DOM |
| All-day + timed events | Scrollable schedule list only → simple HTML list |
| Mobile-responsive calendar | Static printed calendar → CSS grid |

> **Rule of thumb:** if the user needs a calendar with month/week/day views and interactive events, use FullCalendar. For linear timelines or Gantt charts, use vis-timeline.

---

## Step 1 — CDN Setup

```html
<!-- FullCalendar (all-in-one bundle) -->
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@6/index.global.min.js"></script>
```

> The v6 global bundle includes all standard plugins (dayGrid, timeGrid, list, interaction). No separate CSS file needed—styles are injected automatically.

---

## Step 2 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Calendar</title>
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
      padding: 28px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }

    /* ── FullCalendar Dark Theme ── */
    .fc { --fc-border-color: rgba(255,255,255,0.08); --fc-page-bg-color: transparent; --fc-neutral-bg-color: rgba(255,255,255,0.03); --fc-today-bg-color: rgba(99,102,241,0.08); }
    .fc .fc-toolbar-title { font-size: 1rem; color: #f1f5f9; }
    .fc .fc-button { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; font-size: 12px; border-radius: 6px; padding: 4px 12px; }
    .fc .fc-button:hover { background: rgba(255,255,255,0.1); color: #f1f5f9; }
    .fc .fc-button-active { background: #6366f1 !important; color: #fff !important; border-color: #6366f1 !important; }
    .fc .fc-col-header-cell { background: rgba(255,255,255,0.03); }
    .fc .fc-col-header-cell-cushion { color: #94a3b8; font-size: 12px; font-weight: 500; text-decoration: none; }
    .fc .fc-daygrid-day-number { color: #94a3b8; font-size: 12px; text-decoration: none; }
    .fc .fc-daygrid-day.fc-day-today .fc-daygrid-day-number { color: #6366f1; font-weight: 700; }
    .fc .fc-event { border: none; border-radius: 4px; padding: 1px 4px; font-size: 11px; }
    .fc .fc-timegrid-slot { border-color: rgba(255,255,255,0.05); }
    .fc .fc-timegrid-axis-cushion { color: #64748b; font-size: 11px; }
    .fc .fc-list-event:hover td { background: rgba(255,255,255,0.05); }
    .fc .fc-popover { background: #1a1d27; border: 1px solid rgba(255,255,255,0.1); }
    .fc .fc-popover-header { background: rgba(255,255,255,0.03); color: #94a3b8; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Calendar Title</h1>
    <p class="sub">Click a date to add event · drag events to reschedule</p>
    <div id="calendar"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6/index.global.min.js"></script>
  <script>
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      // options...
    });
    calendar.render();
  </script>
</body>
</html>
```

---

## Step 3 — Minimal Setup

```javascript
const calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
  initialView: 'dayGridMonth',   // month view
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
  },
  editable: true,          // enable drag-and-drop
  selectable: true,        // click + drag to create events
  dayMaxEvents: true,      // show "+N more" popover
  nowIndicator: true,      // red line for current time (week/day views)
  events: [
    { title: 'Meeting', start: '2025-01-15T10:00:00', end: '2025-01-15T11:30:00', color: '#6366f1' },
    { title: 'Launch Day', start: '2025-01-20', allDay: true, color: '#22c55e' },
  ],
});
calendar.render();
```

---

## Step 4 — Event Format

```javascript
// Complete event object
{
  id: '1',
  title: 'Team Standup',
  start: '2025-01-15T09:00:00',      // ISO 8601
  end: '2025-01-15T09:30:00',
  allDay: false,
  color: '#6366f1',                    // background + border
  textColor: '#fff',
  url: 'https://example.com',         // click opens URL
  editable: true,                      // per-event override
  extendedProps: { category: 'work' }, // custom data
  display: 'block',                    // 'auto' | 'block' | 'list-item' | 'background' | 'inverse-background' | 'none'
}

// All-day event (date only, no time)
{ title: 'Holiday', start: '2025-01-20', color: '#22c55e' }

// Multi-day event
{ title: 'Conference', start: '2025-01-22', end: '2025-01-25', color: '#f97316' }
```

---

## Step 5 — Event Interactions

```javascript
const calendar = new FullCalendar.Calendar(el, {
  editable: true,
  selectable: true,

  // Click on a date range to create event
  select: (info) => {
    const title = prompt('Event title:');
    if (title) {
      calendar.addEvent({
        title,
        start: info.startStr,
        end: info.endStr,
        allDay: info.allDay,
        color: '#6366f1',
      });
    }
    calendar.unselect();
  },

  // Click on existing event
  eventClick: (info) => {
    if (confirm(`Delete "${info.event.title}"?`)) {
      info.event.remove();
    }
  },

  // Drag event to new date/time
  eventDrop: (info) => {
    console.log('Moved:', info.event.title, '→', info.event.startStr);
  },

  // Resize event duration
  eventResize: (info) => {
    console.log('Resized:', info.event.title, 'to', info.event.endStr);
  },
});
```

---

## Step 6 — Views

```javascript
initialView: 'dayGridMonth',   // options:

// dayGridMonth  — traditional month calendar
// timeGridWeek  — week with time slots
// timeGridDay   — single day with time slots
// listWeek      — list/agenda for the week
// listMonth     — list/agenda for the month
// listDay       — list/agenda for the day
// listYear      — list/agenda for the year
// multiMonthYear — year view with multiple months
```

---

## Step 7 — Date Navigation

```javascript
// Programmatic navigation
calendar.today();
calendar.prev();
calendar.next();
calendar.gotoDate('2025-06-01');
calendar.changeView('timeGridWeek');
calendar.changeView('dayGridMonth', '2025-03-01');

// Get current date
const currentDate = calendar.getDate();  // Date object
```

---

## Step 8 — Event Sources (Dynamic)

```javascript
// Array source
events: [
  { title: 'Event 1', start: '2025-01-10' },
  { title: 'Event 2', start: '2025-01-15' },
]

// Function source (called when view changes)
events: function(info, successCallback, failureCallback) {
  fetch(`/api/events?start=${info.startStr}&end=${info.endStr}`)
    .then(res => res.json())
    .then(events => successCallback(events))
    .catch(err => failureCallback(err));
}

// JSON feed (auto-adds start/end params)
events: { url: '/api/events', method: 'GET', extraParams: { filter: 'active' } }

// Multiple sources with colors
eventSources: [
  { events: workEvents, color: '#6366f1' },
  { events: personalEvents, color: '#22c55e' },
]
```

---

## Step 9 — Custom Rendering

```javascript
// Custom event content
eventContent: (arg) => {
  return {
    html: `<div style="padding:2px 6px;">
      <strong>${arg.event.title}</strong>
      <br><span style="font-size:10px; opacity:0.7;">${arg.timeText}</span>
    </div>`,
  };
},

// Custom day cell content
dayCellContent: (arg) => {
  return { html: `<span>${arg.dayNumberText.replace('日', '')}</span>` };
},

// Event class names
eventClassNames: (arg) => {
  return arg.event.extendedProps.priority === 'high' ? ['high-priority'] : [];
},
```

---

## Step 10 — Design & Polish Guidelines

- **Dark CSS overrides** — FullCalendar ships with light defaults; always override `--fc-border-color`, `--fc-page-bg-color`, `--fc-today-bg-color`, and toolbar button styles
- **Event colors** — assign colors per event category; use the project palette (`#6366f1`, `#22c55e`, `#ec4899`, `#f97316`, `#06b6d4`)
- **Toolbar consistency** — style buttons with `rgba(255,255,255,0.06)` background and `#94a3b8` text; active state with `#6366f1`
- **Font sizes** — FullCalendar defaults are too large for embedded cards; scale down day numbers to `12px`, events to `11px`
- **Today indicator** — use `nowIndicator: true` for week/day views; today's cell gets a subtle accent background
- **dayMaxEvents** — set `dayMaxEvents: true` to prevent overcrowded cells; the "+N more" popover should also be dark-themed
- **Responsive** — FullCalendar is responsive by default; on narrow screens, consider defaulting to `listWeek` view
- **Event border radius** — add `border-radius: 4px` to `.fc-event` for softer look
- **Select highlight** — the drag-to-select highlight should be subtle; use `--fc-highlight-color: rgba(99,102,241,0.15)`
- **Time slot height** — adjust `slotMinTime` and `slotMaxTime` to show only relevant hours (e.g., `06:00` to `22:00`)

---

## Step 11 — Complete Example: Team Calendar

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Team Calendar</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 28px; width: 100%; max-width: 1000px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p.sub { font-size: 0.82rem; color: #64748b; margin-bottom: 20px; }

    .fc { --fc-border-color: rgba(255,255,255,0.08); --fc-page-bg-color: transparent; --fc-neutral-bg-color: rgba(255,255,255,0.03); --fc-today-bg-color: rgba(99,102,241,0.08); --fc-highlight-color: rgba(99,102,241,0.15); }
    .fc .fc-toolbar-title { font-size: 1rem; color: #f1f5f9; }
    .fc .fc-button { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; font-size: 12px; border-radius: 6px; padding: 4px 12px; }
    .fc .fc-button:hover { background: rgba(255,255,255,0.1); color: #f1f5f9; }
    .fc .fc-button-active { background: #6366f1 !important; color: #fff !important; border-color: #6366f1 !important; }
    .fc .fc-col-header-cell { background: rgba(255,255,255,0.03); }
    .fc .fc-col-header-cell-cushion { color: #94a3b8; font-size: 12px; font-weight: 500; text-decoration: none; }
    .fc .fc-daygrid-day-number { color: #94a3b8; font-size: 12px; text-decoration: none; }
    .fc .fc-daygrid-day.fc-day-today .fc-daygrid-day-number { color: #6366f1; font-weight: 700; }
    .fc .fc-event { border: none; border-radius: 4px; padding: 1px 4px; font-size: 11px; cursor: pointer; }
    .fc .fc-timegrid-slot { border-color: rgba(255,255,255,0.05); }
    .fc .fc-timegrid-axis-cushion { color: #64748b; font-size: 11px; }
    .fc .fc-popover { background: #1a1d27; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; }
    .fc .fc-popover-header { background: rgba(255,255,255,0.05); color: #94a3b8; border-radius: 10px 10px 0 0; }
    .fc .fc-list-event:hover td { background: rgba(255,255,255,0.05); }
    .fc .fc-list-day-cushion { background: rgba(255,255,255,0.03); }
    .fc .fc-list-event-title a { color: #e2e8f0; text-decoration: none; }
    .fc .fc-list-event-time { color: #94a3b8; }

    .legend { display: flex; gap: 16px; margin-top: 16px; flex-wrap: wrap; }
    .legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #94a3b8; }
    .legend-dot { width: 10px; height: 10px; border-radius: 3px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Team Calendar</h1>
    <p class="sub">Click + drag a date range to add events · click an event to delete · drag events to reschedule</p>
    <div id="calendar"></div>
    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:#6366f1;"></div>Meeting</div>
      <div class="legend-item"><div class="legend-dot" style="background:#22c55e;"></div>Milestone</div>
      <div class="legend-item"><div class="legend-dot" style="background:#f97316;"></div>Deadline</div>
      <div class="legend-item"><div class="legend-dot" style="background:#ec4899;"></div>Social</div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6/index.global.min.js"></script>
  <script>
    const COLORS = { meeting: '#6366f1', milestone: '#22c55e', deadline: '#f97316', social: '#ec4899' };
    const today = new Date();
    const y = today.getFullYear();
    const m = String(today.getMonth() + 1).padStart(2, '0');

    const events = [
      { title: 'Sprint Planning', start: `${y}-${m}-05T09:00:00`, end: `${y}-${m}-05T10:30:00`, color: COLORS.meeting },
      { title: 'Design Review', start: `${y}-${m}-08T14:00:00`, end: `${y}-${m}-08T15:00:00`, color: COLORS.meeting },
      { title: 'v2.0 Release', start: `${y}-${m}-12`, allDay: true, color: COLORS.milestone },
      { title: 'Report Due', start: `${y}-${m}-18`, allDay: true, color: COLORS.deadline },
      { title: 'Team Lunch', start: `${y}-${m}-20T12:00:00`, end: `${y}-${m}-20T13:30:00`, color: COLORS.social },
      { title: 'Hackathon', start: `${y}-${m}-22`, end: `${y}-${m}-24`, color: COLORS.milestone },
      { title: 'Retro', start: `${y}-${m}-25T16:00:00`, end: `${y}-${m}-25T17:00:00`, color: COLORS.meeting },
    ];

    const calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
      initialView: 'dayGridMonth',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,listWeek',
      },
      editable: true,
      selectable: true,
      dayMaxEvents: true,
      nowIndicator: true,
      slotMinTime: '07:00:00',
      slotMaxTime: '21:00:00',
      events,

      select(info) {
        const title = prompt('Event title:');
        if (title) {
          const cat = prompt('Category (meeting/milestone/deadline/social):', 'meeting') || 'meeting';
          calendar.addEvent({
            title,
            start: info.startStr,
            end: info.endStr,
            allDay: info.allDay,
            color: COLORS[cat] || COLORS.meeting,
          });
        }
        calendar.unselect();
      },

      eventClick(info) {
        if (confirm(`Delete "${info.event.title}"?`)) info.event.remove();
      },
    });
    calendar.render();
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Missing global bundle** — use `fullcalendar@6/index.global.min.js` which includes all plugins; individual plugin imports are for npm/ESM only
- **No `calendar.render()`** — the calendar won't appear without calling `.render()` after construction
- **Dark theme not applied** — FullCalendar's default styles are light; always override CSS custom properties and button/cell styles
- **`editable: true` without interaction plugin** — the global bundle includes it, but if using ESM, `@fullcalendar/interaction` must be imported
- **Event `end` is exclusive** — an event ending on `2025-01-25` will NOT show on Jan 25; it's exclusive (up to but not including)
- **No `selectable: true`** — without it, click+drag date selection won't work; both `selectable` and a `select` callback are needed
- **Missing `allDay` for all-day events** — dates without times default to all-day, but explicitly setting `allDay: true` is clearer
- **Toolbar overflow on mobile** — the default toolbar with many buttons wraps badly; simplify for mobile or use responsive views
- **Popover not dark-themed** — the "+N more" popover has its own styles; override `.fc-popover` and `.fc-popover-header`
- **Not unselecting** — call `calendar.unselect()` after handling the `select` event to clear the visual highlight
