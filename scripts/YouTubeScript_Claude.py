import json
import os
import time
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------------------
# 1. Setup & Configuration
# -------------------------------

# Claude-specific configuration
CONTENT_GENERATOR = os.getenv("CONTENT_GENERATOR", "claude")
CLAUDE_MODEL_PREFERENCE = os.getenv("CLAUDE_MODEL_PREFERENCE", "quality")

# File paths
ARTICLE_FILE = os.getenv("ARTICLE_DRAFT_FILE", "article_draft_claude.json")
YOUTUBE_INSTRUCTIONS_FILE = "youtube_instructions.json"

# Output files with Claude suffix
OUTPUT_JSON = "youtube_script_claude.json"
OUTPUT_MD = "youtube_script_claude.md"

print("🎬 ContentEngine - YouTube Script Writer (Claude-Powered)")
print(f"🤖 Using {CONTENT_GENERATOR.upper()} for video content creation")
print(f"🎯 Quality Setting: {CLAUDE_MODEL_PREFERENCE}")
print("")

# -------------------------------
# 2. YouTube Content Strategy & Guidelines
# -------------------------------
class YouTubeContentFramework:
    """Framework for creating engaging YouTube video content"""
    
    VIDEO_TYPES = {
        "educational": {
            "name": "Educational/Tutorial",
            "description": "Step-by-step teaching content",
            "typical_length": "8-15 minutes",
            "structure": ["Hook", "Introduction", "Teaching sections", "Summary", "CTA"],
            "best_practices": [
                "Clear learning outcomes",
                "Step-by-step progression",
                "Visual aids and examples",
                "Recap key points",
                "Actionable next steps"
            ]
        },
        "explainer": {
            "name": "Explainer/Overview", 
            "description": "Comprehensive topic explanation",
            "typical_length": "10-20 minutes",
            "structure": ["Hook", "Problem setup", "Solution explanation", "Examples", "Implementation", "Wrap-up"],
            "best_practices": [
                "Start with relatable problem",
                "Use storytelling techniques", 
                "Include real examples",
                "Clear visual progression",
                "Strong conclusion"
            ]
        },
        "case_study": {
            "name": "Case Study/Results",
            "description": "Real business results and analysis",
            "typical_length": "12-18 minutes", 
            "structure": ["Hook", "Background", "Challenge", "Solution", "Results", "Lessons"],
            "best_practices": [
                "Compelling before/after",
                "Specific metrics and data",
                "Process transparency",
                "Replicable insights",
                "Clear takeaways"
            ]
        }
    }
    
    ENGAGEMENT_STRATEGIES = {
        "hook_techniques": [
            "Start with a surprising statistic",
            "Ask a provocative question", 
            "Share a personal story",
            "Present a common mistake",
            "Promise a specific outcome"
        ],
        "retention_tactics": [
            "Preview what's coming",
            "Use pattern interrupts",
            "Include visual variety",
            "Ask engaging questions",
            "Tease upcoming points"
        ],
        "call_to_actions": [
            "Subscribe for more content",
            "Download free resources",
            "Book a consultation call",
            "Join a community/course",
            "Share experiences in comments"
        ]
    }
    
    TECHNICAL_REQUIREMENTS = {
        "title_optimization": {
            "length": "60-70 characters",
            "include_keyword": True,
            "power_words": ["Ultimate", "Complete", "Step-by-Step", "Proven", "Secret"],
            "numbers": "Use specific numbers when possible",
            "curiosity_gap": "Create intrigue without clickbait"
        },
        "description_optimization": {
            "length": "125-200 words", 
            "first_line": "Include keyword and compelling hook",
            "timestamps": "Include for videos over 10 minutes",
            "links": "Include relevant links to resources",
            "keywords": "Naturally include related terms"
        },
        "tags_strategy": {
            "primary_tags": "Direct keyword variations",
            "secondary_tags": "Related industry terms",
            "location_tags": "Geographic relevance if applicable",
            "format_tags": "Content type descriptors"
        }
    }

# -------------------------------
# 3. YouTube Script Structure Framework
# -------------------------------
class YouTubeScriptWriter:
    """Framework for creating comprehensive YouTube scripts using Claude"""
    
    def __init__(self, article_data, video_type="educational"):
        self.article_data = article_data
        self.video_type = video_type
        self.keyword = article_data.get('keyword', '')
        self.article_content = article_data.get('article_content', '')
        self.metadata = article_data.get('metadata', {})
        
        # Extract content elements
        self.key_points = self.extract_key_teaching_points()
        self.examples = self.extract_examples_and_stories()
        self.actionable_steps = self.extract_actionable_steps()
        
    def extract_key_teaching_points(self):
        """Extract main teaching points from the article"""
        
        # Framework for Claude to extract key points
        teaching_framework = {
            "main_concepts": [
                f"Core concepts about {self.keyword}",
                "Framework or methodology presented",
                "Key principles explained"
            ],
            "problem_solutions": [
                "Main problems addressed",
                "Solutions provided",
                "Alternative approaches discussed"
            ],
            "practical_applications": [
                "How to implement the concepts",
                "Real-world applications",
                "Industry-specific adaptations"
            ],
            "common_mistakes": [
                "Mistakes to avoid",
                "Misconceptions addressed", 
                "Contrarian viewpoints shared"
            ]
        }
        
        return teaching_framework
    
    def extract_examples_and_stories(self):
        """Extract examples and stories suitable for video content"""
        
        examples_framework = {
            "case_studies": [
                "Client success stories (anonymized)",
                "Before/after scenarios",
                "Implementation examples"
            ],
            "personal_anecdotes": [
                "Consultant's personal experiences",
                "Lessons learned from failures",
                "Industry observations"
            ],
            "industry_examples": [
                "Well-known company examples",
                "Industry trends and patterns",
                "Market data and insights"
            ]
        }
        
        return examples_framework
    
    def extract_actionable_steps(self):
        """Extract specific, actionable steps for viewers"""
        
        steps_framework = {
            "immediate_actions": [
                "What viewers can do right after watching",
                "Quick wins and implementations",
                "First steps to take"
            ],
            "step_by_step_process": [
                "Systematic implementation guide",
                "Progressive skill building",
                "Milestone achievements"  
            ],
            "resources_needed": [
                "Tools mentioned in article",
                "Skills required",
                "Budget considerations"
            ]
        }
        
        return steps_framework

# -------------------------------
# 4. Claude Prompt Generation for YouTube Scripts
# -------------------------------
def create_youtube_script_prompts(article_data, video_type="educational"):
    """Create comprehensive prompts for YouTube script generation using Claude"""
    
    keyword = article_data.get('keyword', '')
    script_writer = YouTubeScriptWriter(article_data, video_type)
    
    # Main script prompt
    main_script_prompt = f"""
Create a comprehensive YouTube video script about {keyword} based on an article I've written.

## VIDEO SPECIFICATIONS

**Topic**: {keyword}
**Video Type**: {video_type.title()} Video
**Target Length**: 12-18 minutes
**Target Audience**: Business owners, marketing professionals, consultants in India
**Brand Voice**: Professional but approachable, data-driven, practical, systems-focused

## SCRIPT REQUIREMENTS

**Presenter**: Anoop Kurup, marketing consultant
**Tone**: Conversational expert - like explaining to a colleague
**Style**: Educational but engaging, with personal insights
**Focus**: Practical implementation over theory

## VIDEO STRUCTURE

### 1. HOOK (First 15 seconds) - CRITICAL
- Start with a compelling statistic or surprising insight about {keyword}
- Create curiosity gap: "By the end of this video, you'll know..."
- Personal credibility statement
- Preview the main points

### 2. INTRODUCTION (15-45 seconds)
- Introduce yourself briefly
- State the problem most businesses face with {keyword}
- Promise specific outcomes from watching
- Ask viewers to subscribe

### 3. MAIN CONTENT SECTIONS (10-15 minutes)
Structure the content into 4-5 clear sections:

**Section 1**: Problem Definition
- Why most {keyword} approaches fail
- Common mistakes businesses make
- Cost of getting it wrong

**Section 2**: Framework/System Overview
- Introduce your systematic approach
- Why systems beat tactics
- High-level methodology preview

**Section 3**: Step-by-Step Implementation
- Detailed process breakdown
- Specific tools and resources
- Real examples and case studies

**Section 4**: Advanced Tips & Troubleshooting
- Pro-level insights
- Common implementation challenges
- How to measure success

**Section 5**: Results & Case Study
- Share specific results (anonymized)
- Before/after scenarios
- Key lessons learned

### 4. CALL TO ACTION & CONCLUSION (1-2 minutes)
- Summarize key takeaways
- Provide clear next steps
- Multiple CTAs: subscribe, download resource, book consultation
- Suggest related videos

## SCRIPT FORMATTING

Format as a proper video script with:
- **[VISUAL CUE]**: Describe what should be shown on screen
- **[PAUSE]**: Indicate strategic pauses
- **[EMPHASIS]**: Words to emphasize vocally
- **[TITLE CARD]**: Text overlays or graphics
- **Voiceover**: Complete spoken content

## ENGAGEMENT ELEMENTS TO INCLUDE

- Personal stories and experiences
- Specific statistics and data points
- Interactive questions for audience
- Pattern interrupts to maintain attention
- Clear preview of what's coming next
- Visual metaphors and analogies

## BRAND POSITIONING

Reinforce these themes throughout:
- Systems over tactics
- Anti-hype, realistic approach
- Indian market expertise
- Data-driven methodology
- Practical implementation focus

## CONTENT ADAPTATION NOTES

Base the script on the article about {keyword}, but:
- Make it more conversational and personal
- Add visual elements and demonstrations
- Include audience interaction moments
- Expand on practical implementation
- Add video-specific examples and stories

Write the complete video script now, following this structure exactly.
"""

    # Title and description prompts
    title_description_prompt = f"""
Create optimized YouTube title and description for a {keyword} video.

## TITLE REQUIREMENTS
- 60-70 characters maximum
- Include the keyword "{keyword}" naturally  
- Create curiosity without clickbait
- Include a number or specific benefit
- Professional but engaging tone

Create 5 title options:

1. Educational focus: "How to..."
2. Results focus: "The [System/Method] that..."
3. Problem focus: "Why Most [Topic] Fails..."
4. Comprehensive focus: "Complete Guide to..."
5. Contrarian focus: "The Truth About..."

## DESCRIPTION REQUIREMENTS
- First line: Compelling hook with keyword
- 150-200 words total
- Include video timestamps
- Add relevant links
- Include call-to-action
- Use related keywords naturally

Write the complete description including:
- Hook paragraph
- Video overview
- Key points covered
- Timestamps (estimate based on content)
- Links to resources
- Subscribe CTA
- About Anoop Kurup
- Tags suggestions

Create the titles and description now.
"""

    # Thumbnail and visual prompts
    visual_elements_prompt = f"""
Create visual elements guide for the {keyword} YouTube video.

## THUMBNAIL DESIGN
- Main element: Professional photo of Anoop Kurup
- Text overlay: Key phrase from title
- Visual metaphor related to {keyword}
- Color scheme: Professional blue/orange
- Style: Clean, business-focused

Describe 3 thumbnail concepts with:
- Main visual elements
- Text overlay suggestions  
- Color and style notes
- What emotion/curiosity it creates

## VIDEO GRAPHICS NEEDED
List and describe:
- Title cards for each section
- Key statistics or data points
- Process diagrams or frameworks
- Before/after comparisons
- Resource lists or checklists
- Call-to-action graphics

## B-ROLL SUGGESTIONS
Suggest relevant footage:
- Business/office environments
- People working with technology
- Indian business contexts
- Symbolic imagery for concepts
- Screen recordings of tools/processes

Create the complete visual elements guide now.
"""

    return {
        "main_script": main_script_prompt,
        "title_description": title_description_prompt, 
        "visual_elements": visual_elements_prompt,
        "video_type": video_type,
        "estimated_length": "12-18 minutes",
        "target_audience": "Business professionals in India"
    }

def create_youtube_optimization_prompts(article_data):
    """Create prompts for YouTube SEO and optimization using Claude"""
    
    keyword = article_data.get('keyword', '')
    
    optimization_prompts = {
        "seo_strategy": f"""
Create a comprehensive YouTube SEO strategy for the {keyword} video.

## KEYWORD RESEARCH
Primary Keyword: {keyword}
Research and suggest:
- 10 related keywords for tags
- 5 long-tail keyword variations
- 3 competitor keywords to target
- Regional keywords (India-specific)

## VIDEO OPTIMIZATION
**Title Optimization**:
- Include primary keyword naturally
- Create curiosity gap
- Use power words effectively
- Optimize for search and click-through

**Description Optimization**:
- First 125 characters are critical
- Include primary and secondary keywords
- Add relevant hashtags (3-5 max)
- Include call-to-action

**Tags Strategy**:
- Primary tags: Direct keyword matches
- Secondary tags: Related business terms  
- Location tags: India, Indian business
- Format tags: Tutorial, guide, etc.

## ENGAGEMENT OPTIMIZATION
**Thumbnail Strategy**:
- High contrast and readability
- Emotional trigger or curiosity
- Consistent branding
- Mobile-optimized design

**Content Structure**:
- Hook in first 15 seconds
- Pattern interrupts every 30-60 seconds
- Clear preview of value
- Strong call-to-action

Create the complete SEO strategy now.
""",

        "content_series": f"""
Create a YouTube content series plan around {keyword}.

## SERIES CONCEPT
Main Theme: {keyword} mastery for business owners

Suggest 8-10 related video topics that build on each other:
1. Introduction/Overview video (current)
2. Deep-dive videos on sub-topics
3. Case study videos
4. Q&A or troubleshooting videos
5. Advanced strategy videos

## SERIES STRUCTURE
For each video suggest:
- Specific title
- Key points to cover
- How it connects to other videos
- Estimated length
- Difficulty level

## CONTENT CALENDAR
Suggest optimal publishing schedule:
- Frequency (weekly, bi-weekly)
- Best days/times for target audience
- Seasonal considerations
- Content variety balance

## CROSS-PROMOTION STRATEGY
How to link videos together:
- End screen suggestions
- Playlist organization
- Cards and annotations
- Community posts
- Shorts tie-ins

Create the complete series plan now.
"""
    }
    
    return optimization_prompts

# -------------------------------
# 5. Output Generation & Management  
# -------------------------------
def create_youtube_prompt_file(script_prompts, optimization_prompts, keyword):
    """Create comprehensive YouTube prompt file for Claude"""
    
    prompt_content = f"""# YouTube Script Generation Prompts
# Keyword: {keyword}

## CLAUDE CODE INTEGRATION INSTRUCTIONS

1. **Choose Your Content Type**: Start with main script, then move to optimization
2. **Copy Complete Prompts**: Use entire prompt sections for best results
3. **Generate with Claude**: Paste into Claude Code for comprehensive output
4. **Save All Results**: Keep scripts, titles, descriptions, and SEO elements
5. **Iterate if Needed**: Refine based on Claude's initial output

---

# MAIN VIDEO SCRIPT PROMPT

{script_prompts['main_script']}

---

# TITLE & DESCRIPTION PROMPT

{script_prompts['title_description']}

---

# VISUAL ELEMENTS PROMPT

{script_prompts['visual_elements']}

---

# SEO OPTIMIZATION PROMPT

{optimization_prompts['seo_strategy']}

---

# CONTENT SERIES PROMPT

{optimization_prompts['content_series']}

---

# YOUTUBE BEST PRACTICES REFERENCE

## Video Structure Guidelines
- Hook: First 15 seconds are critical
- Introduction: 30-45 seconds max
- Main content: 8-15 minutes with clear sections
- Conclusion: 1-2 minutes with strong CTA

## Engagement Optimization
- Ask questions to encourage comments
- Use pattern interrupts every 60 seconds
- Include clear value previews
- End with specific next action

## Technical Specifications
- Title: 60-70 characters optimal
- Description: First 125 characters crucial
- Tags: 10-15 relevant tags maximum
- Thumbnail: High contrast, readable on mobile

## Brand Consistency
- Maintain Anoop Kurup's professional voice
- Focus on systems over tactics
- Include Indian market context
- Emphasize practical implementation

---

# PRODUCTION CHECKLIST

## Pre-Production
- [ ] Script finalized and rehearsed
- [ ] Visual elements designed
- [ ] B-roll footage identified
- [ ] Equipment and setup ready

## Production  
- [ ] Strong opening hook delivered
- [ ] Clear audio and video quality
- [ ] Visual aids incorporated
- [ ] Energy and engagement maintained

## Post-Production
- [ ] Professional editing completed
- [ ] Graphics and titles added
- [ ] SEO elements optimized
- [ ] Thumbnail designed and tested

## Publishing
- [ ] Title and description finalized
- [ ] Tags and categories set
- [ ] Thumbnail uploaded
- [ ] End screens and cards configured
- [ ] Publishing scheduled

---

*Generated by ContentEngine Claude Integration*
*Use with Claude Code for optimal results*
"""
    
    return prompt_content

# -------------------------------
# 6. Main Execution
# -------------------------------
def main():
    print("📺 Loading article content for YouTube script generation...")
    
    # Load article data
    try:
        with open(ARTICLE_FILE, "r") as f:
            article_data = json.load(f)
            
        keyword = article_data.get('keyword', 'Unknown')
        print(f"✅ Loaded article: {keyword}")
        
    except FileNotFoundError:
        print(f"❌ Article file not found: {ARTICLE_FILE}")
        print("Please run ArticleWriter_Claude.py first to generate article content")
        return
    except Exception as e:
        print(f"❌ Error loading article: {e}")
        return
    
    print(f"\n🎬 Preparing YouTube video script for: {keyword}")
    print(f"🎯 Video type: Educational/Tutorial")
    print(f"⏱️  Target length: 12-18 minutes")
    
    # Generate script prompts
    print("\n🤖 Generating Claude prompts for YouTube content...")
    script_prompts = create_youtube_script_prompts(article_data, "educational")
    optimization_prompts = create_youtube_optimization_prompts(article_data)
    
    # Create comprehensive prompt file
    prompt_file_content = create_youtube_prompt_file(script_prompts, optimization_prompts, keyword)
    
    # Save prompt file
    prompt_filename = f"claude_youtube_prompts_{keyword.lower().replace(' ', '_')}.md"
    with open(prompt_filename, "w") as f:
        f.write(prompt_file_content)
    
    # Create output structure
    output_data = {
        "keyword": keyword,
        "article_metadata": article_data.get('metadata', {}),
        "video_strategy": {
            "video_type": "Educational Tutorial",
            "target_length": "12-18 minutes",
            "target_audience": "Business professionals in India",
            "key_elements": [
                "Compelling 15-second hook",
                "Systematic framework presentation", 
                "Step-by-step implementation guide",
                "Real case study examples",
                "Clear call-to-action"
            ]
        },
        "content_deliverables": {
            "main_script": "Complete video script with visual cues",
            "title_options": "5 optimized title variations",
            "description": "SEO-optimized video description", 
            "visual_guide": "Thumbnail and graphics specifications",
            "seo_strategy": "Keywords, tags, and optimization plan",
            "series_plan": "8-10 related video concepts"
        },
        "claude_prompts": {
            "script_prompts": script_prompts,
            "optimization_prompts": optimization_prompts
        },
        "generation_method": "Claude Code Integration",
        "prompt_file": prompt_filename,
        "status": "Ready for Claude video generation",
        "next_steps": [
            f"Open {prompt_filename} for detailed prompts",
            "Use Claude Code to generate video script",
            "Create supporting visual elements",
            "Optimize for YouTube SEO",
            "Plan related video series"
        ]
    }
    
    # Save JSON output
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n💾 Files created:")
    print(f"   🎬 {prompt_filename} - Complete YouTube prompts for Claude")
    print(f"   📊 {OUTPUT_JSON} - Video strategy and framework")
    
    print(f"\n🤖 CLAUDE CODE INTEGRATION")
    print("=" * 50)
    print("YouTube video script prompts have been prepared. Here's how to use them:")
    print()
    print("📋 STEP-BY-STEP PROCESS:")
    print(f"1. Open the file: {prompt_filename}")
    print("2. Start with 'Main Video Script Prompt'")
    print("3. Copy and paste into Claude Code")
    print("4. Generate the complete video script")
    print("5. Use other prompts for titles, SEO, and optimization")
    print("6. Save all generated content for video production")
    print()
    print("🎬 CONTENT BREAKDOWN:")
    print("   📝 Main Script: Complete 12-18 minute video script")
    print("   🏷️  Titles: 5 optimized title options")
    print("   📄 Description: SEO-optimized video description")
    print("   🎨 Visuals: Thumbnail and graphics guide")
    print("   🔍 SEO: Keywords, tags, and optimization")
    print("   📺 Series: 8-10 related video concepts")
    print()
    print("🎉 Ready for Claude Code YouTube generation!")
    print("   Complete video production package ready")
    print("   Professional YouTube content optimized for engagement")

def process_youtube_content(script_content, video_type="educational", article_file=None):
    """
    Helper function to process YouTube content after it's been generated by Claude Code.
    Use this after getting the video script from Claude.
    """
    
    if article_file is None:
        article_file = ARTICLE_FILE
    
    # Load original article data
    with open(article_file, "r") as f:
        article_data = json.load(f)
    
    # Analyze script content
    word_count = len(script_content.split())
    estimated_duration = round(word_count / 150, 1)  # Assume 150 words per minute
    
    processed_content = {
        "keyword": article_data.get('keyword', ''),
        "video_type": video_type,
        "script_content": script_content,
        "script_analysis": {
            "word_count": word_count,
            "estimated_duration_minutes": estimated_duration,
            "character_count": len(script_content)
        },
        "generation_method": "Claude Code Integration",
        "processing_date": time.strftime('%Y-%m-%d %H:%M:%S'),
        "status": "Ready for video production",
        "production_notes": [
            "Script includes visual cues and directions",
            "Optimized for audience engagement", 
            "Includes strategic pauses and emphasis",
            "Ready for teleprompter or rehearsal"
        ]
    }
    
    # Save processed script
    output_filename = f"youtube_script_final_{article_data.get('keyword', 'unknown').replace(' ', '_')}.json"
    with open(output_filename, "w") as f:
        json.dump(processed_content, f, indent=2)
    
    # Save markdown version
    md_filename = f"youtube_script_final_{article_data.get('keyword', 'unknown').replace(' ', '_')}.md"
    with open(md_filename, "w") as f:
        f.write(f"# YouTube Video Script: {article_data.get('keyword', '')}\n\n")
        f.write(f"**Duration**: ~{estimated_duration} minutes\n")
        f.write(f"**Word Count**: {word_count} words\n\n")
        f.write("---\n\n")
        f.write(script_content)
    
    print(f"✅ YouTube script processed and saved:")
    print(f"   📊 JSON: {output_filename}")
    print(f"   📝 Markdown: {md_filename}")
    print(f"   ⏱️  Estimated Duration: {estimated_duration} minutes")
    print(f"   📏 Word Count: {word_count} words")
    
    return processed_content

if __name__ == "__main__":
    main()