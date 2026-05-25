from services.shared.celery_app import celery_app
from services.shared.logging import get_logger
from services.shared.database import SessionLocal
from services.shared.models import Job
import asyncio
from playwright.async_api import async_playwright

logger = get_logger("services.scraper.tasks")

@celery_app.task(name="services.scraper.tasks.scrape_indeed")
def scrape_indeed_task(keywords: str, location: str):
    async def run():
        db = SessionLocal()
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_record_context().new_page()
            
            # Simple Indeed scrape logic
            url = f"https://www.indeed.com/jobs?q={keywords}&l={location}"
            logger.info("scraping_started", url=url)
            await page.goto(url)
            
            # Mock extraction for demonstration
            # In production, use the modules/scraper.py logic here
            jobs_found = [
                {"title": "Software Engineer", "company": "Tech Corp", "url": "https://indeed.com/1"},
                {"title": "Python Developer", "company": "AI Inc", "url": "https://indeed.com/2"}
            ]
            
            for j_data in jobs_found:
                new_job = Job(
                    title=j_data['title'],
                    company=j_data['company'],
                    url=j_data['url'],
                    source="indeed"
                )
                db.add(new_job)
            
            db.commit()
            await browser.close()
            logger.info("scraping_complete", jobs_count=len(jobs_found))
        db.close()

    asyncio.run(run())
 stories
