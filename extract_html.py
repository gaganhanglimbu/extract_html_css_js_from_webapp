import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://smarthr.co.in/demo/html/template/"
OUTPUT_DIR = "smarthr_html"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_html(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Saved: {filename}")
        return response.text
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

def find_and_download_all_pages(base_html):
    soup = BeautifulSoup(base_html, "html.parser")
    links = soup.find_all("a", href=True)
    visited = set()
    for link in links:
        href = link['href']
        if href.endswith('.html') and href not in visited:
            full_url = urljoin(BASE_URL, href)
            filename = href.split('/')[-1]
            download_html(full_url, filename)
            visited.add(href)

# Step 1: Download the index page
index_html = download_html(BASE_URL + "index.html", "index.html")

# Step 2: Find and download all linked HTML pages
find_and_download_all_pages(index_html)
