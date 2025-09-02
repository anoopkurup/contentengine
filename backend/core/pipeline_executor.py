import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from models.project import ContentProject
from core.script_executor import ScriptExecutor

class PipelineExecutor:
    """
    Executes the ContentEngine pipeline stages for projects.
    Handles both OpenAI and Claude implementations with progress tracking.
    """
    
    def __init__(self, scripts_dir: str = "scripts"):
        # Ensure scripts_dir is resolved relative to the project root
        if not Path(scripts_dir).is_absolute():
            # Get the project root directory (three levels up from this file)
            project_root = Path(__file__).parent.parent.parent
            self.scripts_dir = project_root / scripts_dir
        else:
            self.scripts_dir = Path(scripts_dir)
        
        self.script_executor = ScriptExecutor(str(self.scripts_dir))
        
        # Available stages and their corresponding scripts
        self.stage_scripts = {
            "keyword_research": {
                "script": "KeywordResearcher.py",
                "description": "Keyword clustering and SERP analysis",
                "outputs": ["keyword_clusters.csv", "cluster_summary.csv"]
            },
            "content_briefs": {
                "openai": "ArticleBrief.py",
                "claude": "ArticleBrief_Claude.py", 
                "description": "Content outline generation with competitive analysis",
                "outputs": ["article_briefs.json", "article_briefs.md"]
            },
            "article_writing": {
                "openai": "ArticleWriter.py",
                "claude": "ArticleWriter_Claude.py",
                "description": "Article generation and writing",
                "outputs": ["article_draft.json", "article_draft.md"]
            },
            "social_media": {
                "openai": "SocialMedia.py", 
                "claude": "SocialMedia_Claude.py",
                "description": "Multi-platform social media content creation",
                "outputs": ["social_posts.json", "social_posts.md"]
            },
            "youtube_scripts": {
                "openai": "YoutTubeScript.py",
                "claude": "YouTubeScript_Claude.py", 
                "description": "YouTube video script generation",
                "outputs": ["youtube_script.json", "youtube_script.md"]
            }
        }
        
        # Progress tracking
        self.current_execution = {}
        self.progress_callbacks = []
        
    def add_progress_callback(self, callback: Callable[[str, str, float], None]):
        """Add a callback function for progress updates"""
        self.progress_callbacks.append(callback)
        
    def _notify_progress(self, project_id: str, stage: str, progress: float, message: str = ""):
        """Notify all progress callbacks"""
        for callback in self.progress_callbacks:
            try:
                callback(project_id, stage, progress, message)
            except Exception as e:
                print(f"Progress callback error: {e}")
                
    def _setup_project_environment(self, project: ContentProject) -> Dict[str, str]:
        """Setup environment variables for project execution"""
        env = os.environ.copy()
        
        # Set project-specific paths
        project_path = project.get_project_path()
        
        # Update environment with project configuration
        env.update({
            "TARGET_LOCATION": project.config.get("target_location", "India"),
            "TARGET_LANGUAGE": project.config.get("target_language", "en"),
            "SERP_OVERLAP_THRESHOLD": str(project.config.get("serp_overlap_threshold", 0.3)),
            "MIN_SEARCH_VOLUME": str(project.config.get("min_search_volume", 100)),
            "MAX_COMPETITION": str(project.config.get("max_competition", 0.3)),
            "CONTENT_GENERATOR": project.config.get("content_generator", "claude"),
            "CLAUDE_MODEL_PREFERENCE": project.config.get("claude_model_preference", "quality")
        })
        
        return env
        
    def _get_script_path(self, stage: str, content_generator: str = "claude") -> Optional[Path]:
        """Get the script path for a given stage and generator type"""
        stage_config = self.stage_scripts.get(stage)
        if not stage_config:
            return None
            
        # Handle keyword research (no generator variant)
        if stage == "keyword_research":
            script_name = stage_config["script"]
        else:
            # Get generator-specific script
            script_name = stage_config.get(content_generator)
            if not script_name:
                # Fallback to OpenAI if Claude not available
                script_name = stage_config.get("openai")
                
        if script_name:
            return self.scripts_dir / script_name
            
        return None
        
    def execute_stage(self, project: ContentProject, stage: str, 
                     force_regenerate: bool = False) -> Dict[str, Any]:
        """Execute a single pipeline stage"""
        
        # Check if stage already completed and not forcing regeneration
        stage_status = project.execution_status.get(stage, {})
        if stage_status.get("status") == "completed" and not force_regenerate:
            return {
                "success": True,
                "message": f"Stage {stage} already completed",
                "outputs": project.get_stage_files(stage)
            }
            
        # Update project status to running
        project.update_stage_status(stage, "running")
        self._notify_progress(project.project_id, stage, 0, "Starting stage execution")
        
        try:
            # Use ScriptExecutor for integrated execution
            if stage == "keyword_research":
                success = self.script_executor.execute_keyword_research(
                    project, 
                    progress_callback=lambda progress, message: self._notify_progress(
                        project.project_id, stage, progress, message
                    )
                )
                if not success:
                    raise Exception("Keyword research execution failed")
                
                # Update project status and save
                project.update_stage_status(stage, "completed")
                project.save_config()
                
                return {
                    "success": True,
                    "message": f"Stage {stage} completed successfully",
                    "outputs": project.output_files.get(stage, [])
                }
                    
            elif stage == "content_briefs":
                success = self.script_executor.execute_article_brief(
                    project,
                    progress_callback=lambda progress, message: self._notify_progress(
                        project.project_id, stage, progress, message
                    )
                )
                if not success:
                    raise Exception("Article brief generation failed")
                
                # Update project status and save
                project.update_stage_status(stage, "completed") 
                project.save_config()
                
                return {
                    "success": True,
                    "message": f"Stage {stage} completed successfully", 
                    "outputs": project.output_files.get(stage, [])
                }
                    
            else:
                # Fallback to original script execution for other stages
                content_generator = project.config.get("content_generator", "claude")
                script_path = self._get_script_path(stage, content_generator)
                
                if not script_path or not script_path.exists():
                    raise FileNotFoundError(f"Script not found for stage {stage}")
                    
                # Setup environment
                env = self._setup_project_environment(project)
                
                # Change working directory to project directory
                original_cwd = os.getcwd()
                project_path = project.get_project_path()
                
                try:
                    os.chdir(project_path)
                    
                    # Execute the script
                    self._notify_progress(project.project_id, stage, 25, "Executing script")
                    
                    result = subprocess.run([
                        sys.executable, str(script_path.absolute())
                    ], 
                    capture_output=True, 
                    text=True, 
                    env=env,
                    timeout=3600  # 1 hour timeout
                    )
                    
                    self._notify_progress(project.project_id, stage, 75, "Processing outputs")
                    
                    # Check if execution was successful
                    if result.returncode == 0:
                        # Move outputs to appropriate stage directory
                        self._organize_stage_outputs(project, stage)
                        
                        # Update project status
                        project.update_stage_status(stage, "completed")
                        self._notify_progress(project.project_id, stage, 100, "Stage completed successfully")
                        
                        return {
                            "success": True,
                            "message": f"Stage {stage} completed successfully",
                            "outputs": project.get_stage_files(stage),
                            "stdout": result.stdout,
                            "stderr": result.stderr
                        }
                    else:
                        # Execution failed
                        error_msg = f"Script execution failed: {result.stderr}"
                        project.update_stage_status(stage, "failed", error_msg)
                        
                        return {
                            "success": False,
                            "message": error_msg,
                            "stdout": result.stdout,
                            "stderr": result.stderr
                        }
                        
                finally:
                    os.chdir(original_cwd)
                
        except subprocess.TimeoutExpired:
            error_msg = "Script execution timed out"
            project.update_stage_status(stage, "failed", error_msg)
            return {"success": False, "message": error_msg}
            
        except Exception as e:
            error_msg = f"Error executing stage: {str(e)}"
            project.update_stage_status(stage, "failed", error_msg)
            return {"success": False, "message": error_msg}
            
    def _organize_stage_outputs(self, project: ContentProject, stage: str):
        """Organize outputs into appropriate stage directories"""
        
        project_path = project.get_project_path()
        stage_mapping = {
            "keyword_research": "stage_01_keyword_research",
            "content_briefs": "stage_02_content_briefs", 
            "article_writing": "stage_03_articles",
            "social_media": "stage_04_social_media",
            "youtube_scripts": "stage_05_youtube"
        }
        
        stage_dir = project_path / stage_mapping.get(stage, stage)
        stage_dir.mkdir(exist_ok=True)
        
        # Expected output files for each stage
        expected_outputs = self.stage_scripts.get(stage, {}).get("outputs", [])
        
        # Move files from project root to stage directory
        for output_file in expected_outputs:
            source_file = project_path / output_file
            if source_file.exists():
                dest_file = stage_dir / output_file
                source_file.rename(dest_file)
                
                # Record the output file
                project.add_output_file(stage, str(dest_file))
                
        # Also move any files with Claude-specific naming
        if project.config.get("content_generator") == "claude":
            claude_patterns = [
                "claude_writing_prompt.md",
                "claude_social_prompts_*.md",
                "claude_youtube_prompts_*.md",
                "*_claude.json",
                "*_claude.md"
            ]
            
            import glob
            for pattern in claude_patterns:
                for file_path in glob.glob(str(project_path / pattern)):
                    source_file = Path(file_path)
                    dest_file = stage_dir / source_file.name
                    if source_file != dest_file:  # Avoid moving file to itself
                        source_file.rename(dest_file)
                        project.add_output_file(stage, str(dest_file))
                        
    def execute_full_pipeline(self, project: ContentProject, 
                            start_stage: str = None,
                            force_regenerate: bool = False) -> Dict[str, Any]:
        """Execute the complete pipeline or start from a specific stage"""
        
        stages = ["keyword_research", "content_briefs", "article_writing", 
                 "social_media", "youtube_scripts"]
        
        # Find starting point
        start_index = 0
        if start_stage and start_stage in stages:
            start_index = stages.index(start_stage)
            
        results = {}
        overall_success = True
        
        for i, stage in enumerate(stages[start_index:], start_index):
            self._notify_progress(project.project_id, "pipeline", 
                                (i / len(stages)) * 100, f"Executing {stage}")
            
            result = self.execute_stage(project, stage, force_regenerate)
            results[stage] = result
            
            if not result["success"]:
                overall_success = False
                break
                
        self._notify_progress(project.project_id, "pipeline", 100, 
                            "Pipeline execution completed" if overall_success else "Pipeline execution failed")
        
        return {
            "success": overall_success,
            "results": results,
            "project_id": project.project_id
        }
        
    def get_stage_status(self, project: ContentProject, stage: str) -> Dict[str, Any]:
        """Get the current status of a pipeline stage"""
        return {
            "stage": stage,
            "status": project.execution_status.get(stage, {}).get("status", "pending"),
            "completed_at": project.execution_status.get(stage, {}).get("completed_at"),
            "error": project.execution_status.get(stage, {}).get("error"),
            "outputs": project.get_stage_files(stage)
        }
        
    def get_pipeline_status(self, project: ContentProject) -> Dict[str, Any]:
        """Get the status of the entire pipeline"""
        stages = ["keyword_research", "content_briefs", "article_writing", 
                 "social_media", "youtube_scripts"]
                 
        stage_statuses = {}
        for stage in stages:
            stage_statuses[stage] = self.get_stage_status(project, stage)
            
        return {
            "project_id": project.project_id,
            "completion_percentage": project.get_completion_percentage(),
            "stages": stage_statuses
        }
        
    def can_execute_stage(self, project: ContentProject, stage: str) -> tuple[bool, str]:
        """Check if a stage can be executed (dependencies met)"""
        
        stage_dependencies = {
            "keyword_research": [],
            "content_briefs": ["keyword_research"],
            "article_writing": ["keyword_research", "content_briefs"],
            "social_media": ["keyword_research", "content_briefs", "article_writing"],
            "youtube_scripts": ["keyword_research", "content_briefs", "article_writing"]
        }
        
        dependencies = stage_dependencies.get(stage, [])
        
        for dep_stage in dependencies:
            dep_status = project.execution_status.get(dep_stage, {}).get("status", "pending")
            if dep_status != "completed":
                return False, f"Dependency {dep_stage} not completed (status: {dep_status})"
                
        return True, "Dependencies satisfied"
        
    def validate_project_setup(self, project: ContentProject) -> Dict[str, Any]:
        """Validate that a project is ready for execution"""
        issues = []
        
        # Check if seed keywords are provided
        if not project.input_data.get("seed_keywords"):
            issues.append("No seed keywords provided")
            
        # Check if required scripts exist
        content_generator = project.config.get("content_generator", "claude")
        for stage, config in self.stage_scripts.items():
            script_path = self._get_script_path(stage, content_generator)
            if not script_path or not script_path.exists():
                issues.append(f"Script not found for stage {stage}")
                
        # Check environment variables
        required_env_vars = ["DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD"]
        if content_generator == "openai":
            required_env_vars.append("OPENAI_API_KEY")
            
        for env_var in required_env_vars:
            if not os.getenv(env_var):
                issues.append(f"Environment variable {env_var} not set")
                
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }