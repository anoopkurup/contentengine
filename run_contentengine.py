#!/usr/bin/env python3
"""
ContentEngine Startup Script
Launch the Streamlit frontend application for ContentEngine.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def install_requirements():
    """Install required packages"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    # Check if packages are already available
    try:
        import streamlit
        import pandas
        import requests
        print("✅ Required packages already available")
        return True
    except ImportError:
        pass
        
    try:
        print("📦 Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                      check=True, capture_output=True, text=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        print("💡 Try running in virtual environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("   pip install -r requirements.txt")
        print("   python run_contentengine.py")
        return False

def check_environment_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("⚠️  .env file not found. Creating template...")
        create_env_template()
        return False
    
    required_vars = ['DATAFORSEO_LOGIN', 'DATAFORSEO_PASSWORD']
    optional_vars = ['OPENAI_API_KEY', 'TARGET_LOCATION', 'TARGET_LANGUAGE']
    
    env_content = env_file.read_text()
    missing_required = []
    
    for var in required_vars:
        if f"{var}=" not in env_content or f"{var}=" in env_content and not env_content.split(f"{var}=")[1].split('\n')[0].strip():
            missing_required.append(var)
    
    if missing_required:
        print(f"⚠️  Missing required environment variables: {', '.join(missing_required)}")
        print("Please update your .env file with the required API credentials.")
        return False
    
    return True

def create_env_template():
    """Create .env template file"""
    env_template = """# ContentEngine Environment Variables

# DataForSEO API Credentials (Required)
DATAFORSEO_LOGIN=your_dataforseo_login
DATAFORSEO_PASSWORD=your_dataforseo_password

# OpenAI API Key (Optional - only if using OpenAI content generation)
OPENAI_API_KEY=your_openai_api_key

# Default Settings (Optional)
TARGET_LOCATION=India
TARGET_LANGUAGE=en
CONTENT_GENERATOR=claude
CLAUDE_MODEL_PREFERENCE=quality
SERP_OVERLAP_THRESHOLD=0.3
MIN_SEARCH_VOLUME=100
MAX_COMPETITION=0.3

# Application Settings (Optional)
DEBUG=False
LOG_LEVEL=INFO
"""
    
    env_file = Path(__file__).parent / ".env"
    env_file.write_text(env_template)
    print(f"✅ Created .env template at {env_file}")
    print("Please edit the .env file with your actual API credentials.")

def create_required_directories():
    """Create required directories if they don't exist"""
    base_dir = Path(__file__).parent
    directories = [
        base_dir / "projects",
        base_dir / "backend" / "scripts",
    ]
    
    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")

def launch_streamlit():
    """Launch the Streamlit application"""
    frontend_dir = Path(__file__).parent / "frontend"
    app_file = frontend_dir / "app.py"
    
    if not app_file.exists():
        print(f"❌ Streamlit app not found at {app_file}")
        return False
    
    try:
        print("🚀 Launching ContentEngine...")
        print("🌐 Opening http://localhost:8501 in your browser...")
        
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=localhost", 
            "--browser.gatherUsageStats=false",
            "--server.headless=true"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 ContentEngine stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch Streamlit: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🎯 ContentEngine Startup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check virtual environment
    if not check_virtual_environment():
        print("⚠️  Not running in virtual environment. Consider using: python -m venv venv && source venv/bin/activate")
    
    # Install requirements
    if not install_requirements():
        print("❌ Could not install requirements. Please run in virtual environment:")
        print("   source venv/bin/activate && python run_contentengine.py")
        sys.exit(1)
    
    # Check environment file
    if not check_environment_file():
        response = input("Continue with incomplete environment setup? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create required directories
    create_required_directories()
    
    print("=" * 50)
    print("✅ All checks passed!")
    print("🚀 Starting ContentEngine frontend...")
    print("=" * 50)
    
    # Launch application
    launch_streamlit()

if __name__ == "__main__":
    main()