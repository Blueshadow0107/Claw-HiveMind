"""
Discord Hook for Cross-Channel Context

Automatically detects channel changes and logs them.
"""

from typing import Optional
from .context_logger import log_switch

# Track last channel per session
_last_channel: Optional[str] = None
_current_context: Optional[str] = None
_current_open_loops: Optional[list] = None


def set_context(context: str, open_loops: Optional[list] = None) -> None:
    """
    Set the current context to be logged on next channel switch.
    
    Args:
        context: What we're currently doing
        open_loops: Unresolved items
    """
    global _current_context, _current_open_loops
    _current_context = context
    _current_open_loops = open_loops or []


def on_message_received(
    channel_name: str,
    agent: str = "Vayu"
) -> Optional[str]:
    """
    Call this when receiving a message in a channel.
    Detects channel switches and auto-logs them.
    
    Args:
        channel_name: Current channel (e.g., "#workspace")
        agent: Which agent is processing
        
    Returns:
        Previous channel name if switch detected, None otherwise
    """
    global _last_channel, _current_context, _current_open_loops
    
    # First message in session
    if _last_channel is None:
        _last_channel = channel_name
        return None
    
    # Channel switch detected
    if channel_name != _last_channel:
        prev_channel = _last_channel
        
        # Log the switch
        log_switch(
            from_channel=prev_channel,
            to_channel=channel_name,
            context=_current_context or "Context not set",
            open_loops=_current_open_loops,
            agent=agent
        )
        
        # Update tracking
        _last_channel = channel_name
        
        return prev_channel
    
    return None


def get_context_summary(minutes: int = 30) -> str:
    """
    Get a summary of recent context across channels.
    Useful for starting a reply with continuity.
    
    Args:
        minutes: How far back to look
        
    Returns:
        Formatted context summary
    """
    from .context_logger import get_recent_switches
    
    switches = get_recent_switches(minutes=minutes)
    
    if not switches:
        return ""
    
    # Build summary
    summary_parts = []
    for s in switches[-3:]:  # Last 3 switches max
        summary_parts.append(
            f"[{s['timestamp']}] {s['from_channel']} → {s['to_channel']}: {s['context']}"
        )
    
    return "Recent context:\n" + "\n".join(summary_parts)
