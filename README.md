# ContentEngine

**AI-Powered Content Creation Platform with Interactive Pipeline Management**

ContentEngine is a comprehensive Python-based platform that automates the entire content creation workflow—from keyword research to multi-platform content distribution. Built with a modern web interface for seamless project management and real-time pipeline execution.

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.49.1-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### One-Command Launch
```bash
./start.sh
```

This automatically:
- Activates the virtual environment
- Launches the Streamlit web interface
- Opens ContentEngine in your browser at http://localhost:8501

### Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API credentials
streamlit run frontend/app.py
```

## 🏗️ Architecture

ContentEngine features a modern **frontend/backend architecture** with interactive web interface:

```
🎯 Project Creation → 🔍 Keyword Research → 📝 Content Briefs → ✍️ Article Writing → 📱 Social Media → 🎬 YouTube Scripts
```

### 🖥️ Web Interface Components

- **📊 Dashboard**: Project overview and quick actions
- **🧙 Project Wizard**: Step-by-step project creation with configuration
- **🚀 Pipeline Runner**: Execute stages with real-time progress tracking
- **📁 Content Manager**: View, edit, and manage generated content
- **⚙️ Project Settings**: Configure target markets and generation preferences

### 🤖 Content Generation Options

**Claude Integration** (Recommended)
- Superior content quality with strategic thinking
- Interactive keyword selection and content refinement
- Enhanced competitive analysis and content gap identification

**OpenAI Implementation** (Legacy)
- Automated high-volume content generation
- Fully scripted pipeline execution
- Predictable API costs and processing time

## ✨ Key Features

### 🎯 Interactive Project Management
- **Visual Pipeline Runner**: Execute individual stages or complete workflows
- **Real-time Progress Tracking**: Live updates during script execution
- **Project Organization**: Structured file management with stage-based directories
- **Content Preview**: View and edit generated content directly in the interface

### 🔍 Advanced Keyword Research
- **SERP-based Clustering**: DataForSEO-powered keyword analysis with overlap detection
- **Interactive Selection**: Choose specific keywords from research results for content creation
- **Competition Analysis**: Filter by search volume, competition, and market opportunity
- **Export Capabilities**: Download research results in multiple formats

### 📝 Multi-Stage Content Pipeline
- **Content Briefs**: AI-powered outlines with competitive research
- **Article Writing**: SEO-optimized long-form content (1,500-2,500 words)
- **Social Media**: Platform-specific content for LinkedIn, Twitter, Instagram
- **YouTube Scripts**: Professional video content with visual direction

### 🔧 Technical Excellence
- **Environment Management**: Secure API credential handling
- **Error Handling**: Comprehensive validation and user-friendly error messages
- **File Organization**: Automatic organization of outputs by pipeline stage
- **State Management**: Persistent project configuration and execution status

## ⚙️ Configuration

### Required API Credentials

Add to your `.env` file:

```bash
# DataForSEO API (Required for keyword research)
DATAFORSEO_LOGIN=your_dataforseo_login
DATAFORSEO_PASSWORD=your_dataforseo_password

# OpenAI API (Required for OpenAI implementation)
OPENAI_API_KEY=your_openai_api_key
```

### Project Configuration Options

Configure through the web interface or environment variables:

```bash
TARGET_LOCATION=India                # Geographic targeting
TARGET_LANGUAGE=en                   # Content language
SERP_OVERLAP_THRESHOLD=0.3          # Keyword clustering sensitivity
MIN_SEARCH_VOLUME=100               # Minimum search volume filter
MAX_COMPETITION=0.3                 # Maximum competition filter
CONTENT_GENERATOR=claude            # claude or openai
CLAUDE_MODEL_PREFERENCE=quality     # quality or speed
```

## 🎯 Getting Started

### 1. Launch the Platform
```bash
./start.sh
```

### 2. Create Your First Project
1. Click **"Create New Project"** on the dashboard
2. Follow the 4-step wizard:
   - **Project Setup**: Name, description, target audience
   - **Keywords**: Add seed keywords for research
   - **Configuration**: Set location, language, thresholds
   - **Content Settings**: Choose generation method (Claude/OpenAI)

### 3. Execute the Pipeline
1. Navigate to **"Pipeline Runner"**
2. Select your project from the sidebar
3. Run individual stages or the complete pipeline:
   - **🔍 Keyword Research**: Generate keyword clusters and SERP analysis
   - **📄 Content Brief**: Create detailed content outlines
   - **📝 Article Writing**: Generate SEO-optimized articles
   - **📱 Social Media**: Create platform-specific posts
   - **🎥 YouTube Script**: Generate video scripts and metadata

### 4. Manage Your Content
1. Visit **"Content Manager"**
2. Review generated content files
3. Select keywords from research results
4. Edit content directly in the interface
5. Download files or export entire projects

## 📁 Project Structure

```
ContentEngine/
├── 🖥️ Frontend/                    # Streamlit web interface
│   ├── app.py                      # Main dashboard
│   └── pages/
│       ├── project_wizard.py       # Project creation wizard
│       ├── pipeline_runner.py      # Pipeline execution interface
│       ├── content_manager.py      # Content management interface
│       └── project_settings.py     # Configuration management
│
├── 🔧 Backend/                     # Core application logic
│   ├── core/
│   │   ├── project_manager.py      # Project lifecycle management
│   │   ├── pipeline_executor.py    # Script execution coordinator
│   │   └── script_executor.py      # Real script execution wrapper
│   ├── models/
│   │   └── project.py             # Project data model
│   └── utils/
│       ├── file_utils.py          # File management utilities
│       └── progress_tracker.py    # Real-time progress tracking
│
├── 📝 Scripts/                     # Content generation scripts
│   ├── KeywordResearcher.py       # DataForSEO keyword clustering
│   ├── ArticleBrief_Claude.py     # Enhanced content briefs
│   ├── ArticleWriter_Claude.py    # Strategic article creation
│   ├── SocialMedia_Claude.py      # Multi-platform content
│   ├── YouTubeScript_Claude.py    # Professional video scripts
│   └── [OpenAI variants...]       # Legacy OpenAI implementations
│
├── 📊 Projects/                    # Project workspace
│   └── project-{id}-{name}/
│       ├── config.json            # Project configuration
│       ├── inputs/                # Seed keywords and settings
│       ├── stage_01_keyword_research/  # Research results
│       ├── stage_02_content_briefs/    # Content outlines
│       ├── stage_03_articles/          # Generated articles
│       ├── stage_04_social_media/      # Social content
│       └── stage_05_youtube/           # Video scripts
│
└── 🔧 Configuration/
    ├── .env.example               # Environment template
    ├── requirements.txt           # Python dependencies
    ├── start.sh                  # Launch script
    └── run_contentengine.py      # CLI runner
```

## 🔄 Pipeline Execution

### Web Interface (Recommended)
1. **Interactive Execution**: Run stages through the web interface
2. **Real-time Monitoring**: Watch progress with live updates
3. **Error Handling**: User-friendly error messages and recovery options
4. **Content Review**: Immediate access to generated content

### Command Line Interface
```bash
# Activate environment
source venv/bin/activate

# Run individual scripts
python scripts/KeywordResearcher.py
python scripts/ArticleBrief_Claude.py
python scripts/ArticleWriter_Claude.py

# Or use the CLI runner
python run_contentengine.py --project "My Project" --stage keyword_research
```

## 🛠️ Advanced Features

### 🔍 Keyword Research Intelligence
- **SERP Overlap Analysis**: Group keywords by search result similarity
- **Cluster Identification**: Automatic pillar/cluster post categorization
- **Competition Scoring**: DataForSEO-powered competition analysis
- **Volume Filtering**: Customizable search volume and competition thresholds

### 📊 Content Analytics
- **Progress Tracking**: Visual pipeline progress indicators
- **File Organization**: Automatic stage-based file management
- **Export Options**: Multiple format downloads (CSV, MD, JSON)
- **Content Metrics**: Word counts, reading time estimates

### ⚙️ Configuration Management
- **Project Templates**: Reusable configuration presets
- **Environment Variables**: Secure credential management
- **API Integration**: Seamless DataForSEO and OpenAI connectivity
- **Error Validation**: Comprehensive input validation and error handling

## 🔒 Security & Best Practices

- ✅ **Environment Variables**: All credentials stored securely in `.env`
- ✅ **Git Security**: Sensitive files excluded from version control
- ✅ **Input Validation**: Comprehensive validation throughout the pipeline
- ✅ **Error Handling**: User-friendly error messages without exposing internals
- ✅ **File Permissions**: Proper file access controls and organization

## 🎯 Target Use Cases

### Marketing Agencies
- **Client Projects**: Manage multiple client content pipelines
- **Scalable Workflows**: Handle high-volume content generation
- **Brand Consistency**: Maintain brand voice across all content

### Content Teams
- **Editorial Planning**: Research-driven content calendar creation
- **SEO Optimization**: Data-driven keyword targeting and optimization
- **Multi-Platform Publishing**: Consistent content across all channels

### Solo Consultants
- **Thought Leadership**: Create authoritative content in your niche
- **Lead Generation**: SEO-optimized content for organic discovery
- **Time Efficiency**: Automate content creation while maintaining quality

## 📚 Documentation

- **[Development Guidelines](CLAUDE.md)**: Technical documentation for contributors
- **[Environment Setup](.env.example)**: Configuration template and options
- **[API Integration](scripts/)**: Script documentation and customization guides

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Test your changes with the web interface
4. Commit: `git commit -m 'Add feature-name'`
5. Push: `git push origin feature-name`
6. Submit a Pull Request

## 🔗 Links

- **Repository**: https://github.com/anoopkurup/contentengine
- **Issues**: https://github.com/anoopkurup/contentengine/issues
- **Claude Code**: https://claude.ai/code
- **DataForSEO API**: https://dataforseo.com/
- **Streamlit Documentation**: https://docs.streamlit.io/

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for modern content creators**

*ContentEngine combines the power of AI-driven content generation with intuitive project management, making professional content creation accessible to everyone.*