import json
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Base URL
BASE_URL = "https://developer.apple.com/documentation/visionos"
OUTPUT_JSON = "visionos_docs.json"

# Set up Selenium with Headless Chrome
options = Options()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_doc_links(base_url):
    """Extract all documentation links dynamically using Selenium."""
    driver.get(base_url)
    time.sleep(3)  # Allow JavaScript to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    doc_links = set()
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/documentation/visionos"):
            doc_links.add("https://developer.apple.com" + href)

    return list(doc_links)

def extract_text_from_page(url):
    """Scrape the main content from a VisionOS documentation page using Selenium."""
    driver.get(url)
    time.sleep(3)  # Allow JavaScript to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the main content section
    main_content = soup.find("main")
    if not main_content:
        return ""

    paragraphs = main_content.find_all(["p", "li", "h1", "h2", "h3"])
    text_content = "\n".join([p.get_text(strip=True) for p in paragraphs])

    return text_content

def scrape_and_save_docs(base_url, output_json):
    """Scrape all VisionOS documentation and save to JSON."""
    print(f"🔍 Finding documentation links on {base_url}...")
    doc_links = get_doc_links(base_url)

    if not doc_links:
        print("❌ No documentation links found!")
        return

    print(f"✅ Found {len(doc_links)} documentation pages. Scraping now...")

    docs_data = {}
    for link in tqdm(doc_links, desc="Scraping pages"):
        page_text = extract_text_from_page(link)
        if page_text:
            docs_data[link] = page_text

    # Save extracted data to JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(docs_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Extracted documentation saved to {output_json}")

# Run the scraper
scrape_and_save_docs(BASE_URL, OUTPUT_JSON)

# Close Selenium driver
driver.quit()
