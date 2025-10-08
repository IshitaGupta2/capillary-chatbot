import requests, time, json, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ROOT_URL = "https://docs.capillarytech.com"  # base site
OUT_FILE = "../data/pages.jsonl"
DELAY = 0.5
MAX_PAGES = 80   # 👈 stop after fetching this many pages

def is_internal(url):
    """Check if URL belongs to the same site"""
    return url.startswith(ROOT_URL)

def extract_text(soup):
    main = soup.find("article") or soup.find("main") or soup.body
    return main.get_text(separator="\n", strip=True) if main else ""

def crawl(root):
    visited, queue, pages = set(), [root], []
    while queue and len(visited) < MAX_PAGES:
        url = queue.pop(0)
        if url in visited:
            continue
        print(f"[{len(visited)+1}/{MAX_PAGES}] Fetching:", url)
        try:
            r = requests.get(url, timeout=10)
        except Exception as e:
            print("Error:", e)
            continue
        visited.add(url)
        soup = BeautifulSoup(r.text, "html.parser")
        text = extract_text(soup)
        title = soup.title.string.strip() if soup.title else url
        pages.append({"url": url, "title": title, "text": text})

        # find and queue next links
        for a in soup.find_all("a", href=True):
            next_url = urljoin(url, a["href"].split("#")[0])
            if is_internal(next_url) and next_url not in visited and next_url not in queue:
                queue.append(next_url)

        time.sleep(DELAY)

    print(f"\n✅ Done! Scraped {len(pages)} pages total.\n")
    return pages

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    pages = crawl(ROOT_URL)
    with open("data/pages.jsonl", "w", encoding="utf-8") as f:
        for p in pages:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    print("✅ Scraping complete! Saved to data/pages.jsonl")

