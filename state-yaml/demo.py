#!/usr/bin/env python3
"""
Demo: STATE.yaml PM Delegation Pattern
Shows how main agent coordinates with PM subagents via STATE.yaml
"""

import yaml
from datetime import datetime
from pathlib import Path

# Simulated PROJECT_REGISTRY
REGISTRY = {}


def demo_main_agent_receives_task():
    """Step 1: Main agent receives a complex task"""
    print("=" * 60)
    print("🎯 DEMO: STATE.yaml PM Delegation Pattern")
    print("=" * 60)
    print()
    print("📥 User: 'Refactor the auth module and update the docs'")
    print()
    print("🤖 Main Agent thinks:")
    print("   - This is a multi-step task")
    print("   - Should delegate to a PM")
    print("   - Check if pm-auth-refactor already exists")
    print()


def demo_check_registry():
    """Step 2: Check PROJECT_REGISTRY"""
    print("📋 Checking PROJECT_REGISTRY.md...")
    
    if "auth-refactor" not in REGISTRY:
        print("   ❌ No active PM for auth-refactor")
        print("   → Decision: Spawn new PM")
    else:
        print(f"   ✅ Found PM: {REGISTRY['auth-refactor']['pm_label']}")
        print("   → Decision: Send task to existing PM")
    print()


def demo_spawn_pm():
    """Step 3: Create project and spawn PM"""
    print("🚀 Spawning PM subagent...")
    print()
    print("   sessions_spawn(")
    print('       label="pm-auth-refactor",')
    print('       task="""')
    print("           Refactor auth module and update docs.")
    print("           Track all work in STATE.yaml.")
    print("           Break down into tasks:")
    print("           1. Audit current auth implementation")
    print("           2. Refactor to new pattern")
    print("           3. Update documentation")
    print("           4. Test changes")
    print('       """')
    print("   )")
    print()
    
    # Create initial STATE.yaml
    state = {
        "project": "auth-refactor",
        "created": "2026-02-20T10:00:00Z",
        "updated": "2026-02-20T10:00:00Z",
        "tasks": [
            {
                "id": "audit",
                "status": "pending",
                "owner": "pm-auth-refactor",
                "description": "Audit current auth implementation",
                "notes": ""
            },
            {
                "id": "refactor",
                "status": "pending",
                "owner": "pm-auth-refactor",
                "description": "Refactor to new pattern",
                "notes": "",
                "blocked_by": ["audit"]
            },
            {
                "id": "docs",
                "status": "pending",
                "owner": "pm-auth-refactor",
                "description": "Update documentation",
                "notes": "",
                "blocked_by": ["refactor"]
            },
            {
                "id": "test",
                "status": "pending",
                "owner": "pm-auth-refactor",
                "description": "Test changes",
                "notes": "",
                "blocked_by": ["refactor"]
            }
        ],
        "next_actions": [
            "pm-auth-refactor: Start audit task"
        ]
    }
    
    REGISTRY["auth-refactor"] = {
        "pm_label": "pm-auth-refactor",
        "state": state,
        "status": "active"
    }
    
    print("📁 Created STATE.yaml:")
    print("-" * 40)
    print(yaml.dump(state, default_flow_style=False))
    print("-" * 40)
    print()


def demo_pm_updates_state():
    """Step 4: PM updates state as work progresses"""
    print("⏱️  10 minutes later...")
    print()
    print("🤖 PM subagent updates STATE.yaml:")
    print()
    
    state = REGISTRY["auth-refactor"]["state"]
    
    # PM starts audit
    state["tasks"][0]["status"] = "in_progress"
    state["tasks"][0]["started"] = "2026-02-20T10:05:00Z"
    state["tasks"][0]["notes"] = "Found 3 legacy auth patterns"
    state["updated"] = "2026-02-20T10:05:00Z"
    
    print("   → audit: pending → in_progress")
    print()
    
    # PM completes audit
    state["tasks"][0]["status"] = "done"
    state["tasks"][0]["completed"] = "2026-02-20T10:12:00Z"
    
    # Unblock refactor task
    state["tasks"][1]["status"] = "pending"  # Ready to start
    del state["tasks"][1]["blocked_by"]  # Dependency resolved
    
    state["next_actions"] = [
        "pm-auth-refactor: Start refactor task (audit complete)"
    ]
    
    print("   → audit: in_progress → done")
    print("   → refactor: unblocked (audit done)")
    print("   → Git commit: [STATE] complete: audit")
    print()


def demo_main_agent_checks():
    """Step 5: Main agent checks status on demand"""
    print("📊 User: 'How's the auth refactor going?'")
    print()
    print("🤖 Main Agent checks STATE.yaml:")
    print()
    
    state = REGISTRY["auth-refactor"]["state"]
    
    done = sum(1 for t in state["tasks"] if t["status"] == "done")
    pending = sum(1 for t in state["tasks"] if t["status"] == "pending")
    in_progress = sum(1 for t in state["tasks"] if t["status"] == "in_progress")
    
    print(f"   Project: {state['project']}")
    print(f"   Updated: {state['updated']}")
    print(f"   Tasks: {done} done, {in_progress} in progress, {pending} pending")
    print()
    print("   Recent activity:")
    print(f"     ✅ audit: complete (3 legacy patterns found)")
    print(f"     ⏳ refactor: ready to start")
    print()


def demo_final_completion():
    """Step 6: All tasks complete"""
    print("⏱️  30 minutes later...")
    print()
    print("🤖 PM subagent reports completion")
    print()
    
    state = REGISTRY["auth-refactor"]["state"]
    
    # Complete all tasks
    for task in state["tasks"]:
        task["status"] = "done"
        task["completed"] = "2026-02-20T10:45:00Z"
    
    state["next_actions"] = ["Project complete — notify main agent"]
    
    print("📤 PM → Main Agent:")
    print("   'Auth refactor complete. 4 tasks done, 3 files changed,'")
    print("   'documentation updated in /docs/auth.md'")
    print()
    
    print("🤖 Main Agent → User:")
    print("   ✅ Auth refactor complete!")
    print("   📁 Files changed: src/auth.js, src/auth.test.js, docs/auth.md")
    print("   📝 See full breakdown in STATE.yaml")
    print()


def demo_summary():
    """Summary of the pattern"""
    print("=" * 60)
    print("📋 PATTERN SUMMARY")
    print("=" * 60)
    print()
    print("Key Benefits:")
    print("  ✓ Main agent stays thin (only 2 tool calls)")
    print("  ✓ PM works autonomously without constant check-ins")
    print("  ✓ State is persistent and version-controlled")
    print("  ✓ Easy to resume if PM fails (just read STATE.yaml)")
    print("  ✓ Multiple PMs can coordinate via shared state")
    print()
    print("Git History:")
    print("  [STATE] init: project setup")
    print("  [STATE] start: audit")
    print("  [STATE] complete: audit")
    print("  [STATE] start: refactor")
    print("  [STATE] complete: refactor")
    print("  ...")
    print()


if __name__ == "__main__":
    demo_main_agent_receives_task()
    demo_check_registry()
    demo_spawn_pm()
    demo_pm_updates_state()
    demo_main_agent_checks()
    demo_final_completion()
    demo_summary()
