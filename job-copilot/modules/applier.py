import asyncio
import os
import json
import sqlite3
import random
import time
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth
try:
    from modules.tracker import DB_PATH
except ImportError:
    # Fallback if running from within modules/
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from tracker import DB_PATH

# Create necessary directories
os.makedirs("job-copilot/debug/screenshots", exist_ok=True)
os.makedirs("job-copilot/cookies", exist_ok=True)

async def apply_to_job(job_id: int):
    """
    Main entry point for auto-applying to a job.
    1. Read job info from DB
    2. Read resume info from resume.json
    3. Detect platform and fill form
    4. Human-in-the-loop validation
    5. Update DB
    """
    # 1. Read job info
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()

    if not job:
        print(f"Error: Job ID {job_id} not found in database.")
        return False

    # 2. Read resume info
    resume_path = "job-copilot/resume.json"
    if not os.path.exists(resume_path):
        print(f"Error: {resume_path} not found.")
        return False
    
    with open(resume_path, "r") as f:
        resume_data = json.load(f)

    # 3. Launch browser
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Headful mode as requested
        
        # Load cookies if they exist
        context_args = {}
        cookie_path = f"job-copilot/cookies/{job['company'].lower().replace(' ', '_')}_cookies.json"
        if os.path.exists(cookie_path):
            context_args["storage_state"] = cookie_path
            
        context = await browser.new_context(**context_args)
        page = await context.new_page()
        await stealth(page)

        print(f"Applying for: {job['title']} at {job['company']}")
        print(f"URL: {job['url']}")

        try:
            # 4. Navigate to URL
            await page.goto(job['url'], wait_until="networkidle")
            await asyncio.sleep(random.uniform(2, 4))

            # 5. Detect Platform and Fill
            success = False
            if "boards.greenhouse.io" in job['url']:
                success = await fill_greenhouse(page, resume_data)
            elif "jobs.lever.co" in job['url']:
                success = await fill_lever(page, resume_data)
            elif "myworkdayjobs.com" in job['url']:
                success = await fill_workday(page, resume_data)
            elif "linkedin.com" in job['url']:
                success = await fill_linkedin(page, resume_data)
            elif "indeed.com" in job['url']:
                success = await fill_indeed(page, resume_data)
            else:
                success = await fill_generic(page, resume_data)

            if success:
                # 6. Human-in-the-loop: Stop before final submit
                print("\n--- PREVIEW MODE ---")
                print("Form filled. Please review the application in the browser.")
                print("You have 30 seconds to press ENTER to confirm submission or 'c' to cancel.")
                
                # Using a simple input with timeout simulation
                user_input = await async_input("Press ENTER to SUBMIT, or type 'c' to CANCEL (Auto-cancel in 30s): ", timeout=30)
                
                if user_input.lower() == "":
                    # 7. Submit
                    print("Submitting...")
                    # Try to find a submit button
                    submit_button = await page.query_selector("button[type='submit'], input[type='submit'], #submit-application")
                    if submit_button:
                        await submit_button.click()
                        await asyncio.sleep(5) # Wait for submission response
                        
                        # 8. Log success
                        update_db_after_apply(job_id, "auto")
                        print(f"Successfully applied to {job['company']}!")
                        # Save cookies
                        await context.storage_state(path=cookie_path)
                    else:
                        print("Submit button not found. Please click it manually and update the dashboard.")
                else:
                    print("Submission cancelled by user.")
                    update_db_status(job_id, "manual")
            else:
                print("Failed to auto-fill the form.")
                screenshot_path = f"job-copilot/debug/screenshots/failed_{job_id}_{int(time.time())}.png"
                await page.screenshot(path=screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
                update_db_status(job_id, "failed")

        except Exception as e:
            print(f"An error occurred during application: {e}")
            screenshot_path = f"job-copilot/debug/screenshots/error_{job_id}_{int(time.time())}.png"
            await page.screenshot(path=screenshot_path)
            update_db_status(job_id, "error")
        finally:
            await browser.close()

async def fill_greenhouse(page, resume_data):
    print("Detected Greenhouse platform.")
    try:
        await page.fill("input[name='job_application[first_name]']", resume_data.get('name', '').split(' ')[0])
        await page.fill("input[name='job_application[last_name]']", ' '.join(resume_data.get('name', '').split(' ')[1:]))
        await page.fill("input[name='job_application[email]']", resume_data.get('email', ''))
        await page.fill("input[name='job_application[phone]']", resume_data.get('phone', ''))
        
        # Resume upload
        resume_file = resume_data.get("resume_pdf_path", "resume.pdf")
        if os.path.exists(resume_file):
            await page.set_input_files("input[type='file'][accept*='pdf']", resume_file)
            
        # LinkedIn
        if resume_data.get("linkedin"):
            await page.fill("input[name*='linkedin']", resume_data["linkedin"])
            
        return True
    except Exception as e:
        print(f"Greenhouse fill error: {e}")
        return False

async def fill_lever(page, resume_data):
    print("Detected Lever platform.")
    try:
        await page.fill("input[name='name']", resume_data.get('name', ''))
        await page.fill("input[name='email']", resume_data.get('email', ''))
        await page.fill("input[name='phone']", resume_data.get('phone', ''))
        
        # Resume upload
        resume_file = resume_data.get("resume_pdf_path", "resume.pdf")
        if os.path.exists(resume_file):
            await page.set_input_files("input[type='file']", resume_file)
            
        return True
    except Exception as e:
        print(f"Lever fill error: {e}")
        return False

async def fill_workday(page, resume_data):
    print("Detected Workday platform (Limited support).")
    # Workday is complex and often requires login
    return await fill_generic(page, resume_data)

async def fill_linkedin(page, resume_data):
    print("Detected LinkedIn.")
    # Usually "Easy Apply"
    return await fill_generic(page, resume_data)

async def fill_indeed(page, resume_data):
    print("Detected Indeed.")
    return await fill_generic(page, resume_data)

async def fill_generic(page, resume_data):
    print("Using generic fallback filler...")
    try:
        # Highlight common fields
        selectors = {
            "name": "input[name*='name'], input[id*='name']",
            "email": "input[name*='email'], input[id*='email']",
            "phone": "input[name*='phone'], input[id*='phone']"
        }
        
        for field, selector in selectors.items():
            elements = await page.query_selector_all(selector)
            for el in elements:
                await el.evaluate("el => el.style.backgroundColor = 'yellow'")
                if field == "name": await el.fill(resume_data.get('name', ''))
                if field == "email": await el.fill(resume_data.get('email', ''))
                if field == "phone": await el.fill(resume_data.get('phone', ''))
        
        return True
    except Exception as e:
        print(f"Generic fill error: {e}")
        return False

def update_db_after_apply(job_id, method):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET status = 'applied', applied_date = datetime('now') WHERE id = ?", (job_id,))
    cursor.execute('''
        INSERT INTO applications (job_id, status, applied_date, notes)
        VALUES (?, 'applied', datetime('now'), ?)
    ''', (job_id, f"auto via {method}"))
    conn.commit()
    conn.close()

def update_db_status(job_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()

async def async_input(prompt, timeout=30):
    """Wait for user input with a timeout."""
    print(prompt, end='', flush=True)
    loop = asyncio.get_event_loop()
    user_input_task = loop.run_in_executor(None, sys.stdin.readline)
    try:
        result = await asyncio.wait_for(user_input_task, timeout=timeout)
        return result.strip()
    except asyncio.TimeoutError:
        print("\nTimeout reached. Defaulting to cancel.")
        return "c"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        asyncio.run(apply_to_job(int(sys.argv[1])))
