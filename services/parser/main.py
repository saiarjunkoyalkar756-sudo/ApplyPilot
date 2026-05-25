from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.shared.models import Resume
from services.shared.database import get_db

app = FastAPI(title="Job Copilot Parser Service")

@app.post("/api/v1/resumes/upload", status_code=202)
def upload_resume(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    resume_id = uuid.uuid4()
    
    # MVP: Mock saving and parsing. You can later integrate `job-copilot/modules/parser.py` here.
    file_path = f"/tmp/{resume_id}_{file.filename}"
    
    new_resume = Resume(
        id=resume_id,
        filename=file.filename,
        storage_path=file_path,
        parsed_data={"status": "parsing"}
    )
    db.add(new_resume)
    db.commit()
    
    return {
        "id": str(resume_id),
        "status": "parsing",
        "upload_url": file_path,
        "message": "Resume uploaded successfully and queued for AI parsing."
    }
