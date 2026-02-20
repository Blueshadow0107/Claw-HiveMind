#!/usr/bin/env python3
"""
Semantic Search with Caching
Wraps memory_search with intelligent caching and result ranking.
"""

import json
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Optional

CACHE_DIR = Path(".cache/searches")
CACHE_TTL_SECONDS = 600  # 10 minutes

def get_query_hash(query: str, max_results: int) -> str:
    """Generate cache key for query."""
    key = f"{query}:{max_results}"
    return hashlib.md5(key.encode()).hexdigest()

def cached_search(query: str, max_results: int = 5, use_cache: bool = True) -> Dict:
    """
    Search with caching and result enhancement.
    
    Args:
        query: Search query
        max_results: Maximum results to return
        use_cache: Whether to use cached results
    
    Returns:
        Dict with results and metadata
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    cache_key = get_query_hash(query, max_results)
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    # Check cache
    if use_cache and cache_file.exists():
        with open(cache_file) as f:
            cached = json.load(f)
        
        age = time.time() - cached.get('cached_at', 0)
        if age < CACHE_TTL_SECONDS:
            return {
                'results': cached['results'],
                'source': 'cache',
                'cache_age_seconds': int(age),
                'query': query
            }
    
    # Perform search (placeholder - integrate with actual memory_search)
    # In real implementation, this would call:
    # results = memory_search(query=query, maxResults=max_results)
    
    # For now, return mock structure
    results = []
    
    # Cache results
    if use_cache:
        with open(cache_file, 'w') as f:
            json.dump({
                'results': results,
                'cached_at': time.time(),
                'query': query
            }, f)
    
    return {
        'results': results,
        'source': 'fresh',
        'query': query
    }

def extract_keywords(query: str) -> List[str]:
    """Extract high-value keywords from query."""
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 
        'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall',
        'and', 'but', 'or', 'yet', 'so', 'for', 'nor',
        'in', 'on', 'at', 'to', 'from', 'by', 'with',
        'of', 'this', 'that', 'these', 'those', 'i', 'you'
    }
    
    words = query.lower().split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    return keywords[:5]

def rank_results(results: List[Dict], keywords: List[str]) -> List[Dict]:
    """Rank results by relevance to keywords."""
    scored = []
    
    for result in results:
        score = 0
        content = result.get('content', '').lower()
        
        for kw in keywords:
            if kw in content:
                score += content.count(kw) * 0.5
        
        result['_relevance_score'] = round(score, 2)
        scored.append((result, score))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    return [r for r, _ in scored]

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: cached-search.py <query> [max_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    keywords = extract_keywords(query)
    print(f"Keywords: {', '.join(keywords)}")
    print("")
    
    result = cached_search(query, max_results)
    print(f"Source: {result['source']}")
    if 'cache_age_seconds' in result:
        print(f"Cache age: {result['cache_age_seconds']}s")
    print("")
    print(json.dumps(result['results'], indent=2))


if __name__ == "__main__":
    main()
