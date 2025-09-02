import json
import openai
import re
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

BRIEF_FILE = os.getenv("ARTICLE_BRIEFS_FILE", "article_briefs.json")
INSTRUCTIONS_FILE = "writing_instructions.json"

OUTPUT_JSON = os.getenv("ARTICLE_DRAFT_FILE", "article_draft.json")
OUTPUT_MD = "article_draft.md"

# -------------------------------
# 2. Load Inputs
# -------------------------------
with open(BRIEF_FILE, "r") as f:
    briefs = json.load(f)

with open(INSTRUCTIONS_FILE, "r") as f:
    instructions = json.load(f)

# -------------------------------
# 3. Pick Brief to Write
# -------------------------------
# For demo: pick first brief
brief = briefs[0]
keyword = brief["Keyword"]
role = brief["Role"]
outline = brief["Outline"]
internal_links = brief["Internal Links"]

# -------------------------------
# 4. Prompt Builder
# -------------------------------
def build_prompt(keyword, role, outline, instructions, internal_links):
    prompt = f"""
You are a professional content writer. Write a full blog article using the following instructions:

Brand Voice: {instructions.get("brand_voice", "Professional but approachable")}
Target Audience: {instructions.get("target_audience", "B2B decision makers")}
Tone: {instructions.get("tone", "Informative and engaging")}
Writing Style: {instructions.get("style", "Clear, actionable, authoritative")}
Other Notes: {instructions.get("other", "Follow SEO best practices")}

Keyword (target): {keyword}
Post Type: {role}

Use this outline as structure:
{json.dumps(outline, indent=2)}

Add internal links (Markdown format) to:
{json.dumps(internal_links, indent=2)}

SEO best practices:
- Use the target keyword in title, intro, and conclusion
- Add related keywords naturally
- Keep paragraphs short and scannable
- Suggest image/video placeholders
- End with SEO metadata (meta title, meta description, slug, focus keyword)

Now write the full draft article in Markdown format.
"""
    return prompt

# -------------------------------
# 5. Call OpenAI to Write Article
# -------------------------------
def generate_article(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Or "gpt-5" if available
        messages=[{"role": "system", "content": "You are an SEO content writer."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message["content"]

# -------------------------------
# 6. Word Count & Reading Time
# -------------------------------
def get_word_count_and_reading_time(markdown_text, wpm=200):
    # remove markdown syntax
    clean_text = re.sub(r"[#*_\-\[\]\(\)!]", " ", markdown_text)
    words = clean_text.split()
    word_count = len(words)
    reading_time = round(word_count / wpm, 1)  # minutes
    return word_count, reading_time

# -------------------------------
# 7. Run
# -------------------------------
prompt = build_prompt(keyword, role, outline, instructions, internal_links)
article_md = generate_article(prompt)

# word count + reading time
word_count, reading_time = get_word_count_and_reading_time(article_md)

# Package JSON output
article_json = {
    "Keyword": keyword,
    "Role": role,
    "Article": article_md,
    "SEO": {
        "Meta Title": f"{keyword.title()} | {instructions.get('brand_name', 'Your Brand')}",
        "Meta Description": f"Learn about {keyword} in this {role.lower()} tailored for {instructions.get('target_audience', 'professionals')}.",
        "Slug": keyword.replace(" ", "-"),
        "Focus Keyword": keyword,
        "Word Count": word_count,
        "Estimated Reading Time (mins)": reading_time
    }
}

# Save outputs
with open(OUTPUT_JSON, "w") as f:
    json.dump(article_json, f, indent=2)

with open(OUTPUT_MD, "w") as f:
    f.write(article_md)

print(f"✅ Draft article saved as {OUTPUT_JSON} and {OUTPUT_MD}")