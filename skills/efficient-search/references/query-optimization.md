# Query Optimization Patterns

## Keyword Extraction

Extract optimized keywords from natural language queries for better retrieval.

```python
import re
from typing import List, Set

def extract_keywords(query: str, max_keywords: int = 5) -> List[str]:
    """
    Extract high-value keywords from query.
    
    Strategy:
    1. Remove stop words
    2. Extract nouns and noun phrases
    3. Prioritize capitalized terms (proper nouns)
    4. Include technical terms
    """
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 
        'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall',
        'can', 'need', 'dare', 'ought', 'used',
        'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their',
        'and', 'but', 'or', 'yet', 'so', 'for', 'nor',
        'in', 'on', 'at', 'to', 'from', 'by', 'with',
        'about', 'as', 'into', 'through', 'during',
        'of', 'this', 'that', 'these', 'those'
    }
    
    # Normalize
    query_lower = query.lower()
    
    # Find technical terms (camelCase, snake_case, PascalCase)
    technical_pattern = r'\b[a-z]+(?:[A-Z][a-z]+)+\b|\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b|\b[a-z]+_[a-z_]+\b'
    technical_terms = re.findall(technical_pattern, query)
    
    # Find capitalized terms (proper nouns)
    proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', query)
    
    # Extract all words
    words = re.findall(r'\b[a-zA-Z]+\b', query_lower)
    content_words = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Score and rank
    scored = {}
    for word in set(content_words):
        score = 0
        # Prioritize technical terms
        if any(t.lower() == word for t in technical_terms):
            score += 10
        # Prioritize proper nouns
        if any(p.lower() == word for p in proper_nouns):
            score += 5
        # Prioritize longer words (more specific)
        score += min(len(word) / 3, 3)
        scored[word] = score
    
    # Return top keywords
    sorted_keywords = sorted(scored.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_keywords[:max_keywords]]

# Example usage
query = "How do I optimize the token caching strategy for my Claude agent?"
keywords = extract_keywords(query)
# Result: ['token', 'caching', 'strategy', 'claude', 'agent', 'optimize']
```

## Query Batching

Batch multiple related queries to reduce API calls.

```python
from typing import List, Dict, Callable
from dataclasses import dataclass
import time

@dataclass
class Query:
    id: str
    text: str
    priority: int = 1  # 1=high, 2=normal, 3=low

class BatchedQueryExecutor:
    """Execute multiple queries efficiently."""
    
    def __init__(self, batch_size: int = 5, delay_ms: int = 100):
        self.batch_size = batch_size
        self.delay_ms = delay_ms
        self.pending: List[Query] = []
    
    def add(self, query: Query):
        """Add query to batch."""
        self.pending.append(query)
    
    def execute(self, search_fn: Callable[[str], List[dict]]) -> Dict[str, List[dict]]:
        """
        Execute all pending queries.
        
        Returns:
            Dict mapping query_id to results
        """
        # Sort by priority
        sorted_queries = sorted(self.pending, key=lambda q: q.priority)
        
        results = {}
        batch = []
        
        for query in sorted_queries:
            batch.append(query)
            
            if len(batch) >= self.batch_size:
                # Execute batch
                batch_results = self._execute_batch(batch, search_fn)
                results.update(batch_results)
                batch = []
                time.sleep(self.delay_ms / 1000)
        
        # Execute remaining
        if batch:
            batch_results = self._execute_batch(batch, search_fn)
            results.update(batch_results)
        
        self.pending = []
        return results
    
    def _execute_batch(self, queries: List[Query], search_fn) -> Dict[str, List[dict]]:
        """Execute a single batch."""
        results = {}
        for query in queries:
            try:
                results[query.id] = search_fn(query.text)
            except Exception as e:
                results[query.id] = [{'error': str(e)}]
        return results

# Usage example
executor = BatchedQueryExecutor(batch_size=3)
executor.add(Query(id="q1", text="trading strategy", priority=1))
executor.add(Query(id="q2", text="token optimization", priority=1))
executor.add(Query(id="q3", text="memory cache", priority=2))

all_results = executor.execute(lambda q: memory_search(query=q, maxResults=3))
```

## Relevance Scoring

Score and rank search results for better quality.

```python
from typing import List, Dict
import re

def score_result(result: Dict, keywords: List[str], query: str) -> float:
    """
    Score a search result for relevance.
    
    Scoring factors:
    - Keyword matches in content (0.3 per match)
    - Keyword matches in title/path (0.5 per match)
    - Exact phrase match (2.0)
    - Recency bonus (0.1 for recent files)
    """
    score = 0.0
    content = result.get('content', '').lower()
    title = result.get('title', result.get('path', '')).lower()
    
    # Keyword matches in content
    for kw in keywords:
        count = content.count(kw.lower())
        score += min(count * 0.3, 1.5)  # Cap at 1.5 per keyword
    
    # Keyword matches in title/path (worth more)
    for kw in keywords:
        if kw.lower() in title:
            score += 0.5
    
    # Exact phrase match
    if query.lower() in content:
        score += 2.0
    
    # Recency bonus (if timestamp available)
    if 'timestamp' in result:
        age_days = (time.time() - result['timestamp']) / 86400
        if age_days < 7:
            score += 0.1
    
    return score

def rank_results(results: List[Dict], keywords: List[str], query: str) -> List[Dict]:
    """Sort results by relevance score."""
    scored = [(r, score_result(r, keywords, query)) for r in results]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [r for r, _ in scored]
```

## Fallback Strategies

When primary search fails, try alternatives.

```python
class SearchWithFallback:
    """Multi-tier search with fallback strategies."""
    
    def __init__(self):
        self.strategies = [
            self._exact_match,
            self._semantic_search,
            self._keyword_search,
            self._grep_search,
        ]
    
    def search(self, query: str, min_results: int = 3) -> List[Dict]:
        """
        Try search strategies in order until min_results found.
        """
        all_results = []
        
        for strategy in self.strategies:
            try:
                results = strategy(query)
                if results:
                    all_results.extend(results)
                    if len(all_results) >= min_results:
                        break
            except Exception as e:
                continue
        
        # Deduplicate by path/content hash
        seen = set()
        unique = []
        for r in all_results:
            key = r.get('path', '') + r.get('content', '')[:50]
            if key not in seen:
                seen.add(key)
                unique.append(r)
        
        return unique[:10]  # Return top 10
    
    def _exact_match(self, query: str) -> List[Dict]:
        """Try exact phrase match first."""
        return memory_search(query=f'"{query}"', maxResults=5)
    
    def _semantic_search(self, query: str) -> List[Dict]:
        """Semantic/similarity search."""
        return memory_search(query=query, maxResults=5)
    
    def _keyword_search(self, query: str) -> List[Dict]:
        """Extract keywords and search."""
        keywords = extract_keywords(query)
        combined = ' '.join(keywords)
        return memory_search(query=combined, maxResults=5)
    
    def _grep_search(self, query: str) -> List[Dict]:
        """Fallback to grep for exact term."""
        import subprocess
        try:
            result = subprocess.run(
                ['grep', '-r', '-l', query, '.'],
                capture_output=True, text=True, timeout=10
            )
            files = result.stdout.strip().split('\n')[:5]
            return [{'path': f, 'content': f'Matched: {query}'} for f in files if f]
        except:
            return []
```

## Token Budget-Aware Search

Stop searching when token budget is exceeded.

```python
class TokenBudgetSearch:
    """Search with strict token budget enforcement."""
    
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
        self.used_tokens = 0
    
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimate (1 token ≈ 4 chars)."""
        return len(text) // 4
    
    def can_read(self, content: str) -> bool:
        """Check if reading content fits in budget."""
        estimated = self.estimate_tokens(content)
        return self.used_tokens + estimated <= self.max_tokens
    
    def read_with_budget(self, path: str) -> str:
        """
        Read file respecting token budget.
        Returns truncated content if needed.
        """
        with open(path) as f:
            content = f.read()
        
        estimated = self.estimate_tokens(content)
        
        if estimated <= self.max_tokens - self.used_tokens:
            self.used_tokens += estimated
            return content
        else:
            # Truncate to fit
            available = (self.max_tokens - self.used_tokens) * 4
            truncated = content[:available]
            self.used_tokens = self.max_tokens
            return truncated + "\n... [truncated for token budget]"
    
    def get_remaining(self) -> int:
        """Get remaining token budget."""
        return self.max_tokens - self.used_tokens
```
