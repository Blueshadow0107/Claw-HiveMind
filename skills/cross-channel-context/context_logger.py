"""
Cross-Channel Context Logger

Automatically logs channel switches to AGENTS_SHARED.md for continuity.
"""

import os
import re
from datetime import datetime, timezone
from typing import List, Optional, Dict
from pathlib import Path

# Default location for shared memory (CLAW-D repo - shared between agents)
DEFAULT_SHARED_FILE = Path("/home/cyanidepopcorn/.openclaw/workspace/CLAW-D/AGENTS_SHARED.md")


def log_switch(
    from_channel: str,
    to_channel: str,
    context: str,
    open_loops: Optional[List[str]] = None,
    agent: str = "Vayu",
    file_path: Optional[Path] = None
) -> None:
    """
    Log a channel switch with context to AGENTS_SHARED.md.
    
    Args:
        from_channel: Channel we're leaving (e.g., "#workspace")
        to_channel: Channel we're entering (e.g., "#agents-chat")
        context: Brief summary of what we were doing (1-2 sentences)
        open_loops: List of unresolved items or next steps
        agent: Which agent is logging (Vayu or SodaPoppy)
        file_path: Override default AGENTS_SHARED.md location
    """
    file_path = file_path or DEFAULT_SHARED_FILE
    
    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Build log entry
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M GMT")
    
    entry = f"""\n### {timestamp}
- **From:** {from_channel} → **To:** {to_channel}
- **Context:** {context}
"""
    
    if open_loops:
        entry += f"- **Open threads:** {', '.join(open_loops)}\n"
    
    entry += f"- **Agent:** {agent}\n"
    
    # Read existing content or create header
    if file_path.exists():
        content = file_path.read_text()
        # Check if header exists
        if "# Channel Context Log" not in content:
            content = "# Channel Context Log\n\n" + content
    else:
        content = "# Channel Context Log\n"
    
    # Append new entry
    content += entry
    
    # Write back
    file_path.write_text(content)


def get_recent_switches(
    minutes: int = 30,
    file_path: Optional[Path] = None
) -> List[Dict]:
    """
    Get recent channel switches from AGENTS_SHARED.md.
    
    Args:
        minutes: How far back to look
        file_path: Override default location
        
    Returns:
        List of switch entries as dictionaries
    """
    file_path = file_path or DEFAULT_SHARED_FILE
    
    if not file_path.exists():
        return []
    
    content = file_path.read_text()
    switches = []
    
    # Parse entries using regex (captures agent too)
    pattern = r'### (\d{4}-\d{2}-\d{2} \d{2}:\d{2} GMT)\n.*?\*\*From:\*\* (.+?) → \*\*To:\*\* (.+?)\n.*?\*\*Context:\*\* (.+?)(?:\n.*?\*\*Agent:\*\* (\w+))?(?:\n|$)'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        timestamp_str = match.group(1)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M GMT")
        timestamp = timestamp.replace(tzinfo=timezone.utc)
        
        # Check if within time window
        cutoff = datetime.now(timezone.utc) - __import__('datetime').timedelta(minutes=minutes)
        if timestamp >= cutoff:
            switches.append({
                'timestamp': timestamp_str,
                'from_channel': match.group(2).strip(),
                'to_channel': match.group(3).strip(),
                'context': match.group(4).strip(),
                'agent': match.group(5).strip() if match.group(5) else 'unknown'
            })
    
    return switches


def get_last_context(
    channel: Optional[str] = None,
    file_path: Optional[Path] = None
) -> Optional[str]:
    """
    Get the most recent context summary.
    
    Args:
        channel: Filter by specific channel (e.g., "#workspace")
        file_path: Override default location
        
    Returns:
        Context string or None if not found
    """
    file_path = file_path or DEFAULT_SHARED_FILE
    
    if not file_path.exists():
        return None
    
    content = file_path.read_text()
    
    # Find last entry, optionally filtered by channel
    pattern = r'### \d{4}-\d{2}-\d{2} \d{2}:\d{2} GMT\n.*?\*\*Context:\*\* (.+?)(?:\n|$)'
    
    if channel:
        # Look for entries where we switched TO this channel
        pattern = rf'### \d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}} GMT\n.*?→ \*\*To:\*\* {re.escape(channel)}.*?\*\*Context:\*\* (.+?)(?:\n|$)'
    
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if matches:
        return matches[-1].group(1).strip()
    
    return None


if __name__ == "__main__":
    # Test logging
    log_switch(
        from_channel="#workspace",
        to_channel="#agent-lab",
        context="Building cross-channel context skill",
        open_loops=["Waiting for SodaPoppy's retrieval function"],
        agent="Vayu"
    )
    print("Logged test entry!")
    
    # Test retrieval
    switches = get_recent_switches(minutes=5)
    print(f"Found {len(switches)} recent switches")
    for s in switches:
        print(f"  {s['timestamp']}: {s['from_channel']} → {s['to_channel']}")
