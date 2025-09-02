import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import io
import uuid

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from core.project_manager import ProjectManager
from config.app_config import AppConfig

def validate_keywords(keywords_text):
    """Validate and clean keyword input"""
    if not keywords_text.strip():
        return []
    
    keywords = [kw.strip() for kw in keywords_text.split('\n') if kw.strip()]
    return keywords

def process_csv_keywords(uploaded_file):
    """Process uploaded CSV file for keywords"""
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        
        # Look for keyword column (flexible naming)
        keyword_cols = [col for col in df.columns.str.lower() 
                       if any(term in col for term in ['keyword', 'query', 'term'])]
        
        if not keyword_cols:
            st.error("No keyword column found. Please ensure your CSV has a 'keyword' column.")
            return []
        
        # Use the first keyword column found
        keyword_col = keyword_cols[0]
        keywords = df[keyword_col].dropna().tolist()
        
        st.success(f"✅ Loaded {len(keywords)} keywords from CSV")
        return [str(kw).strip() for kw in keywords if str(kw).strip()]
        
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return []

def show_project_wizard():
    """Display the project creation wizard"""
    st.title("➕ Create New Project")
    st.markdown("Follow these steps to set up your content creation project")
    
    # Initialize session state for wizard
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1
    if 'wizard_data' not in st.session_state:
        st.session_state.wizard_data = {}
    
    # Progress indicator
    progress = st.session_state.wizard_step / 4
    st.progress(progress)
    st.write(f"Step {st.session_state.wizard_step} of 4")
    
    # Step 1: Project Details
    if st.session_state.wizard_step == 1:
        show_step_1_project_details()
    
    # Step 2: Keywords
    elif st.session_state.wizard_step == 2:
        show_step_2_keywords()
    
    # Step 3: Configuration
    elif st.session_state.wizard_step == 3:
        show_step_3_configuration()
    
    # Step 4: Review and Create
    elif st.session_state.wizard_step == 4:
        show_step_4_review()

def show_step_1_project_details():
    """Step 1: Basic project information"""
    st.subheader("📝 Project Information")
    
    # Project name
    project_name = st.text_input(
        "Project Name *", 
        value=st.session_state.wizard_data.get('project_name', ''),
        placeholder="e.g., Digital Marketing Tips Blog",
        help="Choose a descriptive name for your content project"
    )
    
    # Project description
    project_description = st.text_area(
        "Project Description",
        value=st.session_state.wizard_data.get('project_description', ''),
        placeholder="Brief description of your content goals and target audience...",
        help="Optional: Describe what type of content you want to create"
    )
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    
    with col2:
        if st.button("Next ➡️", type="primary", disabled=not project_name.strip()):
            st.session_state.wizard_data['project_name'] = project_name.strip()
            st.session_state.wizard_data['project_description'] = project_description.strip()
            st.session_state.wizard_step = 2
            st.rerun()
    
    if not project_name.strip():
        st.warning("Please enter a project name to continue")

def show_step_2_keywords():
    """Step 2: Keywords input"""
    st.subheader("🔍 Target Keywords")
    st.markdown("Add the keywords you want to target for content creation")
    
    # Keyword input method selection
    input_method = st.radio(
        "Choose how to add keywords:",
        ["Manual Entry", "CSV Upload", "Seed Keywords"],
        horizontal=True
    )
    
    keywords = []
    
    if input_method == "Manual Entry":
        keywords_text = st.text_area(
            "Enter Keywords (one per line)",
            value=st.session_state.wizard_data.get('keywords_text', ''),
            placeholder="digital marketing\nseo tips\ncontent strategy\nsocial media marketing",
            height=150,
            help="Enter each keyword on a separate line"
        )
        keywords = validate_keywords(keywords_text)
        if keywords_text:
            st.session_state.wizard_data['keywords_text'] = keywords_text
    
    elif input_method == "CSV Upload":
        uploaded_file = st.file_uploader(
            "Upload CSV file with keywords",
            type=['csv'],
            help="CSV should have a column named 'keyword' or similar"
        )
        
        if uploaded_file:
            keywords = process_csv_keywords(uploaded_file)
            # Store keywords as text for consistency
            st.session_state.wizard_data['keywords_text'] = '\n'.join(keywords)
    
    elif input_method == "Seed Keywords":
        seed_keywords = st.text_input(
            "Enter 2-3 seed keywords (comma separated)",
            value=st.session_state.wizard_data.get('seed_keywords', ''),
            placeholder="digital marketing, SEO, content creation",
            help="We'll expand these into related keywords automatically"
        )
        
        if seed_keywords:
            st.session_state.wizard_data['seed_keywords'] = seed_keywords
            # For now, just split the seed keywords
            keywords = [kw.strip() for kw in seed_keywords.split(',') if kw.strip()]
            st.info(f"✨ Will expand {len(keywords)} seed keywords during keyword research")
    
    # Show keyword preview
    if keywords:
        st.markdown("**Keywords Preview:**")
        if len(keywords) <= 10:
            for i, keyword in enumerate(keywords, 1):
                st.write(f"{i}. {keyword}")
        else:
            for i, keyword in enumerate(keywords[:10], 1):
                st.write(f"{i}. {keyword}")
            st.write(f"... and {len(keywords) - 10} more keywords")
        
        st.success(f"✅ {len(keywords)} keywords ready")
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.wizard_step = 1
            st.rerun()
    
    with col2:
        can_continue = len(keywords) > 0
        if st.button("Next ➡️", type="primary", disabled=not can_continue):
            st.session_state.wizard_data['keywords'] = keywords
            st.session_state.wizard_step = 3
            st.rerun()
    
    if not keywords:
        st.warning("Please add at least one keyword to continue")

def show_step_3_configuration():
    """Step 3: Project configuration"""
    st.subheader("⚙️ Project Configuration")
    st.markdown("Customize your project settings for optimal content generation")
    
    # SEO Settings
    st.markdown("#### 🎯 SEO Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        target_location = st.selectbox(
            "Target Location",
            ["India", "United States", "United Kingdom", "Canada", "Australia", "Germany", "France", "Spain"],
            index=0,
            help="Geographic target for keyword research and content"
        )
        
        target_language = st.selectbox(
            "Target Language",
            ["en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh"],
            format_func=lambda x: {"en": "English", "es": "Spanish", "fr": "French", 
                                  "de": "German", "it": "Italian", "pt": "Portuguese",
                                  "ja": "Japanese", "ko": "Korean", "zh": "Chinese"}[x],
            help="Language for content generation"
        )
    
    with col2:
        min_search_volume = st.number_input(
            "Minimum Search Volume",
            min_value=0,
            max_value=10000,
            value=100,
            step=50,
            help="Minimum monthly search volume for keywords"
        )
        
        max_competition = st.slider(
            "Maximum Competition Level",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Maximum competition level (0 = low, 1 = high)"
        )
    
    # Content Generation Settings
    st.markdown("#### 🤖 Content Generation")
    col3, col4 = st.columns(2)
    
    with col3:
        content_generator = st.selectbox(
            "Content Generator",
            ["claude", "openai"],
            format_func=lambda x: "Claude (Recommended)" if x == "claude" else "OpenAI GPT",
            help="AI model for content generation"
        )
    
    with col4:
        if content_generator == "claude":
            claude_preference = st.selectbox(
                "Claude Model Preference", 
                ["quality", "speed"],
                format_func=lambda x: "Quality (Sonnet)" if x == "quality" else "Speed (Haiku)",
                help="Balance between content quality and generation speed"
            )
        else:
            claude_preference = "quality"
    
    # Advanced Settings
    with st.expander("🔧 Advanced Settings"):
        serp_overlap = st.slider(
            "SERP Overlap Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Minimum overlap threshold for SERP analysis"
        )
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.wizard_step = 2
            st.rerun()
    
    with col2:
        if st.button("Review ➡️", type="primary"):
            # Store configuration
            st.session_state.wizard_data.update({
                'target_location': target_location,
                'target_language': target_language,
                'min_search_volume': min_search_volume,
                'max_competition': max_competition,
                'content_generator': content_generator,
                'claude_preference': claude_preference,
                'serp_overlap': serp_overlap
            })
            st.session_state.wizard_step = 4
            st.rerun()

def show_step_4_review():
    """Step 4: Review and create project"""
    st.subheader("📋 Review Project Details")
    st.markdown("Please review your project configuration before creating")
    
    data = st.session_state.wizard_data
    
    # Project Summary
    st.markdown("#### 📝 Project Information")
    st.write(f"**Name:** {data['project_name']}")
    if data.get('project_description'):
        st.write(f"**Description:** {data['project_description']}")
    
    # Keywords Summary
    st.markdown("#### 🔍 Keywords")
    keywords = data.get('keywords', [])
    st.write(f"**Total Keywords:** {len(keywords)}")
    if keywords:
        if len(keywords) <= 5:
            st.write("**Keywords:** " + ", ".join(keywords))
        else:
            st.write("**Keywords:** " + ", ".join(keywords[:5]) + f", ... ({len(keywords) - 5} more)")
    
    # Configuration Summary
    st.markdown("#### ⚙️ Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Target Location:** {data.get('target_location', 'India')}")
        st.write(f"**Language:** {data.get('target_language', 'en')}")
        st.write(f"**Content Generator:** {data.get('content_generator', 'claude').title()}")
    
    with col2:
        st.write(f"**Min Search Volume:** {data.get('min_search_volume', 100)}")
        st.write(f"**Max Competition:** {data.get('max_competition', 0.3)}")
        if data.get('content_generator') == 'claude':
            st.write(f"**Claude Model:** {data.get('claude_preference', 'quality').title()}")
    
    # Create project
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.wizard_step = 3
            st.rerun()
    
    with col2:
        if st.button("🚀 Create Project", type="primary"):
            create_project()

def create_project():
    """Create the project with all configured settings"""
    try:
        data = st.session_state.wizard_data
        
        # Initialize project manager
        project_manager = ProjectManager()
        
        # Generate project ID
        project_id = str(uuid.uuid4())[:8]
        
        # Create project configuration (only config overrides)
        config_overrides = {
            'target_location': data.get('target_location', 'India'),
            'target_language': data.get('target_language', 'en'),
            'content_generator': data.get('content_generator', 'claude'),
            'claude_model_preference': data.get('claude_preference', 'quality'),
            'min_search_volume': data.get('min_search_volume', 100),
            'max_competition': data.get('max_competition', 0.3),
            'serp_overlap_threshold': data.get('serp_overlap', 0.3)
        }
        
        # Create project
        project = project_manager.create_project(
            name=data['project_name'],
            description=data.get('project_description', ''),
            seed_keywords=data.get('keywords', []),
            config_overrides=config_overrides
        )
        
        st.success(f"✅ Project '{data['project_name']}' created successfully!")
        st.balloons()
        
        # Clear wizard data
        st.session_state.wizard_data = {}
        st.session_state.wizard_step = 1
        
        # Show next steps
        st.markdown("### 🎉 Project Created!")
        st.markdown("**What's next?**")
        st.markdown("- Go to **🚀 Pipeline** to start generating content")
        st.markdown("- Check **📁 Content Manager** to view generated files")
        st.markdown("- Visit **⚙️ Settings** to modify project configuration")
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏠 Dashboard"):
                st.switch_page("app.py")
        
        with col2:
            if st.button("🚀 Start Pipeline"):
                st.switch_page("pages/pipeline_runner.py")
        
        with col3:
            if st.button("➕ New Project"):
                st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error creating project: {e}")
        st.exception(e)

def main():
    """Main project wizard interface"""
    st.set_page_config(
        page_title="ContentEngine - Project Wizard",
        page_icon="➕",
        layout="wide"
    )
    
    # Check if project manager is available
    try:
        project_manager = ProjectManager()
        show_project_wizard()
    except Exception as e:
        st.error("⚠️ Unable to initialize project manager")
        st.error(f"Error: {e}")
        st.info("Please ensure the backend is properly configured.")

if __name__ == "__main__":
    main()