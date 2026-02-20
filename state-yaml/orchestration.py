#!/usr/bin/env python3
"""
STATE.yaml Orchestration Utilities
Handles PM spawning, state polling, and coordination logic
"""

import os
import yaml
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# Base directory for all projects
PROJECTS_ROOT = Path.home() / "clawd" / "projects"
REGISTRY_FILE = Path.home() / "clawd" / "PROJECT_REGISTRY.md"


def get_state_path(project_name: str) -> Path:
    """Get the path to a project's STATE.yaml file"""
    return PROJECTS_ROOT / project_name / "STATE.yaml"


def read_state(project_name: str) -> Optional[Dict]:
    """Read and parse a project's STATE.yaml"""
    state_path = get_state_path(project_name)
    if not state_path.exists():
        return None
    
    with open(state_path, 'r') as f:
        return yaml.safe_load(f)


def get_project_status(project_name: str) -> Dict[str, Any]:
    """Get quick status overview of a project"""
    state = read_state(project_name)
    if not state:
        return {"error": "Project not found"}
    
    tasks = state.get('tasks', [])
    return {
        "project": project_name,
        "updated": state.get('updated'),
        "total_tasks": len(tasks),
        "pending": sum(1 for t in tasks if t.get('status') == 'pending'),
        "in_progress": sum(1 for t in tasks if t.get('status') == 'in_progress'),
        "blocked": sum(1 for t in tasks if t.get('status') == 'blocked'),
        "done": sum(1 for t in tasks if t.get('status') == 'done'),
        "failed": sum(1 for t in tasks if t.get('status') == 'failed'),
    }


def format_status_report(project_name: str) -> str:
    """Format a human-readable status report"""
    status = get_project_status(project_name)
    
    if "error" in status:
        return f"❌ {status['error']}"
    
    lines = [
        f"📊 **{project_name}** — Last updated: {status['updated']}",
        f"",
        f"Tasks: {status['total_tasks']} total",
        f"  ✅ Done: {status['done']}",
        f"  🔄 In Progress: {status['in_progress']}",
        f"  ⏳ Pending: {status['pending']}",
        f"  🚫 Blocked: {status['blocked']}",
    ]
    
    if status['failed'] > 0:
        lines.append(f"  ❌ Failed: {status['failed']}")
    
    return "\n".join(lines)


def generate_pm_label(project_name: str, scope: str = "main") -> str:
    """Generate a PM label following conventions"""
    return f"pm-{project_name}-{scope}"


def parse_pm_label(label: str) -> Optional[Dict[str, str]]:
    """Parse a PM label into components"""
    if not label.startswith("pm-"):
        return None
    
    parts = label.split('-')
    if len(parts) < 3:
        return None
    
    return {
        "project": parts[1],
        "scope": '-'.join(parts[2:]) if len(parts) > 2 else "main"
    }


def create_project(project_name: str, initial_task: str) -> Dict[str, Any]:
    """
    Create a new project directory with initial STATE.yaml
    Returns info needed for spawning PM
    """
    project_dir = PROJECTS_ROOT / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    state_path = project_dir / "STATE.yaml"
    
    initial_state = {
        "project": project_name,
        "created": datetime.utcnow().isoformat() + "Z",
        "updated": datetime.utcnow().isoformat() + "Z",
        "tasks": [
            {
                "id": "setup",
                "status": "in_progress",
                "owner": generate_pm_label(project_name),
                "started": datetime.utcnow().isoformat() + "Z",
                "description": initial_task,
                "notes": "Project initialization"
            }
        ],
        "next_actions": []
    }
    
    with open(state_path, 'w') as f:
        yaml.dump(initial_state, f, default_flow_style=False, sort_keys=False)
    
    # Initial git commit
    commit_state_change(project_name, "init", "setup")
    
    return {
        "project_name": project_name,
        "project_dir": str(project_dir),
        "state_file": str(state_path),
        "pm_label": generate_pm_label(project_name)
    }


def commit_state_change(project_name: str, action: str, task_id: str) -> bool:
    """
    Commit STATE.yaml changes to git
    Format: [STATE] {action}: {task_id}
    """
    project_dir = PROJECTS_ROOT / project_name
    state_path = project_dir / "STATE.yaml"
    
    if not state_path.exists():
        return False
    
    try:
        # Check if git repo exists
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            # Initialize git repo
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
        
        # Add and commit
        subprocess.run(["git", "add", "STATE.yaml"], cwd=project_dir, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"[STATE] {action}: {task_id}"],
            cwd=project_dir,
            capture_output=True
        )
        return True
        
    except Exception as e:
        print(f"Git commit failed: {e}")
        return False


def find_blocked_ready_tasks(project_name: str) -> List[Dict]:
    """
    Find tasks that are blocked but whose dependencies are now complete
    Returns list of tasks ready to be unblocked
    """
    state = read_state(project_name)
    if not state:
        return []
    
    tasks = {t['id']: t for t in state.get('tasks', [])}
    ready = []
    
    for task in state.get('tasks', []):
        if task.get('status') != 'blocked':
            continue
        
        blocked_by = task.get('blocked_by', [])
        if isinstance(blocked_by, str):
            blocked_by = [blocked_by]
        
        # Check if all blockers are done
        all_done = all(
            tasks.get(b, {}).get('status') == 'done'
            for b in blocked_by
        )
        
        if all_done:
            ready.append(task)
    
    return ready


if __name__ == "__main__":
    # Quick test
    print("STATE.yaml Orchestration Utilities")
    print("=" * 40)
    
    # Test label generation
    label = generate_pm_label("website", "frontend")
    print(f"Generated label: {label}")
    print(f"Parsed: {parse_pm_label(label)}")
    
    # Test project creation
    # info = create_project("test-project", "Initial test task")
    # print(f"Created project: {info}")
