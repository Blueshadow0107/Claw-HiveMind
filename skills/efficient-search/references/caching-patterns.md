# Caching Patterns for Agent Efficiency

## File Content Cache

Cache file contents by checksum to avoid re-reading unchanged files.

```python
import hashlib
import json
import os
from pathlib import Path

CACHE_DIR = Path(".cache/agent-files")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def file_checksum(path: str) -> str:
    """Generate MD5 checksum of file contents."""
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def cached_read(path: str, max_age_seconds: int = 300) -> str:
    """
    Read file with caching. Returns cached version if checksum matches.
    
    Args:
        path: File path to read
        max_age_seconds: Cache TTL (default 5 minutes)
    
    Returns:
        File contents (cached or fresh)
    """
    cache_key = path.replace('/', '_').replace('\\', '_')
    cache_meta = CACHE_DIR / f"{cache_key}.json"
    cache_data = CACHE_DIR / f"{cache_key}.txt"
    
    current_checksum = file_checksum(path)
    current_mtime = os.path.getmtime(path)
    
    # Check cache validity
    if cache_meta.exists() and cache_data.exists():
        with open(cache_meta) as f:
            meta = json.load(f)
        
        # Validate checksum and age
        if (meta['checksum'] == current_checksum and 
            meta['mtime'] == current_mtime and
            time.time() - meta['cached_at'] < max_age_seconds):
            with open(cache_data) as f:
                return f.read()
    
    # Cache miss - read and cache
    with open(path) as f:
        content = f.read()
    
    with open(cache_data, 'w') as f:
        f.write(content)
    
    with open(cache_meta, 'w') as f:
        json.dump({
            'checksum': current_checksum,
            'mtime': current_mtime,
            'cached_at': time.time()
        }, f)
    
    return content
```

## Query Result Cache

Cache expensive search operations.

```python
import time
from functools import wraps

def memoize_with_ttl(ttl_seconds: int = 300):
    """Decorator to cache function results with TTL."""
    cache = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            now = time.time()
            
            if key in cache:
                result, expiry = cache[key]
                if now < expiry:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, now + ttl_seconds)
            return result
        
        wrapper.cache = cache
        wrapper.clear_cache = lambda: cache.clear()
        return wrapper
    return decorator

@memoize_with_ttl(ttl_seconds=600)
def semantic_search(query: str, max_results: int = 5):
    """Cached semantic search - results valid for 10 minutes."""
    # Expensive operation here
    return memory_search(query=query, maxResults=max_results)
```

## Session Cache

Maintain cache for duration of session only.

```python
class SessionCache:
    """In-memory cache for session-scoped data."""
    
    def __init__(self):
        self._cache = {}
        self._access_count = {}
    
    def get(self, key: str, default=None):
        """Get value from cache, track access."""
        self._access_count[key] = self._access_count.get(key, 0) + 1
        return self._cache.get(key, default)
    
    def set(self, key: str, value: any):
        """Store value in cache."""
        self._cache[key] = value
    
    def get_stats(self) -> dict:
        """Return cache hit statistics."""
        return {
            'keys_cached': len(self._cache),
            'access_patterns': self._access_count,
            'most_accessed': sorted(
                self._access_count.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
        }

# Global session cache
session_cache = SessionCache()

# Usage
file_list = session_cache.get('repo_files')
if file_list is None:
    file_list = list(Path('.').rglob('*.py'))
    session_cache.set('repo_files', file_list)
```

## Cache Invalidation Strategies

### Time-Based (TTL)
- Simple, predictable
- Good for: File contents, search indices
- Trade-off: May serve stale data

### Event-Based
- Invalidate on file change, git commit, or explicit trigger
- Good for: Code references, documentation
- Trade-off: Requires event propagation

### Manual
- Explicit cache.clear() calls
- Good for: Debugging, critical operations
- Trade-off: Easy to forget

## Token Savings Calculation

```python
def estimate_savings(cache_hits: int, avg_content_tokens: int = 500) -> dict:
    """Estimate token savings from caching."""
    # Approximate tokens saved
    tokens_saved = cache_hits * avg_content_tokens
    
    # Cost estimate (Kimi K2 ~$3/million tokens)
    cost_saved = (tokens_saved / 1_000_000) * 3
    
    return {
        'cache_hits': cache_hits,
        'tokens_saved': tokens_saved,
        'estimated_cost_saved_usd': round(cost_saved, 4),
        'efficiency_gain': f"{cache_hits * 100}%" if cache_hits > 0 else "0%"
    }
```
