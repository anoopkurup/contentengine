import streamlit as st
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import sys

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from core.project_manager import ProjectManager
from utils.file_utils import ContentFileManager

def init_content_manager():
    """Initialize the content manager"""
    if 'content_manager' not in st.session_state:
        st.session_state.content_manager = ContentFileManager()
    return st.session_state.content_manager

def show_project_content(project_manager: ProjectManager, project_id: str):
    """Display content for a specific project"""
    project = project_manager.load_project(project_id)
    if not project:
        st.error("Project not found")
        return
    
    project_dir = Path(project.project_path)
    
    st.subheader(f"📁 Content for: {project.name}")
    
    # Content categories with actual file paths
    categories = {
        "🔍 Keyword Research": "stage_01_keyword_research/keyword_clusters.csv",
        "📄 Content Brief": "stage_02_content_briefs/article_brief.md", 
        "📝 Article": "stage_03_articles/article_draft.md",
        "📱 Social Media": "stage_04_social_media/social_posts.md",
        "🎥 YouTube Script": "stage_05_youtube/youtube_script.md"
    }
    
    # Create tabs for different content types
    tabs = st.tabs(list(categories.keys()))
    
    for i, (category, filename) in enumerate(categories.items()):
        with tabs[i]:
            file_path = project_dir / filename
            
            if file_path.exists():
                if filename.endswith('.csv'):
                    show_csv_content(file_path, category)
                elif filename.endswith('.md'):
                    show_markdown_content(file_path, category)
                else:
                    show_text_content(file_path, category)
            else:
                st.info(f"No {category.lower()} content generated yet")
                
                # Show generation button if content doesn't exist
                if st.button(f"Generate {category}", key=f"generate_{i}"):
                    st.info(f"Content generation for {category} would be triggered here")

def show_csv_content(file_path: Path, category: str):
    """Display CSV content"""
    try:
        df = pd.read_csv(file_path)
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv_data = df.to_csv(index=False)
        st.download_button(
            label=f"📥 Download {category} CSV",
            data=csv_data,
            file_name=file_path.name,
            mime="text/csv"
        )
        
        # Basic statistics for keyword research
        if 'Search Volume' in df.columns:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Keywords", len(df))
            with col2:
                st.metric("Avg Search Volume", f"{df['Search Volume'].mean():.0f}")
            with col3:
                st.metric("Max Search Volume", f"{df['Search Volume'].max():.0f}")
            with col4:
                total_volume = df['Search Volume'].sum()
                st.metric("Total Volume", f"{total_volume:,}")
            
            # Show cluster summary if available
            cluster_summary_path = project_dir / "stage_01_keyword_research" / "cluster_summary.csv"
            if cluster_summary_path.exists():
                st.subheader("📊 Keyword Clusters Summary")
                try:
                    cluster_df = pd.read_csv(cluster_summary_path)
                    st.dataframe(cluster_df, use_container_width=True)
                    
                    # Show cluster metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Clusters", len(cluster_df))
                    with col2:
                        if 'Total Search Volume' in cluster_df.columns:
                            total_cluster_volume = cluster_df['Total Search Volume'].sum()
                            st.metric("Total Cluster Volume", f"{total_cluster_volume:,}")
                except Exception as e:
                    st.error(f"Error reading cluster summary: {e}")
            
            # Keyword selection for next stages
            st.subheader("🎯 Select Keywords for Content Creation")
            st.info("Select the keywords you want to use for article brief and content generation.")
            
            # Allow user to select keywords from the research results
            selected_keywords = []
            
            # Group keywords by cluster for easier selection
            if 'Cluster' in df.columns:
                clusters = df['Cluster'].unique()
                for cluster_name in clusters[:5]:  # Show top 5 clusters
                    cluster_keywords = df[df['Cluster'] == cluster_name]
                    with st.expander(f"📋 {cluster_name} ({len(cluster_keywords)} keywords)"):
                        # Show pillar keyword first
                        pillar_keywords = cluster_keywords[cluster_keywords['Role'] == 'Pillar Post']
                        if not pillar_keywords.empty:
                            pillar_kw = pillar_keywords.iloc[0]['Keyword']
                            if st.checkbox(f"🎯 **{pillar_kw}** (Pillar)", key=f"pillar_{cluster_name}", value=True):
                                selected_keywords.append(pillar_kw)
                        
                        # Show cluster keywords
                        cluster_posts = cluster_keywords[cluster_keywords['Role'] == 'Cluster Post']
                        for _, row in cluster_posts.head(3).iterrows():  # Top 3 cluster keywords
                            if st.checkbox(f"• {row['Keyword']} ({row['Search Volume']} searches)", 
                                         key=f"cluster_{row['Keyword']}"):
                                selected_keywords.append(row['Keyword'])
            
            if selected_keywords:
                st.success(f"✅ Selected {len(selected_keywords)} keywords for content creation")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("💾 Save Selection", type="primary"):
                        # Save selected keywords to project
                        selection_file = project_dir / "stage_01_keyword_research" / "selected_keywords.json"
                        try:
                            with open(selection_file, 'w') as f:
                                json.dump({
                                    "selected_keywords": selected_keywords,
                                    "selection_date": datetime.now().isoformat(),
                                    "total_keywords": len(selected_keywords)
                                }, f, indent=2)
                            st.success("Keywords saved successfully! You can now proceed to generate content briefs.")
                        except Exception as e:
                            st.error(f"Error saving selection: {e}")
                
                with col2:
                    # Show selected keywords as downloadable list
                    keywords_text = "\n".join(selected_keywords)
                    st.download_button(
                        "📥 Download Selected Keywords",
                        data=keywords_text,
                        file_name="selected_keywords.txt",
                        mime="text/plain"
                    )
            else:
                st.info("👆 Select keywords above to proceed with content creation")
                
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

def show_markdown_content(file_path: Path, category: str):
    """Display markdown content"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Show preview/edit toggle
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{category}** - *Last modified: {datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}*")
        with col2:
            edit_mode = st.toggle("Edit Mode", key=f"edit_{file_path.name}")
        
        if edit_mode:
            # Edit mode
            edited_content = st.text_area(
                "Content", 
                value=content, 
                height=400,
                key=f"editor_{file_path.name}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Changes", key=f"save_{file_path.name}"):
                    try:
                        file_path.write_text(edited_content, encoding='utf-8')
                        st.success("Content saved successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving content: {e}")
            
            with col2:
                if st.button("🔄 Reset", key=f"reset_{file_path.name}"):
                    st.rerun()
        else:
            # Preview mode
            st.markdown(content)
        
        # Download button
        st.download_button(
            label=f"📥 Download {category}",
            data=content,
            file_name=file_path.name,
            mime="text/markdown"
        )
        
        # Word count and reading time
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)  # Assume 200 words per minute
        
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"📊 {word_count} words")
        with col2:
            st.caption(f"⏱️ ~{reading_time} min read")
            
    except Exception as e:
        st.error(f"Error reading file: {e}")

def show_text_content(file_path: Path, category: str):
    """Display text content"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        st.markdown(f"**{category}**")
        st.text_area("Content", content, height=300, disabled=True)
        
        # Download button
        st.download_button(
            label=f"📥 Download {category}",
            data=content,
            file_name=file_path.name,
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"Error reading file: {e}")

def show_content_overview(project_manager: ProjectManager):
    """Show overview of all projects and their content"""
    projects = project_manager.list_projects()
    
    if not projects:
        st.info("No projects found. Create a project first!")
        return
    
    st.subheader("📊 Content Overview")
    
    # Create overview table
    overview_data = []
    
    for project in projects:
        project_dir = Path(project.project_path)
        
        # Count content files using actual stage directories
        content_status = {
            "Project": project.name,
            "Created": project.created_date.strftime("%Y-%m-%d"),
            "Keywords": "✅" if (project_dir / "stage_01_keyword_research" / "keyword_clusters.csv").exists() else "❌",
            "Brief": "✅" if (project_dir / "stage_02_content_briefs" / "article_brief.md").exists() else "❌",
            "Article": "✅" if (project_dir / "stage_03_articles" / "article_draft.md").exists() else "❌", 
            "Social Media": "✅" if (project_dir / "stage_04_social_media" / "social_posts.md").exists() else "❌",
            "YouTube": "✅" if (project_dir / "stage_05_youtube" / "youtube_script.md").exists() else "❌",
            "Progress": f"{project.get_progress_percentage():.0f}%"
        }
        overview_data.append(content_status)
    
    if overview_data:
        df = pd.DataFrame(overview_data)
        st.dataframe(df, use_container_width=True)
        
        # Export overview
        if st.button("📥 Export Overview"):
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Download Overview CSV",
                data=csv_data,
                file_name=f"content_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

def main():
    """Main content manager interface"""
    st.set_page_config(
        page_title="ContentEngine - Content Manager",
        page_icon="📁",
        layout="wide"
    )
    
    st.title("📁 Content Manager")
    st.markdown("View, edit, and manage your generated content")
    
    # Initialize managers
    project_manager = ProjectManager()
    content_manager = init_content_manager()
    
    # Sidebar for project selection
    with st.sidebar:
        st.header("Select Project")
        
        projects = project_manager.list_projects()
        if not projects:
            st.info("No projects found")
            if st.button("➕ Create New Project"):
                st.switch_page("pages/project_wizard.py")
            return
        
        project_options = {}
        for project in projects:
            project_options[f"{project.name} ({project.project_id})"] = project.project_id
        
        if project_options:
            selected_project_key = st.selectbox(
                "Choose a project:",
                list(project_options.keys())
            )
            selected_project_id = project_options[selected_project_key]
        else:
            st.error("No valid projects found")
            return
    
    # Main content area
    if selected_project_id:
        # Tabs for different views
        tab1, tab2 = st.tabs(["📄 Project Content", "📊 Overview"])
        
        with tab1:
            show_project_content(project_manager, selected_project_id)
        
        with tab2:
            show_content_overview(project_manager)
    
    # Quick actions in sidebar
    with st.sidebar:
        st.markdown("---")
        st.header("Quick Actions")
        
        if st.button("🏠 Back to Dashboard"):
            st.switch_page("app.py")
        
        if st.button("➕ New Project"):
            st.switch_page("pages/project_wizard.py")
        
        if st.button("⚙️ Project Settings"):
            st.switch_page("pages/project_settings.py")

if __name__ == "__main__":
    main()