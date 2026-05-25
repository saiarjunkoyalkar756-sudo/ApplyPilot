from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.shared.models import Match, Job
from services.shared.database import get_db

app = FastAPI(title="Job Copilot Matcher Service")

@app.get("/api/v1/matches")
def get_matches(user_id: str, min_score: float = 0.7, limit: int = 20, db: Session = Depends(get_db)):
    from services.shared.models import Resume, Match
    from services.shared.vector import search_similar_jobs
    import uuid

    # 1. Get the latest resume for the user
    resume = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).first()
    if not resume or not resume.parsed_data or 'embedding' not in resume.parsed_data:
        # Fallback to current behavior if no vector data
        matches = db.query(Match).filter(Match.match_score >= (min_score * 100)).limit(limit).all()
    else:
        # 2. Perform semantic vector search
        results = search_similar_jobs(resume.parsed_data['embedding'], limit=limit)
        
        matches = []
        for res in results:
            if res.score < min_score:
                continue
                
            # Check if match already exists in DB
            existing_match = db.query(Match).filter(
                Match.user_id == user_id, 
                Match.job_id == uuid.UUID(res.id)
            ).first()
            
            if not existing_match:
                # Create a new semantic match entry
                existing_match = Match(
                    user_id=user_id,
                    resume_id=resume.id,
                    job_id=uuid.UUID(res.id),
                    match_score=res.score * 100,
                    status="new"
                )
                db.add(existing_match)
                db.commit()
                db.refresh(existing_match)
            
            matches.append(existing_match)

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
