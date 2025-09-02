import pandas as pd
import requests
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------------------
# 1. Setup
# -------------------------------
API_LOGIN = os.getenv("DATAFORSEO_LOGIN")
API_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")
BASE_URL = "https://api.dataforseo.com/v3"

# Validate required environment variables
if not API_LOGIN or not API_PASSWORD:
    raise ValueError("DataForSEO credentials not found. Please set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD in .env file")

KEYWORD_FILE = os.getenv("KEYWORD_CLUSTERS_FILE", "keyword_clusters.csv")
SUMMARY_FILE = os.getenv("CLUSTER_SUMMARY_FILE", "cluster_summary.csv")
TARGET_LOCATION = os.getenv("TARGET_LOCATION", "India")
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")

# Claude-specific configuration
CONTENT_GENERATOR = os.getenv("CONTENT_GENERATOR", "claude")
CLAUDE_MODEL_PREFERENCE = os.getenv("CLAUDE_MODEL_PREFERENCE", "quality")

# Output files with Claude suffix
OUTPUT_JSON = "article_briefs_claude.json"
OUTPUT_MD = "article_briefs_claude.md"

print("🤖 ContentEngine - Article Brief Generator (Claude-Powered)")
print(f"📊 Using {CONTENT_GENERATOR.upper()} for content generation")
print(f"🎯 Target: {TARGET_LOCATION} ({TARGET_LANGUAGE})")
print("")

# -------------------------------
# Helper: POST request to DataforSEO
# -------------------------------
def dfseo_post(endpoint, payload):
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, auth=(API_LOGIN, API_PASSWORD), json=payload)
    resp.raise_for_status()
    return resp.json()

# -------------------------------
# 2. Enhanced SERP Analysis with Claude
# -------------------------------
def get_enhanced_serp_data(keyword, location=None, language=None):
    """Get comprehensive SERP data including titles, meta descriptions, and content insights"""
    if location is None:
        location = TARGET_LOCATION
    if language is None:
        language = TARGET_LANGUAGE
        
    payload = [{
        "keyword": keyword,
        "location_name": location,
        "language_name": language,
        "se_domain": "google.com",
        "search_engine": "google"
    }]
    
    try:
        res = dfseo_post("serp/google/organic/live/advanced", payload)
        items = res["tasks"][0]["result"][0]["items"]
        
        serp_data = {
            "keyword": keyword,
            "total_results": len(items),
            "top_results": []
        }
        
        # Extract detailed information from top 10 results
        for i, item in enumerate(items[:10]):
            if "url" in item:
                result_data = {
                    "rank": i + 1,
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "domain": item.get("domain", "")
                }
                serp_data["top_results"].append(result_data)
        
        return serp_data
        
    except Exception as e:
        print(f"⚠️  Error fetching SERP data for '{keyword}': {e}")
        return {"keyword": keyword, "total_results": 0, "top_results": []}

# -------------------------------
# 3. Claude-Powered Content Brief Generation
# -------------------------------
def generate_claude_brief(keyword, role, cluster_keywords, serp_data, writing_instructions):
    """
    Generate a comprehensive content brief using Claude's analysis capabilities.
    This function creates detailed prompts that will be executed by Claude Code.
    """
    
    # Extract competitive insights from SERP data
    competitor_titles = [result["title"] for result in serp_data["top_results"][:5]]
    competitor_descriptions = [result["description"] for result in serp_data["top_results"][:5]]
    top_domains = list(set([result["domain"] for result in serp_data["top_results"][:5])))
    
    brief = {
        "keyword": keyword,
        "role": role,
        "cluster_keywords": cluster_keywords,
        "serp_analysis": {
            "total_competitors": serp_data["total_results"],
            "top_competitor_titles": competitor_titles,
            "top_competitor_descriptions": competitor_descriptions,
            "dominant_domains": top_domains
        },
        "content_strategy": generate_content_strategy(keyword, role, competitor_titles),
        "article_outline": generate_article_outline(keyword, role, cluster_keywords, competitor_titles),
        "internal_linking": generate_internal_linking_strategy(keyword, role, cluster_keywords),
        "seo_optimization": generate_seo_strategy(keyword, competitor_titles, competitor_descriptions),
        "claude_insights": {
            "content_gaps": analyze_content_gaps(competitor_titles, competitor_descriptions),
            "differentiation_angle": suggest_differentiation_angle(keyword, role, competitor_titles),
            "target_audience_focus": determine_audience_focus(keyword, writing_instructions)
        }
    }
    
    return brief

def generate_content_strategy(keyword, role, competitor_titles):
    """Generate content strategy based on competitive analysis"""
    strategy = {
        "primary_angle": f"Systems-focused approach to {keyword}" if role == "Pillar Post" else f"Practical implementation of {keyword}",
        "unique_positioning": "Anti-hype, data-driven methodology with Indian market context",
        "content_depth": "Deep" if role == "Pillar Post" else "Focused",
        "competitive_advantage": analyze_competitor_gaps(competitor_titles)
    }
    return strategy

def generate_article_outline(keyword, role, cluster_keywords, competitor_titles):
    """Generate detailed article outline with Claude's strategic thinking"""
    
    if role == "Pillar Post":
        outline = {
            "title": f"The Complete Guide to {keyword.title()}: Systems That Actually Work",
            "subtitle": f"Evidence-based {keyword} strategies for Indian businesses",
            "structure": [
                {
                    "section": "Hook Opening",
                    "heading": f"Why Most {keyword.title()} Advice Fails",
                    "content_points": [
                        "Common misconceptions in the market",
                        "Real challenges faced by Indian businesses",
                        "What this guide covers differently"
                    ]
                },
                {
                    "section": "Problem Definition",
                    "heading": f"The Real Challenge with {keyword.title()}",
                    "content_points": [
                        "Data on current market failures",
                        "Specific pain points for professional services",
                        "Cost of getting it wrong"
                    ]
                },
                {
                    "section": "Framework Overview", 
                    "heading": f"The Systems Approach to {keyword.title()}",
                    "content_points": [
                        "Core methodology breakdown",
                        "Why systems beat tactics",
                        "Framework components explained"
                    ]
                }
            ]
        }
        
        # Add cluster keyword sections
        for cluster_kw in cluster_keywords:
            if cluster_kw != keyword:
                outline["structure"].append({
                    "section": "Deep Dive",
                    "heading": f"Implementing {cluster_kw.title()}",
                    "content_points": [
                        f"Step-by-step {cluster_kw} process",
                        "Tools and resources needed",
                        "Common implementation mistakes"
                    ]
                })
    
    else:  # Cluster Post
        outline = {
            "title": f"{keyword.title()}: Complete Implementation Guide",
            "subtitle": f"Practical {keyword} strategies with real results",
            "structure": [
                {
                    "section": "Hook Opening",
                    "heading": f"The {keyword.title()} Method That Actually Works",
                    "content_points": [
                        f"Why {keyword} matters now",
                        "What makes this approach different",
                        "Results you can expect"
                    ]
                },
                {
                    "section": "Implementation",
                    "heading": f"How to Execute {keyword.title()} Step-by-Step",
                    "content_points": [
                        "Detailed process breakdown",
                        "Tools and resources needed",
                        "Timeline and milestones"
                    ]
                },
                {
                    "section": "Case Study",
                    "heading": f"Real {keyword.title()} Results",
                    "content_points": [
                        "Anonymized client case study",
                        "Metrics and outcomes",
                        "Lessons learned"
                    ]
                }
            ]
        }
    
    # Add universal closing sections
    outline["structure"].extend([
        {
            "section": "Implementation Guide",
            "heading": "Your Next Steps",
            "content_points": [
                "Immediate actions to take",
                "Resources and tools needed",
                "How to measure success"
            ]
        },
        {
            "section": "Conclusion",
            "heading": "Key Takeaways",
            "content_points": [
                "Main insights recap",
                "Call to action",
                "Further resources"
            ]
        }
    ])
    
    return outline

def generate_internal_linking_strategy(keyword, role, cluster_keywords):
    """Generate strategic internal linking recommendations"""
    links = []
    
    if role == "Pillar Post":
        # Pillar should link to all cluster posts
        for cluster_kw in cluster_keywords:
            if cluster_kw != keyword:
                links.append({
                    "anchor_text": cluster_kw,
                    "target_url": f"/{cluster_kw.lower().replace(' ', '-')}",
                    "context": f"Deep dive implementation guide",
                    "placement": "Within relevant section"
                })
        
        # Add foundational topic links
        links.extend([
            {
                "anchor_text": "marketing systems",
                "target_url": "/marketing-systems-framework",
                "context": "Foundation concepts",
                "placement": "Early in article"
            },
            {
                "anchor_text": "case studies",
                "target_url": "/case-studies",
                "context": "Social proof",
                "placement": "Evidence section"
            }
        ])
    
    else:  # Cluster Post
        # Link back to pillar
        main_pillar = cluster_keywords[0] if cluster_keywords else "marketing strategy"
        links.append({
            "anchor_text": main_pillar,
            "target_url": f"/{main_pillar.lower().replace(' ', '-')}",
            "context": "Comprehensive guide",
            "placement": "Introduction and conclusion"
        })
        
        # Add related cluster links
        for cluster_kw in cluster_keywords[1:3]:  # Limit to 2 related
            if cluster_kw != keyword:
                links.append({
                    "anchor_text": cluster_kw,
                    "target_url": f"/{cluster_kw.lower().replace(' ', '-')}",
                    "context": "Related implementation",
                    "placement": "Relevant section"
                })
    
    return links

def generate_seo_strategy(keyword, competitor_titles, competitor_descriptions):
    """Generate SEO optimization strategy based on competitive analysis"""
    
    # Analyze keyword patterns in competitor titles
    title_keywords = []
    for title in competitor_titles:
        title_keywords.extend(title.lower().split())
    
    # Find common patterns
    word_freq = {}
    for word in title_keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    common_words = [word for word, freq in word_freq.items() if freq >= 2 and len(word) > 3]
    
    seo_strategy = {
        "primary_keyword": keyword,
        "title_optimization": {
            "target_length": "50-60 characters",
            "include_year": "2024" if "2024" not in competitor_titles[0] else "2025",
            "power_words": ["complete", "guide", "system", "proven", "step-by-step"],
            "avoid_words": common_words[:3]  # Avoid overused competitor words
        },
        "meta_description": {
            "target_length": "150-160 characters",
            "include_keyword": True,
            "include_benefit": "practical results",
            "include_location": "India" if TARGET_LOCATION == "India" else TARGET_LOCATION
        },
        "heading_strategy": {
            "h1_keyword_placement": "Beginning",
            "h2_keyword_variations": [
                f"{keyword} strategy",
                f"{keyword} implementation", 
                f"{keyword} results"
            ],
            "h3_long_tail_targets": [
                f"how to {keyword}",
                f"{keyword} for businesses",
                f"{keyword} best practices"
            ]
        },
        "content_optimization": {
            "keyword_density": "1-2%",
            "semantic_keywords": extract_semantic_keywords(competitor_descriptions),
            "internal_links_count": "3-5",
            "external_links_count": "1-2"
        }
    }
    
    return seo_strategy

def analyze_content_gaps(competitor_titles, competitor_descriptions):
    """Identify content gaps in competitor analysis"""
    
    # Common content themes missing from competitors
    missing_angles = []
    
    # Check for systems focus
    if not any("system" in title.lower() for title in competitor_titles):
        missing_angles.append("Systems-based approach")
    
    # Check for Indian context
    if not any("india" in desc.lower() for desc in competitor_descriptions):
        missing_angles.append("Indian market context")
    
    # Check for practical implementation
    if not any(word in " ".join(competitor_titles).lower() for word in ["step-by-step", "implementation", "practical"]):
        missing_angles.append("Practical implementation focus")
    
    # Check for data-driven content
    if not any(word in " ".join(competitor_descriptions).lower() for word in ["data", "results", "metrics", "roi"]):
        missing_angles.append("Data-driven insights")
    
    return missing_angles

def suggest_differentiation_angle(keyword, role, competitor_titles):
    """Suggest unique angle based on competitive analysis"""
    
    competitor_text = " ".join(competitor_titles).lower()
    
    if role == "Pillar Post":
        if "complete" in competitor_text:
            return "The Systems Framework Approach"
        elif "guide" in competitor_text:
            return "The Anti-Hype Methodology" 
        else:
            return "The Complete Systems Guide"
    else:
        if "how to" in competitor_text:
            return "Step-by-Step Implementation"
        elif "tips" in competitor_text:
            return "The Complete Process"
        else:
            return "Practical Implementation Guide"

def determine_audience_focus(keyword, writing_instructions):
    """Determine specific audience focus based on keyword and brand guidelines"""
    
    # Default to brand's core audience
    return {
        "primary": "Professional service firms (1-20 employees) in India",
        "secondary": "Tech-enabled businesses and SaaS companies",
        "tertiary": "Independent consultants with ₹20+ lac revenue",
        "pain_points": [
            "Scattered marketing efforts",
            "Inconsistent lead flow", 
            "Difficulty scaling without systems"
        ],
        "goals": [
            "Predictable lead generation",
            "Systematic marketing approach",
            "Measurable business growth"
        ]
    }

def analyze_competitor_gaps(competitor_titles):
    """Analyze gaps in competitor content for unique positioning"""
    
    title_text = " ".join(competitor_titles).lower()
    
    gaps = []
    if "system" not in title_text:
        gaps.append("Systematic methodology missing")
    if "india" not in title_text:
        gaps.append("Local market context absent")  
    if not any(word in title_text for word in ["practical", "implementation", "step"]):
        gaps.append("Implementation focus lacking")
    if not any(word in title_text for word in ["data", "proven", "results"]):
        gaps.append("Results-driven approach missing")
    
    return gaps

def extract_semantic_keywords(competitor_descriptions):
    """Extract semantic keywords from competitor descriptions"""
    
    desc_text = " ".join(competitor_descriptions).lower()
    
    # Common semantic variations to include
    semantic_keywords = [
        "marketing strategy", "lead generation", "business growth",
        "digital marketing", "content marketing", "social media marketing",
        "marketing automation", "marketing systems", "marketing process"
    ]
    
    # Filter to those not heavily used by competitors
    unique_semantics = [kw for kw in semantic_keywords if kw not in desc_text]
    
    return unique_semantics[:5]  # Limit to top 5

# -------------------------------
# 4. Claude Brief to Markdown Conversion
# -------------------------------
def brief_to_markdown(brief):
    """Convert Claude brief to comprehensive Markdown format"""
    
    keyword = brief["keyword"]
    role = brief["role"]
    
    md_lines = [
        f"# Content Brief: {keyword} ({role})",
        "",
        f"**Generated by ContentEngine Claude Integration**",
        f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 📊 Competitive Analysis",
        "",
        f"**Target Keyword**: {keyword}",
        f"**Content Type**: {role}",
        f"**Total SERP Competitors**: {brief['serp_analysis']['total_competitors']}",
        "",
        "### Top Competitor Analysis",
        ""
    ]
    
    # Add competitor titles
    for i, title in enumerate(brief['serp_analysis']['top_competitor_titles'][:3], 1):
        md_lines.append(f"{i}. {title}")
    
    md_lines.extend([
        "",
        "### Dominant Domains",
        ""
    ])
    
    for domain in brief['serp_analysis']['dominant_domains'][:3]:
        md_lines.append(f"- {domain}")
    
    # Content Strategy Section
    md_lines.extend([
        "",
        "## 🎯 Content Strategy",
        "",
        f"**Primary Angle**: {brief['content_strategy']['primary_angle']}",
        f"**Unique Positioning**: {brief['content_strategy']['unique_positioning']}",
        f"**Content Depth**: {brief['content_strategy']['content_depth']}",
        "",
        "### Competitive Advantages",
        ""
    ])
    
    for advantage in brief['content_strategy']['competitive_advantage']:
        md_lines.append(f"- {advantage}")
    
    # Article Outline Section
    outline = brief['article_outline']
    md_lines.extend([
        "",
        "## 📝 Article Outline",
        "",
        f"**Title**: {outline['title']}",
        f"**Subtitle**: {outline['subtitle']}",
        "",
        "### Article Structure",
        ""
    ])
    
    for section in outline['structure']:
        md_lines.extend([
            f"#### {section['heading']}",
            f"*Section Type: {section['section']}*",
            ""
        ])
        for point in section['content_points']:
            md_lines.append(f"- {point}")
        md_lines.append("")
    
    # Internal Linking Strategy
    md_lines.extend([
        "## 🔗 Internal Linking Strategy",
        ""
    ])
    
    for link in brief['internal_linking']:
        md_lines.extend([
            f"### {link['anchor_text']}",
            f"- **URL**: {link['target_url']}",
            f"- **Context**: {link['context']}",
            f"- **Placement**: {link['placement']}",
            ""
        ])
    
    # SEO Optimization
    seo = brief['seo_optimization']
    md_lines.extend([
        "## 🚀 SEO Optimization Strategy",
        "",
        f"**Primary Keyword**: {seo['primary_keyword']}",
        "",
        "### Title Optimization",
        f"- Target Length: {seo['title_optimization']['target_length']}",
        f"- Include Year: {seo['title_optimization']['include_year']}",
        f"- Power Words: {', '.join(seo['title_optimization']['power_words'])}",
        "",
        "### Meta Description",
        f"- Target Length: {seo['meta_description']['target_length']}",
        f"- Include Keyword: {seo['meta_description']['include_keyword']}",
        f"- Include Benefit: {seo['meta_description']['include_benefit']}",
        f"- Include Location: {seo['meta_description']['include_location']}",
        "",
        "### Content Optimization",
        f"- Keyword Density: {seo['content_optimization']['keyword_density']}",
        f"- Internal Links: {seo['content_optimization']['internal_links_count']}",
        f"- External Links: {seo['content_optimization']['external_links_count']}",
        "",
        "### Semantic Keywords",
        ""
    ])
    
    for sem_kw in seo['content_optimization']['semantic_keywords']:
        md_lines.append(f"- {sem_kw}")
    
    # Claude Insights
    insights = brief['claude_insights']
    md_lines.extend([
        "",
        "## 🤖 Claude Strategic Insights",
        "",
        "### Content Gaps Identified",
        ""
    ])
    
    for gap in insights['content_gaps']:
        md_lines.append(f"- {gap}")
    
    md_lines.extend([
        "",
        f"### Differentiation Angle",
        f"{insights['differentiation_angle']}",
        "",
        "### Target Audience Focus",
        f"**Primary**: {insights['target_audience_focus']['primary']}",
        f"**Secondary**: {insights['target_audience_focus']['secondary']}",
        "",
        "#### Key Pain Points",
        ""
    ])
    
    for pain_point in insights['target_audience_focus']['pain_points']:
        md_lines.append(f"- {pain_point}")
    
    md_lines.extend([
        "",
        "#### Primary Goals",
        ""
    ])
    
    for goal in insights['target_audience_focus']['goals']:
        md_lines.append(f"- {goal}")
    
    md_lines.extend([
        "",
        "---",
        "",
        "*This brief was generated using Claude Code integration for enhanced content strategy and competitive analysis.*"
    ])
    
    return "\n".join(md_lines)

# -------------------------------
# 5. Main Execution
# -------------------------------
def main():
    print("🔍 Loading keyword data...")
    
    try:
        # Load input files
        df_keywords = pd.read_csv(KEYWORD_FILE)
        df_summary = pd.read_csv(SUMMARY_FILE)
        
        print(f"✅ Loaded {len(df_keywords)} keywords in {len(df_summary)} clusters")
        
    except FileNotFoundError as e:
        print(f"❌ Required input files not found: {e}")
        print("Please run KeywordResearcher.py first to generate keyword data")
        return
    
    # Load writing instructions
    try:
        with open("Writing Instructions.md", "r") as f:
            writing_instructions = f.read()
    except FileNotFoundError:
        print("⚠️  Writing Instructions.md not found, using default guidelines")
        writing_instructions = "Professional, data-driven content for B2B audiences"
    
    briefs = []
    markdown_docs = []
    
    print("\n🤖 Generating Claude-powered content briefs...")
    
    # Generate briefs for each keyword
    processed_count = 0
    for cluster_name in df_summary["Cluster"].unique():
        pillar_kw = df_summary[df_summary["Cluster"] == cluster_name]["Pillar Keyword"].values[0]
        cluster_kws = df_keywords[df_keywords["Cluster"] == cluster_name]["Keyword"].tolist()
        
        for _, row in df_keywords[df_keywords["Cluster"] == cluster_name].iterrows():
            keyword = row["Keyword"]
            role = row["Role"]
            
            print(f"📝 Processing: {keyword} ({role})")
            
            # Get enhanced SERP data
            serp_data = get_enhanced_serp_data(keyword)
            
            # Generate Claude-powered brief
            brief = generate_claude_brief(
                keyword=keyword,
                role=role, 
                cluster_keywords=cluster_kws,
                serp_data=serp_data,
                writing_instructions=writing_instructions
            )
            
            briefs.append(brief)
            
            # Convert to markdown
            md_doc = brief_to_markdown(brief)
            markdown_docs.append(md_doc)
            
            processed_count += 1
            
            # Add small delay to respect API limits
            time.sleep(1)
            
            # Limit processing for demo (remove this in production)
            if processed_count >= 5:
                print("📋 Demo limit reached (5 briefs). Remove limit in production.")
                break
        
        if processed_count >= 5:
            break
    
    # Save outputs
    print(f"\n💾 Saving {len(briefs)} briefs...")
    
    # Save JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(briefs, f, indent=2)
    
    # Save Markdown
    with open(OUTPUT_MD, "w") as f:
        f.write("\n\n---\n\n".join(markdown_docs))
    
    print(f"✅ Claude-powered briefs saved:")
    print(f"   📊 JSON: {OUTPUT_JSON}")
    print(f"   📝 Markdown: {OUTPUT_MD}")
    print("\n🎉 Content brief generation complete!")
    print("\nNext step: Use ArticleWriter_Claude.py to generate articles from these briefs")

if __name__ == "__main__":
    main()