#!/usr/bin/env python3
"""
STATE.yaml utilities for agent coordination.

Usage:
    python state_utils.py read <path>                    # Read full state
    python state_utils.py status <path>                  # Quick status summary
    python state_utils.py update <path> <task_id> <status> [--notes "..."]
    python state_utils.py add <path> <task_id> <title> <owner> [--priority high]
    python state_utils.py next <path>                    # Show next actions
    python state_utils.py unblock <path>                 # Auto-resolve blocked tasks
    python state_utils.py init <path> <project> <owner>  # Create new STATE.yaml
"""

import yaml
import sys
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_state(path: str) -> dict:
    """Read and parse STATE.yaml."""
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def write_state(path: str, state: dict, commit_msg: str = None):
    """Write STATE.yaml and optionally git commit."""
    state['updated'] = now_iso()
    with open(path, 'w') as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    if commit_msg:
        git_commit(path, commit_msg)


def git_commit(path: str, message: str):
    """Git add + commit the state file."""
    try:
        dir_path = os.path.dirname(os.path.abspath(path))
        subprocess.run(['git', 'add', path], cwd=dir_path, capture_output=True)
        subprocess.run(['git', 'commit', '-m', message], cwd=dir_path, capture_output=True)
    except Exception:
        pass  # Git not available or not a repo — that's fine


def get_task(state: dict, task_id: str):
    """Find a task by ID."""
    for task in state.get('tasks', []):
        if task['id'] == task_id:
            return task
    return None


def update_task(path: str, task_id: str, new_status: str, notes: str = None):
    """Update a task's status and optionally add notes."""
    state = read_state(path)
    task = get_task(state, task_id)
    if not task:
        print(f"Error: task '{task_id}' not found")
        sys.exit(1)
    
    old_status = task['status']
    task['status'] = new_status
    
    if new_status == 'in_progress' and old_status == 'pending':
        task['started'] = now_iso()
    elif new_status == 'done':
        task['completed'] = now_iso()
    
    if notes:
        task['notes'] = notes
    
    # Auto-unblock dependent tasks
    if new_status == 'done':
        unblock_dependents(state, task_id)
    
    action = {
        'in_progress': 'start',
        'done': 'complete',
        'failed': 'fail',
        'blocked': 'block',
    }.get(new_status, 'update')
    
    write_state(path, state, f"[STATE] {action}: {task_id}")
    print(f"✓ {task_id}: {old_status} → {new_status}")


def unblock_dependents(state: dict, completed_task_id: str):
    """Move blocked tasks to pending if their dependency just completed."""
    for task in state.get('tasks', []):
        if task.get('blocked_by') == completed_task_id and task['status'] == 'blocked':
            task['status'] = 'pending'
            task.pop('blocked_by', None)
            # Add to next_actions
            if 'next_actions' not in state:
                state['next_actions'] = []
            state['next_actions'].append({
                'owner': task.get('owner', 'unassigned'),
                'action': f"Unblocked: {task['title']}",
                'unblocked_by': completed_task_id,
            })
            print(f"  ↳ Unblocked: {task['id']}")


def add_task(path: str, task_id: str, title: str, owner: str, priority: str = 'medium'):
    """Add a new task to the project."""
    state = read_state(path)
    if get_task(state, task_id):
        print(f"Error: task '{task_id}' already exists")
        sys.exit(1)
    
    state.setdefault('tasks', []).append({
        'id': task_id,
        'title': title,
        'status': 'pending',
        'owner': owner,
        'priority': priority,
        'created': now_iso(),
    })
    
    write_state(path, state, f"[STATE] add-task: {task_id}")
    print(f"✓ Added: {task_id} ({title})")


def init_state(path: str, project: str, owner: str, description: str = ''):
    """Create a new STATE.yaml."""
    state = {
        'project': project,
        'version': 1,
        'created': now_iso(),
        'updated': now_iso(),
        'owner': owner,
        'status': 'active',
        'description': description,
        'tasks': [],
        'next_actions': [],
    }
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    write_state(path, state, f"[STATE] create: {project}")
    print(f"✓ Initialized: {project} at {path}")


def print_status(path: str):
    """Print a quick status summary."""
    state = read_state(path)
    print(f"📋 {state['project']} [{state['status']}]")
    print(f"   Owner: {state.get('owner', 'unassigned')}")
    print(f"   Updated: {state['updated']}")
    print()
    
    counts = {}
    for task in state.get('tasks', []):
        s = task['status']
        counts[s] = counts.get(s, 0) + 1
    
    total = sum(counts.values())
    done = counts.get('done', 0)
    print(f"   Progress: {done}/{total} tasks done")
    for status, count in sorted(counts.items()):
        icon = {'done': '✅', 'in_progress': '🔄', 'pending': '⏳', 'blocked': '🚫', 'failed': '❌'}.get(status, '•')
        print(f"   {icon} {status}: {count}")
    
    print()
    actions = state.get('next_actions', [])
    if actions:
        print("   Next actions:")
        for a in actions:
            print(f"   → {a.get('owner', '?')}: {a.get('action', '?')}")


def print_next(path: str):
    """Print next actions only."""
    state = read_state(path)
    actions = state.get('next_actions', [])
    if not actions:
        print("No pending actions.")
        return
    for a in actions:
        print(f"→ {a.get('owner', '?')}: {a.get('action', '?')}")


def auto_unblock(path: str):
    """Scan for tasks that can be unblocked."""
    state = read_state(path)
    done_ids = {t['id'] for t in state.get('tasks', []) if t['status'] == 'done'}
    changed = False
    
    for task in state.get('tasks', []):
        if task['status'] == 'blocked' and task.get('blocked_by') in done_ids:
            task['status'] = 'pending'
            blocker = task.pop('blocked_by')
            print(f"✓ Unblocked: {task['id']} (was blocked by {blocker})")
            changed = True
    
    if changed:
        write_state(path, state, "[STATE] unblock: auto-resolve")
    else:
        print("Nothing to unblock.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'read' and len(sys.argv) >= 3:
        state = read_state(sys.argv[2])
        print(yaml.dump(state, default_flow_style=False, sort_keys=False))
    
    elif cmd == 'status' and len(sys.argv) >= 3:
        print_status(sys.argv[2])
    
    elif cmd == 'update' and len(sys.argv) >= 5:
        notes = None
        if '--notes' in sys.argv:
            idx = sys.argv.index('--notes')
            notes = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        update_task(sys.argv[2], sys.argv[3], sys.argv[4], notes)
    
    elif cmd == 'add' and len(sys.argv) >= 6:
        priority = 'medium'
        if '--priority' in sys.argv:
            idx = sys.argv.index('--priority')
            priority = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else 'medium'
        add_task(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], priority)
    
    elif cmd == 'next' and len(sys.argv) >= 3:
        print_next(sys.argv[2])
    
    elif cmd == 'unblock' and len(sys.argv) >= 3:
        auto_unblock(sys.argv[2])
    
    elif cmd == 'init' and len(sys.argv) >= 5:
        desc = sys.argv[5] if len(sys.argv) > 5 else ''
        init_state(sys.argv[2], sys.argv[3], sys.argv[4], desc)
    
    else:
        print(__doc__)
        sys.exit(1)
