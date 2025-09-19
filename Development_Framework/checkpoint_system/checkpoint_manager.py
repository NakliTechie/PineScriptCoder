#!/usr/bin/env python3
"""
Checkpoint Management Script for Pine Script Development
"""

import json
import os
import datetime
from typing import Dict, List, Any

class CheckpointManager:
    def __init__(self, project_root: str = "/Users/chiragpatnaik/Pinescript"):
        self.project_root = project_root
        self.checkpoints_dir = os.path.join(project_root, "checkpoints")
        self.template_file = os.path.join(self.checkpoints_dir, "template_checkpoint.json")
        
        # Ensure checkpoints directory exists
        os.makedirs(self.checkpoints_dir, exist_ok=True)
        
        # Ensure template exists
        self._ensure_template()
    
    def _ensure_template(self):
        """Ensure checkpoint template exists"""
        if not os.path.exists(self.template_file):
            template = {
                "timestamp": "",
                "project_name": "",
                "session_id": "",
                "overall_progress": 0,
                "completed_tasks": [],
                "pending_tasks": [],
                "milestones_reached": [],
                "current_focus": "",
                "current_file": "",
                "current_section": "",
                "next_steps": [],
                "lines_of_code": 0,
                "functions_implemented": 0,
                "features_completed": 0,
                "testing_status": "not_started",
                "resume_instructions": [],
                "dependencies_resolved": False,
                "known_issues": [],
                "blocking_factors": [],
                "additional_notes": ""
            }
            
            with open(self.template_file, 'w') as f:
                json.dump(template, f, indent=2)
    
    def create_checkpoint(self, project_name: str, session_id: str = None, **kwargs) -> str:
        """
        Create a new checkpoint for a project
        
        Args:
            project_name: Name of the project
            session_id: Optional session identifier
            **kwargs: Additional checkpoint data to override template values
            
        Returns:
            Path to created checkpoint file
        """
        # Load template
        with open(self.template_file, 'r') as f:
            checkpoint = json.load(f)
        
        # Update with provided data
        checkpoint.update({
            "timestamp": datetime.datetime.now().isoformat(),
            "project_name": project_name,
            "session_id": session_id or f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        })
        
        # Update with any additional kwargs
        checkpoint.update(kwargs)
        
        # Create checkpoint filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"checkpoint_{timestamp}.json"
        filepath = os.path.join(self.checkpoints_dir, filename)
        
        # Save checkpoint
        with open(filepath, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        # Update latest checkpoint symlink
        latest_path = os.path.join(self.checkpoints_dir, "latest_checkpoint.json")
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(filename, latest_path)
        
        print(f"Checkpoint created: {filename}")
        return filepath
    
    def get_latest_checkpoint(self) -> Dict[str, Any]:
        """
        Get the most recent checkpoint
        
        Returns:
            Checkpoint data dictionary or None if no checkpoints exist
        """
        latest_path = os.path.join(self.checkpoints_dir, "latest_checkpoint.json")
        
        if not os.path.exists(latest_path):
            print("No checkpoints found")
            return None
        
        try:
            with open(latest_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading latest checkpoint: {e}")
            return None
    
    def list_checkpoints(self, limit: int = 10) -> List[str]:
        """
        List recent checkpoint files
        
        Args:
            limit: Maximum number of checkpoints to list
            
        Returns:
            List of checkpoint filenames
        """
        checkpoints = []
        
        for filename in os.listdir(self.checkpoints_dir):
            if filename.startswith("checkpoint_") and filename.endswith(".json"):
                checkpoints.append(filename)
        
        # Sort by timestamp (newest first)
        checkpoints.sort(reverse=True)
        
        return checkpoints[:limit]
    
    def load_checkpoint(self, filename: str) -> Dict[str, Any]:
        """
        Load a specific checkpoint file
        
        Args:
            filename: Name of checkpoint file to load
            
        Returns:
            Checkpoint data dictionary
        """
        filepath = os.path.join(self.checkpoints_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Checkpoint file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def update_progress(self, progress_delta: int, additional_notes: str = ""):
        """
        Update progress in the latest checkpoint
        
        Args:
            progress_delta: Amount to increase progress by
            additional_notes: Additional notes about progress
        """
        latest = self.get_latest_checkpoint()
        
        if not latest:
            print("No checkpoint to update")
            return
        
        # Update progress
        latest["overall_progress"] = min(100, latest["overall_progress"] + progress_delta)
        
        if additional_notes:
            latest["additional_notes"] += f"\n{additional_notes}"
        
        # Save updated checkpoint
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"checkpoint_{timestamp}.json"
        filepath = os.path.join(self.checkpoints_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(latest, f, indent=2)
        
        # Update latest checkpoint symlink
        latest_path = os.path.join(self.checkpoints_dir, "latest_checkpoint.json")
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(filename, latest_path)
        
        print(f"Progress updated to {latest['overall_progress']}%")

def main():
    """Main function for checkpoint management"""
    print("Pine Script Development Checkpoint Manager")
    print("===========================================")
    
    manager = CheckpointManager()
    
    print("\nAvailable commands:")
    print("1. create - Create a new checkpoint")
    print("2. latest - Show latest checkpoint")
    print("3. list - List recent checkpoints")
    print("4. load - Load a specific checkpoint")
    print("5. progress - Update progress in latest checkpoint")
    print("6. help - Show this help")
    
    # This script is primarily meant to be imported and used by other scripts
    print("\nThis script is designed to be imported and used by development scripts.")
    print("Import it in your development workflow to create automatic checkpoints.")

if __name__ == "__main__":
    main()