import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AppConfig:
    """Application configuration management"""
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    PROJECTS_DIR = BASE_DIR / "projects"
    SCRIPTS_DIR = BASE_DIR / "scripts"
    FRONTEND_DIR = BASE_DIR / "frontend"
    
    # API Credentials
    DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
    DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Default Project Settings
    DEFAULT_TARGET_LOCATION = os.getenv("TARGET_LOCATION", "India")
    DEFAULT_TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")
    DEFAULT_CONTENT_GENERATOR = os.getenv("CONTENT_GENERATOR", "claude")
    DEFAULT_CLAUDE_MODEL_PREFERENCE = os.getenv("CLAUDE_MODEL_PREFERENCE", "quality")
    DEFAULT_SERP_OVERLAP_THRESHOLD = float(os.getenv("SERP_OVERLAP_THRESHOLD", "0.3"))
    DEFAULT_MIN_SEARCH_VOLUME = int(os.getenv("MIN_SEARCH_VOLUME", "100"))
    DEFAULT_MAX_COMPETITION = float(os.getenv("MAX_COMPETITION", "0.3"))
    
    # Application Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Streamlit Configuration
    STREAMLIT_THEME = {
        "primaryColor": "#1f77b4",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#262730"
    }
    
    @classmethod
    def validate_setup(cls) -> dict:
        """Validate application setup and return status"""
        issues = []
        
        # Check required directories
        for dir_path in [cls.PROJECTS_DIR, cls.SCRIPTS_DIR]:
            if not dir_path.exists():
                issues.append(f"Directory not found: {dir_path}")
        
        # Check API credentials
        if not cls.DATAFORSEO_LOGIN:
            issues.append("DATAFORSEO_LOGIN not configured")
        if not cls.DATAFORSEO_PASSWORD:
            issues.append("DATAFORSEO_PASSWORD not configured")
        
        # Check script files
        required_scripts = [
            "KeywordResearcher.py",
            "ArticleBrief_Claude.py", 
            "ArticleWriter_Claude.py",
            "SocialMedia_Claude.py",
            "YouTubeScript_Claude.py"
        ]
        
        for script in required_scripts:
            script_path = cls.SCRIPTS_DIR / script
            if not script_path.exists():
                issues.append(f"Required script not found: {script}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    @classmethod
    def get_project_defaults(cls) -> dict:
        """Get default configuration for new projects"""
        return {
            "target_location": cls.DEFAULT_TARGET_LOCATION,
            "target_language": cls.DEFAULT_TARGET_LANGUAGE,
            "content_generator": cls.DEFAULT_CONTENT_GENERATOR,
            "claude_model_preference": cls.DEFAULT_CLAUDE_MODEL_PREFERENCE,
            "serp_overlap_threshold": cls.DEFAULT_SERP_OVERLAP_THRESHOLD,
            "min_search_volume": cls.DEFAULT_MIN_SEARCH_VOLUME,
            "max_competition": cls.DEFAULT_MAX_COMPETITION
        }