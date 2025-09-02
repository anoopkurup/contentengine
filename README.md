# ContentEngine

**AI-Powered Content Creation Pipeline for Marketing Agencies**

ContentEngine is a comprehensive Python-based system that automates the entire content creation workflow—from keyword research to multi-platform content distribution. Built specifically for marketing consultancies targeting professional services and tech-enabled businesses in India.

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### One-Command Setup
```bash
./setup.sh
```

This automatically:
- Creates a Python virtual environment
- Installs all dependencies
- Sets up environment configuration
- Provides next steps

### Manual Setup
```bash
python3 -m venv ContentEngine-env
source ContentEngine-env/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API credentials
```

## 🏗️ Architecture

ContentEngine offers two powerful implementation options:

```
📊 Keyword Research → 📝 Content Briefs → ✍️ Article Writing → 📱 Social Media → 🎬 YouTube Scripts
```

### 🤖 Claude Code Integration (Recommended)

**Superior content quality with strategic thinking**

1. **🔍 KeywordResearcher.py** - DataForSEO-powered keyword clustering and SERP analysis
2. **📋 ArticleBrief_Claude.py** - Enhanced competitive analysis with content gap identification
3. **✍️ ArticleWriter_Claude.py** - Strategic article creation with Claude Code prompts
4. **📱 SocialMedia_Claude.py** - Multi-platform optimization with platform-specific best practices
5. **🎬 YouTubeScript_Claude.py** - Professional video content with engagement optimization

### 🔧 OpenAI Implementation (Legacy)

**Automated content generation for high-volume needs**

1. **🔍 KeywordResearcher.py** - DataForSEO-powered keyword clustering and SERP analysis
2. **📋 ArticleBrief.py** - Basic content outlines with internal linking strategies
3. **✍️ ArticleWriter.py** - OpenAI GPT-powered article generation
4. **📱 SocialMedia.py** - Standard multi-platform content repurposing
5. **🎬 YoutTubeScript.py** - Basic video script and metadata generation

## 🛠️ Features

### Content Intelligence
- **SERP-based keyword clustering** using overlap analysis
- **AI-powered content briefs** with competitive research
- **Brand voice consistency** across all content formats
- **Internal linking automation** for SEO optimization

### Multi-Platform Output
- **Blog articles** (1,500-2,500 words) with SEO optimization
- **LinkedIn posts** with engagement hooks
- **Twitter threads** and standalone tweets
- **Email newsletters** for subscriber nurturing
- **YouTube scripts** with visual direction and CTAs
- **Instagram carousels** ready for design

### Security & Best Practices
- **Environment variable management** for API credentials
- **Comprehensive .gitignore** protecting sensitive data
- **Runtime credential validation** with helpful error messages
- **Production-ready security** practices

## ⚙️ Configuration

### Required API Keys

Create accounts and add credentials to `.env`:

**DataForSEO API** (Keyword Research)
- Sign up: https://dataforseo.com/
- Set: `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`

**OpenAI API** (Content Generation)  
- Get key: https://platform.openai.com/account/api-keys
- Set: `OPENAI_API_KEY`

### Content Configuration

Customize for your target market in `.env`:

```bash
TARGET_LOCATION=India                # Geographic targeting
TARGET_LANGUAGE=en                   # Content language
SERP_OVERLAP_THRESHOLD=0.3          # Keyword clustering sensitivity
MIN_SEARCH_VOLUME=100               # Minimum search volume filter
MAX_COMPETITION=0.3                 # Maximum competition filter
```

## 🎯 Target Audience

ContentEngine is optimized for:

- **Professional Service Firms** (1-20 employees) - Marketing agencies, law firms, consulting practices
- **Tech-Enabled Businesses** - SaaS companies, IT service providers, digital agencies  
- **Independent Consultants** - Boutique consultancies with ₹20 lac+ revenue
- **Geographic Focus** - Indian market with global content standards

## 📊 Usage

### 🤖 Claude Code Pipeline (Recommended)

```bash
# Activate environment
source ContentEngine-env/bin/activate

# Step 1: Keyword research (unchanged)
python KeywordResearcher.py    # → keyword_clusters.csv, cluster_summary.csv

# Step 2: Enhanced content briefs
python ArticleBrief_Claude.py  # → article_briefs_claude.json, competitive analysis

# Step 3: Generate Claude prompts for article writing
python ArticleWriter_Claude.py # → claude_writing_prompt.md

# Step 4: Use Claude Code to write article (copy prompts from generated files)
# Copy claude_writing_prompt.md content into Claude Code
# Save Claude's article output, then process it

# Step 5: Generate social media prompts  
python SocialMedia_Claude.py   # → claude_social_prompts_[keyword].md

# Step 6: Use Claude Code for social content (copy prompts from generated files)
# Generate LinkedIn posts, Twitter threads, newsletters, Instagram content

# Step 7: Generate YouTube prompts
python YouTubeScript_Claude.py # → claude_youtube_prompts_[keyword].md

# Step 8: Use Claude Code for video scripts (copy prompts from generated files)
```

### 🔧 OpenAI Pipeline (Legacy)

```bash
# Activate environment
source ContentEngine-env/bin/activate

# Execute pipeline in order
python KeywordResearcher.py    # → keyword_clusters.csv, cluster_summary.csv
python ArticleBrief.py         # → article_briefs.json, article_briefs.md
python ArticleWriter.py        # → article_draft.json, article_draft.md
python SocialMedia.py          # → social_posts.json, social_posts.md  
python YoutTubeScript.py       # → youtube_script.json, youtube_script.md
```

### Output Files

Each script generates both structured JSON data and human-readable Markdown:

- **Keyword Research**: Clustered keywords with search volumes and competition scores
- **Content Briefs**: Detailed outlines with internal linking suggestions
- **Articles**: Complete blog posts with SEO metadata
- **Social Media**: Platform-specific content variants
- **YouTube**: Scripts with visual cues and optimization tags

## 🔧 Dependencies

- `python-dotenv` - Environment variable management
- `requests` - DataForSEO API integration
- `pandas` - Data manipulation and analysis
- `openai` - GPT model integration

Install via: `pip install -r requirements.txt`

## 🎯 Choosing Your Implementation

### 🤖 Choose Claude Code Integration When:
- **Quality is priority**: Need superior, strategic content with deeper insights
- **Brand consistency matters**: Require precise brand voice and messaging alignment
- **Competitive advantage**: Want content that stands out with unique positioning
- **Interactive refinement**: Need ability to iterate and perfect content through conversation
- **Professional publishing**: Creating flagship content for thought leadership

### 🔧 Choose OpenAI Implementation When:
- **Volume is priority**: Need to generate large amounts of content quickly
- **Automation is key**: Want fully automated pipeline without manual intervention
- **Budget constraints**: API costs need to be predictable and controlled
- **Simple content needs**: Standard content formats without advanced strategy
- **Legacy system integration**: Working with existing OpenAI-based workflows

### 📊 Implementation Comparison

| Feature | Claude Code | OpenAI Legacy |
|---------|-------------|---------------|
| **Content Quality** | Superior, strategic | Good, professional |
| **Setup Complexity** | Moderate (interactive) | Simple (automated) |
| **Time Investment** | Higher initially | Lower overall |
| **Cost Model** | Fixed subscription | Per-API-call |
| **Customization** | Highly flexible | Template-based |
| **Brand Alignment** | Excellent | Good |
| **Scalability** | Quality-focused | Volume-focused |

### 🔄 Hybrid Approach
You can also use both implementations strategically:
- **Claude Code** for premium content (pillar articles, key social posts)
- **OpenAI Scripts** for supporting content (cluster posts, routine updates)
- **Mix and match** based on content importance and time availability

## 📁 Project Structure

```
ContentEngine/
├── Keyword Research/
│   └── KeywordResearcher.py    # DataForSEO-powered clustering
│
├── Claude Code Integration/ (Recommended)
│   ├── ArticleBrief_Claude.py   # Enhanced competitive analysis
│   ├── ArticleWriter_Claude.py  # Strategic content creation
│   ├── SocialMedia_Claude.py   # Multi-platform optimization
│   └── YouTubeScript_Claude.py # Professional video content
│
├── OpenAI Implementation/ (Legacy)
│   ├── ArticleBrief.py         # Basic content outlines
│   ├── ArticleWriter.py        # Standard article generation
│   ├── SocialMedia.py          # Basic social repurposing
│   └── YoutTubeScript.py       # Simple video scripts
│
├── Configuration/
│   ├── Writing Instructions.md # Brand voice guidelines
│   ├── .env.example           # Environment template
│   ├── setup.sh              # Automated setup script
│   └── requirements.txt      # Python dependencies
│
└── Documentation/
    ├── README.md             # Project overview (this file)
    ├── CLAUDE.md            # Development guidelines
    ├── CLAUDE_INTEGRATION.md # Claude Code usage guide
    └── .gitignore          # Security exclusions
```

## 🔒 Security

- ✅ **No hardcoded credentials** - All API keys stored in environment variables
- ✅ **Git security** - `.env` file excluded from version control
- ✅ **Runtime validation** - Clear error messages for missing credentials
- ✅ **Best practices** - Following Python security guidelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit: `git commit -m 'Add feature-name'`
5. Push: `git push origin feature-name`
6. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

- **[Claude Integration Guide](CLAUDE_INTEGRATION.md)**: Comprehensive guide for using Claude Code with ContentEngine
- **[Development Guidelines](CLAUDE.md)**: Technical documentation for contributors
- **[Writing Instructions](Writing%20Instructions.md)**: Brand voice and content guidelines

## 🔗 Links

- **Repository**: https://github.com/anoopkurup/contentengine
- **Issues**: https://github.com/anoopkurup/contentengine/issues
- **Claude Code**: https://claude.ai/code
- **DataForSEO API**: https://dataforseo.com/
- **OpenAI API**: https://platform.openai.com/

---

**Built with ❤️ for content creators and marketing professionals**

*ContentEngine streamlines the content creation process, allowing you to focus on strategy while AI handles the execution.*