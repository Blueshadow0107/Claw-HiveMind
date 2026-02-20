---
name: open-loop-tracker
description: Track and manage open loops — items waiting for external response, pending decisions, or blocked tasks. Use when adding something to wait on, checking what's stale, resolving completed items, or during heartbeat reviews. Optimized for ADHD workflows where external tracking prevents mental load.
---

# Open Loop Tracker

Manages `memory/open-loops.md` as a lightweight waiting-on tracker.

## File Format

```markdown
# Open Loops

## 🔴 Blocked (needs action)
- [ ] [TOPIC] Waiting for: [what] | Since: [date] | Context: [brief]

## 🟡 Pending (in progress)
- [ ] [TOPIC] Waiting for: [what] | Since: [date] | Context: [brief]

## 🟢 Resolved (last 7 days)
- [x] [TOPIC] Resolved: [date] | Outcome: [brief]
```

## Operations

### Add Loop
```
- [ ] [API Keys] Waiting for: Sripaad to configure OpenAI | Since: 2026-02-01 | Context: Coding agents blocked
```

### Resolve Loop
Move from 🔴/🟡 to 🟢, mark `[x]`, add resolution date and outcome.

### Escalate
If loop age > threshold:
- >24h in 🔴 → ping with summary
- >4h in 🟡 during waking hours → gentle nudge

### Review (heartbeats)
1. Check 🔴 section for stale items (>24h)
2. Check 🟡 section for items that might resolve
3. Archive 🟢 items older than 7 days (delete or move to daily log)

## Staleness Thresholds
| Section | Threshold | Action |
|---------|-----------|--------|
| 🔴 Blocked | 24h | Ping user with summary |
| 🟡 Pending | 4h (waking) | Gentle nudge if decision-blocking |
| 🟢 Resolved | 7d | Archive to daily log |

## Example Ping Format
> **Open Loop:** API Keys for Coding Agents
> **Waiting since:** Feb 1, 2026 (32h ago)
> **Why it matters:** Blocks Codex/Claude Code/OpenCode practice
> **What I need:** Configure one of: OpenAI key, Claude credits, or GOOGLE_GENERATIVE_AI_API_KEY
