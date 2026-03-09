---
name: shadcn-ui
description: Build polished, accessible React interfaces using shadcn/ui components, delivered as React artifacts (.jsx). Use this skill whenever someone needs a production-quality React UI with pre-built accessible components: dashboards, settings panels, forms with validation, data tables, modals, command palettes, sidebars, or any complex interactive UI. Trigger on requests like "build a settings page", "create a dashboard with tabs and cards", "make a dialog with a form", "build a data table with filtering", "create a command palette", or any React UI request that would benefit from ready-made accessible components. shadcn/ui shines for polished, complex interfaces where accessibility, keyboard navigation, and visual consistency matter. Do NOT use for static HTML pages (→ bulma-css or tailwind-css), raw canvas/WebGL (→ threejs-3d or p5js), or data visualization charts (→ charting skill).
---

# shadcn/ui Skill — React Artifacts

shadcn/ui is not a traditional component library — it is a **collection of copy-paste React components** built on top of Radix UI primitives and styled with Tailwind CSS. There is no npm package to install and no CDN URL. In Claude artifacts, shadcn/ui components are available via pre-configured `@/components/ui/` imports.

---

## Artifact Presentation & Use Cases

Every shadcn/ui artifact is a React component (`.jsx`) rendered in the artifact sandbox. The visual structure follows:

- **Dark background** via CSS variables (`--background: #0f1117`) applied to the root
- **Card components** (`<Card>`) with dark surfaces, subtle borders, and rounded corners
- **Typography** — Tailwind utilities for consistent text sizing and color
- **Interactive components** — Radix-based primitives with keyboard navigation and ARIA attributes
- **State management** via React hooks (`useState`, `useEffect`) for dynamic UI updates

### Typical use cases

- **Settings panels** — tabs, switches, selects, forms with validation and save actions
- **Dashboards** — card grids, summary stats, data tables, navigation sidebars
- **Forms** — multi-step wizards, validated inputs, file uploads, date pickers
- **Command palettes** — searchable command menus with keyboard shortcuts
- **Data tables** — sortable, filterable tables with pagination and row actions
- **Modal dialogs** — confirmation dialogs, detail views, form modals with proper focus trapping

### What the user sees

A polished React interface: accessible components respond to keyboard and mouse, modals trap focus correctly, selects and dropdowns align automatically, and the dark theme is consistent across all components. The UI feels production-ready without additional styling effort.

---

## When to Use shadcn/ui vs. Alternatives

| Use shadcn/ui when… | Use another tool when… |
|---|---|
| Complex React UI with state management | Static HTML page with no interactivity → **Bulma / Tailwind** |
| Accessible components (keyboard, ARIA) | Data visualization charts → **Chart.js / Plotly / D3** |
| Dashboards with tabs, modals, forms | Tabular data with sort/filter/edit → **Tabulator** (HTML) |
| Command palette, data table, dialogs | Diagrams and flowcharts → **Mermaid** |
| Production-quality UI patterns | DOM/SVG animations → **Anime.js** |
| Tailwind-styled component consistency | Interactive maps → **Leaflet** |

> **Rule of thumb:** if the output is a React app with interactive UI components (forms, modals, tables, navigation), use shadcn/ui. For static HTML pages, use Tailwind or Bulma.

---

## Step 1 — How shadcn/ui Works in Artifacts

In React artifacts, shadcn/ui components are pre-available via imports from `@/components/ui/`. Every component is styled with Tailwind utility classes and uses Radix UI under the hood for accessibility (keyboard navigation, focus management, ARIA attributes).

```jsx
// Import pattern — from @/components/ui/<component>
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Slider } from '@/components/ui/slider'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
```

> **⚠️ No CDN, no npm install.** shadcn/ui components are available in artifacts via the `@/components/ui/` import path only. They do NOT work in plain HTML files — only in React (`.jsx`) artifacts.

---

## Step 2 — React Artifact Shell

```jsx
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function App() {
  return (
    <div className="min-h-screen bg-background text-foreground p-6">
      {/* Your UI here */}
    </div>
  )
}
```

### CSS variable tokens (use these in `className`)
shadcn/ui defines a semantic color system via CSS variables. Always prefer these over raw Tailwind palette colors:

```
-- Backgrounds --
bg-background        // main page background
bg-card              // card surface
bg-popover           // dropdown / popover surface
bg-muted             // subtle background (inactive, code blocks)
bg-accent            // hover highlight background
bg-primary           // brand primary (buttons)
bg-secondary         // secondary button / pill background
bg-destructive       // red destructive action

-- Text --
text-foreground      // main body text
text-muted-foreground  // secondary / placeholder text
text-card-foreground
text-primary-foreground  // text on primary bg
text-secondary-foreground
text-accent-foreground
text-destructive

-- Borders --
border-border        // default border color
border-input         // input border
border-ring          // focus ring

-- Other --
ring-ring            // focus ring color
```

---

## Step 3 — Complete Component Reference

### Button
```jsx
import { Button } from "@/components/ui/button"

<Button>Default</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Delete</Button>
<Button variant="link">Link style</Button>

<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><TrashIcon className="h-4 w-4" /></Button>

<Button disabled>Disabled</Button>
<Button onClick={handleClick} className="w-full">Full width</Button>
```

### Card
```jsx
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Supporting description text</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Main content goes here.</p>
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="outline">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>
```

### Input & Label
```jsx
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

<div className="space-y-1.5">
  <Label htmlFor="email">Email address</Label>
  <Input id="email" type="email" placeholder="you@example.com" />
</div>

<div className="space-y-1.5">
  <Label htmlFor="bio">Bio</Label>
  <Textarea id="bio" placeholder="Tell us about yourself…" rows={4} />
</div>

// Controlled input
const [value, setValue] = useState("")
<Input value={value} onChange={(e) => setValue(e.target.value)} />
```

### Badge
```jsx
import { Badge } from "@/components/ui/badge"

<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="outline">Outline</Badge>
<Badge variant="destructive">Destructive</Badge>
```

### Alert
```jsx
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

<Alert>
  <AlertTitle>Info</AlertTitle>
  <AlertDescription>Your session will expire in 5 minutes.</AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Something went wrong. Please try again.</AlertDescription>
</Alert>
```

### Tabs
```jsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

<Tabs defaultValue="overview">
  <TabsList>
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="analytics">Analytics</TabsTrigger>
    <TabsTrigger value="settings">Settings</TabsTrigger>
  </TabsList>

  <TabsContent value="overview">
    <p>Overview content here.</p>
  </TabsContent>
  <TabsContent value="analytics">
    <p>Analytics content here.</p>
  </TabsContent>
  <TabsContent value="settings">
    <p>Settings content here.</p>
  </TabsContent>
</Tabs>
```

### Dialog (Modal)
```jsx
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open dialog</Button>
  </DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit profile</DialogTitle>
      <DialogDescription>Make changes to your profile here.</DialogDescription>
    </DialogHeader>
    {/* form content */}
    <DialogFooter>
      <Button type="submit">Save changes</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>

// Controlled dialog
const [open, setOpen] = useState(false)
<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <Button onClick={() => setOpen(false)}>Close</Button>
  </DialogContent>
</Dialog>
```

### Select
```jsx
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select"

// Uncontrolled
<Select onValueChange={(value) => console.log(value)}>
  <SelectTrigger className="w-[200px]">
    <SelectValue placeholder="Select a role" />
  </SelectTrigger>
  <SelectContent>
    <SelectGroup>
      <SelectLabel>Roles</SelectLabel>
      <SelectItem value="admin">Admin</SelectItem>
      <SelectItem value="editor">Editor</SelectItem>
      <SelectItem value="viewer">Viewer</SelectItem>
    </SelectGroup>
  </SelectContent>
</Select>

// Controlled
const [role, setRole] = useState("viewer")
<Select value={role} onValueChange={setRole}>
```

### Switch
```jsx
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"

const [enabled, setEnabled] = useState(false)

<div className="flex items-center gap-3">
  <Switch id="notifications" checked={enabled} onCheckedChange={setEnabled} />
  <Label htmlFor="notifications">Enable notifications</Label>
</div>
```

### Slider
```jsx
import { Slider } from "@/components/ui/slider"

const [volume, setVolume] = useState([50])

<Slider
  min={0} max={100} step={1}
  value={volume}
  onValueChange={setVolume}
  className="w-full"
/>
<p className="text-sm text-muted-foreground">Volume: {volume[0]}%</p>
```

### Progress
```jsx
import { Progress } from "@/components/ui/progress"

const [value, setValue] = useState(65)
<Progress value={value} className="w-full" />
```

### Separator
```jsx
import { Separator } from "@/components/ui/separator"

<Separator />                                    // horizontal line
<Separator orientation="vertical" className="h-4" /> // vertical line
```

### Avatar
```jsx
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

<Avatar>
  <AvatarImage src="https://github.com/shadcn.png" alt="User" />
  <AvatarFallback>AB</AvatarFallback>  {/* shown while image loads or on error */}
</Avatar>
```

### Tooltip
```jsx
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

// Wrap your app or the relevant section with TooltipProvider
<TooltipProvider>
  <Tooltip>
    <TooltipTrigger asChild>
      <Button variant="ghost" size="icon"><SettingsIcon /></Button>
    </TooltipTrigger>
    <TooltipContent>
      <p>Settings</p>
    </TooltipContent>
  </Tooltip>
</TooltipProvider>
```

### Checkbox
```jsx
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"

const [checked, setChecked] = useState(false)

<div className="flex items-center gap-2">
  <Checkbox id="terms" checked={checked} onCheckedChange={setChecked} />
  <Label htmlFor="terms">Accept terms and conditions</Label>
</div>
```

### RadioGroup
```jsx
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"

<RadioGroup defaultValue="monthly" onValueChange={(v) => console.log(v)}>
  <div className="flex items-center gap-2">
    <RadioGroupItem value="monthly" id="monthly" />
    <Label htmlFor="monthly">Monthly billing</Label>
  </div>
  <div className="flex items-center gap-2">
    <RadioGroupItem value="annual" id="annual" />
    <Label htmlFor="annual">Annual billing (save 20%)</Label>
  </div>
</RadioGroup>
```

### ScrollArea
```jsx
import { ScrollArea } from "@/components/ui/scroll-area"

<ScrollArea className="h-72 w-full rounded-md border">
  <div className="p-4">
    {longList.map((item) => (
      <div key={item.id} className="py-2 border-b border-border last:border-0">
        {item.name}
      </div>
    ))}
  </div>
</ScrollArea>
```

### Sheet (Slide-over panel)
```jsx
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"

<Sheet>
  <SheetTrigger asChild>
    <Button variant="outline">Open panel</Button>
  </SheetTrigger>
  <SheetContent side="right">   {/* "left" | "right" | "top" | "bottom" */}
    <SheetHeader>
      <SheetTitle>Edit settings</SheetTitle>
      <SheetDescription>Make changes to your settings.</SheetDescription>
    </SheetHeader>
    {/* panel content */}
  </SheetContent>
</Sheet>
```

### Dropdown Menu
```jsx
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="outline">Options ▾</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent className="w-48">
    <DropdownMenuLabel>My Account</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuItem onClick={() => {}}>Profile</DropdownMenuItem>
    <DropdownMenuItem onClick={() => {}}>Settings</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem onClick={() => {}} className="text-destructive">
      Logout
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

### Skeleton (loading placeholder)
```jsx
import { Skeleton } from "@/components/ui/skeleton"

<div className="space-y-3">
  <Skeleton className="h-5 w-2/3" />
  <Skeleton className="h-4 w-full" />
  <Skeleton className="h-4 w-full" />
  <Skeleton className="h-4 w-3/4" />
</div>

// Avatar skeleton
<div className="flex items-center gap-4">
  <Skeleton className="h-10 w-10 rounded-full" />
  <div className="space-y-2">
    <Skeleton className="h-4 w-36" />
    <Skeleton className="h-3 w-24" />
  </div>
</div>
```

---

## Step 4 — Layout & Composition Patterns

### Settings page layout
```jsx
<div className="min-h-screen bg-background">
  <div className="max-w-3xl mx-auto px-6 py-10 space-y-8">
    <div>
      <h1 className="text-2xl font-semibold">Settings</h1>
      <p className="text-muted-foreground text-sm mt-1">Manage your account preferences</p>
    </div>
    <Separator />
    <Card>
      <CardHeader>
        <CardTitle>Profile</CardTitle>
        <CardDescription>Update your personal information</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* form fields */}
      </CardContent>
      <CardFooter>
        <Button>Save changes</Button>
      </CardFooter>
    </Card>
  </div>
</div>
```

### Dashboard with tabs and stats
```jsx
<div className="p-6 space-y-6">
  {/* Stats row */}
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    {stats.map(s => (
      <Card key={s.label}>
        <CardHeader className="pb-2">
          <CardDescription>{s.label}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{s.value}</div>
          <p className="text-xs text-muted-foreground mt-1">{s.change}</p>
        </CardContent>
      </Card>
    ))}
  </div>

  {/* Tabs with content */}
  <Tabs defaultValue="overview">
    <TabsList>
      <TabsTrigger value="overview">Overview</TabsTrigger>
      <TabsTrigger value="recent">Recent</TabsTrigger>
    </TabsList>
    <TabsContent value="overview" className="mt-4">
      <Card>
        <CardContent className="pt-6">
          {/* chart or content */}
        </CardContent>
      </Card>
    </TabsContent>
  </Tabs>
</div>
```

---

## Step 5 — Design & Polish Guidelines

- **Dark theme via CSS variables** — define `--background`, `--foreground`, `--card`, `--muted`, `--accent`, `--primary` in the root style; all shadcn components inherit these
- **Consistent spacing** — use Tailwind’s spacing scale (`p-4`, `gap-6`, `mb-3`) rather than arbitrary pixel values
- **Accessible by default** — shadcn components include ARIA attributes, keyboard navigation, and focus rings; do not override `outline` styles
- **Composition over customization** — compose small components (`Card` + `CardHeader` + `CardContent`) rather than building monolithic components
- **Form patterns** — pair `<Label>` with `<Input>` using `htmlFor`/`id`; group related fields in `<div className="space-y-2">`
- **Dialog focus** — `<Dialog>` automatically traps focus and returns it on close; do not add custom focus management
- **Loading states** — use `disabled` prop on `<Button>` during async operations; add a spinner icon inside the button
- **Toast notifications** — use `sonner` for ephemeral feedback; place `<Toaster />` once at the root level
- **Responsive layout** — use Tailwind’s responsive prefixes (`sm:grid-cols-2 lg:grid-cols-3`) on grid containers

---

## Step 6 — Complete Example: User Settings Panel

```jsx
import { useState } from "react"
import { Button }       from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input }        from "@/components/ui/input"
import { Label }        from "@/components/ui/label"
import { Switch }       from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge }        from "@/components/ui/badge"
import { Separator }    from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function Settings() {
  const [saved, setSaved]     = useState(false)
  const [notifs, setNotifs]   = useState({ email: true, push: false, digest: true })
  const [profile, setProfile] = useState({ name: "Alice Martin", email: "alice@example.com", role: "admin" })

  const handleSave = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 2500)
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-2xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold">Settings</h1>
            <p className="text-sm text-muted-foreground mt-0.5">Manage your account preferences</p>
          </div>
          <Badge variant="outline">Pro plan</Badge>
        </div>

        {saved && (
          <Alert>
            <AlertDescription>✓ Settings saved successfully.</AlertDescription>
          </Alert>
        )}

        <Tabs defaultValue="profile">
          <TabsList className="w-full">
            <TabsTrigger value="profile"  className="flex-1">Profile</TabsTrigger>
            <TabsTrigger value="notifs"   className="flex-1">Notifications</TabsTrigger>
            <TabsTrigger value="security" className="flex-1">Security</TabsTrigger>
          </TabsList>

          {/* ── Profile tab ── */}
          <TabsContent value="profile" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Personal information</CardTitle>
                <CardDescription>Update your name, email, and role.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-1.5">
                  <Label htmlFor="name">Full name</Label>
                  <Input id="name" value={profile.name} onChange={e => setProfile(p => ({ ...p, name: e.target.value }))} />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="email">Email address</Label>
                  <Input id="email" type="email" value={profile.email} onChange={e => setProfile(p => ({ ...p, email: e.target.value }))} />
                </div>
                <div className="space-y-1.5">
                  <Label>Role</Label>
                  <Select value={profile.role} onValueChange={v => setProfile(p => ({ ...p, role: v }))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="admin">Admin</SelectItem>
                      <SelectItem value="editor">Editor</SelectItem>
                      <SelectItem value="viewer">Viewer</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
              <CardFooter>
                <Button onClick={handleSave}>Save changes</Button>
              </CardFooter>
            </Card>
          </TabsContent>

          {/* ── Notifications tab ── */}
          <TabsContent value="notifs" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Notification preferences</CardTitle>
                <CardDescription>Choose how you want to be notified.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-0 divide-y divide-border">
                {[
                  { key: "email", label: "Email notifications", desc: "Receive updates via email" },
                  { key: "push",  label: "Push notifications",  desc: "Browser push alerts" },
                  { key: "digest",label: "Weekly digest",       desc: "Summary email every Monday" },
                ].map(item => (
                  <div key={item.key} className="flex items-center justify-between py-4">
                    <div>
                      <p className="text-sm font-medium">{item.label}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">{item.desc}</p>
                    </div>
                    <Switch
                      checked={notifs[item.key]}
                      onCheckedChange={v => setNotifs(n => ({ ...n, [item.key]: v }))}
                    />
                  </div>
                ))}
              </CardContent>
              <CardFooter>
                <Button onClick={handleSave}>Save preferences</Button>
              </CardFooter>
            </Card>
          </TabsContent>

          {/* ── Security tab ── */}
          <TabsContent value="security" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Change password</CardTitle>
                <CardDescription>Use a strong password with at least 12 characters.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-1.5">
                  <Label htmlFor="current">Current password</Label>
                  <Input id="current" type="password" placeholder="••••••••••••" />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="new">New password</Label>
                  <Input id="new" type="password" placeholder="••••••••••••" />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="confirm">Confirm new password</Label>
                  <Input id="confirm" type="password" placeholder="••••••••••••" />
                </div>
              </CardContent>
              <CardFooter className="flex justify-between">
                <Button variant="outline">Cancel</Button>
                <Button onClick={handleSave}>Update password</Button>
              </CardFooter>
            </Card>
            <Separator className="my-4" />
            <Card className="border-destructive/40">
              <CardHeader>
                <CardTitle className="text-destructive">Danger zone</CardTitle>
                <CardDescription>Irreversible account actions.</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">Deleting your account will permanently remove all data. This action cannot be undone.</p>
              </CardContent>
              <CardFooter>
                <Button variant="destructive">Delete account</Button>
              </CardFooter>
            </Card>
          </TabsContent>

        </Tabs>
      </div>
    </div>
  )
}
```

---

## Common Mistakes to Avoid

- **Importing from `shadcn/ui` (npm package)** — there is no `import { Button } from 'shadcn/ui'`. The correct path is always `@/components/ui/button` (and other per-component paths). A bare `shadcn/ui` import will fail with "module not found"
- **Using shadcn/ui in plain HTML artifacts** — components require React and JSX. Always use a `.jsx` artifact (React), not a `.html` artifact, when using shadcn/ui
- **Forgetting `asChild` on trigger elements** — when wrapping your own button/link inside `DialogTrigger`, `SheetTrigger`, or `TooltipTrigger`, add `asChild` to avoid double-rendering a button inside a button: `<DialogTrigger asChild><Button>Open</Button></DialogTrigger>`
- **Hardcoding raw Tailwind colors instead of semantic tokens** — use `bg-background`, `text-foreground`, `border-border`, `text-muted-foreground` etc. instead of `bg-gray-900`, `text-gray-100`. Raw palette colors won't adapt if the theme changes
- **Not wrapping tooltips in `TooltipProvider`** — `<Tooltip>` requires a `<TooltipProvider>` ancestor. Without it, tooltips silently don't appear. Wrap your entire app or the component tree with `<TooltipProvider>`
- **Controlled vs uncontrolled mismatch** — don't mix controlled and uncontrolled usage: if you pass `value` to `Select`, you must also pass `onValueChange`. Passing `value` without `onValueChange` creates a read-only field that never changes
- **Putting content in `Dialog` outside `DialogContent`** — the visible modal content must be inside `<DialogContent>`. Content accidentally placed outside (e.g., as sibling of `DialogTrigger`) will appear inline in the page, not in the modal
- **`localStorage` in artifacts** — browser storage APIs are not supported in Claude artifacts. Use `useState` or `useReducer` to persist state within a session instead
- **Expecting server-side features** — shadcn/ui in artifacts is a client-side React environment. There is no server, no `next/dynamic`, no server components, no file system access. All data must be hardcoded or generated in component state
