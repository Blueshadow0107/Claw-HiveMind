# STATE.yaml Schema Specification

## Overview

STATE.yaml is the single source of truth for project coordination between agents. Sub-agents read and write this file instead of passing messages through an orchestrator.

## Schema (v1)

```yaml
# Required top-level fields
project: string          # Project identifier (kebab-case)
version: 1               # Schema version
created: ISO-8601        # When project was initialized
updated: ISO-8601        # Last modification timestamp
owner: string            # PM label that owns this project (e.g. pm-website-frontend)
status: string           # Overall project status: active | paused | done | failed

# Optional top-level
description: string      # What this project is about
blocked_by: string       # External dependency blocking the whole project
due: ISO-8601            # Project deadline (if any)

# Task list
tasks:
  - id: string           # Unique task ID within project (kebab-case)
    title: string        # Human-readable task name
    status: string       # pending | in_progress | blocked | done | failed
    owner: string        # Agent label responsible (e.g. pm-website-frontend)
    priority: string     # high | medium | low (default: medium)
    created: ISO-8601
    started: ISO-8601    # When status changed to in_progress
    completed: ISO-8601  # When status changed to done
    blocked_by: string   # Task ID this depends on (within same project)
    notes: string        # Free-form progress notes
    output: string       # Path to deliverable (file, directory, URL)
    error: string        # Error details if status is failed

# Actions queue — what should happen next
next_actions:
  - owner: string        # Which agent should act
    action: string       # What they should do
    unblocked_by: string # Task ID that unblocked this (optional)
```

## Status Flow

```
pending → in_progress → done
                      → failed
         → blocked → in_progress (when dependency resolves)
```

## Rules

1. **One writer at a time.** Agents should read → modify → write atomically. No concurrent writes.
2. **Always update `updated` timestamp** when modifying the file.
3. **Git commit every state change.** Format: `[STATE] {action}: {task_id}`
   - Actions: `create`, `start`, `complete`, `fail`, `block`, `unblock`, `add-task`, `update`
   - Example: `[STATE] complete: api-auth`
4. **next_actions drives coordination.** When a task completes, the completing agent updates next_actions for downstream agents.
5. **Owner is responsible for their tasks.** Don't update another agent's task status unless it's a timeout/failure escalation.

## Label Conventions

- PM agents: `pm-{project}-{scope}` (e.g. `pm-website-frontend`, `pm-research-grants`)
- Sub-sub-agents: `pm-{project}-{scope}-{subtask}` (e.g. `pm-website-frontend-hero`)
- Keep labels under 64 chars

## File Location

- Always at `{project_dir}/STATE.yaml`
- Project dir lives under a shared workspace accessible to all agents
- Default: `~/clawd/projects/{project}/STATE.yaml`

## Validation

A valid STATE.yaml must have:
- `project` (non-empty string)
- `version: 1`
- `updated` (valid ISO-8601)
- `status` (one of: active, paused, done, failed)
- At least one task with `id`, `title`, and `status`
