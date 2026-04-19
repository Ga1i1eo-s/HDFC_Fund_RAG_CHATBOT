import sys
import os
import argparse
import logging
from scraper import IndMoneyScraper
from scheduler import start_scheduler

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Phase 3.1 Data Ingestion Pipeline")
    parser.add_argument('--run-now', action='store_true', help="Run the scraper immediately instead of starting the scheduler.")
    args = parser.parse_args()

    if args.run_now:
        logger.info("Running scraper immediately...")
        scraper = IndMoneyScraper()
        scraper.run()
    else:
        logger.info("Starting the scheduled service...")
        start_scheduler()

if __name__ == "__main__":
    main()
