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

# Platform-specific instruction files (optional)
LINKEDIN_FILE = "linkedin_instructions.json"
NEWSLETTER_FILE = "newsletter_instructions.json"
TWITTER_FILE = "twitter_instructions.json"

# Output files with Claude suffix
OUTPUT_JSON = "social_posts_claude.json"
OUTPUT_MD = "social_posts_claude.md"

print("📱 ContentEngine - Social Media Repurposing (Claude-Powered)")
print(f"🤖 Using {CONTENT_GENERATOR.upper()} for content adaptation")
print(f"🎯 Quality Setting: {CLAUDE_MODEL_PREFERENCE}")
print("")

# -------------------------------
# 2. Platform Configuration & Guidelines
# -------------------------------
class SocialMediaPlatforms:
    """Configuration and guidelines for each social media platform"""
    
    LINKEDIN = {
        "name": "LinkedIn",
        "character_limits": {
            "post": 3000,
            "headline": 220,
            "article": 125000
        },
        "best_practices": [
            "Professional tone with personal insights",
            "Use first-person narrative",
            "Include industry-specific hashtags (3-5)",
            "Add engaging questions for comments",
            "Share practical business lessons",
            "Include call-to-action for consultation"
        ],
        "content_types": [
            "Insight posts (personal experience)",
            "Educational threads (multi-post series)", 
            "Case study summaries",
            "Industry observations",
            "Behind-the-scenes content",
            "Long-form LinkedIn articles"
        ],
        "optimal_timing": "Tuesday-Thursday, 8-10 AM or 12-2 PM IST",
        "hashtag_strategy": "Mix of industry, location, and niche tags"
    },
    
    TWITTER = {
        "name": "Twitter/X",
        "character_limits": {
            "tweet": 280,
            "thread": "Unlimited (per tweet 280)",
            "bio": 160
        },
        "best_practices": [
            "Concise, punchy statements",
            "Thread format for complex topics",
            "Use relevant hashtags (2-3 max)",
            "Engage with industry conversations",
            "Share quick wins and insights",
            "Retweet with thoughtful commentary"
        ],
        "content_types": [
            "Quick insights (single tweets)",
            "Educational threads (5-10 tweets)",
            "Industry hot takes",
            "Live-tweeting events",
            "Poll questions",
            "Resource recommendations"
        ],
        "optimal_timing": "Monday-Friday, 9-11 AM or 7-9 PM IST",
        "hashtag_strategy": "Trending + niche industry tags"
    },
    
    NEWSLETTER = {
        "name": "Email Newsletter", 
        "best_practices": [
            "Subject line: 30-50 characters",
            "Personal, conversational tone",
            "Scannable format with bullet points",
            "One primary CTA per email",
            "Include subscriber-only insights",
            "Add social sharing buttons"
        ],
        "content_structure": [
            "Personal greeting/update",
            "Main insight or lesson",
            "Practical implementation tip",
            "Resource recommendation", 
            "Call-to-action",
            "P.S. with additional value"
        ],
        "optimal_frequency": "Weekly or bi-weekly",
        "target_length": "300-800 words"
    },
    
    INSTAGRAM = {
        "name": "Instagram",
        "content_types": [
            "Carousel posts (educational)",
            "Story highlights (tutorials)",
            "Reels (quick tips)",
            "IGTV (longer explanations)"
        ],
        "best_practices": [
            "Visual-first content design",
            "Clear, readable text on images", 
            "Use story-driven captions",
            "Include relevant hashtags (10-20)",
            "Engage with comments quickly",
            "Use Instagram-specific features"
        ]
    },
    
    YOUTUBE = {
        "name": "YouTube Community",
        "content_types": [
            "Community posts",
            "Poll questions",
            "Behind-the-scenes updates",
            "Video teasers"
        ],
        "best_practices": [
            "Visual content with text overlay",
            "Engage subscriber community",
            "Tease upcoming video content",
            "Share industry insights"
        ]
    }

# -------------------------------
# 3. Content Analysis & Strategy
# -------------------------------
class ClaudeSocialMediaRepurposer:
    """Framework for repurposing content across social media platforms using Claude"""
    
    def __init__(self, article_data, platform_config):
        self.article_data = article_data
        self.platform_config = platform_config
        self.keyword = article_data.get('keyword', '')
        self.article_content = article_data.get('article_content', '')
        self.metadata = article_data.get('metadata', {})
        
        # Extract key insights for repurposing
        self.key_insights = self.extract_key_insights()
        self.main_takeaways = self.extract_main_takeaways()
        self.actionable_tips = self.extract_actionable_tips()
        
    def extract_key_insights(self):
        """Extract key insights from the article for social media adaptation"""
        
        # In a real implementation, this would use NLP to extract insights
        # For now, we'll create a framework for Claude to use
        
        insights_framework = {
            "hook_statements": [
                f"Most {self.keyword} advice misses this crucial point...",
                f"After helping 50+ businesses with {self.keyword}, here's what actually works:",
                f"The biggest {self.keyword} mistake I see Indian businesses make:"
            ],
            "data_points": [
                "Specific metrics or percentages from the article",
                "Industry benchmarks mentioned",
                "Case study results"
            ],
            "contrarian_takes": [
                "Points that go against conventional wisdom",
                "Unique angles from the article",
                "Anti-hype positioning"
            ],
            "practical_frameworks": [
                "Step-by-step processes outlined",
                "Checklists or templates mentioned", 
                "Systems described in the article"
            ]
        }
        
        return insights_framework
    
    def extract_main_takeaways(self):
        """Extract main takeaways suitable for different platforms"""
        
        # This would analyze the article content in production
        takeaways = {
            "executive_summary": f"Key insights about {self.keyword} for business leaders",
            "implementation_steps": f"How to implement {self self.keyword} systematically",
            "common_mistakes": f"What to avoid when implementing {self.keyword}",
            "success_metrics": f"How to measure {self.keyword} success",
            "next_steps": f"Immediate actions to take after learning about {self.keyword}"
        }
        
        return takeaways
    
    def extract_actionable_tips(self):
        """Extract specific, actionable tips for quick social media posts"""
        
        tips = {
            "quick_wins": [
                "Immediate actions readers can take",
                "Simple implementations",
                "Low-effort, high-impact tips"
            ],
            "tools_mentioned": [
                "Specific tools recommended in article",
                "Software or platforms referenced",
                "Resources shared"
            ],
            "frameworks": [
                "Mental models presented",
                "Decision-making frameworks",
                "Systematic approaches"
            ]
        }
        
        return tips

# -------------------------------
# 4. Platform-Specific Content Generation
# -------------------------------
def create_linkedin_content_prompts(article_data, repurposer):
    """Create prompts for LinkedIn content generation using Claude"""
    
    keyword = article_data.get('keyword', '')
    
    linkedin_prompts = {
        "insight_post": f"""
Create a LinkedIn post sharing a key insight from an article about {keyword}.

REQUIREMENTS:
- Write in first person as Anoop Kurup, marketing consultant
- Professional but conversational tone
- Include a personal anecdote or client experience (anonymized)
- Share a contrarian or unique perspective
- End with an engaging question for comments
- Include 3-4 relevant hashtags
- Keep to 1,500 characters max
- Focus on practical business value

CONTENT ANGLE: 
Share why most {keyword} advice fails and what actually works for Indian businesses.

STRUCTURE:
1. Hook statement (personal observation)
2. Brief story or example
3. Key insight or lesson
4. Practical application
5. Engaging question
6. Relevant hashtags

Write the LinkedIn post now:""",

        "educational_thread": f"""
Create a LinkedIn post series (carousel-style) about {keyword} implementation.

REQUIREMENTS:
- Write as Anoop Kurup, marketing consultant
- Professional educational tone
- 5-7 connected posts that can be shared individually
- Each post should be 1,200-1,500 characters
- Include actionable steps
- Focus on systems over tactics
- Add relevant hashtags to each post

THREAD TOPIC:
"The 5-Step System for {keyword} That Actually Works"

POST STRUCTURE:
Post 1: Hook + System overview
Post 2-5: Each step detailed
Final Post: Results/next steps + CTA

Write the complete thread now:""",

        "case_study_summary": f"""
Create a LinkedIn post sharing a case study summary about {keyword}.

REQUIREMENTS:
- Write as Anoop Kurup, marketing consultant
- Share an anonymized client success story
- Include specific (but anonymous) metrics
- Highlight the systematic approach used
- Professional storytelling tone
- Include key lessons learned
- End with subtle consultation CTA
- 2,000-2,500 characters
- Use 3-4 industry hashtags

CASE STUDY FOCUS:
How a [type of business] used {keyword} to achieve [specific result].

Write the case study post now:""",

        "linkedin_article": f"""
Write a comprehensive LinkedIn article about {keyword}.

REQUIREMENTS:
- Write as Anoop Kurup, marketing consultant
- 1,000-1,500 words
- Professional but approachable tone
- Include personal insights and experience
- Focus on practical implementation
- Add subheadings for readability
- Include a compelling headline
- End with clear call-to-action

ARTICLE ANGLE:
"Why Most {keyword} Strategies Fail (And What Works Instead)"

STRUCTURE:
1. Compelling headline
2. Hook opening with personal observation
3. Problem definition
4. Solution framework
5. Implementation steps
6. Case example (anonymized)
7. Key takeaways
8. Call-to-action

Write the LinkedIn article now:"""
    }
    
    return linkedin_prompts

def create_twitter_content_prompts(article_data, repurposer):
    """Create prompts for Twitter content generation using Claude"""
    
    keyword = article_data.get('keyword', '')
    
    twitter_prompts = {
        "insight_tweets": f"""
Create 5 standalone tweets sharing insights about {keyword}.

REQUIREMENTS:
- Write as Anoop Kurup (@anoopkurup)
- Each tweet under 280 characters
- Professional but punchy tone
- Include relevant hashtags (2 max per tweet)
- Share practical business insights
- Focus on contrarian or unique perspectives

TWEET TOPICS:
1. Common mistake people make with {keyword}
2. Surprising insight about {keyword}
3. Quick tip for {keyword} implementation
4. Data point or statistic about {keyword}
5. Contrarian take on {keyword}

Write 5 individual tweets now:""",

        "educational_thread": f"""
Create a Twitter thread about {keyword} implementation.

REQUIREMENTS:
- Write as Anoop Kurup (@anoopkurup)
- 7-10 tweets in thread format
- Each tweet under 280 characters
- Start with hook tweet
- Educational/tutorial style
- Include actionable steps
- Professional but accessible tone
- End with clear CTA
- Use 2-3 hashtags total

THREAD TOPIC:
"🧵 How to implement {keyword} systematically (7-step process)"

THREAD STRUCTURE:
Tweet 1: Hook + thread preview
Tweets 2-8: Each step with brief explanation
Tweet 9: Common mistakes to avoid
Tweet 10: Next steps + CTA

Write the complete thread now:""",

        "quote_tweets": f"""
Create 3 quote-worthy statements about {keyword} for Twitter.

REQUIREMENTS:
- Write as thought-provoking quotes
- Under 200 characters each
- Suitable for quote graphics
- Professional business focus
- Contrarian or insightful angle
- Include relevant hashtags

QUOTE THEMES:
1. Contrarian perspective on {keyword}
2. Practical wisdom about {keyword}
3. Systems thinking approach to {keyword}

Write 3 quoteable tweets now:"""
    }
    
    return twitter_prompts

def create_newsletter_content_prompts(article_data, repurposer):
    """Create prompts for newsletter content generation using Claude"""
    
    keyword = article_data.get('keyword', '')
    
    newsletter_prompts = {
        "main_newsletter": f"""
Create a newsletter issue based on the {keyword} article.

REQUIREMENTS:
- Write as Anoop Kurup for existing subscribers
- Personal, conversational tone
- 600-800 words total
- Include personal update/greeting
- One main insight about {keyword}
- Practical implementation tip
- Resource recommendation
- Clear call-to-action
- P.S. with additional value

NEWSLETTER STRUCTURE:
Subject Line: [Create compelling subject]
Personal Update: [Brief personal note]
Main Insight: [Key lesson about {keyword}]
Implementation Tip: [Actionable advice]
Resource: [Tool or resource recommendation]
CTA: [Workshop, consultation, or content]
P.S.: [Additional value or insight]

Write the complete newsletter now:""",

        "newsletter_sequence": f"""
Create a 3-part newsletter sequence about {keyword}.

REQUIREMENTS:
- Write as Anoop Kurup for subscribers
- Personal, educational tone
- Each newsletter 400-500 words
- Build on each other progressively
- Include clear next steps
- Focus on implementation

SEQUENCE STRUCTURE:
Email 1: Problem identification + framework overview
Email 2: Step-by-step implementation
Email 3: Advanced tips + case study

Write all 3 newsletters now:"""
    }
    
    return newsletter_prompts

def create_instagram_content_prompts(article_data, repurposer):
    """Create prompts for Instagram content generation using Claude"""
    
    keyword = article_data.get('keyword', '')
    
    instagram_prompts = {
        "carousel_post": f"""
Create an Instagram carousel post about {keyword}.

REQUIREMENTS:
- 8-10 slides of educational content
- Each slide: headline + 2-3 bullet points
- Professional but visually engaging
- Include actionable insights
- Suitable for graphic design
- Caption: 1,500-2,200 characters
- Include 15-20 relevant hashtags

CAROUSEL TOPIC:
"The Complete Guide to {keyword} for Business Owners"

SLIDE STRUCTURE:
Slide 1: Hook + preview
Slides 2-8: Key concepts/steps
Slide 9: Common mistakes
Slide 10: Next steps + CTA

Write carousel content and caption now:""",

        "story_highlights": f"""
Create Instagram Story content about {keyword} for Highlights.

REQUIREMENTS:
- 12-15 story frames
- Brief, scannable text
- Include polls, questions, or interactive elements
- Professional business focus
- Suitable for "Marketing Tips" highlight

STORY SEQUENCE:
- Introduction to {keyword}
- Why it matters
- Key steps/tips
- Common mistakes
- Resources
- CTA

Write story sequence now:"""
    }
    
    return instagram_prompts

# -------------------------------
# 5. Content Generation Framework
# -------------------------------
def generate_claude_prompts_for_all_platforms(article_data):
    """Generate comprehensive prompts for all social media platforms"""
    
    repurposer = ClaudeSocialMediaRepurposer(article_data, SocialMediaPlatforms)
    
    all_prompts = {
        "article_summary": {
            "keyword": article_data.get('keyword', ''),
            "title": article_data.get('metadata', {}).get('title', ''),
            "key_insights": repurposer.key_insights,
            "main_takeaways": repurposer.main_takeaways
        },
        "linkedin": create_linkedin_content_prompts(article_data, repurposer),
        "twitter": create_twitter_content_prompts(article_data, repurposer),
        "newsletter": create_newsletter_content_prompts(article_data, repurposer),
        "instagram": create_instagram_content_prompts(article_data, repurposer),
        "platform_guidelines": {
            "linkedin": SocialMediaPlatforms.LINKEDIN,
            "twitter": SocialMediaPlatforms.TWITTER,
            "newsletter": SocialMediaPlatforms.NEWSLETTER,
            "instagram": SocialMediaPlatforms.INSTAGRAM
        }
    }
    
    return all_prompts

# -------------------------------
# 6. Output Generation & Management
# -------------------------------
def create_social_media_prompt_file(prompts_data, keyword):
    """Create a comprehensive prompt file for Claude social media generation"""
    
    prompt_content = f"""# Social Media Content Generation Prompts
# Keyword: {keyword}

## Article Summary
**Keyword**: {prompts_data['article_summary']['keyword']}
**Article Title**: {prompts_data['article_summary']['title']}

## IMPORTANT: Claude Usage Instructions

1. **Choose Your Platform**: Select one platform at a time from the sections below
2. **Copy the Prompt**: Copy the complete prompt for your chosen content type
3. **Use Claude Code**: Paste into Claude Code and generate the content
4. **Save Results**: Save Claude's output for each platform
5. **Repeat**: Continue with other platforms as needed

---

# LINKEDIN CONTENT PROMPTS

## LinkedIn Insight Post
{prompts_data['linkedin']['insight_post']}

---

## LinkedIn Educational Thread  
{prompts_data['linkedin']['educational_thread']}

---

## LinkedIn Case Study
{prompts_data['linkedin']['case_study_summary']}

---

## LinkedIn Article
{prompts_data['linkedin']['linkedin_article']}

---

# TWITTER CONTENT PROMPTS

## Twitter Insight Tweets
{prompts_data['twitter']['insight_tweets']}

---

## Twitter Educational Thread
{prompts_data['twitter']['educational_thread']}

---

## Twitter Quote Tweets
{prompts_data['twitter']['quote_tweets']}

---

# NEWSLETTER CONTENT PROMPTS

## Main Newsletter Issue
{prompts_data['newsletter']['main_newsletter']}

---

## Newsletter Sequence
{prompts_data['newsletter']['newsletter_sequence']}

---

# INSTAGRAM CONTENT PROMPTS

## Instagram Carousel
{prompts_data['instagram']['carousel_post']}

---

## Instagram Stories
{prompts_data['instagram']['story_highlights']}

---

# PLATFORM GUIDELINES REFERENCE

## LinkedIn Best Practices
- Character limits: {prompts_data['platform_guidelines']['linkedin']['character_limits']}
- Best practices: {', '.join(prompts_data['platform_guidelines']['linkedin']['best_practices'])}
- Optimal timing: {prompts_data['platform_guidelines']['linkedin']['optimal_timing']}

## Twitter Best Practices  
- Character limits: {prompts_data['platform_guidelines']['twitter']['character_limits']}
- Best practices: {', '.join(prompts_data['platform_guidelines']['twitter']['best_practices'])}
- Optimal timing: {prompts_data['platform_guidelines']['twitter']['optimal_timing']}

## Newsletter Best Practices
- Best practices: {', '.join(prompts_data['platform_guidelines']['newsletter']['best_practices'])}
- Target length: {prompts_data['platform_guidelines']['newsletter']['target_length']}
- Optimal frequency: {prompts_data['platform_guidelines']['newsletter']['optimal_frequency']}

## Instagram Best Practices
- Content types: {', '.join(prompts_data['platform_guidelines']['instagram']['content_types'])}
- Best practices: {', '.join(prompts_data['platform_guidelines']['instagram']['best_practices'])}

---

# USAGE NOTES

- Use these prompts with Claude Code for best results
- Each prompt is optimized for Claude's capabilities
- Maintain consistent brand voice across all platforms
- Adapt content based on platform-specific best practices
- Test and iterate based on engagement metrics

---

*Generated by ContentEngine Claude Integration*
"""
    
    return prompt_content

# -------------------------------
# 7. Main Execution
# -------------------------------
def main():
    print("📖 Loading article content for social media repurposing...")
    
    # Load the article data
    try:
        with open(ARTICLE_FILE, "r") as f:
            article_data = json.load(f)
            
        keyword = article_data.get('keyword', 'Unknown')
        print(f"✅ Loaded article: {keyword}")
        
        if 'article_content' not in article_data:
            print("⚠️  Article content not found. Make sure ArticleWriter_Claude.py has been run successfully.")
            print("    Using article structure for prompt generation...")
            
    except FileNotFoundError:
        print(f"❌ Article file not found: {ARTICLE_FILE}")
        print("Please run ArticleWriter_Claude.py first to generate article content")
        return
    except Exception as e:
        print(f"❌ Error loading article: {e}")
        return
    
    print(f"\n🎯 Preparing social media repurposing for: {keyword}")
    print(f"📱 Target platforms: LinkedIn, Twitter, Newsletter, Instagram")
    
    # Generate comprehensive prompts for all platforms
    print("\n🤖 Generating Claude prompts for social media platforms...")
    all_prompts = generate_claude_prompts_for_all_platforms(article_data)
    
    # Create the comprehensive prompt file
    prompt_file_content = create_social_media_prompt_file(all_prompts, keyword)
    
    # Save prompt file
    prompt_filename = f"claude_social_prompts_{keyword.lower().replace(' ', '_')}.md"
    with open(prompt_filename, "w") as f:
        f.write(prompt_file_content)
    
    # Create output structure
    output_data = {
        "keyword": keyword,
        "article_metadata": article_data.get('metadata', {}),
        "social_media_strategy": {
            "platforms": ["LinkedIn", "Twitter", "Newsletter", "Instagram"],
            "content_types_per_platform": {
                "linkedin": ["Insight Posts", "Educational Threads", "Case Studies", "Long-form Articles"],
                "twitter": ["Insight Tweets", "Educational Threads", "Quote Tweets"],
                "newsletter": ["Main Issues", "Email Sequences"],
                "instagram": ["Carousel Posts", "Story Highlights"]
            },
            "total_content_pieces": 15
        },
        "claude_prompts": all_prompts,
        "generation_method": "Claude Code Integration",
        "prompt_file": prompt_filename,
        "status": "Ready for Claude content generation",
        "next_steps": [
            f"Open {prompt_filename} for detailed prompts",
            "Use Claude Code to generate content for each platform",
            "Save generated content for publishing",
            "Continue with YouTubeScript_Claude.py for video content"
        ]
    }
    
    # Save JSON output
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n💾 Files created:")
    print(f"   📝 {prompt_filename} - Complete social media prompts for Claude")
    print(f"   📊 {OUTPUT_JSON} - Social media strategy and framework")
    
    print(f"\n🤖 CLAUDE CODE INTEGRATION")
    print("=" * 50)
    print("Social media content prompts have been prepared. Here's how to use them:")
    print()
    print("📋 STEP-BY-STEP PROCESS:")
    print(f"1. Open the file: {prompt_filename}")
    print("2. Choose a platform section (LinkedIn, Twitter, etc.)")
    print("3. Copy the specific prompt for the content type you want")
    print("4. Paste into Claude Code and generate content")
    print("5. Save Claude's response")
    print("6. Repeat for other platforms/content types")
    print()
    print("📱 CONTENT BREAKDOWN:")
    print("   LinkedIn: 4 content types (posts, threads, case studies, articles)")
    print("   Twitter: 3 content types (tweets, threads, quotes)")
    print("   Newsletter: 2 content types (main issues, sequences)")
    print("   Instagram: 2 content types (carousels, stories)")
    print()
    print(f"✅ Total: 15+ pieces of social media content ready for generation")
    print()
    print("🎉 Ready for Claude Code social media generation!")
    print("   Use the prompts to create platform-optimized content")
    print("   Then continue with YouTubeScript_Claude.py for video content")

def process_social_media_content(platform_content, platform_name, article_file=None):
    """
    Helper function to process social media content after it's been generated by Claude Code.
    Use this after getting the social media content from Claude.
    """
    
    if article_file is None:
        article_file = ARTICLE_FILE
    
    # Load original article data
    with open(article_file, "r") as f:
        article_data = json.load(f)
    
    processed_content = {
        "platform": platform_name,
        "keyword": article_data.get('keyword', ''),
        "content": platform_content,
        "generation_method": "Claude Code Integration",
        "processing_date": time.strftime('%Y-%m-%d %H:%M:%S'),
        "character_count": len(platform_content),
        "status": "Ready for publishing"
    }
    
    # Save processed content
    output_filename = f"social_content_{platform_name.lower()}_{article_data.get('keyword', 'unknown').replace(' ', '_')}.json"
    with open(output_filename, "w") as f:
        json.dump(processed_content, f, indent=2)
    
    print(f"✅ {platform_name} content processed and saved: {output_filename}")
    
    return processed_content

if __name__ == "__main__":
    main()