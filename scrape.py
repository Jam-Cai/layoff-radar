import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from bs4 import BeautifulSoup
import time
import requests
import random
import sqlite3
import json
from prompts_claude import *

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/121.0.2277.83",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.184 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
]
conn = sqlite3.connect("articles.db")
cur = conn.cursor()

def setup_database():

    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            content TEXT,
            companies TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
        )
    """)

    conn.commit()

def add_article(title, link, content, companies):
    companies_json = json.dumps(companies)

    cur.execute("""
        INSERT INTO articles (title, link, content, companies)
        VALUES (?, ?, ?, ?)
    """, (title, link, content, companies_json))

    conn.commit()


def get_unique_companies():

    cur.execute("SELECT companies FROM articles")
    rows = cur.fetchall()

    unique_companies = set()

    for r in rows:
        companies_json = r[0]
        if companies_json:
            try:
                companies = json.loads(companies_json)
                for c in companies:
                    unique_companies.add(c.strip())
            except json.JSONDecodeError:
                continue  

    for c in unique_companies:
        cur.execute("INSERT OR IGNORE INTO companies (name) VALUES (?)", (c,))

    conn.commit()


def find_articles(search_term="meta layoffs"):
	options = uc.ChromeOptions()
	options.add_argument("--headless=new")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--disable-blink-features=AutomationControlled")

	driver = uc.Chrome(options=options)
	wait = WebDriverWait(driver, 10)

	driver.get(f"https://news.search.yahoo.com/search?p={search_term}")
	wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h4.s-title a")))
	links = driver.find_elements(By.CSS_SELECTOR, "h4.s-title a")

	articles = []
	for l in links:
		title = l.text.strip()
		link = l.get_attribute("href")
		articles.append({"title": title, "link": link})

	driver.quit()
	return articles

def get_article_text(link):
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        resp = requests.get(link, timeout=10, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    except requests.exceptions.Timeout:
        return "[TIMEOUT ERROR]"
    except requests.exceptions.RequestException as e:
        return f"[REQUEST FAILED] {e}"

def process_articles(articles):
    with ThreadPoolExecutor(max_workers=100) as executor:
        texts = list(executor.map(get_article_text, [a["link"] for a in articles]))

    print("got article texts")    

    for i, article in enumerate(articles):
        title = article["title"]
        link = article["link"]
        text = texts[i]

        try:
            raw_json = extract_companies(text)  
            companies = raw_json.get("company_names", [])
        except Exception as e:
            print(f"Failed to extract companies for article {i + 1}: {e}")
            companies = []

        add_article(title, link, text, companies)


def display_articles(articles):
	for i, article in enumerate(articles, start=1):
		print(f"\n{'=' * 80}")
		print(f"[{i}] Title: {article['title']}")
		print(f"URL: {article['link']}")
		print("-" * 80)
		text = article.get("text", "[No Content]")
		print(text)
		print('=' * 80)

def dump_table_contents(table_name):

    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()

    # Fetch column names
    column_names = [description[0] for description in cur.description]

    print(f"\n--- Contents of '{table_name}' ---")
    print("\t".join(column_names))
    for row in rows:
        print("\t".join(str(item) for item in row))


def scrape_articles():
    setup_database()
     
    searches = ["tech layoffs", "tech scandals", "tech companies", "company layoffs", "tech layoffs",
    "software industry layoffs",
    "AI job losses",
    "cloud computing layoffs",
    "data science job trends",
    "machine learning layoffs",
    "fintech layoffs",
    "cybersecurity job cuts",
    "semiconductor industry layoffs",
    "robotics sector job reductions",
    "IT services downsizing",
    "tech hiring slowdown",
    "developer job market 2025",
    "tech support layoffs",
    "blockchain industry layoffs",
    "e-commerce tech layoffs",
    "gaming industry job cuts",
    "enterprise tech job trends",
    "startup layoffs 2025",
    "tech layoffs economic impact",
    "automobile layoffs"]



    articles = []
    for s in searches:
        articles.extend(find_articles(s))
        print(f"got {s} articles")
    
    process_articles(articles)

            
# if __name__ == "__main__":
#     scrape()
#     dump_table_contents("companies")
