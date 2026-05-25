from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.shared.models import Application
from services.shared.database import get_db

app = FastAPI(title="Job Copilot Applier Service")

class AppStart(BaseModel):
    match_id: str
    auto_submit: bool = False
    generate_tailored_resume: bool = True
    generate_cover_letter: bool = True

@app.post("/api/v1/applications", status_code=201)
def start_application(app_req: AppStart, db: Session = Depends(get_db)):
    app_id = uuid.uuid4()
    
    new_app = Application(
        id=app_id,
        match_id=app_req.match_id,
        status="queued"
    )
    db.add(new_app)
    db.commit()
    
    # Trigger Celery Task
    from services.applier.tasks import fill_application_task
    fill_application_task.delay(application_id=str(app_id))
    
    return {
        "id": str(app_id),
        "status": "queued",
        "websocket_url": f"wss://api.jobcopilot.io/ws/applications/{app_id}",
        "message": "Application automation queued via Playwright cluster."
    }

class AppApprove(BaseModel):
    approved: bool
    notes: str = ""

@app.post("/api/v1/applications/{app_id}/approve")
def approve_application(app_id: str, req: AppApprove, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == app_id).first()
    
    if application:
        application.status = "submitted" if req.approved else "cancelled"
        db.commit()
        
    return {
        "id": app_id, 
        "status": application.status if application else "not_found",
        "message": "Application manually approved and submitted." if req.approved else "Application cancelled."
    }
