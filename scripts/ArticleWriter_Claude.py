import json
import re
import os
import time
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
BRIEF_FILE = os.getenv("ARTICLE_BRIEFS_FILE", "article_briefs_claude.json")
WRITING_INSTRUCTIONS_FILE = "Writing Instructions.md"

# Output files with Claude suffix
OUTPUT_JSON = "article_draft_claude.json"
OUTPUT_MD = "article_draft_claude.md"

print("✍️  ContentEngine - Article Writer (Claude-Powered)")
print(f"🤖 Using {CONTENT_GENERATOR.upper()} for content generation")
print(f"🎯 Quality Setting: {CLAUDE_MODEL_PREFERENCE}")
print("")

# -------------------------------
# 2. Load Inputs & Instructions
# -------------------------------
def load_writing_instructions():
    """Load and parse the Writing Instructions.md file"""
    try:
        with open(WRITING_INSTRUCTIONS_FILE, "r") as f:
            content = f.read()
            
        instructions = {
            "brand_voice": "Professional yet approachable, data-driven, practical, no-fluff, systems-focused",
            "target_audience": "Professional service firms, tech-enabled businesses, independent consultants in India",
            "content_themes": [
                "Marketing strategy and positioning", "Lead generation systems", 
                "AI-powered marketing workflows", "Personal branding for service businesses"
            ],
            "article_length": "1,500-2,500 words",
            "tone": "Professional but conversational, direct and practical, confident but not arrogant",
            "style_preferences": [
                "First person (as Anoop Kurup)", "Active voice", "Short paragraphs (2-3 sentences)",
                "Specific examples", "Avoid buzzwords"
            ],
            "seo_requirements": [
                "Primary keyword in title, first paragraph, and 1-2 H2 headings",
                "Secondary keywords naturally distributed", "2-3 internal links",
                "1-2 external authoritative sources"
            ]
        }
        
        print("✅ Writing instructions loaded from Writing Instructions.md")
        return instructions
        
    except FileNotFoundError:
        print("⚠️  Writing Instructions.md not found, using default guidelines")
        return {
            "brand_voice": "Professional, data-driven, practical",
            "target_audience": "Business professionals in India",
            "tone": "Professional but conversational"
        }

def load_article_brief():
    """Load the Claude-generated article brief"""
    try:
        with open(BRIEF_FILE, "r") as f:
            briefs = json.load(f)
            
        if not briefs:
            raise ValueError("No briefs found in file")
            
        # For this demo, use the first brief (in production, allow selection)
        selected_brief = briefs[0]
        print(f"✅ Loaded brief for: {selected_brief['keyword']} ({selected_brief['role']})")
        return selected_brief
        
    except FileNotFoundError:
        print(f"❌ Brief file not found: {BRIEF_FILE}")
        print("Please run ArticleBrief_Claude.py first to generate content briefs")
        return None
    except Exception as e:
        print(f"❌ Error loading brief: {e}")
        return None

# -------------------------------
# 3. Claude Content Generation Framework
# -------------------------------
class ClaudeArticleWriter:
    """
    Framework for generating articles using Claude Code's conversational interface.
    This class structures the content generation process into manageable components.
    """
    
    def __init__(self, brief, instructions):
        self.brief = brief
        self.instructions = instructions
        self.keyword = brief['keyword']
        self.role = brief['role']
        self.article_outline = brief['article_outline']
        self.seo_strategy = brief['seo_optimization']
        self.claude_insights = brief['claude_insights']
        
    def generate_article_metadata(self):
        """Generate article metadata including title, description, tags"""
        
        # Use the title from the brief
        title = self.article_outline['title']
        
        # Generate meta description
        meta_description = f"Learn {self.keyword} with this comprehensive guide. " + \
                          f"Practical strategies for {self.instructions['target_audience'].split(',')[0].strip()}. " + \
                          f"Systems-focused approach with real results."
        
        # Truncate meta description if too long
        if len(meta_description) > 160:
            meta_description = meta_description[:157] + "..."
            
        # Generate tags based on keyword and cluster
        tags = [
            self.keyword,
            "marketing strategy",
            "business growth"
        ]
        
        # Add location tag if relevant
        if "India" in self.instructions.get('target_audience', ''):
            tags.append("India business")
        
        # Calculate estimated reading time (average 200 words per minute)
        estimated_word_count = 2000  # Based on target length
        reading_time = f"{round(estimated_word_count / 200)} min read"
        
        metadata = {
            "title": title,
            "meta_description": meta_description,
            "tags": tags,
            "reading_time": reading_time,
            "author": "Anoop Kurup",
            "keyword": self.keyword,
            "content_type": self.role,
            "target_audience": self.instructions['target_audience'],
            "publication_date": time.strftime('%Y-%m-%d'),
            "slug": self.keyword.lower().replace(' ', '-'),
            "category": "Marketing Strategy"
        }
        
        return metadata
    
    def create_claude_writing_prompt(self):
        """Create a comprehensive prompt for Claude to write the article"""
        
        # Extract key information from brief
        outline = self.article_outline
        competitive_insights = self.brief['serp_analysis']
        content_strategy = self.brief['content_strategy']
        internal_links = self.brief['internal_linking']
        
        prompt = f"""I need you to write a comprehensive {self.role.lower()} article about "{self.keyword}" following specific brand guidelines and competitive positioning.

## ARTICLE REQUIREMENTS

**Target Keyword**: {self.keyword}
**Article Type**: {self.role}
**Target Length**: {self.instructions.get('article_length', '1,500-2,500 words')}
**Target Audience**: {self.instructions['target_audience']}

## BRAND VOICE & STYLE

**Brand Voice**: {self.instructions['brand_voice']}
**Tone**: {self.instructions.get('tone', 'Professional but conversational')}

**Writing Style Requirements**:
- Write in first person as Anoop Kurup, a marketing consultant
- Use active voice and short paragraphs (2-3 sentences max)
- Include specific examples and avoid generic buzzwords
- Focus on practical implementation over theory
- Maintain an anti-hype, realistic approach
- Include data-driven insights when possible

## COMPETITIVE POSITIONING

**Unique Angle**: {content_strategy['primary_angle']}
**Differentiation**: {content_strategy['unique_positioning']}

**Content Gaps to Fill** (things competitors miss):
{chr(10).join(f'- {gap}' for gap in self.claude_insights['content_gaps'])}

**Top Competitors Cover** (for reference, not copying):
{chr(10).join(f'- {title}' for title in competitive_insights['top_competitor_titles'][:3])}

## DETAILED ARTICLE OUTLINE

**Main Title**: {outline['title']}
**Subtitle**: {outline['subtitle']}

### Article Structure:
"""

        # Add detailed outline sections
        for i, section in enumerate(outline['structure'], 1):
            prompt += f"""
{i}. **{section['heading']}** ({section['section']})
   Content to cover:
   {chr(10).join(f'   - {point}' for point in section['content_points'])}
"""

        prompt += f"""

## SEO OPTIMIZATION

**Primary Keyword**: Include "{self.keyword}" in:
- Article title (already done)
- First paragraph naturally
- At least 2 H2 headings
- Throughout content with 1-2% density

**Secondary Keywords** to include naturally:
{chr(10).join(f'- {kw}' for kw in self.seo_strategy['content_optimization']['semantic_keywords'])}

## INTERNAL LINKING

Include these internal links naturally within the content:
"""

        for link in internal_links:
            prompt += f"- [{link['anchor_text']}]({link['target_url']}) - {link['context']} ({link['placement']})\n"

        prompt += f"""

## CONTENT REQUIREMENTS

1. **Hook Opening**: Start with a relatable problem or specific scenario that draws readers in
2. **Problem Definition**: Clearly articulate the challenges your audience faces
3. **Systematic Solution**: Present your approach as a system/framework, not just tips
4. **Practical Implementation**: Include specific steps, tools, and processes
5. **Evidence/Proof**: Add a case study or example (can be anonymized)
6. **Clear Next Steps**: End with 2-3 specific actions readers can take

## TARGET AUDIENCE CONTEXT

**Primary Audience**: {self.claude_insights['target_audience_focus']['primary']}
**Key Pain Points**:
{chr(10).join(f'- {pain}' for pain in self.claude_insights['target_audience_focus']['pain_points'])}

**Their Goals**:
{chr(10).join(f'- {goal}' for goal in self.claude_insights['target_audience_focus']['goals'])}

## FORMATTING REQUIREMENTS

- Use Markdown formatting
- Include H2 and H3 headings as outlined
- Add bullet points and numbered lists for readability
- Include a brief author bio at the end
- Add a subtle call-to-action for consultation or workshop

## FINAL CHECKLIST

Please ensure the article:
- ✅ Follows the exact outline structure provided
- ✅ Maintains Anoop Kurup's brand voice throughout
- ✅ Includes primary keyword naturally (not stuffed)
- ✅ Provides practical, actionable advice
- ✅ Differentiates from competitor approaches
- ✅ Includes internal links contextually
- ✅ Ends with clear next steps
- ✅ Is comprehensive yet scannable

Write the complete article now, following this prompt exactly."""

        return prompt

    def generate_article_structure(self):
        """Generate the basic article structure that Claude will fill"""
        
        structure = {
            "front_matter": self.generate_front_matter(),
            "sections": [],
            "meta_data": self.generate_article_metadata()
        }
        
        # Convert outline to structured sections
        for section in self.article_outline['structure']:
            section_data = {
                "heading": section['heading'],
                "type": section['section'],
                "content_points": section['content_points'],
                "word_target": self.calculate_section_word_target(section['section'])
            }
            structure["sections"].append(section_data)
        
        return structure
    
    def generate_front_matter(self):
        """Generate YAML front matter for the article"""
        
        metadata = self.generate_article_metadata()
        
        front_matter = f"""---
title: "{metadata['title']}"
date: {metadata['publication_date']}
description: "{metadata['meta_description']}"
tags: {json.dumps(metadata['tags'])}
read_time: "{metadata['reading_time']}"
author: "{metadata['author']}"
category: "{metadata['category']}"
keyword: "{metadata['keyword']}"
content_type: "{metadata['content_type']}"
slug: "{metadata['slug']}"
---"""
        
        return front_matter
    
    def calculate_section_word_target(self, section_type):
        """Calculate target word count for each section type"""
        
        total_target = 2000  # Target article length
        
        word_distribution = {
            "Hook Opening": 200,
            "Problem Definition": 300, 
            "Framework Overview": 400,
            "Deep Dive": 500,
            "Implementation": 350,
            "Case Study": 250,
            "Implementation Guide": 200,
            "Conclusion": 150
        }
        
        return word_distribution.get(section_type, 300)

# -------------------------------
# 4. Article Generation & Processing
# -------------------------------
def create_claude_instructions_summary(brief, instructions):
    """Create a summary of instructions for the user to reference when writing with Claude"""
    
    summary = f"""
# Claude Article Writing Session Guide

## Quick Reference for Writing with Claude

**Article**: {brief['keyword']} ({brief['role']})
**Target Length**: 1,500-2,500 words
**Brand Voice**: {instructions['brand_voice']}

## Key Points to Emphasize:
- Systems-focused approach (not just tips)
- Indian market context
- First-person perspective as Anoop Kurup
- Practical, anti-hype methodology
- Data-driven insights

## Content Structure Required:
1. Hook opening with specific problem
2. Problem definition with pain points
3. Systematic framework presentation
4. Implementation details
5. Case study or proof
6. Clear next steps

## SEO Requirements:
- Include "{brief['keyword']}" naturally throughout
- Use these semantic keywords: {', '.join(brief['seo_optimization']['content_optimization']['semantic_keywords'][:3])}
- Add internal links to related content

## Competitive Advantage:
{brief['claude_insights']['differentiation_angle']}

## Content Gaps to Fill:
{chr(10).join(f'- {gap}' for gap in brief['claude_insights']['content_gaps'])}
"""
    
    return summary

def process_claude_generated_content(content, metadata):
    """Process and structure the article content generated by Claude"""
    
    # Add front matter if not present
    if not content.strip().startswith('---'):
        front_matter = f"""---
title: "{metadata['title']}"
date: {metadata['publication_date']}
description: "{metadata['meta_description']}"
tags: {json.dumps(metadata['tags'])}
read_time: "{metadata['reading_time']}"
author: "{metadata['author']}"
category: "{metadata['category']}"
keyword: "{metadata['keyword']}"
slug: "{metadata['slug']}"
---

"""
        content = front_matter + content
    
    # Calculate actual word count
    word_count = len(re.findall(r'\b\w+\b', content))
    reading_time = f"{round(word_count / 200)} min read"
    
    # Update metadata with actual metrics
    metadata.update({
        "actual_word_count": word_count,
        "actual_reading_time": reading_time,
        "generation_method": "Claude Code Integration",
        "processing_date": time.strftime('%Y-%m-%d %H:%M:%S')
    })
    
    return content, metadata

# -------------------------------
# 5. Main Execution
# -------------------------------
def main():
    print("📚 Loading article brief and writing instructions...")
    
    # Load inputs
    brief = load_article_brief()
    if not brief:
        return
    
    instructions = load_writing_instructions()
    
    # Initialize Claude writer
    writer = ClaudeArticleWriter(brief, instructions)
    
    print(f"\n🎯 Preparing to write: {brief['keyword']} ({brief['role']})")
    print(f"📋 Competitive analysis: {brief['serp_analysis']['total_competitors']} competitors analyzed")
    print(f"💡 Content gaps identified: {len(brief['claude_insights']['content_gaps'])}")
    print(f"🔗 Internal links planned: {len(brief['internal_linking'])}")
    
    # Generate metadata
    metadata = writer.generate_article_metadata()
    print(f"\n📊 Article Metadata:")
    print(f"   📝 Title: {metadata['title']}")
    print(f"   📏 Target Length: {instructions.get('article_length', '1,500-2,500 words')}")
    print(f"   👥 Audience: {metadata['target_audience']}")
    print(f"   🏷️  Tags: {', '.join(metadata['tags'])}")
    
    # Create writing prompt for Claude
    claude_prompt = writer.create_claude_writing_prompt()
    
    # Create instructions summary
    instructions_summary = create_claude_instructions_summary(brief, instructions)
    
    print(f"\n🤖 CLAUDE CODE INTEGRATION")
    print("=" * 50)
    print("The article writing prompt has been prepared. Here are your options:")
    print()
    print("OPTION 1: Interactive Claude Writing")
    print("- Copy the prompt below and paste it into Claude Code")
    print("- Claude will write the complete article following all specifications")
    print("- Save Claude's response to continue with the pipeline")
    print()
    print("OPTION 2: Use Generated Framework")
    print("- Use the structured outline and metadata provided")
    print("- Write sections manually using the guidelines")
    print("- Combine with the processing functions")
    print()
    
    # Save the prompt and instructions for easy access
    with open("claude_writing_prompt.md", "w") as f:
        f.write("# Claude Article Writing Prompt\n\n")
        f.write(claude_prompt)
        f.write("\n\n---\n\n")
        f.write("# Writing Session Guide\n")
        f.write(instructions_summary)
    
    print("💾 Files created:")
    print(f"   📝 claude_writing_prompt.md - Complete writing prompt for Claude")
    print()
    print("📋 NEXT STEPS:")
    print("1. Open Claude Code in your browser")
    print("2. Copy the prompt from 'claude_writing_prompt.md'")
    print("3. Paste into Claude Code and let it write the article")
    print("4. Save Claude's response as the article content")
    print("5. Run the processing function to finalize")
    print()
    
    # Create a placeholder article structure for demonstration
    demo_article_structure = writer.generate_article_structure()
    
    # Save structured output for reference
    output_data = {
        "metadata": metadata,
        "brief_summary": {
            "keyword": brief['keyword'],
            "role": brief['role'],
            "differentiation_angle": brief['claude_insights']['differentiation_angle'],
            "content_gaps": brief['claude_insights']['content_gaps']
        },
        "article_structure": demo_article_structure,
        "claude_prompt": claude_prompt,
        "instructions_summary": instructions_summary,
        "generation_method": "Claude Code Integration",
        "status": "Ready for Claude writing",
        "next_steps": [
            "Use Claude Code to generate article content",
            "Process generated content through this pipeline", 
            "Continue with SocialMedia_Claude.py for repurposing"
        ]
    }
    
    # Save JSON output
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✅ Article writing framework saved: {OUTPUT_JSON}")
    print()
    print("🎉 Ready for Claude Code article generation!")
    print("   Use the prompt in claude_writing_prompt.md with Claude Code")
    print("   Then continue with the social media repurposing pipeline")

def process_claude_article(article_content, brief_file=None):
    """
    Helper function to process an article after it's been written by Claude Code.
    Use this after getting the article content from Claude.
    """
    
    if brief_file is None:
        brief_file = BRIEF_FILE
    
    # Load the original brief for metadata
    with open(brief_file, "r") as f:
        briefs = json.load(f)
    brief = briefs[0]  # Use first brief
    
    # Load instructions
    instructions = load_writing_instructions()
    
    # Create writer instance
    writer = ClaudeArticleWriter(brief, instructions)
    metadata = writer.generate_article_metadata()
    
    # Process the article content
    processed_content, final_metadata = process_claude_generated_content(article_content, metadata)
    
    # Create final output
    final_output = {
        "keyword": brief['keyword'],
        "role": brief['role'],
        "article_content": processed_content,
        "metadata": final_metadata,
        "brief_data": brief,
        "generation_method": "Claude Code Integration",
        "processing_complete": True
    }
    
    # Save processed article
    with open(OUTPUT_JSON, "w") as f:
        json.dump(final_output, f, indent=2)
    
    # Save markdown version
    with open(OUTPUT_MD, "w") as f:
        f.write(processed_content)
    
    print(f"✅ Article processed and saved:")
    print(f"   📊 JSON: {OUTPUT_JSON}")
    print(f"   📝 Markdown: {OUTPUT_MD}")
    print(f"   📏 Word count: {final_metadata['actual_word_count']}")
    print(f"   ⏱️  Reading time: {final_metadata['actual_reading_time']}")
    
    return final_output

if __name__ == "__main__":
    main()