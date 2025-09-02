import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from models.project import ContentProject

class ProjectManager:
    """
    Manages multiple ContentEngine projects.
    Handles project discovery, creation, and organization.
    """
    
    def __init__(self, projects_base_dir: str = "projects"):
        self.projects_base_dir = Path(projects_base_dir)
        self.projects_base_dir.mkdir(exist_ok=True)
        
        # Cache for loaded projects
        self._project_cache = {}
        
    def create_project(self, name: str, description: str = "", 
                      seed_keywords: List[str] = None,
                      config_overrides: Dict[str, Any] = None) -> ContentProject:
        """Create a new content project"""
        
        # Create project instance
        project = ContentProject(name=name, description=description)
        
        # Set input data
        if seed_keywords:
            project.input_data["seed_keywords"] = seed_keywords
            
        # Apply configuration overrides
        if config_overrides:
            project.config.update(config_overrides)
            
        # Create project structure
        if project.create_project_structure(str(self.projects_base_dir)):
            # Cache the project
            self._project_cache[project.project_id] = project
            return project
        else:
            raise Exception("Failed to create project structure")
            
    def load_project(self, project_id: str) -> Optional[ContentProject]:
        """Load an existing project by ID with validation"""
        
        # Check cache first
        if project_id in self._project_cache:
            cached_project = self._project_cache[project_id]
            # Verify cached project still exists on filesystem
            if self._project_exists_on_filesystem(cached_project):
                return cached_project
            else:
                # Remove invalid cached project
                del self._project_cache[project_id]
        
        # Find project directory on filesystem
        try:
            for project_dir in self.projects_base_dir.iterdir():
                if project_dir.is_dir() and project_id in project_dir.name:
                    project = ContentProject.load_from_config(str(project_dir))
                    if project and project.project_id == project_id:
                        # Validate project before caching
                        if self._validate_project(project):
                            self._project_cache[project_id] = project
                            return project
                        else:
                            print(f"Project {project_id} failed validation")
                            return None
        except Exception as e:
            print(f"Error loading project {project_id}: {e}")
                    
        return None
    
    def _project_exists_on_filesystem(self, project: ContentProject) -> bool:
        """Check if a project's directory and config file exist"""
        try:
            if not self.projects_base_dir.exists():
                return False
            
            # Check for project directory
            expected_dir_name = f"project-{project.project_id[:8]}-{project.name.lower().replace(' ', '-')}"
            project_dir = self.projects_base_dir / expected_dir_name
            
            if not project_dir.exists() or not project_dir.is_dir():
                return False
            
            # Check for config file
            config_file = project_dir / "config.json"
            return config_file.exists()
            
        except Exception:
            return False
        
    def load_project_by_name(self, project_name: str) -> Optional[ContentProject]:
        """Load a project by its name"""
        projects = self.list_projects()
        for project in projects:
            if project.name.lower() == project_name.lower():
                return self.load_project(project.project_id)
        return None
        
    def list_projects(self, include_details: bool = False) -> List[ContentProject]:
        """List all available projects that can be loaded from filesystem"""
        projects = []
        
        try:
            # Clear cache of projects that don't exist on filesystem
            self._cleanup_cache()
            
            # Only scan filesystem for actual project directories
            if not self.projects_base_dir.exists():
                return projects
                
            for project_dir in self.projects_base_dir.iterdir():
                if project_dir.is_dir() and project_dir.name.startswith("project-"):
                    try:
                        # Validate that the project can be loaded
                        project = ContentProject.load_from_config(str(project_dir))
                        if project and self._validate_project(project):
                            # Cache the loaded project
                            self._project_cache[project.project_id] = project
                            
                            if not include_details:
                                # Return minimal project info for performance
                                minimal_project = ContentProject(
                                    name=project.name,
                                    description=project.description,
                                    project_id=project.project_id
                                )
                                minimal_project.created_at = project.created_at
                                minimal_project.updated_at = project.updated_at
                                minimal_project.execution_status = project.execution_status
                                projects.append(minimal_project)
                            else:
                                projects.append(project)
                    except Exception as e:
                        print(f"Skipping invalid project {project_dir.name}: {e}")
                        continue
                            
        except Exception as e:
            print(f"Error listing projects: {e}")
            
        # Sort by creation date (newest first)
        projects.sort(key=lambda x: x.created_at, reverse=True)
        return projects
    
    def _cleanup_cache(self):
        """Remove cached projects that don't exist on filesystem"""
        if not self.projects_base_dir.exists():
            self._project_cache.clear()
            return
            
        existing_project_dirs = set()
        for project_dir in self.projects_base_dir.iterdir():
            if project_dir.is_dir() and project_dir.name.startswith("project-"):
                existing_project_dirs.add(project_dir.name)
        
        # Remove cached projects that don't have directories
        cached_ids_to_remove = []
        for project_id, project in self._project_cache.items():
            expected_dir_name = f"project-{project_id[:8]}-{project.name.lower().replace(' ', '-')}"
            if expected_dir_name not in existing_project_dirs:
                cached_ids_to_remove.append(project_id)
        
        for project_id in cached_ids_to_remove:
            del self._project_cache[project_id]
    
    def _validate_project(self, project: ContentProject) -> bool:
        """Validate that a project is properly configured"""
        try:
            # Check required attributes
            if not project.project_id or not project.name:
                return False
            
            # Check that the project has the expected structure
            if not hasattr(project, 'execution_status') or not project.execution_status:
                return False
            
            # Check that required stages exist
            expected_stages = ['keyword_research', 'content_briefs', 'article_writing', 'social_media', 'youtube_scripts']
            for stage in expected_stages:
                if stage not in project.execution_status:
                    return False
            
            return True
        except Exception:
            return False
        
    def get_project_summaries(self) -> List[Dict[str, Any]]:
        """Get summary information for all projects"""
        summaries = []
        
        for project in self.list_projects():
            summaries.append({
                "project_id": project.project_id,
                "name": project.name,
                "description": project.description,
                "completion_percentage": project.get_completion_percentage(),
                "created_at": project.created_at,
                "updated_at": project.updated_at,
                "stage_count": len([s for s in project.execution_status.values() 
                                 if s["status"] == "completed"])
            })
            
        return summaries
        
    def delete_project(self, project_id: str) -> bool:
        """Delete a project and all its files"""
        try:
            project = self.load_project(project_id)
            if not project:
                return False
                
            # Remove project directory
            project_path = project.get_project_path(str(self.projects_base_dir))
            if project_path.exists():
                import shutil
                shutil.rmtree(project_path)
                
            # Remove from cache
            if project_id in self._project_cache:
                del self._project_cache[project_id]
                
            return True
            
        except Exception as e:
            print(f"Error deleting project: {e}")
            return False
            
    def duplicate_project(self, project_id: str, new_name: str) -> Optional[ContentProject]:
        """Create a duplicate of an existing project"""
        try:
            original_project = self.load_project(project_id)
            if not original_project:
                return None
                
            # Create new project with same configuration
            new_project = self.create_project(
                name=new_name,
                description=f"Copy of {original_project.name}",
                seed_keywords=original_project.input_data.get("seed_keywords", []),
                config_overrides=original_project.config.copy()
            )
            
            # Copy custom instructions if any
            if original_project.input_data.get("custom_instructions"):
                new_project.input_data["custom_instructions"] = original_project.input_data["custom_instructions"]
                new_project.save_inputs()
                
            return new_project
            
        except Exception as e:
            print(f"Error duplicating project: {e}")
            return None
            
    def search_projects(self, query: str) -> List[ContentProject]:
        """Search projects by name or description"""
        projects = self.list_projects()
        query = query.lower()
        
        matching_projects = []
        for project in projects:
            if (query in project.name.lower() or 
                query in project.description.lower() or
                any(query in keyword.lower() for keyword in project.input_data.get("seed_keywords", []))):
                matching_projects.append(project)
                
        return matching_projects
        
    def get_recent_projects(self, limit: int = 5) -> List[ContentProject]:
        """Get recently updated projects"""
        projects = self.list_projects()
        # Already sorted by creation date, but let's sort by updated date
        projects.sort(key=lambda x: x.updated_at, reverse=True)
        return projects[:limit]
        
    def get_project_statistics(self) -> Dict[str, Any]:
        """Get statistics about all projects"""
        projects = self.list_projects(include_details=True)
        
        if not projects:
            return {
                "total_projects": 0,
                "completed_projects": 0,
                "in_progress_projects": 0,
                "total_articles": 0,
                "avg_completion": 0
            }
            
        completed_projects = sum(1 for p in projects if p.get_completion_percentage() == 100)
        in_progress_projects = sum(1 for p in projects if 0 < p.get_completion_percentage() < 100)
        
        total_articles = sum(1 for p in projects 
                           if p.execution_status.get("article_writing", {}).get("status") == "completed")
                           
        avg_completion = sum(p.get_completion_percentage() for p in projects) / len(projects)
        
        return {
            "total_projects": len(projects),
            "completed_projects": completed_projects,
            "in_progress_projects": in_progress_projects,
            "pending_projects": len(projects) - completed_projects - in_progress_projects,
            "total_articles": total_articles,
            "avg_completion": round(avg_completion, 1)
        }
        
    def export_project_list(self, format: str = "json") -> str:
        """Export project list in specified format"""
        summaries = self.get_project_summaries()
        
        if format.lower() == "json":
            return json.dumps(summaries, indent=2)
        elif format.lower() == "csv":
            import csv
            import io
            
            output = io.StringIO()
            if summaries:
                writer = csv.DictWriter(output, fieldnames=summaries[0].keys())
                writer.writeheader()
                writer.writerows(summaries)
            return output.getvalue()
        else:
            return str(summaries)
            
    def cleanup_cache(self):
        """Clear the project cache"""
        self._project_cache.clear()
        
    def refresh_project(self, project_id: str) -> Optional[ContentProject]:
        """Refresh a project from disk, clearing cache"""
        if project_id in self._project_cache:
            del self._project_cache[project_id]
        return self.load_project(project_id)