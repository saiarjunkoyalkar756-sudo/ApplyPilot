from services.shared.celery_app import celery_app
from services.shared.logging import get_logger
from services.shared.database import SessionLocal
from services.shared.models import Application, Match, Job, Resume
import asyncio
import os
import time
from playwright.async_api import async_playwright

logger = get_logger("services.applier.tasks")

@celery_app.task(name="services.applier.tasks.fill_application")
def fill_application_task(application_id: str):
    async def run():
        db = SessionLocal()
        try:
            app = db.query(Application).filter(Application.id == application_id).first()
            if not app:
                logger.error("application_not_found", app_id=application_id)
                return

            job = app.match.job
            resume = app.match.resume
            
            logger.info("application_started", app_id=application_id, job_url=job.url)
            app.status = "filling_form"
            db.commit()

            import requests
            def broadcast(msg):
                try:
                    requests.post(f"http://localhost:8006/api/v1/applications/{application_id}/status", json={"message": msg})
                except: pass

            broadcast("Starting browser...")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True) # Usually Headless in workers
                context = await browser.new_context()
                page = await context.new_page()
                
                try:
                    broadcast(f"Navigating to {job.company} portal...")
                    await page.goto(job.url, wait_until="networkidle", timeout=60000)
                    await asyncio.sleep(2)
                    
                    broadcast("Detecting form fields...")
                    # ... (selectors logic)
                    
                    broadcast("Filling personal information...")
                    # ... (filling logic)

                    for field, selector in selectors.items():
                        elements = await page.query_selector_all(selector)
                        for el in elements:
                            if field == "name": await el.fill(name)
                            if field == "email": await el.fill(email)
                            if field == "phone": await el.fill(phone)

                    broadcast("Uploading resume...")
                    # Check for resume upload input
                    upload_input = await page.query_selector("input[type='file']")
                    if upload_input and os.path.exists(resume.storage_path):
                        await upload_input.set_input_files(resume.storage_path)

                    broadcast("Taking proof screenshot...")
                    # Save a screenshot to prove we filled it
                    os.makedirs("/tmp/screenshots", exist_ok=True)
                    screenshot_path = f"/tmp/screenshots/{application_id}.png"
                    await page.screenshot(path=screenshot_path)
                    
                    broadcast("Application ready for review!")
                    # Update status
                    app.status = "awaiting_approval"
                    app.screenshots = [screenshot_path]
                    db.commit()
                    logger.info("application_form_filled", app_id=application_id)

                except Exception as inner_e:
                    app.status = "error"
                    db.commit()
                    logger.error("application_fill_failed", error=str(inner_e))
                finally:
                    await browser.close()
        except Exception as e:
            logger.error("application_task_failed", error=str(e))
        finally:
            db.close()

    asyncio.run(run())
