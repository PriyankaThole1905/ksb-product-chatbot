# scraper.py
import requests
from bs4 import BeautifulSoup
import os
import re

BASE_URL = "https://www.ksb.com/en-fr/product"
OUTPUT_DIR = "scraped_data"

def sanitize_filename(url):
    """Removes or replaces invalid characters for filenames."""
    return re.sub(r'[^\w\-_\.]', '_', url)

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        text_parts = soup.find_all('p') + soup.find_all('h1') + soup.find_all('h2') + soup.find_all('h3') + soup.find_all('li')
        text = "\n".join([part.get_text(strip=True) for part in text_parts if part.get_text(strip=True)])
        return text, url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, url

def crawl_website(start_url, visited=None, output_dir=OUTPUT_DIR):
    if visited is None:
        visited = set()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    queue = [start_url]
    visited.add(start_url)

    while queue:
        current_url = queue.pop(0)
        print(f"Crawling: {current_url}")
        text, url = extract_text_from_url(current_url)
        if text:
            sanitized_url = sanitize_filename(url)
            filename = os.path.join(output_dir, f"{sanitized_url}.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)

        try:
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                absolute_url = requests.compat.urljoin(current_url, link['href']).split('#')[0] # Handle relative URLs and fragments
                if absolute_url.startswith(BASE_URL) and absolute_url not in visited:
                    visited.add(absolute_url)
                    queue.append(absolute_url)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching links from {current_url}: {e}")

if __name__ == "__main__":
    crawl_website(BASE_URL)
    print(f"Scraped data saved in: {OUTPUT_DIR}")