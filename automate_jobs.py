import asyncio
import os
import sys
import json
import sqlite3

# Add project to path
sys.path.append(os.path.abspath("job-copilot"))

from modules.scraper import run_scrapers
from modules.matcher import score_all_new_jobs
from modules.tracker import get_db_connection

async def main():
    print("--- Phase 1: Scraping Jobs ---")
    try:
        jobs = await run_scrapers()
        print(f"Found {len(jobs)} new jobs.")
    except Exception as e:
        print(f"Scraping failed: {e}")
        print("Note: If Playwright fails due to missing dependencies, you may need to run this on a local machine with a GUI.")
        return

    print("\n--- Phase 2: Analyzing and Matching Resume ---")
    try:
        score_all_new_jobs()
        print("Matching complete.")
    except Exception as e:
        print(f"Matching failed: {e}")

    print("\n--- Phase 3: Top Recommendations ---")
    conn = sqlite3.connect("job-copilot/database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, match_score, url FROM jobs WHERE match_score >= 70 ORDER BY match_score DESC LIMIT 5")
    rows = cursor.fetchall()
    
    if not rows:
        print("No high-matching jobs found yet. Try broadening your search in config.yaml.")
    else:
        for row in rows:
            print(f"[{row['match_score']}% Match] {row['title']} at {row['company']}")
            print(f"   URL: {row['url']}")
            print("-" * 30)
    
    conn.close()
    print("\nTo apply, use the Dashboard (python3 job-copilot/main.py) or run: python3 -c \"from modules.applier import open_application; import asyncio; import json; resume=json.load(open('job-copilot/resume.json')); asyncio.run(open_application('<JOB_URL>', resume))\"")

if __name__ == "__main__":
    asyncio.run(main())
