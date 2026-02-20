# Shared Cron Templates

Standard cron jobs for all agents. Personalize where noted.

## Required (Personalize)

### Morning Briefing
- **Schedule:** `0 8 * * 1-5` (8 AM weekdays — adjust per user)
- **Task:** Deliver personalized morning briefing with calendar, weather, tasks, priorities
- **Notes:** Each agent customizes for their human. Use Eisenhower matrix for prioritization.

## Standard (Copy As-Is)

### Memory Sync
- **Schedule:** `0 8,16,0 * * *` (8 AM, 4 PM, midnight)
- **Task:** Sync memory files, review recent context, update long-term memory

### Self-Improvement Loop
- **Schedule:** `0 14 * * *` (2 PM daily)
- **Task:** Research and self-improvement cycle

### Evening Wrap-Up
- **Schedule:** `0 18 * * 1-5` (6 PM weekdays)
- **Task:** Summarize day's activity, flag incomplete items, prep for next day

### Nightly Cleanup
- **Schedule:** `0 23 * * *` (11 PM daily)
- **Task:** Clean temp files, archive old data, run maintenance

### Weekly Review
- **Schedule:** `0 18 * * 0` (6 PM Sundays)
- **Task:** Review week's progress, plan next week, update project notes

## Timezone
All times in **Europe/London** — adjust if your human is elsewhere.
