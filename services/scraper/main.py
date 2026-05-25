from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.shared.models import Job
from services.shared.database import get_db

app = FastAPI(title="Job Copilot Scraper Service")

class JobSearch(BaseModel):
    boards: List[str]
    keywords: str
    location: str
    remote: Optional[bool] = False
    experience_level: Optional[str] = "mid"
    days_posted: Optional[int] = 7

@app.post("/api/v1/scraper/jobs/search", status_code=202)
def search_jobs(search: JobSearch, db: Session = Depends(get_db)):
    # MVP: Integrates Playwright scraping asynchronously via Celery or BackgroundTasks
    job_batch_id = uuid.uuid4()
    
    return {
        "job_id": str(job_batch_id),
        "status": "queued",
        "message": f"Scraping queued for '{search.keywords}' in '{search.location}' on boards: {search.boards}"
    }
