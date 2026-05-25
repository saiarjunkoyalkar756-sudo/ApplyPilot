from fastapi import FastAPI, Depends
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.shared.database import get_db

app = FastAPI(title="Job Copilot Resume Builder Service")

class TailorRequest(BaseModel):
    match_id: str
    job_id: str

@app.post("/api/v1/resumes/{resume_id}/tailor")
def tailor_resume(resume_id: str, req: TailorRequest):
    # MVP logic: Will call OpenAI to rewrite bullets based on Job ID description
    return {
        "resume_id": resume_id,
        "status": "tailored",
        "download_url": f"/files/tailored_resumes/{resume_id}_tailored.pdf",
        "message": "Resume successfully tailored and PDF generated."
    }
