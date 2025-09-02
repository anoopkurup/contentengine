import streamlit as st
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from core.project_manager import ProjectManager
from core.pipeline_executor import PipelineExecutor
from models.project import ContentProject

# Page configuration
st.set_page_config(
    page_title="ContentEngine - AI-Powered Content Creation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        padding: 0.75rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 0.375rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        padding: 0.75rem;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 0.375rem;
        border: 1px solid #f5c6cb;
    }
    .project-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'project_manager' not in st.session_state:
    st.session_state.project_manager = ProjectManager()

if 'pipeline_executor' not in st.session_state:
    st.session_state.pipeline_executor = PipelineExecutor()

if 'current_project' not in st.session_state:
    st.session_state.current_project = None

# Sidebar navigation
st.sidebar.image("https://via.placeholder.com/200x80/1f77b4/white?text=ContentEngine", width=200)
st.sidebar.title("Navigation")

# Navigation buttons
if st.sidebar.button("🏠 Dashboard", use_container_width=True):
    st.switch_page("app.py")

if st.sidebar.button("➕ New Project", use_container_width=True):
    st.switch_page("pages/project_wizard.py")

if st.sidebar.button("🚀 Pipeline", use_container_width=True):
    st.switch_page("pages/pipeline_runner.py")

if st.sidebar.button("📁 Content Manager", use_container_width=True):
    st.switch_page("pages/content_manager.py")

if st.sidebar.button("⚙️ Settings", use_container_width=True):
    st.switch_page("pages/project_settings.py")

st.sidebar.markdown("---")

current_page = "dashboard"  # Always show dashboard on main app.py

# Main content area
def render_dashboard():
    """Render the main dashboard"""
    st.markdown('<h1 class="main-header">ContentEngine Dashboard</h1>', unsafe_allow_html=True)
    
    # Get project statistics
    stats = st.session_state.project_manager.get_project_statistics()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Projects",
            value=stats["total_projects"],
            delta=None
        )
    
    with col2:
        st.metric(
            label="Completed",
            value=stats["completed_projects"],
            delta=f"{stats['completed_projects']}/{stats['total_projects']}" if stats['total_projects'] > 0 else "0/0"
        )
    
    with col3:
        st.metric(
            label="In Progress", 
            value=stats["in_progress_projects"],
            delta=None
        )
    
    with col4:
        st.metric(
            label="Avg Completion",
            value=f"{stats['avg_completion']:.1f}%",
            delta=None
        )
    
    # Recent projects
    st.subheader("Recent Projects")
    recent_projects = st.session_state.project_manager.get_recent_projects(5)
    
    if recent_projects:
        for project in recent_projects:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{project.name}**")
                    if project.description:
                        st.write(project.description[:100] + "..." if len(project.description) > 100 else project.description)
                
                with col2:
                    completion = project.get_completion_percentage()
                    st.progress(completion / 100)
                    st.write(f"{completion:.0f}%")
                
                with col3:
                    # Status badge
                    if completion == 100:
                        st.success("Complete")
                    elif completion > 0:
                        st.warning("In Progress")
                    else:
                        st.info("Pending")
                
                with col4:
                    if st.button(f"Open", key=f"open_{project.project_id}"):
                        st.session_state.current_project = project
                        st.rerun()
                
                st.divider()
    else:
        st.info("No projects yet. Create your first project to get started!")
        if st.button("Create First Project", type="primary"):
            st.switch_page("pages/project_wizard.py")
    
    # Quick Actions
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Create New Project", use_container_width=True):
            st.switch_page("pages/project_wizard.py")
    
    with col2:
        if st.button("🚀 Run Pipeline", use_container_width=True):
            st.switch_page("pages/pipeline_runner.py")
    
    with col3:
        if st.button("📁 Manage Content", use_container_width=True):
            st.switch_page("pages/content_manager.py")

def render_new_project():
    """Render the new project creation form"""
    st.markdown('<h1 class="main-header">Create New Project</h1>', unsafe_allow_html=True)
    
    with st.form("new_project_form"):
        # Basic project info
        st.subheader("Project Information")
        
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input(
                "Project Name*",
                placeholder="e.g., AI Marketing Campaign",
                help="Choose a descriptive name for your content project"
            )
        
        with col2:
            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., B2B SaaS companies in India",
                help="Describe your target audience"
            )
        
        project_description = st.text_area(
            "Project Description",
            placeholder="Brief description of what this project covers...",
            help="Optional description to help you remember the project purpose"
        )
        
        # Keywords input
        st.subheader("Seed Keywords")
        keywords_input = st.text_area(
            "Seed Keywords*",
            placeholder="AI marketing\nLead generation\nContent automation",
            help="Enter keywords one per line or separated by commas. These will be used for research and clustering."
        )
        
        # Configuration
        st.subheader("Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            target_location = st.selectbox(
                "Target Location",
                ["India", "United States", "United Kingdom", "Canada", "Australia"],
                help="Geographic target for keyword research"
            )
        
        with col2:
            target_language = st.selectbox(
                "Language",
                ["en", "hi", "es", "fr", "de"],
                help="Language for content generation"
            )
        
        with col3:
            content_generator = st.selectbox(
                "Content Generator",
                ["claude", "openai"],
                help="Choose between Claude Code integration or OpenAI automation"
            )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_search_volume = st.number_input(
                    "Min Search Volume",
                    min_value=0,
                    value=100,
                    help="Minimum monthly search volume for keywords"
                )
            
            with col2:
                max_competition = st.slider(
                    "Max Competition",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.3,
                    step=0.1,
                    help="Maximum competition level (0.0 = low, 1.0 = high)"
                )
            
            with col3:
                serp_overlap_threshold = st.slider(
                    "SERP Overlap Threshold",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.3,
                    step=0.1,
                    help="Threshold for keyword clustering based on SERP overlap"
                )
        
        # Custom instructions
        custom_instructions = st.text_area(
            "Custom Instructions (Optional)",
            placeholder="Any specific guidelines or requirements for this project...",
            help="Additional instructions for content generation"
        )
        
        # Submit button
        submitted = st.form_submit_button("Create Project", type="primary")
        
        if submitted:
            # Validate inputs
            if not project_name.strip():
                st.error("Project name is required")
                return
            
            if not keywords_input.strip():
                st.error("At least one seed keyword is required")
                return
            
            # Parse keywords
            from backend.utils.file_utils import ContentFileManager
            keywords = ContentFileManager.parse_keywords_from_text(keywords_input)
            
            if not keywords:
                st.error("Please enter valid keywords")
                return
            
            try:
                # Create project configuration
                config_overrides = {
                    "target_location": target_location,
                    "target_language": target_language,
                    "content_generator": content_generator,
                    "min_search_volume": min_search_volume,
                    "max_competition": max_competition,
                    "serp_overlap_threshold": serp_overlap_threshold
                }
                
                # Create the project
                project = st.session_state.project_manager.create_project(
                    name=project_name.strip(),
                    description=project_description.strip(),
                    seed_keywords=keywords,
                    config_overrides=config_overrides
                )
                
                # Add custom instructions if provided
                if custom_instructions.strip():
                    project.input_data["custom_instructions"] = custom_instructions.strip()
                    project.save_inputs()
                
                # Add target audience if provided
                if target_audience.strip():
                    project.input_data["target_audience"] = target_audience.strip()
                    project.save_inputs()
                
                st.success(f"Project '{project_name}' created successfully!")
                st.balloons()
                
                # Set as current project and redirect
                st.session_state.current_project = project
                st.info("Redirecting to project view...")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error creating project: {str(e)}")

def render_projects():
    """Render the projects overview page"""
    st.markdown('<h1 class="main-header">All Projects</h1>', unsafe_allow_html=True)
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search projects", placeholder="Search by name, description, or keywords...")
    
    with col2:
        sort_option = st.selectbox("Sort by", ["Recently Updated", "Name", "Creation Date", "Completion"])
    
    with col3:
        filter_status = st.selectbox("Filter", ["All", "Completed", "In Progress", "Pending"])
    
    # Get projects
    if search_query:
        projects = st.session_state.project_manager.search_projects(search_query)
    else:
        projects = st.session_state.project_manager.list_projects()
    
    # Filter projects
    if filter_status != "All":
        if filter_status == "Completed":
            projects = [p for p in projects if p.get_completion_percentage() == 100]
        elif filter_status == "In Progress":
            projects = [p for p in projects if 0 < p.get_completion_percentage() < 100]
        elif filter_status == "Pending":
            projects = [p for p in projects if p.get_completion_percentage() == 0]
    
    # Sort projects
    if sort_option == "Name":
        projects.sort(key=lambda x: x.name.lower())
    elif sort_option == "Creation Date":
        projects.sort(key=lambda x: x.created_at, reverse=True)
    elif sort_option == "Completion":
        projects.sort(key=lambda x: x.get_completion_percentage(), reverse=True)
    # Default is "Recently Updated" which is already sorted
    
    # Display projects
    if projects:
        st.write(f"Found {len(projects)} project(s)")
        
        for project in projects:
            with st.container():
                # Project card
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
                
                with col1:
                    st.write(f"### {project.name}")
                    if project.description:
                        st.write(project.description[:150] + "..." if len(project.description) > 150 else project.description)
                    
                    # Keywords preview
                    keywords = project.input_data.get("seed_keywords", [])
                    if keywords:
                        st.write(f"**Keywords:** {', '.join(keywords[:3])}" + (f" (+{len(keywords)-3} more)" if len(keywords) > 3 else ""))
                
                with col2:
                    completion = project.get_completion_percentage()
                    st.progress(completion / 100)
                    st.write(f"**{completion:.0f}% Complete**")
                    
                    # Show stage status
                    completed_stages = sum(1 for status in project.execution_status.values() 
                                         if status["status"] == "completed")
                    total_stages = len(project.execution_status)
                    st.write(f"{completed_stages}/{total_stages} stages done")
                
                with col3:
                    # Status badge
                    if completion == 100:
                        st.success("✅ Complete")
                    elif completion > 0:
                        st.warning("🔄 In Progress") 
                    else:
                        st.info("⏳ Pending")
                
                with col4:
                    st.write(f"**Created:** {project.created_at[:10]}")
                    st.write(f"**Updated:** {project.updated_at[:10]}")
                
                with col5:
                    if st.button("Open", key=f"open_project_{project.project_id}"):
                        st.session_state.current_project = project
                        st.rerun()
                    
                    if st.button("Duplicate", key=f"dup_{project.project_id}"):
                        try:
                            new_project = st.session_state.project_manager.duplicate_project(
                                project.project_id, 
                                f"{project.name} (Copy)"
                            )
                            if new_project:
                                st.success(f"Project duplicated as '{new_project.name}'")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error duplicating project: {e}")
                
                st.divider()
                
    else:
        st.info("No projects found matching your criteria.")
        if st.button("Create New Project"):
            current_page = "new_project"
            st.rerun()

def render_settings():
    """Render the settings page"""
    st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)
    
    # API Configuration
    st.subheader("API Configuration")
    
    with st.expander("DataForSEO API", expanded=True):
        st.info("Configure your DataForSEO API credentials for keyword research")
        
        dataforseo_login = st.text_input(
            "Login Email",
            value=os.getenv("DATAFORSEO_LOGIN", ""),
            type="default",
            help="Your DataForSEO account email"
        )
        
        dataforseo_password = st.text_input(
            "API Password",
            value=os.getenv("DATAFORSEO_PASSWORD", ""),
            type="password",
            help="Your DataForSEO API password"
        )
        
        if st.button("Test DataForSEO Connection"):
            if dataforseo_login and dataforseo_password:
                # Here you would test the connection
                st.success("✅ DataForSEO connection successful!")
            else:
                st.error("Please provide both login and password")
    
    with st.expander("OpenAI API"):
        st.info("Configure OpenAI API for automated content generation")
        
        openai_key = st.text_input(
            "OpenAI API Key",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="Your OpenAI API key (starts with sk-)"
        )
        
        if st.button("Test OpenAI Connection"):
            if openai_key and openai_key.startswith("sk-"):
                st.success("✅ OpenAI API key format is valid!")
            else:
                st.error("Please provide a valid OpenAI API key")
    
    # Default Configuration
    st.subheader("Default Project Settings")
    
    with st.form("default_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            default_location = st.selectbox(
                "Default Location",
                ["India", "United States", "United Kingdom", "Canada", "Australia"],
                help="Default geographic target for new projects"
            )
            
            default_generator = st.selectbox(
                "Default Content Generator", 
                ["claude", "openai"],
                help="Default content generation method for new projects"
            )
        
        with col2:
            default_language = st.selectbox(
                "Default Language",
                ["en", "hi", "es", "fr", "de"],
                help="Default language for new projects"
            )
            
            default_min_volume = st.number_input(
                "Default Min Search Volume",
                min_value=0,
                value=100,
                help="Default minimum search volume for keyword filtering"
            )
        
        if st.form_submit_button("Save Default Settings"):
            # Here you would save the settings
            st.success("Default settings saved!")
    
    # Maintenance
    st.subheader("Maintenance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear Project Cache", help="Clear cached project data"):
            st.session_state.project_manager.cleanup_cache()
            st.success("Project cache cleared!")
    
    with col2:
        if st.button("Export All Projects", help="Export project list as JSON"):
            projects_json = st.session_state.project_manager.export_project_list("json")
            st.download_button(
                label="Download Projects JSON",
                data=projects_json,
                file_name="contentengine_projects.json",
                mime="application/json"
            )

def render_help():
    """Render the help page"""
    st.markdown('<h1 class="main-header">Help & Documentation</h1>', unsafe_allow_html=True)
    
    # Quick Start Guide
    st.subheader("🚀 Quick Start Guide")
    
    with st.expander("1. Setting Up Your First Project", expanded=True):
        st.markdown("""
        **Step 1:** Click on "➕ New Project" in the sidebar
        
        **Step 2:** Fill in your project details:
        - **Project Name**: Choose a descriptive name
        - **Seed Keywords**: Enter 3-10 keywords related to your topic
        - **Target Audience**: Describe who you're writing for
        - **Configuration**: Choose your location, language, and content generator
        
        **Step 3:** Click "Create Project" to set up the project structure
        """)
    
    with st.expander("2. Running the Content Pipeline"):
        st.markdown("""
        **The ContentEngine pipeline has 5 stages:**
        
        1. **Keyword Research** - Analyzes and clusters your keywords using SERP data
        2. **Content Briefs** - Creates detailed content outlines with competitive analysis
        3. **Article Writing** - Generates full articles (Claude prompts or OpenAI automation)
        4. **Social Media** - Creates platform-specific social media content
        5. **YouTube Scripts** - Generates video scripts with SEO optimization
        
        **You can run stages individually or execute the full pipeline.**
        """)
    
    with st.expander("3. Claude Code vs OpenAI"):
        st.markdown("""
        **Claude Code Integration** (Recommended):
        - ✅ Superior content quality with strategic thinking
        - ✅ Interactive refinement through conversation
        - ✅ Advanced competitive analysis
        - ✅ Platform-specific optimization
        - ⏳ Requires manual copy-paste workflow
        
        **OpenAI Implementation**:
        - ✅ Fully automated pipeline
        - ✅ Fast bulk content generation
        - ✅ Predictable API costs
        - ⚠️ Less strategic, more template-based
        """)
    
    # API Setup
    st.subheader("🔧 API Setup")
    
    st.markdown("""
    **DataForSEO API** (Required for keyword research):
    1. Sign up at [dataforseo.com](https://dataforseo.com/)
    2. Get your login email and API password
    3. Add them in Settings > API Configuration
    
    **OpenAI API** (Required for OpenAI implementation):
    1. Get an API key from [platform.openai.com](https://platform.openai.com/account/api-keys)
    2. Add it in Settings > API Configuration
    
    **Claude Code** (Required for Claude implementation):
    - Ensure you have access to [Claude Code](https://claude.ai/code)
    - No additional API key needed
    """)
    
    # Troubleshooting
    st.subheader("🔍 Troubleshooting")
    
    with st.expander("Common Issues"):
        st.markdown("""
        **"DataForSEO credentials not found"**
        - Make sure you've entered your DataForSEO login and password in Settings
        - Check that your DataForSEO account has API access enabled
        
        **"Script execution failed"**
        - Check that all required dependencies are installed: `pip install -r requirements.txt`
        - Verify your API credentials are correct
        - Check the project logs for specific error details
        
        **"No keywords found"**
        - Try different seed keywords or broader terms
        - Lower the minimum search volume in project settings
        - Increase the maximum competition threshold
        """)
    
    # Contact
    st.subheader("📞 Support")
    st.markdown("""
    **Documentation**: Check the [CLAUDE_INTEGRATION.md](https://github.com/anoopkurup/contentengine) guide for detailed instructions
    
    **Issues**: Report bugs or request features on [GitHub](https://github.com/anoopkurup/contentengine/issues)
    
    **Community**: Join discussions and get help from other users
    """)

# Project view (when a project is selected)
def render_project_view():
    """Render detailed project view with pipeline execution"""
    project = st.session_state.current_project
    
    if not project:
        st.error("No project selected")
        return
    
    # Project header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f'<h1 class="main-header">{project.name}</h1>', unsafe_allow_html=True)
        if project.description:
            st.write(project.description)
    
    with col2:
        completion = project.get_completion_percentage()
        st.metric("Completion", f"{completion:.0f}%")
        st.progress(completion / 100)
        
        if st.button("← Back to Projects"):
            st.session_state.current_project = None
            st.rerun()
    
    # Project details tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Pipeline", "Content", "Settings", "Export"])
    
    with tab1:
        render_pipeline_tab(project)
    
    with tab2:
        render_content_tab(project)
    
    with tab3:
        render_project_settings_tab(project)
    
    with tab4:
        render_export_tab(project)

def render_pipeline_tab(project):
    """Render the pipeline execution tab"""
    st.subheader("Content Pipeline")
    
    # Pipeline status overview
    stages = ["keyword_research", "content_briefs", "article_writing", "social_media", "youtube_scripts"]
    stage_names = ["Keyword Research", "Content Briefs", "Article Writing", "Social Media", "YouTube Scripts"]
    
    # Pipeline progress bar
    completed_stages = sum(1 for stage in stages 
                          if project.execution_status.get(stage, {}).get("status") == "completed")
    progress = completed_stages / len(stages)
    
    st.progress(progress, f"Pipeline Progress: {completed_stages}/{len(stages)} stages completed")
    
    # Stage execution
    for i, (stage, name) in enumerate(zip(stages, stage_names)):
        with st.expander(f"{i+1}. {name}", expanded=True):
            status_info = project.execution_status.get(stage, {})
            status = status_info.get("status", "pending")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Status:** {status.title()}")
                if status_info.get("completed_at"):
                    st.write(f"**Completed:** {status_info['completed_at'][:19]}")
                if status_info.get("error"):
                    st.error(f"Error: {status_info['error']}")
            
            with col2:
                # Check if stage can be executed
                can_execute, reason = st.session_state.pipeline_executor.can_execute_stage(project, stage)
                
                if can_execute and status != "running":
                    if st.button(f"Run {name}", key=f"run_{stage}"):
                        execute_stage(project, stage)
                else:
                    if status == "running":
                        st.info("Running...")
                    else:
                        st.warning(f"Cannot run: {reason}")
            
            with col3:
                # Show outputs if available
                outputs = project.get_stage_files(stage)
                if outputs:
                    st.write(f"**Outputs:** {len(outputs)} files")
                    if st.button(f"View Files", key=f"view_{stage}"):
                        st.session_state.selected_stage = stage
                        st.rerun()
    
    # Bulk actions
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Run Full Pipeline", type="primary"):
            execute_full_pipeline(project)
    
    with col2:
        if st.button("🔄 Restart from Stage"):
            stage_options = dict(zip(stage_names, stages))
            start_stage = st.selectbox("Start from:", stage_options.keys())
            if st.button("Start"):
                execute_full_pipeline(project, stage_options[start_stage])
    
    with col3:
        if st.button("🧹 Clear All Progress"):
            if st.button("Confirm Clear", type="secondary"):
                clear_project_progress(project)

def render_content_tab(project):
    """Render the content management tab"""
    st.subheader("Generated Content")
    
    # Content overview
    total_files = sum(len(files) for files in project.output_files.values())
    st.write(f"**Total Files Generated:** {total_files}")
    
    if total_files == 0:
        st.info("No content generated yet. Run the pipeline to create content.")
        return
    
    # Content by stage
    stages = ["keyword_research", "content_briefs", "articles", "social_media", "youtube"]
    stage_names = ["Keyword Research", "Content Briefs", "Articles", "Social Media", "YouTube"]
    
    for stage, name in zip(stages, stage_names):
        files = project.get_stage_files(stage)
        
        if files:
            with st.expander(f"{name} ({len(files)} files)"):
                for file_path in files:
                    file_name = Path(file_path).name
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"📄 {file_name}")
                    
                    with col2:
                        # File info
                        try:
                            file_size = Path(file_path).stat().st_size
                            st.write(f"{file_size // 1024} KB")
                        except:
                            st.write("N/A")
                    
                    with col3:
                        if st.button("View", key=f"view_file_{file_name}"):
                            view_content_file(file_path)

def render_project_settings_tab(project):
    """Render project settings tab"""
    st.subheader("Project Settings")
    
    # Basic info (editable)
    with st.form("project_info"):
        new_name = st.text_input("Project Name", value=project.name)
        new_description = st.text_area("Description", value=project.description)
        
        if st.form_submit_button("Update Info"):
            project.name = new_name
            project.description = new_description
            project.save_config()
            st.success("Project info updated!")
            st.rerun()
    
    # Keywords management
    st.subheader("Keywords")
    current_keywords = project.input_data.get("seed_keywords", [])
    
    with st.form("keywords_form"):
        from backend.utils.file_utils import ContentFileManager
        keywords_text = ContentFileManager.format_keywords_for_display(current_keywords)
        new_keywords_text = st.text_area("Seed Keywords", value=keywords_text)
        
        if st.form_submit_button("Update Keywords"):
            new_keywords = ContentFileManager.parse_keywords_from_text(new_keywords_text)
            project.input_data["seed_keywords"] = new_keywords
            project.save_inputs()
            st.success("Keywords updated!")
            st.rerun()
    
    # Configuration
    st.subheader("Configuration")
    
    with st.form("config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_location = st.selectbox(
                "Target Location",
                ["India", "United States", "United Kingdom", "Canada", "Australia"],
                index=["India", "United States", "United Kingdom", "Canada", "Australia"].index(
                    project.config.get("target_location", "India")
                )
            )
            
            new_generator = st.selectbox(
                "Content Generator",
                ["claude", "openai"],
                index=["claude", "openai"].index(project.config.get("content_generator", "claude"))
            )
        
        with col2:
            new_language = st.selectbox(
                "Language",
                ["en", "hi", "es", "fr", "de"],
                index=["en", "hi", "es", "fr", "de"].index(
                    project.config.get("target_language", "en")
                )
            )
            
            new_min_volume = st.number_input(
                "Min Search Volume",
                value=project.config.get("min_search_volume", 100)
            )
        
        if st.form_submit_button("Update Configuration"):
            project.config.update({
                "target_location": new_location,
                "target_language": new_language,
                "content_generator": new_generator,
                "min_search_volume": new_min_volume
            })
            project.save_config()
            st.success("Configuration updated!")
            st.rerun()

def render_export_tab(project):
    """Render export tab"""
    st.subheader("Export Content")
    
    # Export options
    export_formats = ["ZIP Archive", "JSON Package", "Individual Files"]
    selected_format = st.selectbox("Export Format", export_formats)
    
    # Include options
    st.write("Include:")
    include_inputs = st.checkbox("Input files", value=True)
    include_outputs = st.checkbox("Generated content", value=True)
    include_config = st.checkbox("Configuration", value=True)
    
    if st.button("Generate Export", type="primary"):
        generate_project_export(project, selected_format, include_inputs, include_outputs, include_config)

# Helper functions for actions
def execute_stage(project, stage):
    """Execute a single pipeline stage"""
    with st.spinner(f"Executing {stage}..."):
        result = st.session_state.pipeline_executor.execute_stage(project, stage)
        
        if result["success"]:
            st.success(f"Stage {stage} completed successfully!")
            st.rerun()
        else:
            st.error(f"Stage execution failed: {result['message']}")

def execute_full_pipeline(project, start_stage=None):
    """Execute the full content pipeline"""
    with st.spinner("Executing pipeline..."):
        result = st.session_state.pipeline_executor.execute_full_pipeline(
            project, start_stage=start_stage
        )
        
        if result["success"]:
            st.success("Pipeline completed successfully!")
            st.balloons()
        else:
            st.error("Pipeline execution failed. Check individual stages for details.")
        
        st.rerun()

def view_content_file(file_path):
    """Display content file in modal or expander"""
    try:
        if file_path.endswith('.json'):
            from backend.utils.file_utils import FileManager
            content = FileManager.read_json_file(file_path)
            st.json(content)
        else:
            from backend.utils.file_utils import FileManager
            content = FileManager.read_text_file(file_path)
            st.code(content, language='markdown')
    except Exception as e:
        st.error(f"Error reading file: {e}")

def generate_project_export(project, format_type, include_inputs, include_outputs, include_config):
    """Generate and offer project export"""
    # Implementation would depend on the selected format
    st.info(f"Generating {format_type} export...")
    # This would create the actual export file and offer it for download

# Main app logic
def main():
    # Handle project view
    if st.session_state.current_project:
        render_project_view()
        return
    
    # Handle page routing
    if current_page == "dashboard":
        render_dashboard()
    elif current_page == "new_project":
        render_new_project()
    elif current_page == "projects":
        render_projects()
    elif current_page == "settings":
        render_settings()
    elif current_page == "help":
        render_help()

if __name__ == "__main__":
    main()