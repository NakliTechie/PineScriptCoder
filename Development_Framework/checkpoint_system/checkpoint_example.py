#!/usr/bin/env python3
"""
Example Development Workflow with Checkpoint Integration
"""

import sys
import os
sys.path.append('./scripts')

from checkpoint_manager import CheckpointManager

def initialize_project_checkpoint(project_name: str, project_type: str):
    """
    Initialize a checkpoint for a new Pine Script project
    
    Args:
        project_name: Name of the project
        project_type: Type of project (screener, indicator, strategy)
    """
    print(f"Initializing checkpoint for {project_name} ({project_type})")
    
    # Create checkpoint manager
    cm = CheckpointManager()
    
    # Define initial project structure
    pending_tasks = [
        f"Create {project_type} template",
        "Define input parameters",
        "Implement core logic functions",
        "Add helper functions",
        "Setup display/output formatting",
        "Integrate ticker inputs",
        "Add signal calculation logic",
        "Implement table display (if screener)",
        "Add alert conditions (if applicable)",
        "Testing and validation",
        "Documentation",
        "Final review"
    ]
    
    # Create initial checkpoint
    checkpoint_file = cm.create_checkpoint(
        project_name=project_name,
        session_id=f"{project_name}_{project_type}",
        overall_progress=0,
        completed_tasks=[],
        pending_tasks=pending_tasks,
        milestones_reached=[],
        current_focus=f"Initialize {project_type} project structure",
        current_file=f"screeners/{project_name.lower().replace(' ', '_')}/wip/{project_name.lower().replace(' ', '_')}.pine",
        next_steps=[
            f"Create {project_type} template file",
            "Define project requirements",
            "Set up development environment"
        ],
        testing_status="not_started",
        dependencies_resolved=False,
        resume_instructions=[
            f"Navigate to screeners/{project_name.lower().replace(' ', '_')}/wip/",
            f"Open {project_name.lower().replace(' ', '_')}.pine in editor",
            "Begin implementing template structure"
        ]
    )
    
    print(f"Project initialized with checkpoint: {os.path.basename(checkpoint_file)}")
    return checkpoint_file

def update_development_progress(project_name: str, task_completed: str, next_task: str, progress_increase: int = 10):
    """
    Update checkpoint when completing a development task
    
    Args:
        project_name: Name of the project
        task_completed: Description of completed task
        next_task: Description of next task
        progress_increase: Amount to increase overall progress
    """
    print(f"Updating checkpoint for {project_name}")
    
    # Create checkpoint manager
    cm = CheckpointManager()
    
    # Get latest checkpoint
    latest = cm.get_latest_checkpoint()
    
    if not latest or latest["project_name"] != project_name:
        print(f"No active checkpoint found for {project_name}")
        return
    
    # Update completed tasks
    if task_completed not in latest["completed_tasks"]:
        latest["completed_tasks"].append(task_completed)
    
    # Update pending tasks (remove completed task)
    if task_completed in latest["pending_tasks"]:
        latest["pending_tasks"].remove(task_completed)
    
    # Update current focus
    latest["current_focus"] = next_task
    
    # Update next steps
    latest["next_steps"] = [next_task] if next_task else []
    
    # Update progress
    latest["overall_progress"] = min(100, latest["overall_progress"] + progress_increase)
    
    # Create updated checkpoint
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"checkpoint_{timestamp}.json"
    filepath = os.path.join(cm.checkpoints_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(latest, f, indent=2)
    
    # Update latest checkpoint symlink
    latest_path = os.path.join(cm.checkpoints_dir, "latest_checkpoint.json")
    if os.path.exists(latest_path):
        os.remove(latest_path)
    os.symlink(filename, latest_path)
    
    print(f"Checkpoint updated: {os.path.basename(filepath)}")
    print(f"Progress: {latest['overall_progress']}%")

def resume_from_checkpoint():
    """
    Resume work from the latest checkpoint
    """
    print("Resuming work from latest checkpoint")
    
    # Create checkpoint manager
    cm = CheckpointManager()
    
    # Get latest checkpoint
    latest = cm.get_latest_checkpoint()
    
    if not latest:
        print("No checkpoint found to resume from")
        return
    
    print(f"\nResuming {latest['project_name']}")
    print(f"Last worked on: {latest['current_focus']}")
    print(f"Progress: {latest['overall_progress']}%")
    
    if latest["resume_instructions"]:
        print("\nResume instructions:")
        for i, instruction in enumerate(latest["resume_instructions"], 1):
            print(f"  {i}. {instruction}")
    
    if latest["next_steps"]:
        print("\nNext steps:")
        for i, step in enumerate(latest["next_steps"], 1):
            print(f"  {i}. {step}")
    
    print(f"\nWorking file: {latest['current_file']}")
    
    return latest

# Example usage functions
def example_workflow():
    """Example workflow demonstrating checkpoint usage"""
    print("=== Pine Script Development Checkpoint Example ===\n")
    
    # Initialize a new project
    project_name = "RSI Screener"
    project_type = "screener"
    
    print("1. Initializing project...")
    initialize_project_checkpoint(project_name, project_type)
    
    print("\n2. Simulating development progress...")
    # Simulate completing tasks
    update_development_progress(
        project_name,
        "Create screener template",
        "Define input parameters",
        15
    )
    
    update_development_progress(
        project_name,
        "Define input parameters",
        "Implement RSI calculation logic",
        10
    )
    
    print("\n3. Resuming from checkpoint...")
    resume_from_checkpoint()
    
    print("\n=== Workflow Complete ===")

if __name__ == "__main__":
    import datetime
    import json
    
    # Run example workflow
    example_workflow()