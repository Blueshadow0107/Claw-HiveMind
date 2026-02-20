---
name: status-indicators
description: Visual status indicator emoji system for AI agent communication. Use when the agent needs to provide visual feedback about what they're doing - reading messages, thinking, processing tasks, searching, or completing work. Helps users understand agent state at a glance through consistent emoji indicators.
---

# Status Indicators

Visual emoji indicators to communicate AI agent state and actions. Provides immediate visual feedback so users know what's happening without reading full text.

## Core Indicators

### 👀 - Acknowledgment
**When to use:** At the start of any response to show the message was received and read.

**Examples:**
- "👀 Looking at your assignment now"
- "👀 I see the issue"

### 🧠 - Thinking/Processing
**When to use:** When analyzing, reasoning, or working through a problem. Shows cognitive effort is happening.

**Examples:**
- "🧠 Let me think about the best approach..."
- "🧠 Analyzing the data structure"

### 🖥️ - Local System Operations
**When to use:** When reading files, executing commands, or interacting with the local system.

**Examples:**
- "🖥️ Reading your files..."
- "🖥️ Checking the directory structure"
- "🖥️ Running the conversion script"

### 🌐 - Web Operations
**When to use:** When searching the web, fetching URLs, or doing online research.

**Examples:**
- "🌐 Searching for that..."
- "🌐 Looking up documentation"

### ⏳ - Long-running Tasks
**When to use:** When a task will take noticeable time (more than a few seconds). Shows work is in progress.

**Examples:**
- "⏳ Converting all 196 files..."
- "⏳ Installing dependencies"

### ✅ - Completion
**When to use:** When a task or step is successfully completed.

**Examples:**
- "✅ Files converted successfully"
- "✅ All done!"

### 🎉 - Success/Celebration
**When to use:** For significant achievements, completions, or positive outcomes.

**Examples:**
- "🎉 Assignment complete!"
- "🎉 The fix worked!"

### ⚠️ - Warning/Issue
**When to use:** When there's a problem, error, or something needs attention.

**Examples:**
- "⚠️ Couldn't find that file"
- "⚠️ There's an issue with the format"

### ❌ - Error/Failure
**When to use:** When something failed or couldn't be completed.

**Examples:**
- "❌ Command failed"
- "❌ File not found"

## Usage Patterns

### Single Response
Use one indicator at the start to set context:
```
🖥️ Reading your files...
```

### Progress Sequence
For multi-step tasks, show progression:
```
👀 Looking at your request...
🖥️ Reading the files...
⏳ Processing data...
✅ Complete!
```

### Contextual Choice
Pick the indicator that best matches the PRIMARY action:
- Reading files locally → 🖥️
- Searching online → 🌐
- Thinking through a problem → 🧠
- Running a long command → ⏳

## Best Practices

1. **Be consistent** - Same action, same indicator
2. **Don't overuse** - One indicator per message is usually enough
3. **Lead with it** - Put the indicator at the very start
4. **Match the tone** - 🎉 for wins, ⚠️ for problems
5. **Combine thoughtfully** - "🖥️ ⏳" for long file operations

## When NOT to Use

- Simple acknowledgments (just say "Got it")
- Every single message (saves it for meaningful status)
- In formal/professional contexts where emoji are inappropriate
