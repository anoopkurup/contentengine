import streamlit as st
import sys
from pathlib import Path
import time
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from core.project_manager import ProjectManager
from core.pipeline_executor import PipelineExecutor
from utils.progress_tracker import StreamlitProgressTracker

def init_pipeline_components():
    """Initialize pipeline components"""
    if 'project_manager' not in st.session_state:
        st.session_state.project_manager = ProjectManager()
    if 'pipeline_executor' not in st.session_state:
        st.session_state.pipeline_executor = PipelineExecutor()
    if 'progress_tracker' not in st.session_state:
        st.session_state.progress_tracker = StreamlitProgressTracker(st.session_state)
    
    return (st.session_state.project_manager, 
            st.session_state.pipeline_executor, 
            st.session_state.progress_tracker)

def show_project_selector(project_manager):
    """Show project selection dropdown"""
    projects = project_manager.list_projects()
    
    if not projects:
        st.warning("No projects found. Please create a project first.")
        if st.button("➕ Create New Project"):
            st.switch_page("pages/project_wizard.py")
        return None
    
    # Create project options
    project_options = {}
    for project in projects:
        project_options[f"{project.name} ({project.project_id})"] = project.project_id
    
    if not project_options:
        st.error("No valid projects found")
        return None
    
    # Project selection
    selected_key = st.selectbox(
        "Select Project:",
        list(project_options.keys()),
        key="project_selector"
    )
    
    return project_options[selected_key]

def show_pipeline_status(project, progress_tracker):
    """Display pipeline stages and their status"""
    st.subheader("📊 Pipeline Status")
    
    stages = {
        'keyword_research': {'name': '🔍 Keyword Research', 'desc': 'Analyze search volumes and competition'},
        'content_briefs': {'name': '📄 Article Brief', 'desc': 'Generate content outline and strategy'},
        'article_writing': {'name': '📝 Article Writing', 'desc': 'Create SEO-optimized article'},
        'social_media': {'name': '📱 Social Media', 'desc': 'Generate platform-specific posts'},
        'youtube_scripts': {'name': '🎥 YouTube Script', 'desc': 'Create video script with timestamps'}
    }
    
    # Progress overview
    completed_stages = project.get_completed_stages()
    progress = (len(completed_stages) / len(stages)) * 100
    
    st.progress(progress / 100)
    st.write(f"Overall Progress: {len(completed_stages)}/{len(stages)} stages completed ({progress:.0f}%)")
    
    # Individual stage status
    for stage_id, stage_info in stages.items():
        stage_data = project.stages[stage_id]
        
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            if stage_data.completed:
                st.success(f"✅ {stage_info['name']}")
                # Handle both string and datetime formats for completed_at
                completed_time = "Unknown"
                if stage_data.completed_at:
                    try:
                        if hasattr(stage_data.completed_at, 'strftime'):
                            # It's a datetime object
                            completed_time = stage_data.completed_at.strftime('%Y-%m-%d %H:%M')
                        else:
                            # It's likely a string, try to parse and format
                            from datetime import datetime
                            if isinstance(stage_data.completed_at, str):
                                # Try different string formats
                                try:
                                    dt = datetime.fromisoformat(stage_data.completed_at.replace('Z', '+00:00'))
                                    completed_time = dt.strftime('%Y-%m-%d %H:%M')
                                except:
                                    completed_time = str(stage_data.completed_at)[:16]  # Truncate if needed
                    except Exception:
                        completed_time = str(stage_data.completed_at) if stage_data.completed_at else "Unknown"
                st.caption(f"Completed: {completed_time}")
            elif stage_data.error:
                st.error(f"❌ {stage_info['name']}")
                st.caption(f"Error: {stage_data.error}")
            elif progress_tracker.is_stage_running(project.project_id, stage_id):
                progress_data = progress_tracker.get_progress(project.project_id, stage_id)
                if progress_data:
                    st.info(f"🔄 {stage_info['name']} ({progress_data['progress']:.0f}%)")
                    st.caption(progress_data['message'])
                else:
                    st.info(f"🔄 {stage_info['name']} (Running...)")
            else:
                st.write(f"⏳ {stage_info['name']}")
                st.caption("Not started")
        
        with col2:
            st.write(stage_info['desc'])
        
        with col3:
            if not stage_data.completed and not progress_tracker.is_stage_running(project.project_id, stage_id):
                if st.button(f"▶️", key=f"run_{stage_id}", help=f"Run {stage_info['name']}"):
                    run_single_stage(project.project_id, stage_id)

def run_single_stage(project_id, stage_name):
    """Run a single pipeline stage"""
    st.session_state.running_stage = stage_name
    st.rerun()

def run_complete_pipeline(project_id):
    """Run the complete pipeline"""
    st.session_state.running_complete = True
    st.rerun()

def execute_pipeline_stage(project_manager, pipeline_executor, progress_tracker, project_id, stage_name=None):
    """Execute pipeline stage(s) with progress tracking"""
    project = project_manager.load_project(project_id)
    
    if not project:
        st.error("Project not found")
        return
    
    # Create placeholder for real-time updates
    status_placeholder = st.empty()
    progress_placeholder = st.empty()
    
    try:
        if stage_name:
            # Run single stage
            with status_placeholder.container():
                st.info(f"🚀 Starting {stage_name}...")
            
            # Execute real stage
            execute_real_stage(progress_tracker, project_manager, pipeline_executor, project_id, stage_name, status_placeholder, progress_placeholder)
            
        else:
            # Run complete pipeline
            stages = ['keyword_research', 'content_briefs', 'article_writing', 'social_media', 'youtube_scripts']
            
            for i, current_stage in enumerate(stages):
                if not project.stages[current_stage].completed:
                    with status_placeholder.container():
                        st.info(f"🚀 Running stage {i+1}/{len(stages)}: {current_stage}")
                    
                    execute_real_stage(progress_tracker, project_manager, pipeline_executor, project_id, current_stage, status_placeholder, progress_placeholder)
            
            st.success("🎉 Pipeline completed successfully!")
    
    except Exception as e:
        st.error(f"❌ Pipeline execution failed: {e}")
    
    finally:
        # Clear running state
        if 'running_stage' in st.session_state:
            del st.session_state.running_stage
        if 'running_complete' in st.session_state:
            del st.session_state.running_complete

def execute_real_stage(progress_tracker, project_manager, pipeline_executor, project_id, stage_name, status_placeholder, progress_placeholder):
    """Execute actual pipeline stage with progress updates"""
    
    try:
        # Load the project
        project = project_manager.load_project(project_id)
        if not project:
            st.error(f"❌ Could not load project {project_id}")
            return
        
        # Set up progress callback to update UI
        def update_ui_progress(progress, message):
            progress_tracker.update_progress(project_id, stage_name, progress, message)
            
            with progress_placeholder.container():
                st.progress(progress / 100 if progress > 0 else 0)
                st.write(f"Progress: {progress:.0f}% - {message}")
        
        # Execute the stage using PipelineExecutor
        with status_placeholder.container():
            st.info(f"🚀 Executing {stage_name}...")
        
        # Execute the actual stage
        result = pipeline_executor.execute_stage(project, stage_name)
        
        if result.get("success"):
            st.success(f"✅ {stage_name} completed successfully!")
            
            # Show outputs if any
            outputs = result.get("outputs", [])
            if outputs:
                st.info(f"📁 Generated {len(outputs)} output file(s)")
                for output in outputs:
                    st.write(f"  - {output}")
        else:
            error_msg = result.get("message", "Unknown error")
            st.error(f"❌ {stage_name} failed: {error_msg}")
            
            # Show stderr if available
            stderr = result.get("stderr")
            if stderr:
                with st.expander("Error Details"):
                    st.code(stderr)
                    
    except Exception as e:
        st.error(f"❌ Error executing {stage_name}: {e}")
        import traceback
        with st.expander("Full Error Details"):
            st.code(traceback.format_exc())

def main():
    """Main pipeline runner interface"""
    st.set_page_config(
        page_title="ContentEngine - Pipeline Runner",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Content Generation Pipeline")
    st.markdown("Execute your content creation pipeline with real-time progress tracking")
    
    # Initialize components
    try:
        project_manager, pipeline_executor, progress_tracker = init_pipeline_components()
    except Exception as e:
        st.error("⚠️ Unable to initialize pipeline components")
        st.error(f"Error: {e}")
        return
    
    # Sidebar for project selection
    with st.sidebar:
        st.header("Project Selection")
        selected_project_id = show_project_selector(project_manager)
        
        if selected_project_id:
            project = project_manager.load_project(selected_project_id)
            if project:
                st.success(f"✅ Selected: {project.name}")
            else:
                st.error("❌ Project Loading Error")
                st.markdown(f"**Could not load project with ID:** `{selected_project_id}`")
                
                # Show diagnostic information
                with st.expander("🔍 Diagnostic Information"):
                    st.markdown("**Possible causes:**")
                    st.markdown("- Project was deleted or moved from filesystem")
                    st.markdown("- Project configuration file is corrupted") 
                    st.markdown("- Project directory permissions issue")
                    
                    # Check if projects directory exists
                    projects_dir = project_manager.projects_base_dir
                    if not projects_dir.exists():
                        st.error(f"Projects directory does not exist: {projects_dir}")
                    else:
                        st.info(f"Projects directory exists: {projects_dir}")
                        
                        # List actual directories
                        actual_dirs = []
                        try:
                            for d in projects_dir.iterdir():
                                if d.is_dir() and d.name.startswith("project-"):
                                    actual_dirs.append(d.name)
                        except Exception as e:
                            st.error(f"Error reading projects directory: {e}")
                        
                        if actual_dirs:
                            st.markdown("**Project directories found:**")
                            for dir_name in actual_dirs:
                                st.code(dir_name)
                        else:
                            st.warning("No project directories found in filesystem")
                
                # Show available projects from list_projects()  
                available_projects = project_manager.list_projects()
                if available_projects:
                    st.info(f"✅ {len(available_projects)} valid project(s) available:")
                    for p in available_projects:
                        st.write(f"- **{p.name}** (ID: `{p.project_id}`)")
                else:
                    st.warning("No valid projects found. Please create a new project.")
                    if st.button("➕ Create New Project", type="primary"):
                        st.switch_page("pages/project_wizard.py")
                
                return
            
            st.markdown("---")
            st.header("Pipeline Actions")
            
            # Check if anything is running
            is_running = ('running_stage' in st.session_state or 
                         'running_complete' in st.session_state)
            
            if st.button("🚀 Run Complete Pipeline", 
                        disabled=is_running,
                        help="Execute all pipeline stages sequentially"):
                run_complete_pipeline(selected_project_id)
            
            if st.button("🔄 Refresh Status"):
                st.rerun()
        
        st.markdown("---")
        st.header("Quick Actions")
        
        if st.button("🏠 Back to Dashboard"):
            st.switch_page("app.py")
        
        if st.button("➕ New Project"):
            st.switch_page("pages/project_wizard.py")
        
        if st.button("📁 Content Manager"):
            st.switch_page("pages/content_manager.py")
    
    # Main content area
    if not selected_project_id:
        st.info("👆 Please select a project from the sidebar to continue")
        return
    
    project = project_manager.load_project(selected_project_id)
    
    if not project:
        st.error("Selected project not found")
        return
    
    # Show pipeline status
    show_pipeline_status(project, progress_tracker)
    
    # Handle pipeline execution
    if st.session_state.get('running_stage'):
        st.markdown("---")
        st.subheader(f"🔄 Executing: {st.session_state.running_stage}")
        execute_pipeline_stage(
            project_manager, 
            pipeline_executor, 
            progress_tracker,
            selected_project_id, 
            st.session_state.running_stage
        )
    
    elif st.session_state.get('running_complete'):
        st.markdown("---")
        st.subheader("🚀 Running Complete Pipeline")
        execute_pipeline_stage(
            project_manager, 
            pipeline_executor, 
            progress_tracker,
            selected_project_id
        )
    
    # Project info
    st.markdown("---")
    st.subheader("📋 Project Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Keywords", len(project.target_keywords))
    
    with col2:
        st.metric("Completed Stages", len(project.get_completed_stages()))
    
    with col3:
        st.metric("Progress", f"{project.get_progress_percentage():.0f}%")
    
    # Keywords preview
    if project.target_keywords:
        with st.expander("🔍 Target Keywords"):
            if len(project.target_keywords) <= 10:
                for keyword in project.target_keywords:
                    st.write(f"• {keyword}")
            else:
                for keyword in project.target_keywords[:10]:
                    st.write(f"• {keyword}")
                st.write(f"... and {len(project.target_keywords) - 10} more keywords")

if __name__ == "__main__":
    main()