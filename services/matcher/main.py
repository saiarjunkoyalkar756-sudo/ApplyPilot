from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.shared.models import Match, Job
from services.shared.database import get_db

app = FastAPI(title="Job Copilot Matcher Service")

@app.get("/api/v1/matches")
def get_matches(min_score: int = 70, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    matches = db.query(Match).filter(Match.match_score >= min_score).limit(limit).offset(offset).all()
    
    # MVP Response Structure
    return {
        "total": len(matches),
        "matches": [
            {
                "id": str(m.id),
                "match_score": m.match_score,
                "status": m.status,
                "job": {
                    "id": str(m.job.id) if m.job else None,
                    "title": m.job.title if m.job else "Unknown",
                    "company": m.job.company if m.job else "Unknown",
                    "url": m.job.url if m.job else "#"
                }
            }
            for m in matches
        ]
    }
