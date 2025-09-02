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
YOUTUBE_FILE = "youtube_instructions.json"

OUTPUT_JSON = os.getenv("YOUTUBE_SCRIPT_FILE", "youtube_script.json")
OUTPUT_MD = "youtube_script.md"

# -------------------------------
# 2. Load Inputs
# -------------------------------
with open(ARTICLE_FILE, "r") as f:
    article = json.load(f)

with open(YOUTUBE_FILE, "r") as f:
    yt_instructions = json.load(f)

article_text = article["Article"]
keyword = article["Keyword"]

# -------------------------------
# 3. Helper: OpenAI Call
# -------------------------------
def gpt_generate(prompt, tokens=1500):
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or gpt-5 if available
        messages=[
            {"role": "system", "content": "You are a skilled YouTube video content creator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=tokens
    )
    return response.choices[0].message["content"]

# -------------------------------
# 4. Generate YouTube Script
# -------------------------------
def generate_youtube_script(article_text, keyword, instructions):
    prompt = f"""
Write a detailed YouTube video script based on the article below.

Instructions:
Tone: {instructions.get("tone", "Conversational and engaging")}
Style: {instructions.get("style", "Explainer style, clear and story-driven")}
Audience: {instructions.get("target_audience", "Business professionals and founders")}
Other Notes: {instructions.get("other", "Add strong hook, keep energy high, include visual cues and CTAs")}

Script structure:
1. Hook (first 15 seconds, must grab attention)
2. Introduction (problem + promise)
3. Main Content (aligned to article headings)
   - Each section: Voiceover + Visual directions
4. Engagement prompts (like/comment/subscribe)
5. Outro (recap + CTA)

Include placeholders like:
[On Screen Text: ...]
[Visual Suggestion: ...]
[Insert B-roll of ...]

Keyword to optimize for: {keyword}

Article:
{article_text}
"""
    return gpt_generate(prompt, tokens=2000)

# -------------------------------
# 5. Generate YouTube Description + Tags
# -------------------------------
def generate_youtube_metadata(article_text, keyword, instructions):
    prompt = f"""
Write a YouTube description and tags for the video based on this article.

Keyword: {keyword}
Tone: {instructions.get("tone", "Friendly and engaging")}
Other Notes: {instructions.get("other", "Include CTA to website/newsletter")}

Format:
Description:
- First 2 lines = hook + keyword
- Summary of what viewers will learn
- CTA with link placeholder

Tags: 10–15 comma-separated SEO keywords

Article:
{article_text}
"""
    return gpt_generate(prompt, tokens=600)

# -------------------------------
# 6. Run
# -------------------------------
youtube_script = generate_youtube_script(article_text, keyword, yt_instructions)
metadata = generate_youtube_metadata(article_text, keyword, yt_instructions)

# Split description and tags
desc, tags = metadata.split("Tags:", 1) if "Tags:" in metadata else (metadata, "")
desc = desc.replace("Description:", "").strip()
tags = tags.strip()

# -------------------------------
# 7. Save Outputs
# -------------------------------
youtube_json = {
    "Keyword": keyword,
    "YouTube Script": youtube_script,
    "YouTube Description": desc,
    "YouTube Tags": [t.strip() for t in tags.split(",") if t.strip()]
}

with open(OUTPUT_JSON, "w") as f:
    json.dump(youtube_json, f, indent=2)

with open(OUTPUT_MD, "w") as f:
    f.write(f"# YouTube Script for {keyword}\n\n")
    f.write("## Script\n")
    f.write(youtube_script + "\n\n")
    f.write("## Description\n")
    f.write(desc + "\n\n")
    f.write("## Tags\n")
    f.write(", ".join(youtube_json["YouTube Tags"]))

print(f"✅ YouTube script + metadata saved as {OUTPUT_JSON} and {OUTPUT_MD}")