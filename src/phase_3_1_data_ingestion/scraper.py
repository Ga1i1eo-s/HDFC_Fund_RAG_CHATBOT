import os
import json
import logging
from datetime import datetime
import re
import cloudscraper
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IndMoneyScraper:
    def __init__(self):
        self.urls = [
            "https://www.indmoney.com/mutual-funds/hdfc-housing-opportunities-fund-direct-growth-9006",
            "https://www.indmoney.com/mutual-funds/hdfc-mid-cap-fund-direct-plan-growth-option-3097",
            "https://www.indmoney.com/mutual-funds/hdfc-focused-fund-direct-plan-growth-option-2795",
            "https://www.indmoney.com/mutual-funds/hdfc-flexi-cap-fund-direct-plan-growth-option-3184",
            "https://www.indmoney.com/mutual-funds/hdfc-small-cap-fund-direct-growth-option-3580"
        ]
        # We use cloudscraper to bypass common anti-bot protections
        self.scraper = cloudscraper.create_scraper()
        
        # Go up two levels from src/phase_3_1_data_ingestion to MF_Project root, then into data/raw
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw'))
        os.makedirs(self.data_dir, exist_ok=True)

    def fetch_page(self, url):
        try:
            response = self.scraper.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_data(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "Unknown Fund"
        
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        
        # Extract structured metadata using Regex
        metadata = {
            "nav": None,
            "minimum_sip": None,
            "fund_size_cr": None,
            "expense_ratio_percent": None,
            "rating": None
        }
        
        nav_match = re.search(r'₹([\d,]+\.\d+).*?NAV', text)
        if nav_match:
            metadata["nav"] = float(nav_match.group(1).replace(',', ''))
            
        sip_match = re.search(r'Min Lumpsum/SIP\s*₹[\d,]+/₹([\d,]+)', text)
        if sip_match:
            metadata["minimum_sip"] = float(sip_match.group(1).replace(',', ''))
            
        aum_match = re.search(r'AUM\s*₹([\d\.,]+)\s*Cr', text)
        if aum_match:
            metadata["fund_size_cr"] = float(aum_match.group(1).replace(',', ''))
            
        expense_match = re.search(r'Expense ratio\s*([\d\.]+)%', text, re.IGNORECASE)
        if expense_match:
            metadata["expense_ratio_percent"] = float(expense_match.group(1))
            
        rating_match = re.search(r'Category Rank\s*([\d/]+)', text)
        if rating_match:
            metadata["rating"] = rating_match.group(1)
        
        data = {
            "url": url,
            "title": title,
            "scraped_at": datetime.now().isoformat(),
            "metadata": metadata,
            "content": text
        }
        return data

    def save_data(self, data, filename):
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved data to {filepath}")

    def run(self):
        logger.info("Starting scraping process for 5 IndMoney mutual funds...")
        for url in self.urls:
            logger.info(f"Scraping: {url}")
            html = self.fetch_page(url)
            if html:
                extracted_data = self.extract_data(html, url)
                # Create a safe, static filename from the URL to overwrite old data and avoid duplicates
                fund_name = url.split('/')[-1]
                filename = f"{fund_name}.json"
                self.save_data(extracted_data, filename)
            else:
                logger.warning(f"Failed to scrape {url}. Skipping.")
        logger.info("Scraping process completed.")

if __name__ == "__main__":
    scraper = IndMoneyScraper()
    scraper.run()
