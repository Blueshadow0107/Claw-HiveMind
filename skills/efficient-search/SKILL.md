---
name: efficient-search
description: Token-efficient search, caching, and query optimization for AI agents. Use when (1) Searching memory or large document collections, (2) Implementing caching for repeated queries, (3) Optimizing RAG retrieval, (4) Reducing token burn on file reads, or (5) Designing query batching/strategies. Reduces API costs through intelligent caching, progressive loading, and query optimization.
---

# Efficient Search & Token Optimization

Optimize agent search operations to minimize token burn and maximize retrieval quality.

## Core Principles

1. **Never read what you can skip** — Check file sizes before reading
2. **Cache aggressively** — Repeated queries should hit cache, not disk/LLM
3. **Progressive disclosure** — Load summaries first, details only when needed
4. **Batch when possible** — Multiple small queries → one batched query

## Quick Patterns

### Pattern 1: File Size Check Before Read
```bash
# Check size first, then decide
wc -l <file>          # Line count
ls -lh <file>         # Human-readable size
head -50 <file>       # Preview first 50 lines
tail -50 <file>       # Preview last 50 lines
```

**Decision matrix:**
| Lines | Action |
|-------|--------|
| <100  | Read full file |
| 100-500 | Read last 100 lines or use head/tail |
| >500 | Search specific sections only |

### Pattern 2: Smart Memory Search
```python
# BAD: Load all memory, then search
read MEMORY.md
read memory/2026-01-01.md
read memory/2026-01-02.md
...

# GOOD: Semantic search first, then targeted reads
memory_search(query="trading strategy", maxResults=3)
memory_get(path="memory/2026-02-01.md", from=1, lines=50)  # Only relevant section
```

### Pattern 3: Session Summarization
When session tokens exceed 8k:
1. Write summary to `context/session-summary.md`
2. Suggest fresh session for new tasks
3. Reference summary instead of full history

## Caching Strategies

See [references/caching-patterns.md](references/caching-patterns.md) for:
- File content caching with checksums
- Query result caching with TTL
- Session-level memory caches
- Invalidation strategies

## Query Optimization

See [references/query-optimization.md](references/query-optimization.md) for:
- Keyword extraction for better retrieval
- Query batching patterns
- Relevance scoring
- Fallback strategies

## Token Budgeting

| Operation | Budget (tokens) | Action if Exceeded |
|-----------|-----------------|-------------------|
| Wake/init | 3,000 | Skip non-essential files |
| Single file read | 1,000 | Use head/tail/search |
| Tool output | 2,000 | Summarize before returning |
| Session total | 8,000 | Checkpoint & suggest refresh |

## Scripts

Use `scripts/check-token-budget.py` to track session token usage.
Use `scripts/smart-read.sh` for size-aware file reading.

## Integration Example

```python
# Before any file operation
from skills.efficient_search import smart_read, check_budget

# Check budget first
if not check_budget.allow_read("large-file.md"):
    summary = smart_read.extractive_summary("large-file.md")
else:
    content = smart_read.load("large-file.md")
```
