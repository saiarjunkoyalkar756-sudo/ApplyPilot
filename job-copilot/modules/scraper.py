import asyncio
import random
import yaml
from playwright.async_api import async_playwright
from playwright_stealth import stealth
from modules.tracker import add_job

# Load config
with open("job-copilot/config.yaml", "r") as f:
    config = yaml.safe_load(f)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

async def scrape_linkedin(keywords, location):
    """Simple LinkedIn scraper (public search results)."""
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
        except Exception as e:
            print(f"Failed to launch browser: {e}")
            return []
            
        context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
        page = await context.new_page()
        await stealth(page)

        # LinkedIn public job search URL
        search_url = f"https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}&f_TPR=r604800" # last 7 days
        
        print(f"Scraping LinkedIn: {search_url}")
        try:
            await page.goto(search_url, timeout=60000)
            await asyncio.sleep(random.uniform(3, 8))

            # Basic extraction (LinkedIn often changes selectors, these are placeholders)
            job_cards = await page.query_selector_all(".base-card")
            
            jobs_found = []
            for card in job_cards[:10]: # Limit to top 10 for testing
                try:
                    title_elem = await card.query_selector(".base-search-card__title")
                    company_elem = await card.query_selector(".base-search-card__subtitle")
                    loc_elem = await card.query_selector(".job-search-card__location")
                    url_elem = await card.query_selector(".base-card__full-link")
                    
                    if not all([title_elem, company_elem, loc_elem, url_elem]):
                        continue
                        
                    title = await title_elem.inner_text()
                    company = await company_elem.inner_text()
                    loc = await loc_elem.inner_text()
                    url = await url_elem.get_attribute("href")
                    
                    job_data = {
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": loc.strip(),
                        "salary": "N/A", 
                        "description": "", 
                        "url": url.split('?')[0],
                        "posting_date": "Recently"
                    }
                    
                    job_id = add_job(job_data)
                    if job_id:
                        jobs_found.append(job_data)
                        print(f"Added job: {title} at {company}")
                    
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                except Exception:
                    continue
        except Exception as e:
            print(f"Error during scraping: {e}")
            jobs_found = []

        await browser.close()
        return jobs_found

async def run_scrapers():
    roles = config.get("target_roles", ["Software Engineer"])
    locations = config.get("locations", ["Remote"])
    
    all_jobs = []
    for role in roles:
        for loc in locations:
            jobs = await scrape_linkedin(role, loc)
            all_jobs.extend(jobs)
            await asyncio.sleep(random.uniform(2, 5)) 
    
    return all_jobs

if __name__ == "__main__":
    pass
