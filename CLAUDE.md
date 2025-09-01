# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ContentEngine is a Python-based content creation pipeline for marketing agencies and consultants. The system creates SEO-optimized blog articles and repurposes them across multiple platforms including social media, YouTube, and newsletters.

## Architecture & Workflow

The content creation follows a sequential pipeline:

1. **Keyword Research** (`KeywordResearcher.py`) - Uses DataForSEO API to find keyword clusters
2. **Content Brief Generation** (`ArticleBrief.py`) - Creates structured article outlines and internal linking strategies  
3. **Article Writing** (`ArticleWriter.py`) - Generates full blog articles using OpenAI GPT
4. **Social Media Repurposing** (`SocialMedia.py`) - Creates LinkedIn posts, tweets, newsletters, and carousel content
5. **YouTube Content** (`YoutTubeScript.py`) - Generates video scripts and metadata

## Quick Setup

### Automated Setup
Run the setup script to configure everything automatically:
```bash
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Copy `.env.example` to `.env`
- Provide next steps

### Manual Setup

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

## Output Files

Each script generates both JSON and Markdown outputs:
- `keyword_clusters.csv` / `cluster_summary.csv` - Keyword research results
- `article_briefs.json` / `article_briefs.md` - Content outlines and internal links
- `article_draft.json` / `article_draft.md` - Complete blog articles
- `social_posts.json` / `social_posts.md` - Multi-platform social content
- `youtube_script.json` / `youtube_script.md` - Video scripts and metadata

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