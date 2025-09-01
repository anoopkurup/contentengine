import json
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------------------
# 1. Setup
# -------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# Validate required environment variables
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")

ARTICLE_FILE = os.getenv("ARTICLE_DRAFT_FILE", "article_draft.json")
LINKEDIN_FILE = "linkedin_post_writer.json"
NEWSLETTER_FILE = "newsletter_instructions.json"

OUTPUT_JSON = os.getenv("SOCIAL_POSTS_FILE", "social_posts.json")
OUTPUT_MD = "social_posts.md"

# -------------------------------
# 2. Load Inputs
# -------------------------------
with open(ARTICLE_FILE, "r") as f:
    article = json.load(f)

with open(LINKEDIN_FILE, "r") as f:
    linkedin_instructions = json.load(f)

with open(NEWSLETTER_FILE, "r") as f:
    newsletter_instructions = json.load(f)

article_text = article["Article"]
keyword = article["Keyword"]

# -------------------------------
# 3. Helper: OpenAI Call
# -------------------------------
def gpt_generate(prompt, tokens=800):
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or gpt-5 if available
        messages=[{"role": "system", "content": "You are a skilled content repurposing assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=tokens
    )
    return response.choices[0].message["content"]

# -------------------------------
# 4. Generate LinkedIn Posts
# -------------------------------
def generate_linkedin_posts(article_text, instructions):
    prompt = f"""
Repurpose the following article into 3-4 LinkedIn posts (based on number of headings).
Tone: {instructions.get("tone", "Professional and conversational")}
Style: {instructions.get("style", "Engaging, story-driven")}
Audience: {instructions.get("target_audience", "B2B professionals")}
Other Notes: {instructions.get("other", "Use LinkedIn formatting with spacing, hooks, and CTAs")}

Article:
{article_text}
"""
    return gpt_generate(prompt, tokens=1200)

# -------------------------------
# 5. Generate Tweets
# -------------------------------
def generate_tweets(article_text):
    prompt = f"""
Repurpose this article into Twitter/X content:
- Create 2 threads (5 tweets each)
- Create 5 standalone tweets
Make them concise, engaging, and value-packed.

Article:
{article_text}
"""
    return gpt_generate(prompt, tokens=1000)

# -------------------------------
# 6. Rewrite as LinkedIn Article
# -------------------------------
def generate_linkedin_article(article_text, keyword):
    prompt = f"""
Rewrite this article for LinkedIn Articles:
- Keep it professional but slightly less formal
- Add hooks for engagement
- Break into short paragraphs
- Optimize for {keyword}
Article:
{article_text}
"""
    return gpt_generate(prompt, tokens=1800)

# -------------------------------
# 7. Generate Newsletter Version
# -------------------------------
def generate_newsletter(article_text, instructions):
    prompt = f"""
Summarize and rewrite this article for a newsletter:
Tone: {instructions.get("tone", "Friendly, insightful")}
Style: {instructions.get("style", "Short, story-driven")}
Audience: {instructions.get("target_audience", "Subscribers interested in marketing and growth")}
Other Notes: {instructions.get("other", "Include CTA for website or workshop")}

Article:
{article_text}
"""
    return gpt_generate(prompt, tokens=1000)

# -------------------------------
# 8. Generate Carousel
# -------------------------------
def generate_carousel(article_text, keyword):
    prompt = f"""
Turn this article into a LinkedIn/Instagram carousel.
Format:
- Slide 1: Hook/attention grabber
- Slides 2-9: One key insight per slide (short, punchy text)
- Slide 10: CTA (call to action)

Keep text short (max 15 words per slide).
Topic: {keyword}

Article:
{article_text}
"""
    return gpt_generate(prompt, tokens=800)

# -------------------------------
# 9. Run
# -------------------------------
linkedin_posts = generate_linkedin_posts(article_text, linkedin_instructions)
tweets = generate_tweets(article_text)
linkedin_article = generate_linkedin_article(article_text, keyword)
newsletter = generate_newsletter(article_text, newsletter_instructions)
carousel = generate_carousel(article_text, keyword)

# -------------------------------
# 10. Save Outputs
# -------------------------------
social_json = {
    "Keyword": keyword,
    "LinkedIn Posts": linkedin_posts,
    "Twitter Threads & Tweets": tweets,
    "LinkedIn Article": linkedin_article,
    "Newsletter Version": newsletter,
    "Carousel Slides": carousel,
    "Other Platforms Suggestions": [
        "Instagram Carousel (use same slides)",
        "YouTube Shorts (explain 1-2 main ideas quickly)",
        "Podcast snippet or LinkedIn Audio",
        "Slide deck for SlideShare or LinkedIn carousel",
        "Medium post (republish article)"
    ]
}

with open(OUTPUT_JSON, "w") as f:
    json.dump(social_json, f, indent=2)

with open(OUTPUT_MD, "w") as f:
    f.write(f"# Social Media Repurposing for {keyword}\n\n")
    f.write("## LinkedIn Posts\n")
    f.write(linkedin_posts + "\n\n")
    f.write("## Twitter Threads & Tweets\n")
    f.write(tweets + "\n\n")
    f.write("## LinkedIn Article\n")
    f.write(linkedin_article + "\n\n")
    f.write("## Newsletter Version\n")
    f.write(newsletter + "\n\n")
    f.write("## Carousel Slides\n")
    f.write(carousel + "\n\n")
    f.write("## Other Platform Suggestions\n")
    for p in social_json["Other Platforms Suggestions"]:
        f.write(f"- {p}\n")

print(f"✅ Social posts saved as {OUTPUT_JSON} and {OUTPUT_MD}")