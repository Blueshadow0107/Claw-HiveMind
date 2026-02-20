#!/usr/bin/env python3
"""
CLI for Cross-Channel Context Skill
Wraps SodaPoppy's context_logger with command-line interface.
"""

import argparse
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from context_logger import log_switch, get_recent_switches, get_last_context

# Load channel aliases
CONFIG_PATH = Path(__file__).parent / "config.json"
CHANNEL_ALIASES = {}

if CONFIG_PATH.exists():
    with open(CONFIG_PATH) as f:
        config = json.load(f)
        CHANNEL_ALIASES = config.get("channel_aliases", {})


def resolve_channel(channel: str) -> str:
    """Resolve channel alias to ID or return as-is."""
    return CHANNEL_ALIASES.get(channel, channel)


def cmd_log(args):
    """Log a channel switch."""
    from_ch = resolve_channel(args.from_channel)
    to_ch = resolve_channel(args.to_channel)
    
    open_loops = args.open_loops.split(",") if args.open_loops else None
    
    log_switch(
        from_channel=f"<#{from_ch}>" if from_ch.isdigit() else from_ch,
        to_channel=f"<#{to_ch}>" if to_ch.isdigit() else to_ch,
        context=args.context,
        open_loops=open_loops,
        agent=args.agent
    )
    print("✅ Logged channel switch")


def cmd_context(args):
    """Get recent context."""
    channel = resolve_channel(args.channel) if args.channel else None
    
    switches = get_recent_switches(minutes=args.minutes)
    
    if not switches:
        print("No recent context found.")
        return
    
    # Filter by channel if specified
    if channel:
        channel_ref = f"<#{channel}>" if channel.isdigit() else channel
        switches = [
            s for s in switches 
            if channel_ref in s.get('to_channel', '') or channel_ref in s.get('from_channel', '')
        ]
    
    print(f"\n📋 Recent context (last {args.minutes} minutes):")
    print("-" * 50)
    
    for s in switches[-args.limit:]:
        print(f"\n🕐 {s['timestamp']}")
        print(f"   {s['from_channel']} → {s['to_channel']}")
        print(f"   Context: {s['context']}")


def cmd_last(args):
    """Get last context for a channel."""
    channel = resolve_channel(args.channel)
    channel_ref = f"<#{channel}>" if channel.isdigit() else channel
    
    context = get_last_context(channel=channel_ref)
    
    if context:
        print(f"Last context for {channel_ref}: {context}")
    else:
        print(f"No context found for {channel_ref}")


def main():
    parser = argparse.ArgumentParser(
        description="Cross-channel context manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ccc log -f workspace -t agent-lab -c "Building skill" --agent Vayu
  ccc context -c agent-lab -m 60
  ccc last -c workspace
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Log command
    log_parser = subparsers.add_parser("log", help="Log a channel switch")
    log_parser.add_argument("-f", "--from", dest="from_channel", required=True,
                           help="From channel (ID or alias)")
    log_parser.add_argument("-t", "--to", dest="to_channel", required=True,
                           help="To channel (ID or alias)")
    log_parser.add_argument("-c", "--context", required=True,
                           help="Context summary")
    log_parser.add_argument("-o", "--open-loops",
                           help="Comma-separated open items")
    log_parser.add_argument("-a", "--agent", default="Vayu",
                           help="Agent name")
    log_parser.set_defaults(func=cmd_log)
    
    # Context command
    ctx_parser = subparsers.add_parser("context", help="Get recent context")
    ctx_parser.add_argument("-c", "--channel",
                           help="Filter by channel (ID or alias)")
    ctx_parser.add_argument("-m", "--minutes", type=int, default=30,
                           help="How far back to look (default: 30)")
    ctx_parser.add_argument("-l", "--limit", type=int, default=5,
                           help="Max entries to show (default: 5)")
    ctx_parser.set_defaults(func=cmd_context)
    
    # Last command
    last_parser = subparsers.add_parser("last", help="Get last context for channel")
    last_parser.add_argument("-c", "--channel", required=True,
                            help="Channel (ID or alias)")
    last_parser.set_defaults(func=cmd_last)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
