from services.shared.celery_app import celery_app
from services.shared.logging import get_logger
from services.shared.database import SessionLocal
from services.shared.models import Job
import asyncio
import random
from playwright.async_api import async_playwright
try:
    from playwright_stealth import stealth
except ImportError:
    stealth = None

logger = get_logger("services.scraper.tasks")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

@celery_app.task(name="services.scraper.tasks.scrape_linkedin")
def scrape_linkedin_task(keywords: str, location: str):
    async def run():
        db = SessionLocal()
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
                page = await context.new_page()
                if stealth:
                    await stealth(page)
                
                search_url = f"https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}&f_TPR=r604800"
                logger.info("scraping_started", url=search_url)
                
                await page.goto(search_url, timeout=60000)
                await asyncio.sleep(random.uniform(3, 8))
                
                job_cards = await page.query_selector_all(".base-card")
                jobs_found = []
                
                for card in job_cards[:15]:
                    try:
                        title_elem = await card.query_selector(".base-search-card__title")
                        company_elem = await card.query_selector(".base-search-card__subtitle")
                        loc_elem = await card.query_selector(".job-search-card__location")
                        url_elem = await card.query_selector(".base-card__full-link")
                        
                        if not all([title_elem, company_elem, loc_elem, url_elem]):
                            continue
                            
                        title = (await title_elem.inner_text()).strip()
                        company = (await company_elem.inner_text()).strip()
                        loc = (await loc_elem.inner_text()).strip()
                        url = await url_elem.get_attribute("href")
                        url = url.split('?')[0] if url else ""
                        
                        # Check if job already exists
                        existing = db.query(Job).filter(Job.url == url).first()
                        if not existing and url:
                            new_job = Job(
                                title=title,
                                company=company,
                                location=loc,
                                url=url,
                                source="linkedin"
                            )
                            db.add(new_job)
                            db.commit()
                            db.refresh(new_job)

                            # Vectorize for semantic search
                            try:
                                from services.shared.vector import upsert_job_vector
                                upsert_job_vector(str(new_job.id), title, title) # Use title as fallback desc for now
                            except Exception as vec_e:
                                logger.error("vectorization_failed", job_id=str(new_job.id), error=str(vec_e))

                            jobs_found.append({"title": title, "company": company})
                        
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                    except Exception as inner_e:
                        logger.error("card_extract_error", error=str(inner_e))
                        continue
                        
                logger.info("scraping_complete", jobs_count=len(jobs_found))
            except Exception as e:
                logger.error("scraping_failed", error=str(e))
            finally:
                await browser.close()
                db.close()

    asyncio.run(run())

@celery_app.task(name="services.scraper.tasks.scrape_indeed")
def scrape_indeed_task(keywords: str, location: str):
    # Place holder for indeed following same pattern
    pass
