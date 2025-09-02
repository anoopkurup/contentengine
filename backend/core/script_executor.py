import os
import sys
import subprocess
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from models.project import ContentProject

class ScriptExecutor:
    """
    Executes ContentEngine scripts with project integration.
    Handles real script execution instead of simulation.
    """
    
    def __init__(self, scripts_dir: str = "scripts"):
        self.scripts_dir = Path(scripts_dir)
        self.base_dir = Path(__file__).parent.parent.parent
        
    def execute_keyword_research(self, project: ContentProject, 
                                progress_callback: Optional[Callable] = None) -> bool:
        """Execute keyword research for a project"""
        try:
            if progress_callback:
                progress_callback(10, "Setting up keyword research...")
            
            # Get project configuration
            project_dir = Path(project.project_path)
            output_dir = project_dir / "stage_01_keyword_research"
            output_dir.mkdir(exist_ok=True)
            
            # Read seed keywords from project
            seed_keywords = project.input_data.get("seed_keywords", [])
            if not seed_keywords:
                raise ValueError("No seed keywords found in project")
            
            if progress_callback:
                progress_callback(20, f"Processing {len(seed_keywords)} seed keywords...")
            
            # Setup environment variables for the script
            env = os.environ.copy()
            env.update({
                "TARGET_LOCATION": project.config.get("target_location", "India"),
                "TARGET_LANGUAGE": project.config.get("target_language", "en"),
                "KEYWORD_CLUSTERS_FILE": str(output_dir / "keyword_clusters.csv"),
                "CLUSTER_SUMMARY_FILE": str(output_dir / "cluster_summary.csv"),
                "SERP_OVERLAP_THRESHOLD": str(project.config.get("serp_overlap_threshold", "0.3")),
                "MIN_SEARCH_VOLUME": str(project.config.get("min_search_volume", "100")),
                "MAX_COMPETITION": str(project.config.get("max_competition", "0.3"))
            })
            
            if progress_callback:
                progress_callback(30, "Creating modified script for project...")
            
            # Create a modified version of the script with project-specific keywords
            script_content = self._create_keyword_research_script(project, seed_keywords, output_dir)
            temp_script = output_dir / "keyword_research_temp.py"
            
            with open(temp_script, 'w') as f:
                f.write(script_content)
            
            if progress_callback:
                progress_callback(40, "Executing keyword research script...")
            
            # Execute the script
            result = subprocess.run([
                sys.executable, str(temp_script)
            ], env=env, cwd=str(output_dir), capture_output=True, text=True, timeout=300)
            
            if progress_callback:
                progress_callback(80, "Processing results...")
            
            if result.returncode != 0:
                error_msg = f"Script execution failed: {result.stderr}"
                print(f"Keyword research error: {error_msg}")
                return False
            
            # Verify output files were created
            output_file = output_dir / "keyword_clusters.csv"
            summary_file = output_dir / "cluster_summary.csv"
            
            if not output_file.exists() or not summary_file.exists():
                print(f"Output files not found: {output_file.exists()=}, {summary_file.exists()=}")
                return False
            
            # Update project output files
            project.output_files["keyword_research"] = [
                str(output_file.relative_to(project_dir)),
                str(summary_file.relative_to(project_dir))
            ]
            
            if progress_callback:
                progress_callback(100, "Keyword research completed successfully!")
            
            # Clean up temporary script
            if temp_script.exists():
                temp_script.unlink()
            
            return True
            
        except Exception as e:
            print(f"Error in keyword research execution: {e}")
            if progress_callback:
                progress_callback(-1, f"Error: {e}")
            return False
    
    def _create_keyword_research_script(self, project: ContentProject, 
                                      seed_keywords: List[str], output_dir: Path) -> str:
        """Create a modified version of KeywordResearcher.py with project-specific data"""
        
        # Read the original script
        original_script = self.scripts_dir / "KeywordResearcher.py"
        with open(original_script, 'r') as f:
            script_content = f.read()
        
        # Replace the hardcoded seed keywords with project keywords
        seed_keywords_str = json.dumps(seed_keywords)
        script_content = script_content.replace(
            'SEED_KEYWORDS = ["AI marketing", "AI lead generation", "AI content automation"]',
            f'SEED_KEYWORDS = {seed_keywords_str}'
        )
        
        # Add progress reporting
        progress_script_addition = '''
# Progress reporting for pipeline integration
def report_progress(step, total, message):
    """Report progress for pipeline integration"""
    progress = (step / total) * 100
    print(f"PROGRESS: {progress:.0f}% - {message}")

# Add progress reporting to main execution
'''
        
        # Insert progress reporting
        script_content = script_content.replace(
            '# -------------------------------\n# 2. Get Keyword Ideas',
            progress_script_addition + '\n# -------------------------------\n# 2. Get Keyword Ideas'
        )
        
        # Add progress calls throughout the script
        script_content = script_content.replace(
            'def get_keyword_ideas(seed_keywords):',
            'def get_keyword_ideas(seed_keywords):\n    report_progress(1, 5, "Fetching keyword ideas from DataForSEO...")'
        )
        
        script_content = script_content.replace(
            'def get_serp_data(keywords):',
            'def get_serp_data(keywords):\n    report_progress(2, 5, "Analyzing SERP data...")'
        )
        
        script_content = script_content.replace(
            'def cluster_keywords(keyword_df, serp_df):',
            'def cluster_keywords(keyword_df, serp_df):\n    report_progress(3, 5, "Clustering keywords...")'
        )
        
        # Add progress at the end
        script_content = script_content.replace(
            'print(f"Keyword-level clusters saved to {OUTPUT_FILE}")',
            '''report_progress(5, 5, "Saving results...")
print(f"Keyword-level clusters saved to {OUTPUT_FILE}")'''
        )
        
        return script_content
    
    def execute_article_brief(self, project: ContentProject, 
                            progress_callback: Optional[Callable] = None) -> bool:
        """Execute article brief generation for a project"""
        try:
            if progress_callback:
                progress_callback(10, "Setting up article brief generation...")
            
            # Check if keyword research results exist
            project_dir = Path(project.project_path)
            keyword_file = project_dir / "stage_01_keyword_research" / "keyword_clusters.csv"
            
            if not keyword_file.exists():
                if progress_callback:
                    progress_callback(-1, "Keyword research must be completed first")
                return False
            
            output_dir = project_dir / "stage_02_content_briefs"
            output_dir.mkdir(exist_ok=True)
            
            if progress_callback:
                progress_callback(50, "Generating article brief...")
            
            # For now, create a placeholder brief based on keywords
            # In the future, this would call the actual ArticleBrief_Claude.py script
            brief_content = self._create_article_brief_placeholder(project, keyword_file)
            
            brief_file = output_dir / "article_brief.md"
            with open(brief_file, 'w') as f:
                f.write(brief_content)
            
            project.output_files["content_briefs"] = [
                str(brief_file.relative_to(project_dir))
            ]
            
            if progress_callback:
                progress_callback(100, "Article brief generated successfully!")
            
            return True
            
        except Exception as e:
            print(f"Error in article brief generation: {e}")
            if progress_callback:
                progress_callback(-1, f"Error: {e}")
            return False
    
    def _create_article_brief_placeholder(self, project: ContentProject, keyword_file: Path) -> str:
        """Create a placeholder article brief based on keyword research"""
        try:
            # Read keyword research results
            df = pd.read_csv(keyword_file)
            
            # Get top keywords
            top_keywords = df.nlargest(10, 'Search Volume')['Keyword'].tolist()
            
            brief_content = f"""# Article Brief for {project.name}

## Project Overview
- **Target Location**: {project.config.get('target_location', 'India')}
- **Target Language**: {project.config.get('target_language', 'en')}
- **Content Generator**: {project.config.get('content_generator', 'claude')}

## Keyword Research Summary
Based on the keyword research, we found {len(df)} relevant keywords.

### Top Keywords by Search Volume:
"""
            
            for i, keyword in enumerate(top_keywords, 1):
                keyword_data = df[df['Keyword'] == keyword].iloc[0]
                brief_content += f"{i}. **{keyword}** - {keyword_data['Search Volume']} searches/month (Competition: {keyword_data['Competition']})\n"
            
            brief_content += f"""

## Article Structure Recommendation

### 1. Introduction
- Hook the reader with a compelling opening
- Introduce the main topic: {top_keywords[0] if top_keywords else 'Main Topic'}

### 2. Main Content Sections
"""
            
            for keyword in top_keywords[:5]:
                brief_content += f"- Section about: {keyword}\n"
            
            brief_content += """
### 3. Conclusion
- Summarize key points
- Call to action

## SEO Recommendations
- Primary keyword: """ + (top_keywords[0] if top_keywords else 'N/A') + """
- Target word count: 1500-2000 words
- Include internal and external links
- Optimize meta description and title tag

---
*This brief was generated automatically. Please review and customize as needed.*
"""
            
            return brief_content
            
        except Exception as e:
            return f"# Article Brief Generation Error\n\nError: {e}\n\nPlease run keyword research first."