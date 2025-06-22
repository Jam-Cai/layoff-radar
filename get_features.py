from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import sqlite3
import json
from prompts_claude import *
from pydantic import BaseModel
from typing import Optional


class Features(BaseModel):
    company_name: str
    layoff_count: Optional[int]
    funding_raised: Optional[int]
    type_of_company: Optional[str]
    country: Optional[str]
    industry: Optional[str]

def read_articles(articles):
    with open("meta_articles.txt", "w", encoding="utf-8") as f:
        for i, a in enumerate(articles, start=1):
            f.write(f"{'='*80}\n")
            f.write(f"Article {i}: {a['title']}\n")
            f.write(f"URL: {a['link']}\n")
            f.write(f"Scraped At: {a['scraped_at']}\n")
            f.write(f"Companies Mentioned: {', '.join(a['companies'])}\n")
            f.write(f"{'-'*80}\n")
            f.write(f"{a['content']}\n")
            f.write(f"{'='*80}\n\n")

    print(f"Saved {len(articles)} articles mentioning 'meta' to meta_articles.txt")


def get_articles_by_company(company_name, db_path="articles.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT title, link, content, companies, scraped_at FROM articles")
    rows = cur.fetchall()
    
    matching_articles = []
    for row in rows:
        title, link, content, companies_json, scraped_at = row
        try:
            companies = json.loads(companies_json)
            if company_name.lower() in (c.lower() for c in companies):
                matching_articles.append({
                    "title": title,
                    "link": link,
                    "content": content,
                    "companies": companies,
                    "scraped_at": scraped_at
                })
        except (json.JSONDecodeError, TypeError):
            continue

    conn.close()
    return matching_articles

def get_features(company_name):
    articles = get_articles_by_company(company_name)

    with ThreadPoolExecutor(max_workers=30) as executor:
        features_list = list(executor.map(extract_features, [company_name] * len(articles), [a["content"] for a in articles]))

    features_json = combine_features(features_list)
    features_json["company_name"] = company_name

    final_features = Features(**features_json)
    return final_features
       
if __name__ == "__main__":
    print(get_features("meta"))

