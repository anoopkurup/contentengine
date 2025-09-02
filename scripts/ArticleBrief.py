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

# -------------------------------
# Helper: POST request to DataforSEO
# -------------------------------
def dfseo_post(endpoint, payload):
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, auth=(API_LOGIN, API_PASSWORD), json=payload)
    resp.raise_for_status()
    return resp.json()

# -------------------------------
# 2. Fetch SERP Headings (optional inspiration)
# -------------------------------
def get_serp_headings(keyword, location=None, language=None):
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
    res = dfseo_post("serp/google/organic/live/advanced", payload)
    items = res["tasks"][0]["result"][0]["items"]

    # Extract titles (as surrogate headings)
    headings = [i.get("title", "") for i in items if "title" in i][:5]
    return headings

# -------------------------------
# 3. Build Outline Generator
# -------------------------------
def generate_outline(keyword, role, cluster_keywords, serp_headings):
    outline = []

    if role == "Pillar Post":
        outline.append({"H1": f"The Ultimate Guide to {keyword.title()}"})
        outline.append({"H2": "Introduction", "points": [
            f"Why {keyword} matters today",
            "Benefits and use cases"
        ]})
        outline.append({"H2": "Key Subtopics", "H3s": [
            f"Overview of {kw}" for kw in cluster_keywords if kw != keyword
        ]})
        outline.append({"H2": "Best Practices", "points": [
            "Common mistakes to avoid",
            "Pro tips from industry"
        ]})
        outline.append({"H2": "Conclusion & Next Steps", "points": [
            "Summary of key insights",
            "Where to go deeper"
        ]})

    else:  # Cluster Post
        outline.append({"H1": f"{keyword.title()} — Complete Breakdown"})
        outline.append({"H2": "Introduction", "points": [
            f"Quick overview of {keyword}",
            f"How it connects to broader {cluster_keywords[0]}"
        ]})
        outline.append({"H2": "Step-by-Step / In-depth", "points": serp_headings})
        outline.append({"H2": "Tools / Examples", "points": [
            "Case study",
            "Recommended tools/resources"
        ]})
        outline.append({"H2": "Conclusion", "points": [
            "Main takeaways",
            "Internal link to pillar"
        ]})
    
    return outline

# -------------------------------
# 4. Add Internal Links
# -------------------------------
def suggest_internal_links(keyword, role, pillar_kw, cluster_keywords):
    links = []
    if role == "Pillar Post":
        for kw in cluster_keywords:
            if kw != pillar_kw:
                links.append({"anchor": kw, "target": f"/{kw.replace(' ', '-')}"})
    else:
        links.append({"anchor": pillar_kw, "target": f"/{pillar_kw.replace(' ', '-')}"})
    return links

# -------------------------------
# 5. Convert Outline to Markdown
# -------------------------------
def outline_to_markdown(keyword, role, outline, links):
    md = [f"# Brief for {keyword} ({role})", ""]
    for section in outline:
        if "H1" in section:
            md.append(f"# {section['H1']}")
        if "H2" in section:
            md.append(f"## {section['H2']}")
            if "points" in section:
                for p in section["points"]:
                    md.append(f"- {p}")
            if "H3s" in section:
                for h3 in section["H3s"]:
                    md.append(f"### {h3}")
        md.append("")
    md.append("### Suggested Internal Links")
    for link in links:
        md.append(f"- [{link['anchor']}]({link['target']})")
    return "\n".join(md)

# -------------------------------
# 6. Run Workflow
# -------------------------------
if __name__ == "__main__":
    # Load input files
    df_keywords = pd.read_csv(KEYWORD_FILE)
    df_summary = pd.read_csv(SUMMARY_FILE)

    briefs = []
    markdown_docs = []

    # Generate outline + internal links for each keyword
    for cluster_name in df_summary["Cluster"].unique():
        pillar_kw = df_summary[df_summary["Cluster"] == cluster_name]["Pillar Keyword"].values[0]
        cluster_kws = df_keywords[df_keywords["Cluster"] == cluster_name]["Keyword"].tolist()

        for _, row in df_keywords[df_keywords["Cluster"] == cluster_name].iterrows():
            keyword = row["Keyword"]
            role = row["Role"]

            # pull some SERP inspiration
            try:
                serp_headings = get_serp_headings(keyword)
            except:
                serp_headings = []

            outline = generate_outline(keyword, role, cluster_kws, serp_headings)
            links = suggest_internal_links(keyword, role, pillar_kw, cluster_kws)

            briefs.append({
                "Cluster": cluster_name,
                "Keyword": keyword,
                "Role": role,
                "Outline": outline,
                "Internal Links": links
            })

            md_doc = outline_to_markdown(keyword, role, outline, links)
            markdown_docs.append(md_doc)
            time.sleep(1)

    # Export JSON
    with open("article_briefs.json", "w") as f:
        json.dump(briefs, f, indent=2)

    # Export Markdown
    with open("article_briefs.md", "w") as f:
        f.write("\n\n---\n\n".join(markdown_docs))

    print("✅ Article briefs saved as article_briefs.json and article_briefs.md")