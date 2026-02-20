---
name: kilo-coding-agent
description: "Delegate coding tasks to Kilo (formerly OpenCode) TUI coding agent. Use when building features, refactoring, or running iterative coding tasks. Kilo supports multiple providers (OpenAI, Anthropic, free models via kilo/ prefix). Requires pty:true."
metadata:
  {
    "openclaw": { "emoji": "⚡", "requires": { "anyBins": ["kilo"] } },
  }
---

# Kilo Coding Agent

Kilo is a TUI-based coding agent (successor to OpenCode). It supports multiple AI providers, custom agents, and MCP servers.

## Quick Reference

```bash
# One-shot task (non-interactive)
kilo run "Your task here"

# Interactive TUI
kilo [project-dir]

# Headless server mode
kilo serve

# Web interface
kilo web
```

## ⚠️ PTY Required

Kilo is a terminal UI app. Always use `pty:true`:

```bash
# ✅ Correct
bash pty:true workdir:~/project command:"kilo run 'Build a REST API'"

# ❌ Wrong — will break
bash command:"kilo run 'Build a REST API'"
```

## One-Shot Tasks

```bash
# Quick task in a project
bash pty:true workdir:~/Projects/myapp command:"kilo run 'Add input validation to all API endpoints'"

# Scratch work (temp directory)
SCRATCH=$(mktemp -d) && cd $SCRATCH && git init
bash pty:true workdir:$SCRATCH command:"kilo run 'Create a Python CLI that converts CSV to JSON'"
```

## Background Tasks

```bash
# Start in background
bash pty:true workdir:~/project background:true command:"kilo run 'Refactor the auth module to use JWT'"
# Returns sessionId

# Monitor
process action:log sessionId:XXX
process action:poll sessionId:XXX

# Send input if needed
process action:submit sessionId:XXX data:"yes"

# Kill if stuck
process action:kill sessionId:XXX
```

## Agents

Kilo has built-in agents. List them:

```bash
kilo agent list
```

Default agents:
- **ask** — Read-only Q&A (no file edits, no commands)
- **code** — Full coding agent (default)

Create custom agents in project `.kilo/agent/` or global config.

## Models

```bash
# List available models
kilo models

# Free models (kilo/ prefix)
kilo/corethink:free
kilo/z-ai/glm-5:free
kilo/arcee-ai/trinity-large-preview:free

# Premium models
openai/gpt-5-codex
anthropic/claude-sonnet-4-20250514
```

To set model, configure in `~/.config/kilo/config.json` or project `.kilo/config.json`:

```json
{
  "mode": {
    "default": {
      "model": "anthropic/claude-sonnet-4-20250514"
    }
  }
}
```

## Project Config

Create `.kilo/` in your project root:

```
.kilo/
├── config.json    # Project-specific config
├── agent/         # Custom agents
│   └── my-agent.md
└── rules.md       # Project coding rules (like .cursorrules)
```

### config.json

```json
{
  "agent": {},
  "mode": {
    "default": {
      "model": "anthropic/claude-sonnet-4-20250514"
    }
  },
  "command": {},
  "plugin": []
}
```

## MCP Integration

Kilo supports MCP servers:

```bash
kilo mcp  # Manage MCP servers
```

## Key Paths

| Path | Purpose |
|------|---------|
| `~/.config/kilo/` | Global config |
| `~/.local/share/kilo/` | Data (sessions, bin) |
| `~/.cache/kilo/` | Cache |
| `~/.local/state/kilo/` | State |
| `.kilo/` | Project-level config |

## Debugging

```bash
kilo debug config     # Show resolved config
kilo debug paths      # Show all paths
kilo debug agent ask  # Show agent details
kilo debug skill      # List skills
```

## OpenClaw Integration

### For Aris (or any agent using Kilo as coding backend)

Add to the agent's OpenClaw config:

```json
{
  "agents": {
    "list": [
      {
        "id": "aris",
        "name": "Aris",
        "model": {
          "primary": "anthropic/claude-sonnet-4-20250514"
        },
        "tools": {
          "exec": {
            "allowlist": ["kilo *"]
          }
        }
      }
    ]
  }
}
```

Then Aris can delegate coding work to Kilo:

```bash
# From within an OpenClaw agent session
bash pty:true workdir:~/Projects/myapp background:true command:"kilo run 'Implement the feature'"
```

### Kilo as Sub-Agent Pattern

Field Marshal spawns task → sub-agent uses Kilo for implementation:

```
Field Marshal (orchestrator)
  └─ Sub-agent (OpenClaw session)
       └─ Kilo (coding execution)
```

## Rules

1. **Always pty:true** — Kilo is a TUI
2. **Use `kilo run` for one-shots** — cleaner than interactive mode
3. **Background for long tasks** — monitor with process:log
4. **Don't run in ~/clawd/** — keep workspace separate from coding projects
5. **Git repo recommended** — Kilo works best in git-tracked directories
