# STATE.yaml Orchestration Layer
# AGENTS.md — PM Delegation Pattern

## PM Delegation Pattern

Main session = coordinator ONLY. All execution goes to subagents.

### Workflow

1. **New task arrives** → Main agent assesses scope
2. **Check PROJECT_REGISTRY.md** for existing PM
3. **If PM exists** → `sessions_send(label="pm-xxx", message="[task]")`
4. **If new project** → `sessions_spawn(label="pm-xxx", task="[task]")`
5. **PM executes** → Updates STATE.yaml, reports back
6. **Main agent summarizes** → Reports completion to user

### Rules

- Main session: 0-2 tool calls max (spawn/send only)
- PMs own their STATE.yaml files
- PMs can spawn sub-subagents for parallel subtasks
- All state changes committed to git
- Main agent never polls — waits for PM reports or checks STATE.yaml on demand

### Label Conventions

```
pm-{project}-{scope}

Examples:
- pm-website-frontend
- pm-api-auth
- pm-research-docs
- pm-content-pipeline
```

### STATE.yaml Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Ready to start | PM should pick up |
| `in_progress` | Actively being worked | Normal state |
| `blocked` | Waiting on dependency | Check blocked_by field |
| `done` | Completed | Archive or close |
| `failed` | Error/needs intervention | Alert main agent |

### Recovery Patterns

**PM timeout (no update in 30 min):**
1. Check STATE.yaml for last update timestamp
2. If stale → spawn new PM with same label, continue from last known state
3. Mark old PM session as abandoned in registry

**PM failure (reports error):**
1. Update STATE.yaml with `status: failed`, `error: [message]`
2. Notify main agent with context
3. Main agent decides: retry, reassign, or escalate to user

**Dependency resolution:**
- PM polls `check_dependencies()` before starting blocked tasks
- When dependency completes, any PM can update dependent task to `pending`

### Example Interaction

```
User: "Refactor the auth module and update the docs"

Main agent:
1. Checks registry → no active pm-auth
2. Spawns: sessions_spawn(
     label="pm-auth-refactor",
     task="Refactor auth module, update docs. Track in STATE.yaml"
   )
3. Responds: "Spawned pm-auth-refactor. Monitoring via STATE.yaml"

PM subagent:
1. Creates ~/clawd/projects/auth-refactor/STATE.yaml
2. Breaks down tasks, updates status as work progresses
3. Commits STATE.yaml changes
4. Reports: "Auth refactor complete. 3 files changed, docs updated."

Main agent:
- Verifies STATE.yaml shows all tasks done
- Summarizes to user
```

### PROJECT_REGISTRY.md Format

```yaml
# ~/clawd/PROJECT_REGISTRY.md

projects:
  auth-refactor:
    pm_label: pm-auth-refactor
    state_file: ~/clawd/projects/auth-refactor/STATE.yaml
    created: 2026-02-20T10:00:00Z
    status: active  # active | paused | completed
    
  website-redesign:
    pm_label: pm-website-frontend
    state_file: ~/clawd/projects/website-redesign/STATE.yaml
    created: 2026-02-19T14:30:00Z
    status: active
```
