# Efficient Search Skill - Quick Start

## Installation

1. Copy skill to your workspace:
```bash
cp -r skills/efficient-search ~/.openclaw/workspace/skills/
```

2. No dependencies required - pure Python 3 + bash

## Usage Patterns

### 1. Before Reading Large Files

```bash
# Check if file fits your token budget
python3 skills/efficient-search/scripts/check-token-budget.py check memory/2026-02-01.md

# Smart read based on file size
./skills/efficient-search/scripts/smart-read.sh MEMORY.md
```

### 2. In Your Agent Session

```python
# Check budget before operations
python3 skills/efficient-search/scripts/check-token-budget.py status

# Result shows:
# {
#   "max_tokens": 8000,
#   "used_tokens": 2450,
#   "remaining_tokens": 5550,
#   "should_checkpoint": false
# }
```

### 3. Search with Caching

```python
# Search with automatic caching (10 min TTL)
python3 skills/efficient-search/scripts/cached-search.py "trading strategy" 5
```

## Token Budget Guidelines

| Phase | Target | Action |
|-------|--------|--------|
| Wake/init | <3k tokens | Skip non-essential files |
| Active work | <6k tokens | Normal operations |
| >8k tokens | Checkpoint | Summarize & suggest refresh |

## Integration with AGENTS.md

Add to your AGENTS.md token optimization section:

```markdown
## Token Efficiency

Use efficient-search skill for:
- File size checks before reads
- Token budget monitoring  
- Cached memory searches
- Smart truncation of large files
```

## Testing

Run validation:
```bash
cd skills/efficient-search

# Test token budget check
python3 scripts/check-token-budget.py estimate "This is a test sentence with about ten tokens."

# Test smart read on small file
./scripts/smart-read.sh SKILL.md

# Test smart read on large file (will auto-summarize)
./scripts/smart-read.sh references/query-optimization.md
```

## Key Features

✅ **File size awareness** - Never read more than needed  
✅ **Token budgeting** - Track usage, enforce limits  
✅ **Smart caching** - Cache search results (10 min TTL)  
✅ **Progressive loading** - Summaries first, details on demand  
✅ **Query optimization** - Keyword extraction, batching  

## Cost Savings Estimate

Based on Kimi K2 pricing (~$3/million tokens):

| Scenario | Without Skill | With Skill | Savings |
|----------|---------------|------------|---------|
| Wake up | 5k tokens | 2k tokens | 60% |
| Memory search | 500 tokens/query | 100 tokens/query | 80% |
| Large file read | 3k tokens | 500 tokens | 83% |
| Session (avg) | 12k tokens | 5k tokens | 58% |

**Monthly estimate:** If running 100 sessions/day = ~$3.60/month saved
