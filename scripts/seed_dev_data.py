import os
from services.shared.database import SessionLocal
from services.shared.models import User, Resume, Job, Match
import uuid

def seed():
    db = SessionLocal()
    
    # 1. Create Test User
    user = User(
        email="test@example.com",
        password_hash="devpassword",
        first_name="Sai Arjun",
        last_name="Koyalkar"
    )
    db.add(user)
    db.flush()
    
    # 2. Create Sample Jobs
    jobs = [
        Job(title="Senior Python Developer", company="Google", location="Mountain View, CA", url="https://google.com/jobs/1"),
        Job(title="Backend Engineer", company="Meta", location="Remote", url="https://meta.com/jobs/2"),
        Job(title="AI Research Engineer", company="OpenAI", location="San Francisco, CA", url="https://openai.com/jobs/3")
    ]
    db.add_all(jobs)
    db.flush()
    
    # 3. Create Resume
    resume = Resume(
        user_id=user.id,
        filename="resume.pdf",
        storage_path="/tmp/resume.pdf",
        parsed_data={"skills": ["Python", "SQL", "FastAPI"]}
    )
    db.add(resume)
    db.flush()
    
    # 4. Create Matches
    matches = [
        Match(user_id=user.id, resume_id=resume.id, job_id=jobs[0].id, match_score=92.5),
        Match(user_id=user.id, resume_id=resume.id, job_id=jobs[1].id, match_score=85.0),
        Match(user_id=user.id, resume_id=resume.id, job_id=jobs[2].id, match_score=78.2)
    ]
    db.add_all(matches)
    
    db.commit()
    db.close()
    print("Database seeded with sample development data.")

if __name__ == "__main__":
    seed()
