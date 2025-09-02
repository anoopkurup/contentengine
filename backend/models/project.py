import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class ContentProject:
    """
    Core model for managing content creation projects.
    Handles project metadata, configuration, and file organization.
    """
    
    def __init__(self, name: str, description: str = "", project_id: str = None):
        self.project_id = project_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
        # Project configuration
        self.config = {
            "target_location": "India",
            "target_language": "en",
            "serp_overlap_threshold": 0.3,
            "min_search_volume": 100,
            "max_competition": 0.3,
            "content_generator": "claude",  # claude or openai
            "claude_model_preference": "quality"
        }
        
        # Input data
        self.input_data = {
            "seed_keywords": [],
            "target_audience": "",
            "custom_instructions": ""
        }
        
        # Execution status for each pipeline stage
        self.execution_status = {
            "keyword_research": {"status": "pending", "completed_at": None, "error": None},
            "content_briefs": {"status": "pending", "completed_at": None, "error": None},
            "article_writing": {"status": "pending", "completed_at": None, "error": None},
            "social_media": {"status": "pending", "completed_at": None, "error": None},
            "youtube_scripts": {"status": "pending", "completed_at": None, "error": None}
        }
        
        # File paths and outputs
        self.output_files = {
            "keyword_research": [],
            "content_briefs": [],
            "articles": [],
            "social_media": [],
            "youtube": []
        }
        
        # Project folder path
        self.project_path = None
        
    @property
    def slug(self) -> str:
        """Generate URL-friendly slug from project name"""
        return self.name.lower().replace(' ', '-').replace('_', '-')
        
    @property
    def project_folder_name(self) -> str:
        """Generate project folder name"""
        return f"project-{self.project_id[:8]}-{self.slug}"
        
    def get_project_path(self, base_projects_dir: str = "projects") -> Path:
        """Get the full path to the project directory"""
        if self.project_path is None:
            self.project_path = Path(base_projects_dir) / self.project_folder_name
        return Path(self.project_path)
        
    def create_project_structure(self, base_projects_dir: str = "projects") -> bool:
        """Create the project directory structure"""
        try:
            project_path = self.get_project_path(base_projects_dir)
            
            # Create main project directory
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            subdirs = [
                "inputs",
                "stage_01_keyword_research",
                "stage_02_content_briefs", 
                "stage_03_articles",
                "stage_04_social_media",
                "stage_05_youtube",
                "exports"
            ]
            
            for subdir in subdirs:
                (project_path / subdir).mkdir(exist_ok=True)
                
            # Create initial configuration files
            self.save_config()
            self.save_inputs()
            
            return True
            
        except Exception as e:
            print(f"Error creating project structure: {e}")
            return False
            
    def save_config(self) -> bool:
        """Save project configuration to JSON file"""
        try:
            project_path = self.get_project_path()
            config_file = project_path / "config.json"
            
            config_data = {
                "project_id": self.project_id,
                "name": self.name,
                "description": self.description,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "config": self.config,
                "input_data": self.input_data,
                "execution_status": self.execution_status,
                "output_files": self.output_files
            }
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
            
    def save_inputs(self) -> bool:
        """Save input data to files"""
        try:
            project_path = self.get_project_path()
            inputs_dir = project_path / "inputs"
            
            # Save seed keywords
            if self.input_data.get("seed_keywords"):
                keywords_file = inputs_dir / "seed_keywords.txt"
                with open(keywords_file, 'w') as f:
                    for keyword in self.input_data["seed_keywords"]:
                        f.write(f"{keyword}\n")
                        
            # Save settings
            settings_file = inputs_dir / "settings.json"
            with open(settings_file, 'w') as f:
                json.dump(self.config, f, indent=2)
                
            # Save custom instructions
            if self.input_data.get("custom_instructions"):
                instructions_file = inputs_dir / "custom_instructions.md"
                with open(instructions_file, 'w') as f:
                    f.write(self.input_data["custom_instructions"])
                    
            return True
            
        except Exception as e:
            print(f"Error saving inputs: {e}")
            return False
            
    @classmethod
    def load_from_config(cls, project_path: str) -> Optional['ContentProject']:
        """Load project from existing configuration file"""
        try:
            config_file = Path(project_path) / "config.json"
            
            if not config_file.exists():
                return None
                
            with open(config_file, 'r') as f:
                data = json.load(f)
                
            # Create project instance
            project = cls(
                name=data["name"],
                description=data["description"],
                project_id=data["project_id"]
            )
            
            # Load all data
            project.created_at = data["created_at"]
            project.updated_at = data["updated_at"]
            project.config = data["config"]
            project.input_data = data["input_data"]
            project.execution_status = data["execution_status"]
            project.output_files = data["output_files"]
            project.project_path = project_path
            
            return project
            
        except Exception as e:
            print(f"Error loading project: {e}")
            return None
            
    def update_stage_status(self, stage: str, status: str, error: str = None) -> bool:
        """Update the status of a pipeline stage"""
        try:
            if stage in self.execution_status:
                self.execution_status[stage]["status"] = status
                if status == "completed":
                    self.execution_status[stage]["completed_at"] = datetime.now().isoformat()
                if error:
                    self.execution_status[stage]["error"] = error
                    
                self.updated_at = datetime.now().isoformat()
                self.save_config()
                return True
                
        except Exception as e:
            print(f"Error updating stage status: {e}")
            
        return False
        
    def add_output_file(self, stage: str, file_path: str) -> bool:
        """Add an output file to the project record"""
        try:
            if stage in self.output_files:
                if file_path not in self.output_files[stage]:
                    self.output_files[stage].append(file_path)
                    self.updated_at = datetime.now().isoformat()
                    self.save_config()
                return True
                
        except Exception as e:
            print(f"Error adding output file: {e}")
            
        return False
        
    def get_stage_files(self, stage: str) -> List[str]:
        """Get all files for a specific stage"""
        stage_map = {
            "keyword_research": "stage_01_keyword_research",
            "content_briefs": "stage_02_content_briefs",
            "articles": "stage_03_articles", 
            "social_media": "stage_04_social_media",
            "youtube": "stage_05_youtube"
        }
        
        if stage in stage_map:
            stage_dir = self.get_project_path() / stage_map[stage]
            if stage_dir.exists():
                return [str(f) for f in stage_dir.iterdir() if f.is_file()]
                
        return []
        
    def get_completion_percentage(self) -> float:
        """Calculate project completion percentage"""
        total_stages = len(self.execution_status)
        completed_stages = sum(1 for status in self.execution_status.values() 
                             if status["status"] == "completed")
        return (completed_stages / total_stages) * 100
        
    def get_status_summary(self) -> Dict[str, Any]:
        """Get a summary of project status"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "completion_percentage": self.get_completion_percentage(),
            "stage_statuses": self.execution_status,
            "last_updated": self.updated_at,
            "total_output_files": sum(len(files) for files in self.output_files.values())
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary for serialization"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "config": self.config,
            "input_data": self.input_data,
            "execution_status": self.execution_status,
            "output_files": self.output_files,
            "project_path": str(self.project_path) if self.project_path else None
        }
    
    # Adapter methods for pipeline runner compatibility
    @property
    def stages(self):
        """Adapter property to make execution_status look like stages"""
        stage_objects = {}
        for stage_name, status_info in self.execution_status.items():
            # Create a simple object that has the expected attributes
            class StageInfo:
                def __init__(self, status_info):
                    self.completed = status_info["status"] == "completed"
                    self.error = status_info.get("error")
                    
                    # Handle completed_at - convert from ISO string to datetime if needed
                    completed_at_raw = status_info.get("completed_at")
                    if completed_at_raw and isinstance(completed_at_raw, str):
                        try:
                            from datetime import datetime
                            self.completed_at = datetime.fromisoformat(completed_at_raw.replace('Z', '+00:00'))
                        except:
                            self.completed_at = completed_at_raw  # Keep as string if parsing fails
                    else:
                        self.completed_at = completed_at_raw
            
            stage_objects[stage_name] = StageInfo(status_info)
        return stage_objects
    
    def get_completed_stages(self):
        """Get list of completed stage names"""
        return [name for name, status in self.execution_status.items() 
                if status["status"] == "completed"]
    
    @property
    def target_keywords(self):
        """Adapter property for target keywords"""
        return self.input_data.get("seed_keywords", [])
    
    def get_progress_percentage(self):
        """Alias for get_completion_percentage for compatibility"""
        return self.get_completion_percentage()
    
    def update_stage_status_compat(self, stage_name: str, completed: bool = None, error: str = None):
        """Compatibility method for pipeline runner"""
        if completed:
            result = self.update_stage_status(stage_name, "completed", error)
            # Ensure the project is saved after status update
            self.save_config()
            return result
        elif error:
            return self.update_stage_status(stage_name, "failed", error)
        else:
            return self.update_stage_status(stage_name, "running", error)