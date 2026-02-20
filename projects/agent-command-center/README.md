# Agent Command Center

A real-time web dashboard for managing an OpenClaw AI agent army. Clean, warm, professional design inspired by OpenClaw Studio.

## Stack
- React 18 + TypeScript + Vite
- Tailwind CSS + shadcn/ui
- Framer Motion (subtle animations)
- Fonts: JetBrains Mono (code), Plus Jakarta Sans (body), DM Serif Display (headings)

## Design
- **Not** a dark hacker terminal — warm off-white (`#FAF9F7`), muted teal accent (`#5BA69E`)
- Clean borders, pill-shaped badges, generous spacing
- Uppercase labels with wide letter-spacing

## Layout — Three Columns

### Left Sidebar (~22%)
- Agent list with avatars, names, status badges (RUNNING/IDLE/ERROR)
- Filter tabs: ALL / NEEDS ATTENTION / RUNNING / IDLE

### Center Panel (~45%)
- Agent header with avatar + name + status
- Model/thinking dropdowns
- Chat/activity feed (messages, thinking blocks, tool calls)
- Message input at bottom

### Right Panel (~33%)
- Agent settings: Identity, Display toggles, Session management
- Cron jobs list
- Heartbeats list
- Danger zone (delete agent)

## Colors
| Token | Value |
|-------|-------|
| Background (main) | `#FAF9F7` |
| Background (sidebar) | `#F5F4F1` |
| Cards | `#FFFFFF` |
| Primary accent | `#5BA69E` |
| Text primary | `#1A1A1A` |
| Text secondary | `#666666` |
| Borders | `#D8D6D3` |
| Status running | `#2A2A2A` bg, white text |
| Status idle | `#E0DFDD` bg |
| Danger | `#D94444` |

## Typography
- Labels: 10-11px, UPPERCASE, letter-spacing 1.5-3px, monospaced
- Body: 13-14px, Plus Jakarta Sans
- Agent names: 16-20px, bold, uppercase, wide spacing
- Code: JetBrains Mono, warm gray bg

## Components
- Border-radius: 12-16px containers, 8px inputs, 20px pill buttons/badges
- Shadows: minimal — use borders for separation
- Animations: subtle fade-in (200-300ms), no CRT/grain effects

## Build & Run

```bash
# Clone and install
git clone <repo-url>
cd agent-command-center
npm install

# Dev server
npm run dev
# → http://localhost:5173

# Production build
npm run build
# Output in dist/
```

## v1 Scope
- Mock data (5-7 agents with realistic names/statuses)
- No real WebSocket connection (v2)
- No auth/login
- Desktop-first (no mobile layout)

## Reference
Original project: `~/Projects/agent-command-center/` on Sripaad's machine.
