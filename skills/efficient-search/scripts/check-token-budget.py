#!/usr/bin/env python3
"""
Token Budget Tracker for Agent Sessions
Tracks token usage and enforces budget limits.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

SESSION_LOG = Path("memory/token-sessions.json")
TOKEN_ESTIMATE_RATIO = 4  # ~4 chars per token

class TokenBudget:
    def __init__(self, session_id: str = None, max_tokens: int = 8000):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.max_tokens = max_tokens
        self.used_tokens = 0
        self.operations = []
        
    def estimate(self, text: str) -> int:
        """Estimate tokens for given text."""
        return len(text) // TOKEN_ESTIMATE_RATIO
    
    def check_file(self, filepath: str) -> dict:
        """Check if file can be read within budget."""
        path = Path(filepath)
        if not path.exists():
            return {'can_read': False, 'reason': 'File not found'}
        
        try:
            size = path.stat().st_size
            estimated_tokens = size // TOKEN_ESTIMATE_RATIO
            
            can_read = self.used_tokens + estimated_tokens <= self.max_tokens
            
            return {
                'can_read': can_read,
                'file_size_bytes': size,
                'estimated_tokens': estimated_tokens,
                'remaining_budget': self.max_tokens - self.used_tokens,
                'will_exceed_by': max(0, self.used_tokens + estimated_tokens - self.max_tokens)
            }
        except Exception as e:
            return {'can_read': False, 'reason': str(e)}
    
    def record_read(self, filepath: str, content: str = None):
        """Record a file read operation."""
        tokens = self.estimate(content) if content else Path(filepath).stat().st_size // TOKEN_ESTIMATE_RATIO
        self.used_tokens += tokens
        self.operations.append({
            'type': 'read',
            'file': filepath,
            'tokens': tokens,
            'timestamp': datetime.now().isoformat()
        })
        
    def get_status(self) -> dict:
        """Get current budget status."""
        return {
            'session_id': self.session_id,
            'max_tokens': self.max_tokens,
            'used_tokens': self.used_tokens,
            'remaining_tokens': self.max_tokens - self.used_tokens,
            'usage_percent': round(self.used_tokens / self.max_tokens * 100, 1),
            'should_checkpoint': self.used_tokens > self.max_tokens * 0.8,
            'operations_count': len(self.operations)
        }
    
    def save_session(self):
        """Save session stats to log."""
        SESSION_LOG.parent.mkdir(parents=True, exist_ok=True)
        
        data = []
        if SESSION_LOG.exists():
            with open(SESSION_LOG) as f:
                data = json.load(f)
        
        data.append({
            'session_id': self.session_id,
            'max_tokens': self.max_tokens,
            'used_tokens': self.used_tokens,
            'ended_at': datetime.now().isoformat(),
            'operation_count': len(self.operations)
        })
        
        with open(SESSION_LOG, 'w') as f:
            json.dump(data[-50:], f, indent=2)  # Keep last 50 sessions


def main():
    if len(sys.argv) < 2:
        print("Usage: check-token-budget.py <command> [args]")
        print("")
        print("Commands:")
        print("  check <filepath>     - Check if file fits in budget")
        print("  status               - Show current budget status")
        print("  estimate <text>      - Estimate tokens for text")
        print("")
        sys.exit(1)
    
    command = sys.argv[1]
    budget = TokenBudget()
    
    if command == "check" and len(sys.argv) > 2:
        result = budget.check_file(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == "status":
        print(json.dumps(budget.get_status(), indent=2))
    
    elif command == "estimate" and len(sys.argv) > 2:
        text = sys.argv[2]
        tokens = budget.estimate(text)
        print(f"Estimated tokens: {tokens}")
        print(f"Character count: {len(text)}")
    
    else:
        print("Unknown command or missing arguments")
        sys.exit(1)


if __name__ == "__main__":
    main()
