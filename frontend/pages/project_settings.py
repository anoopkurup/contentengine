import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import sys

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from core.project_manager import ProjectManager
from config.app_config import AppConfig

def show_project_settings(project_manager: ProjectManager, project_id: str):
    """Show and edit project settings"""
    project = project_manager.get_project(project_id)
    if not project:
        st.error("Project not found")
        return
    
    st.subheader(f"⚙️ Settings for: {project.name}")
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Basic project information
        st.markdown("#### Basic Information")
        
        new_name = st.text_input("Project Name", value=project.name)
        new_description = st.text_area("Description", value=project.description or "")
        
        # SEO Settings
        st.markdown("#### SEO Settings")
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            new_target_location = st.text_input(
                "Target Location", 
                value=project.config.get('target_location', AppConfig.DEFAULT_TARGET_LOCATION)
            )
            new_target_language = st.selectbox(
                "Target Language",
                options=['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh'],
                index=0 if project.config.get('target_language', AppConfig.DEFAULT_TARGET_LANGUAGE) == 'en' else 0
            )
        
        with col1_2:
            new_min_search_volume = st.number_input(
                "Min Search Volume",
                min_value=0,
                max_value=10000,
                value=int(project.config.get('min_search_volume', AppConfig.DEFAULT_MIN_SEARCH_VOLUME))
            )
            new_max_competition = st.slider(
                "Max Competition",
                min_value=0.0,
                max_value=1.0,
                value=float(project.config.get('max_competition', AppConfig.DEFAULT_MAX_COMPETITION)),
                step=0.1
            )
        
        # Content Generation Settings
        st.markdown("#### Content Generation Settings")
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            new_content_generator = st.selectbox(
                "Content Generator",
                options=['claude', 'openai'],
                index=0 if project.config.get('content_generator', AppConfig.DEFAULT_CONTENT_GENERATOR) == 'claude' else 1
            )
            
            if new_content_generator == 'claude':
                new_claude_preference = st.selectbox(
                    "Claude Model Preference",
                    options=['quality', 'speed'],
                    index=0 if project.config.get('claude_model_preference', AppConfig.DEFAULT_CLAUDE_MODEL_PREFERENCE) == 'quality' else 1
                )
            else:
                new_claude_preference = 'quality'
        
        with col2_2:
            new_serp_overlap = st.slider(
                "SERP Overlap Threshold",
                min_value=0.0,
                max_value=1.0,
                value=float(project.config.get('serp_overlap_threshold', AppConfig.DEFAULT_SERP_OVERLAP_THRESHOLD)),
                step=0.1,
                help="Minimum overlap threshold for SERP analysis"
            )
    
    with col2:
        # Project metadata
        st.markdown("#### Project Info")
        
        info_data = {
            "Project ID": project_id,
            "Status": project.status.title(),
            "Created": project.created_date.strftime("%Y-%m-%d %H:%M"),
            "Last Modified": project.modified_date.strftime("%Y-%m-%d %H:%M"),
            "Target Keywords": len(project.target_keywords),
            "Pipeline Stages": len([s for s in project.stages.values() if s.get('completed', False)])
        }
        
        for key, value in info_data.items():
            st.metric(key, value)
        
        # Danger zone
        st.markdown("#### 🚨 Danger Zone")
        
        if st.button("🗑️ Delete Project", type="secondary"):
            if 'confirm_delete' not in st.session_state:
                st.session_state.confirm_delete = False
                
            if not st.session_state.confirm_delete:
                st.session_state.confirm_delete = True
                st.warning("⚠️ This action cannot be undone!")
                st.rerun()
        
        if st.session_state.get('confirm_delete', False):
            st.error("Are you absolutely sure?")
            col_yes, col_no = st.columns(2)
            
            with col_yes:
                if st.button("Yes, Delete", type="primary"):
                    try:
                        project_manager.delete_project(project_id)
                        st.success("Project deleted successfully!")
                        st.session_state.confirm_delete = False
                        st.switch_page("app.py")
                    except Exception as e:
                        st.error(f"Error deleting project: {e}")
            
            with col_no:
                if st.button("Cancel"):
                    st.session_state.confirm_delete = False
                    st.rerun()
    
    # Save button
    st.markdown("---")
    col_save, col_cancel = st.columns([1, 4])
    
    with col_save:
        if st.button("💾 Save Changes", type="primary"):
            try:
                # Update project
                project.name = new_name
                project.description = new_description
                project.modified_date = datetime.now()
                
                # Update config
                project.config.update({
                    'target_location': new_target_location,
                    'target_language': new_target_language,
                    'min_search_volume': new_min_search_volume,
                    'max_competition': new_max_competition,
                    'content_generator': new_content_generator,
                    'claude_model_preference': new_claude_preference,
                    'serp_overlap_threshold': new_serp_overlap
                })
                
                # Save to file
                project.save_config()
                
                st.success("✅ Settings saved successfully!")
                
                # Reset confirmation state
                if 'confirm_delete' in st.session_state:
                    del st.session_state.confirm_delete
                    
            except Exception as e:
                st.error(f"❌ Error saving settings: {e}")

def show_global_settings():
    """Show global application settings"""
    st.subheader("🌐 Global Settings")
    
    # Environment status
    validation = AppConfig.validate_setup()
    
    if validation['valid']:
        st.success("✅ All systems operational")
    else:
        st.warning("⚠️ Configuration issues detected")
        for issue in validation['issues']:
            st.error(f"• {issue}")
    
    # Configuration overview
    st.markdown("#### Current Configuration")
    
    config_data = {
        "Projects Directory": str(AppConfig.PROJECTS_DIR),
        "Scripts Directory": str(AppConfig.SCRIPTS_DIR),
        "Default Location": AppConfig.DEFAULT_TARGET_LOCATION,
        "Default Language": AppConfig.DEFAULT_TARGET_LANGUAGE,
        "Default Generator": AppConfig.DEFAULT_CONTENT_GENERATOR,
        "Debug Mode": "Enabled" if AppConfig.DEBUG else "Disabled",
        "Log Level": AppConfig.LOG_LEVEL
    }
    
    for key, value in config_data.items():
        st.text(f"{key}: {value}")
    
    # API Status
    st.markdown("#### API Configuration Status")
    
    api_status = {
        "DataForSEO Login": "✅ Configured" if AppConfig.DATAFORSEO_LOGIN else "❌ Missing",
        "DataForSEO Password": "✅ Configured" if AppConfig.DATAFORSEO_PASSWORD else "❌ Missing",
        "OpenAI API Key": "✅ Configured" if AppConfig.OPENAI_API_KEY else "❌ Not Set (Optional)"
    }
    
    for api, status in api_status.items():
        if "✅" in status:
            st.success(f"{api}: {status}")
        elif "❌ Missing" in status:
            st.error(f"{api}: {status}")
        else:
            st.info(f"{api}: {status}")
    
    # Defaults configuration
    st.markdown("#### Default Project Settings")
    defaults = AppConfig.get_project_defaults()
    
    for key, value in defaults.items():
        st.text(f"{key.replace('_', ' ').title()}: {value}")

def main():
    """Main project settings interface"""
    st.set_page_config(
        page_title="ContentEngine - Project Settings",
        page_icon="⚙️",
        layout="wide"
    )
    
    st.title("⚙️ Settings")
    st.markdown("Configure your projects and application settings")
    
    # Initialize project manager
    project_manager = ProjectManager()
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Settings")
        
        settings_type = st.radio(
            "Choose settings type:",
            ["Project Settings", "Global Settings"]
        )
        
        if settings_type == "Project Settings":
            st.markdown("#### Select Project")
            
            projects = project_manager.list_projects()
            if not projects:
                st.info("No projects found")
                return
            
            project_options = {}
            for project_id in projects:
                project = project_manager.get_project(project_id)
                if project:
                    project_options[f"{project.name}"] = project_id
            
            if project_options:
                selected_project_name = st.selectbox(
                    "Choose a project:",
                    list(project_options.keys())
                )
                selected_project_id = project_options[selected_project_name]
            else:
                st.error("No valid projects found")
                return
        
        st.markdown("---")
        st.header("Quick Actions")
        
        if st.button("🏠 Back to Dashboard"):
            st.switch_page("app.py")
        
        if st.button("📁 Content Manager"):
            st.switch_page("pages/content_manager.py")
    
    # Main content area
    if settings_type == "Project Settings":
        if 'selected_project_id' in locals():
            show_project_settings(project_manager, selected_project_id)
    else:
        show_global_settings()

if __name__ == "__main__":
    main()