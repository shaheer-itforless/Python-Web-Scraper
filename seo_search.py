import csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import html

urls = open('urls.txt').readlines()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    with open('output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Title', 'Description', 'OG:Title', 'OG:Description'])

        for url in urls:
            url = url.strip()
            if not url:
                continue

            try:
                page.goto(url, wait_until='networkidle', timeout=30000)
                time.sleep(1)  # Wait for any dynamic content

                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')

                title = soup.find('title')
                title = html.unescape(title.text) if title else ''

                meta_desc = soup.find('meta', attrs={'name': 'description'})
                meta_desc = html.unescape(meta_desc['content']) if meta_desc else ''
                
                meta_og_title = soup.find('meta', property='og:title')
                meta_og_title = html.unescape(meta_og_title['content']) if meta_og_title else ''

                meta_og_desc = soup.find('meta', property='og:description')
                meta_og_desc = html.unescape(meta_og_desc['content']) if meta_og_desc else ''

                writer.writerow([
                    url,
                    title,
                    meta_desc,
                    meta_og_title,
                    meta_og_desc,
                ])
                print(f"✓ {url}")

            except Exception as e:
                print(f"✗ {url}: {e}")
                writer.writerow([url, 'ERROR', 'ERROR', 'ERROR'])

    browser.close()

print("\nDone! Check output.csv")
