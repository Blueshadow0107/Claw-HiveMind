# Cross-Channel Context Skill

Maintain shared memory across Discord channels for multi-agent collaboration.

## Problem

Agents operate in isolated sessions per channel. When humans move conversations between channels (#workspace → #agents-chat → #agent-lab), context is lost.

## Solution

Shared `AGENTS_SHARED.md` file with automatic channel switch logging and context retrieval.

## Files

| File | Purpose | Author |
|------|---------|--------|
| `context_logger.py` | Core logging & retrieval | SodaPoppy |
| `discord_hook.py` | Auto-detection hooks | SodaPoppy |
| `cli.py` | Command-line interface | Vayu |
| `ccc` | CLI wrapper script | Vayu |
| `config.json` | Channel aliases | Vayu |
| `SKILL.md` | Documentation | Both |

## Installation

```bash
# Symlink to OpenClaw skills
ln -s ~/.openclaw/workspace/skills/cross-channel-context ~/.openclaw/skills/cross-channel-context
```

## Usage

### CLI (Vayu's interface)

```bash
# Log a channel switch
ccc log -f workspace -t agent-lab -c "Building skill" -a "Vayu" -o "Wait for review"

# Get recent context
ccc context -c agent-lab -m 60

# Get last context for a channel
ccc last -c workspace
```

### Python API (SodaPoppy's interface)

```python
from skills.cross_channel_context import log_switch, get_recent_switches

# Log a switch
log_switch(
    from_channel="#workspace",
    to_channel="#agent-lab",
    context="Building cross-channel skill",
    open_loops=["Waiting for review"],
    agent="Vayu"
)

# Retrieve context
switches = get_recent_switches(minutes=30)
```

### Auto-Log with Discord Hook

```python
from skills.cross_channel_context.discord_hook import set_context, on_message_received

# Set context before channel switch
set_context(
    context="Building cross-channel skill",
    open_loops=["Review from SodaPoppy"]
)

# Call on every message to auto-detect switches
prev_channel = on_message_received(channel_name="#agent-lab", agent="Vayu")
if prev_channel:
    print(f"Switched from {prev_channel}")
```

## AGENTS_SHARED.md Format

```markdown
# Channel Context Log

### 2026-02-03 01:36 GMT
- **From:** <#1467358172288123097> → **To:** <#1467410930328535175>
- **Context:** Merged Vayu CLI with SodaPoppy core
- **Open threads:** Wait for SodaPoppy review
- **Agent:** Vayu
```

## Channel Aliases

Configured in `config.json`:
- `workspace` → 1467358172288123097
- `agent-lab` → 1467410930328535175
- `agents-chat` → 1467985219280965827
- `build-nightly` → 1474164201093074984

## Authors

- **SodaPoppy**: Core logging module, Discord hooks
- **Vayu**: CLI interface, config, integration

## Nightly Build

🌙 Completed: 2026-02-03  
Co-authored during agent collaboration session.
