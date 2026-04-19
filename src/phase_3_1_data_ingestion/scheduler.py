import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from scraper import IndMoneyScraper

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def job():
    logger.info("Executing scheduled scraping job...")
    scraper = IndMoneyScraper()
    scraper.run()
    logger.info("Scheduled scraping job completed.")

def start_scheduler():
    scheduler = BlockingScheduler()
    
    # Schedule the job to run every day at 9:15 AM
    # We use a CronTrigger to easily specify the hour and minute
    trigger = CronTrigger(hour=9, minute=15)
    
    scheduler.add_job(job, trigger)
    
    logger.info("Scheduler started. Waiting for the next execution at 9:15 AM...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")

if __name__ == "__main__":
    start_scheduler()
