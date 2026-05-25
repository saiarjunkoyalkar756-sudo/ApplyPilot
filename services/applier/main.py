from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, List
import sys
import os
import uuid
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.shared.models import Application
from services.shared.database import get_db

app = FastAPI(title="Job Copilot Applier Service")

class AppStart(BaseModel):
    match_id: str
    auto_submit: bool = False
    generate_tailored_resume: bool = True
    generate_cover_letter: bool = True

# Connection manager for WebSockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, application_id: str):
        await websocket.accept()
        if application_id not in self.active_connections:
            self.active_connections[application_id] = []
        self.active_connections[application_id].append(websocket)

    def disconnect(self, websocket: WebSocket, application_id: str):
        if application_id in self.active_connections:
            self.active_connections[application_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_status(self, application_id: str, message: dict):
        if application_id in self.active_connections:
            for connection in self.active_connections[application_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/applications/{application_id}")
async def websocket_endpoint(websocket: WebSocket, application_id: str):
    await manager.connect(websocket, application_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, application_id)

@app.post("/api/v1/applications/{application_id}/status")
async def update_status_broadcast(application_id: str, status_update: dict):
    await manager.broadcast_status(application_id, status_update)
    return {"status": "broadcasted"}

@app.post("/api/v1/applications", status_code=201)
def start_application(app_req: AppStart, db: Session = Depends(get_db)):
    app_id = uuid.uuid4()
    new_app = Application(id=app_id, match_id=app_req.match_id, status="queued")
    db.add(new_app)
    db.commit()
    from services.applier.tasks import fill_application_task
    fill_application_task.delay(application_id=str(app_id))
    return {
        "id": str(app_id),
        "status": "queued",
        "websocket_url": f"ws://localhost:8006/ws/applications/{app_id}",
        "message": "Application automation queued via Playwright cluster."
    }

@app.get("/api/v1/applications/{application_id}/screenshot")
async def get_application_screenshot(application_id: str):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="https://via.placeholder.com/800x600?text=Application+Form+Proof")

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
