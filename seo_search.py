import csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

urls = open('urls.txt').readlines()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    with open('output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Title', 'OG:Title', 'OG:Description'])

        for url in urls:
            url = url.strip()
            if not url:
                continue

            try:
                page.goto(url, wait_until='networkidle', timeout=30000)
                time.sleep(1)  # Wait for any dynamic content

                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')

                title = soup.find('title').text.strip() if soup.find('title') else ''
                og_title = soup.find('meta', property='og:title')
                og_desc = soup.find('meta', property='og:description')

                writer.writerow([
                    url,
                    title,
                    og_title['content'] if og_title else '',
                    og_desc['content'] if og_desc else ''
                ])
                print(f"✓ {url}")

            except Exception as e:
                print(f"✗ {url}: {e}")
                writer.writerow([url, 'ERROR', 'ERROR', 'ERROR'])

    browser.close()

print("\nDone! Check output.csv")
