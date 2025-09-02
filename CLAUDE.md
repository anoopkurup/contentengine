# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ContentEngine is a Python-based content creation pipeline for marketing agencies and consultants. The system creates SEO-optimized blog articles and repurposes them across multiple platforms including social media, YouTube, and newsletters.

**NEW**: The project now includes a modern web-based frontend interface built with Streamlit, providing an intuitive way to create projects, manage content generation, and view results through a browser-based dashboard.

## Architecture & Workflow

The content creation follows a sequential pipeline:

1. **Keyword Research** (`KeywordResearcher.py`) - Uses DataForSEO API to find keyword clusters
2. **Content Brief Generation** (`ArticleBrief.py`) - Creates structured article outlines and internal linking strategies  
3. **Article Writing** (`ArticleWriter.py`) - Generates full blog articles using OpenAI GPT
4. **Social Media Repurposing** (`SocialMedia.py`) - Creates LinkedIn posts, tweets, newsletters, and carousel content
5. **YouTube Content** (`YoutTubeScript.py`) - Generates video scripts and metadata

## Quick Setup

### Frontend Interface (Recommended)
Launch the modern web interface for the best user experience:
```bash
python run_contentengine.py
```

This startup script will:
- Check Python version compatibility
- Install required dependencies
- Validate environment configuration  
- Launch the Streamlit web interface at http://localhost:8501

### Manual Setup (Advanced Users)

1. **Create virtual environment**:
   ```bash
   python3 -m venv ContentEngine-env
   source ContentEngine-env/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

3. **Launch frontend**:
   ```bash
   cd frontend
   streamlit run app.py
   ```

### Required API Credentials

**DataForSEO API** (for keyword research):
- Sign up at https://dataforseo.com/
- Set `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in `.env`

**OpenAI API** (for content generation):
- Get API key from https://platform.openai.com/account/api-keys
- Set `OPENAI_API_KEY` in `.env`

### Optional Configuration
- `TARGET_LOCATION` - Default: "India"
- `TARGET_LANGUAGE` - Default: "en"  
- `SERP_OVERLAP_THRESHOLD` - Default: 0.3
- `MIN_SEARCH_VOLUME` - Default: 100
- `MAX_COMPETITION` - Default: 0.3

### Input Files
Each script expects specific input files from previous steps:
- `ArticleBrief.py` requires: `keyword_clusters.csv`, `cluster_summary.csv`
- `ArticleWriter.py` requires: `article_briefs.json`, `writing_instructions.json`
- `SocialMedia.py` requires: `article_draft.json`, `linkedin_post_writer.json`, `newsletter_instructions.json`
- `YoutTubeScript.py` requires: `article_draft.json`, `youtube_instructions.json`

## Content Guidelines

The system is configured for AnoopKurup.com, a marketing consultancy targeting:
- Professional service firms (1-20 employees) in India
- Tech-enabled businesses and SaaS companies
- Independent consultants with ₹20 lac+ revenue

**Brand Voice**: Professional yet approachable, data-driven, practical, no-fluff, systems-focused

## Running the Pipeline

**Activate the virtual environment first**:
```bash
source ContentEngine-env/bin/activate
```

**Execute scripts in this order**:
```bash
python KeywordResearcher.py
python ArticleBrief.py  
python ArticleWriter.py
python SocialMedia.py
python YoutTubeScript.py
```

## Project Structure

The ContentEngine now uses a modern architecture with separate frontend and backend:

```
ContentEngine/
├── frontend/                 # Streamlit web interface
│   ├── app.py               # Main dashboard application
│   └── pages/               # Additional interface pages
│       ├── project_wizard.py    # Project creation wizard
│       ├── pipeline_runner.py   # Pipeline execution interface  
│       ├── content_manager.py   # Content viewing/editing
│       └── project_settings.py  # Configuration management
├── backend/                 # Core functionality
│   ├── core/               # Main business logic
│   │   ├── project_manager.py   # Project lifecycle management
│   │   └── pipeline_executor.py # Content generation pipeline
│   ├── models/             # Data models
│   │   └── project.py          # Project configuration model
│   ├── utils/              # Utility functions
│   │   ├── progress_tracker.py # Real-time progress tracking
│   │   └── file_utils.py       # File management utilities
│   ├── config/             # Configuration management
│   │   └── app_config.py       # Application settings
│   └── scripts/            # Legacy Python scripts
├── projects/               # Generated project content
│   └── {project_id}/       # Individual project folders
│       ├── config.json         # Project configuration
│       ├── keyword_research.csv   # Keyword research results
│       ├── article_brief.md       # Content brief
│       ├── article.md             # Generated article  
│       ├── social_media_posts.md  # Social media content
│       └── youtube_script.md      # YouTube script
├── run_contentengine.py    # Startup script
└── requirements.txt        # Python dependencies
```

## Output Files

Projects are now organized in individual folders under `projects/`. Each project contains:
- `config.json` - Project settings and metadata  
- `keyword_research.csv` - Keyword research results
- `article_brief.md` - Content outlines and internal links
- `article.md` - Complete blog articles
- `social_media_posts.md` - Multi-platform social content
- `youtube_script.md` - Video scripts and metadata

## Dependencies

The scripts require these Python packages:
- `requests` - API calls to DataForSEO
- `pandas` - Data manipulation and CSV handling
- `openai` - GPT model integration for content generation
- `python-dotenv` - Environment variable management
- `json` - Data serialization (built-in)
- `time` - Rate limiting API calls (built-in)
- `re` - Text processing for word counts (built-in)
- `os` - Operating system interface (built-in)

Install dependencies:
```bash
pip install requests pandas openai python-dotenv
```

## Security Best Practices

- ✅ API credentials are stored in `.env` file (excluded from version control)
- ✅ `.gitignore` protects sensitive files and generated content
- ✅ Environment variables validated at runtime
- ✅ `.env.example` provides setup template for new developers
- ⚠️ Never commit `.env` file or hardcode credentials in source code