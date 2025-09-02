import time
import threading
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProgressUpdate:
    """Represents a progress update"""
    project_id: str
    stage: str
    progress: float  # 0-100
    message: str
    timestamp: datetime
    
class ProgressTracker:
    """
    Real-time progress tracking for ContentEngine operations.
    Supports multiple concurrent operations with callback notifications.
    """
    
    def __init__(self):
        self._progress_data: Dict[str, Dict[str, ProgressUpdate]] = {}
        self._callbacks: list[Callable[[ProgressUpdate], None]] = []
        self._lock = threading.Lock()
        
    def add_callback(self, callback: Callable[[ProgressUpdate], None]):
        """Add a callback function to receive progress updates"""
        with self._lock:
            self._callbacks.append(callback)
            
    def remove_callback(self, callback: Callable[[ProgressUpdate], None]):
        """Remove a callback function"""
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)
                
    def update_progress(self, project_id: str, stage: str, progress: float, message: str = ""):
        """Update progress for a specific project and stage"""
        progress_update = ProgressUpdate(
            project_id=project_id,
            stage=stage,
            progress=max(0, min(100, progress)),  # Clamp to 0-100
            message=message,
            timestamp=datetime.now()
        )
        
        with self._lock:
            # Store progress data
            if project_id not in self._progress_data:
                self._progress_data[project_id] = {}
            self._progress_data[project_id][stage] = progress_update
            
            # Notify callbacks
            for callback in self._callbacks:
                try:
                    callback(progress_update)
                except Exception as e:
                    print(f"Progress callback error: {e}")
                    
    def get_progress(self, project_id: str, stage: str = None) -> Optional[ProgressUpdate]:
        """Get current progress for a project and stage"""
        with self._lock:
            if project_id not in self._progress_data:
                return None
                
            if stage:
                return self._progress_data[project_id].get(stage)
            else:
                # Return most recent update
                if self._progress_data[project_id]:
                    latest = max(
                        self._progress_data[project_id].values(),
                        key=lambda x: x.timestamp
                    )
                    return latest
                return None
                
    def get_all_progress(self, project_id: str) -> Dict[str, ProgressUpdate]:
        """Get all progress data for a project"""
        with self._lock:
            return self._progress_data.get(project_id, {}).copy()
            
    def clear_progress(self, project_id: str, stage: str = None):
        """Clear progress data"""
        with self._lock:
            if project_id in self._progress_data:
                if stage:
                    self._progress_data[project_id].pop(stage, None)
                else:
                    del self._progress_data[project_id]
                    
    def get_active_operations(self) -> Dict[str, Dict[str, ProgressUpdate]]:
        """Get all currently tracked operations"""
        with self._lock:
            return {
                pid: {
                    stage: update for stage, update in stages.items() 
                    if update.progress < 100
                }
                for pid, stages in self._progress_data.items()
            }
            
    def cleanup_completed(self, max_age_hours: int = 24):
        """Clean up completed operations older than specified hours"""
        cutoff_time = datetime.now() - time.timedelta(hours=max_age_hours)
        
        with self._lock:
            projects_to_remove = []
            
            for project_id, stages in self._progress_data.items():
                stages_to_remove = []
                
                for stage, update in stages.items():
                    if update.progress >= 100 and update.timestamp < cutoff_time:
                        stages_to_remove.append(stage)
                
                for stage in stages_to_remove:
                    del stages[stage]
                    
                if not stages:  # No stages left
                    projects_to_remove.append(project_id)
            
            for project_id in projects_to_remove:
                del self._progress_data[project_id]

class StreamlitProgressTracker:
    """
    Streamlit-specific progress tracking with session state integration.
    """
    
    def __init__(self, session_state):
        self.session_state = session_state
        if 'progress_tracker' not in session_state:
            session_state.progress_tracker = ProgressTracker()
        self.tracker = session_state.progress_tracker
        
    def update_progress(self, project_id: str, stage: str, progress: float, message: str = ""):
        """Update progress and trigger Streamlit rerun if needed"""
        self.tracker.update_progress(project_id, stage, progress, message)
        
        # Store in session state for Streamlit access
        if 'current_operations' not in self.session_state:
            self.session_state.current_operations = {}
            
        if project_id not in self.session_state.current_operations:
            self.session_state.current_operations[project_id] = {}
            
        self.session_state.current_operations[project_id][stage] = {
            'progress': progress,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
    def get_progress(self, project_id: str, stage: str = None) -> Optional[Dict[str, Any]]:
        """Get progress data from session state"""
        current_ops = self.session_state.get('current_operations', {})
        if project_id not in current_ops:
            return None
            
        if stage:
            return current_ops[project_id].get(stage)
        else:
            # Return most recent
            if current_ops[project_id]:
                latest_stage = max(
                    current_ops[project_id].keys(),
                    key=lambda s: current_ops[project_id][s]['timestamp']
                )
                return current_ops[project_id][latest_stage]
            return None
            
    def is_stage_running(self, project_id: str, stage: str) -> bool:
        """Check if a stage is currently running"""
        progress_data = self.get_progress(project_id, stage)
        if progress_data:
            return 0 < progress_data['progress'] < 100
        return False
        
    def clear_completed(self, project_id: str):
        """Clear completed operations for a project"""
        current_ops = self.session_state.get('current_operations', {})
        if project_id in current_ops:
            # Remove completed stages
            completed_stages = [
                stage for stage, data in current_ops[project_id].items()
                if data['progress'] >= 100
            ]
            for stage in completed_stages:
                del current_ops[project_id][stage]

class OperationContext:
    """Context manager for tracking long-running operations"""
    
    def __init__(self, tracker: ProgressTracker, project_id: str, stage: str, total_steps: int = 100):
        self.tracker = tracker
        self.project_id = project_id
        self.stage = stage
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
        
    def __enter__(self):
        self.tracker.update_progress(self.project_id, self.stage, 0, "Starting operation...")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.tracker.update_progress(self.project_id, self.stage, 100, "Operation completed")
        else:
            self.tracker.update_progress(self.project_id, self.stage, -1, f"Operation failed: {exc_val}")
            
    def update(self, step: int = None, message: str = "", progress: float = None):
        """Update progress within the operation"""
        if step is not None:
            self.current_step = step
            calculated_progress = (step / self.total_steps) * 100
        elif progress is not None:
            calculated_progress = progress
        else:
            self.current_step += 1
            calculated_progress = (self.current_step / self.total_steps) * 100
            
        elapsed_time = time.time() - self.start_time
        if calculated_progress > 0:
            estimated_total = elapsed_time * (100 / calculated_progress)
            remaining = estimated_total - elapsed_time
            if remaining > 0:
                message += f" (ETA: {remaining:.0f}s)"
                
        self.tracker.update_progress(self.project_id, self.stage, calculated_progress, message)
        
    def set_message(self, message: str):
        """Update just the message without changing progress"""
        current_progress = (self.current_step / self.total_steps) * 100
        self.tracker.update_progress(self.project_id, self.stage, current_progress, message)