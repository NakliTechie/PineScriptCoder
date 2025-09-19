#!/usr/bin/env python3
"""
Simple Checkpoint Creation Utility
"""

import sys
import os
import argparse
from datetime import datetime
import json

# Add project scripts to path
sys.path.append('/Users/chiragpatnaik/Pinescript/scripts')

from checkpoint_manager import CheckpointManager

def create_simple_checkpoint(project_name, progress=None, focus=None, notes=None):
    """
    Create a simple checkpoint with minimal parameters
    
    Args:
        project_name (str): Name of the project
        progress (int): Progress percentage (optional)
        focus (str): Current focus/task (optional)
        notes (str): Additional notes (optional)
    """
    cm = CheckpointManager()
    
    # Get latest checkpoint to inherit some context
    latest = cm.get_latest_checkpoint()
    
    # Prepare checkpoint data
    checkpoint_data = {
        "project_name": project_name,
        "current_focus": focus or (latest.get("current_focus", "") if latest else ""),
        "additional_notes": notes or ""
    }
    
    if progress is not None:
        checkpoint_data["overall_progress"] = progress
    elif latest:
        checkpoint_data["overall_progress"] = latest.get("overall_progress", 0)
    
    # Create checkpoint
    checkpoint_file = cm.create_checkpoint(**checkpoint_data)
    
    print(f"✓ Checkpoint created for '{project_name}'")
    print(f"  Progress: {checkpoint_data.get('overall_progress', 0)}%")
    if focus:
        print(f"  Focus: {focus}")
    if notes:
        print(f"  Notes: {notes}")
    print(f"  File: {os.path.basename(checkpoint_file)}")
    
    return checkpoint_file

def show_latest_checkpoint():
    """Show information about the latest checkpoint"""
    cm = CheckpointManager()
    latest = cm.get_latest_checkpoint()
    
    if not latest:
        print("No checkpoints found")
        return
    
    print("Latest Checkpoint:")
    print(f"  Project: {latest['project_name']}")
    print(f"  Progress: {latest['overall_progress']}%")
    print(f"  Focus: {latest['current_focus']}")
    if latest['completed_tasks']:
        print(f"  Completed Tasks: {len(latest['completed_tasks'])}")
    if latest['pending_tasks']:
        print(f"  Pending Tasks: {len(latest['pending_tasks'])}")
    if latest['additional_notes']:
        print(f"  Notes: {latest['additional_notes']}")

def list_recent_checkpoints(count=5):
    """List recent checkpoints"""
    cm = CheckpointManager()
    checkpoints = cm.list_checkpoints(limit=count)
    
    if not checkpoints:
        print("No checkpoints found")
        return
    
    print(f"Recent Checkpoints (last {count}):")
    for cp_file in checkpoints:
        try:
            cp_data = cm.load_checkpoint(cp_file)
            timestamp = cp_data.get('timestamp', '').split('T')[0] if cp_data.get('timestamp') else 'Unknown'
            print(f"  {cp_file} - {cp_data.get('project_name', 'Unnamed')} ({cp_data.get('overall_progress', 0)}%) - {timestamp}")
        except Exception as e:
            print(f"  {cp_file} - Error reading file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Simple Checkpoint Utility")
    parser.add_argument("action", choices=["create", "latest", "list"], 
                       help="Action to perform")
    parser.add_argument("--project", "-p", help="Project name")
    parser.add_argument("--progress", "-pr", type=int, help="Progress percentage")
    parser.add_argument("--focus", "-f", help="Current focus/task")
    parser.add_argument("--notes", "-n", help="Additional notes")
    parser.add_argument("--count", "-c", type=int, default=5, 
                       help="Number of recent checkpoints to list")
    
    args = parser.parse_args()
    
    if args.action == "create":
        if not args.project:
            print("Error: Project name is required for create action")
            sys.exit(1)
        create_simple_checkpoint(args.project, args.progress, args.focus, args.notes)
    
    elif args.action == "latest":
        show_latest_checkpoint()
    
    elif args.action == "list":
        list_recent_checkpoints(args.count)

if __name__ == "__main__":
    main()