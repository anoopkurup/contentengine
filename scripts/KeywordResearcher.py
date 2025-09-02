import requests
import json
import time
import pandas as pd
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

# User inputs (configurable via environment variables)
SEED_KEYWORDS = ["AI marketing", "AI lead generation", "AI content automation"]
LOCATION = os.getenv("TARGET_LOCATION", "India")
LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")
OUTPUT_FILE = os.getenv("KEYWORD_CLUSTERS_FILE", "keyword_clusters.csv")
SUMMARY_FILE = os.getenv("CLUSTER_SUMMARY_FILE", "cluster_summary.csv")

# Configurable parameters
SERP_THRESHOLD = float(os.getenv("SERP_OVERLAP_THRESHOLD", "0.3"))
MIN_SEARCH_VOL = int(os.getenv("MIN_SEARCH_VOLUME", "100"))
MAX_COMP = float(os.getenv("MAX_COMPETITION", "0.3"))

# -------------------------------
# Helper: POST request
# -------------------------------
def dfseo_post(endpoint, payload):
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, auth=(API_LOGIN, API_PASSWORD), json=payload)
    resp.raise_for_status()
    return resp.json()

# -------------------------------
# 2. Get Keyword Ideas
# -------------------------------
def get_keyword_ideas(seed_keywords):
    payload = [{
        "keywords": seed_keywords,
        "location_name": LOCATION,
        "language_name": LANGUAGE
    }]
    res = dfseo_post("keywords_data/google_ads/keywords_for_keywords/live", payload)
    
    keyword_list = []
    for kw_data in res["tasks"][0]["result"]:
        for kw in kw_data["items"]:
            keyword_list.append({
                "keyword": kw["keyword"],
                "search_volume": kw.get("search_volume", 0),
                "competition": kw.get("competition", 0.0)
            })
    return pd.DataFrame(keyword_list)

# -------------------------------
# 3. Fetch SERPs
# -------------------------------
def get_serp_results(keywords):
    serp_results = {}
    for kw in keywords:
        payload = [{
            "keyword": kw,
            "location_name": LOCATION,
            "language_name": LANGUAGE,
            "se_domain": "google.com",
            "search_engine": "google"
        }]
        res = dfseo_post("serp/google/organic/live/advanced", payload)
        items = res["tasks"][0]["result"][0]["items"]
        urls = [i["url"] for i in items if "url" in i][:10]  # top 10 results
        serp_results[kw] = urls
        time.sleep(2)  # avoid hitting API rate limits
    return serp_results

# -------------------------------
# 4. Cluster by SERP overlap
# -------------------------------
def cluster_keywords(serp_results, threshold=0.3):
    keywords = list(serp_results.keys())
    clusters = []
    visited = set()

    for kw in keywords:
        if kw in visited:
            continue
        cluster = [kw]
        visited.add(kw)
        for other_kw in keywords:
            if other_kw in visited:
                continue
            overlap = len(set(serp_results[kw]) & set(serp_results[other_kw])) / 10
            if overlap >= threshold:
                cluster.append(other_kw)
                visited.add(other_kw)
        clusters.append(cluster)
    return clusters

# -------------------------------
# 5. Run Workflow
# -------------------------------
if __name__ == "__main__":
    # Step 1: keyword ideas
    df_keywords = get_keyword_ideas(SEED_KEYWORDS)
    
    # filter for low competition
    df_filtered = df_keywords[(df_keywords["competition"] < MAX_COMP) & (df_keywords["search_volume"] > MIN_SEARCH_VOL)]
    keywords = df_filtered["keyword"].tolist()

    print(f"Got {len(keywords)} filtered keywords")

    # Step 2: fetch SERPs
    serp_data = get_serp_results(keywords[:20])  # limit to 20 for testing
    print("Fetched SERPs")

    # Step 3: clustering
    clusters = cluster_keywords(serp_data, threshold=SERP_THRESHOLD)

    # Step 4: merge cluster + metrics and assign Pillar vs Cluster
    cluster_records = []
    summary_records = []

    for i, cluster in enumerate(clusters):
        cluster_name = f"Cluster {i+1}"

        # find keyword with max search volume = Pillar
        cluster_df = df_filtered[df_filtered["keyword"].isin(cluster)]
        if cluster_df.empty:
            continue
        pillar_kw = cluster_df.loc[cluster_df["search_volume"].idxmax()]

        vols, comps = [], []
        for _, row in cluster_df.iterrows():
            role = "Pillar Post" if row["keyword"] == pillar_kw["keyword"] else "Cluster Post"
            vols.append(row["search_volume"])
            comps.append(row["competition"])
            cluster_records.append({
                "Cluster": cluster_name,
                "Keyword": row["keyword"],
                "Search Volume": row["search_volume"],
                "Competition": row["competition"],
                "Role": role
            })

        # cluster-level averages
        summary_records.append({
            "Cluster": cluster_name,
            "Pillar Keyword": pillar_kw["keyword"],
            "Keywords in Cluster": len(cluster_df),
            "Avg Search Volume": round(sum(vols) / len(vols), 1),
            "Total Search Volume": sum(vols),
            "Avg Competition": round(sum(comps) / len(comps), 3)
        })

    # Step 5: export
    df_out = pd.DataFrame(cluster_records)
    df_summary = pd.DataFrame(summary_records)

    df_out.to_csv(OUTPUT_FILE, index=False)
    df_summary.to_csv(SUMMARY_FILE, index=False)

    print(f"Keyword-level clusters saved to {OUTPUT_FILE}")
    print(f"Cluster-level summary saved to {SUMMARY_FILE}")