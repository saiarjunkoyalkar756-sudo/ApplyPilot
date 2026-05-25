import pdfplumber
import docx
import os
from services.shared.celery_app import celery_app
from services.shared.logging import get_logger
from services.shared.database import SessionLocal
from services.shared.models import Resume
from openai import OpenAI

logger = get_logger("services.parser.tasks")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@celery_app.task(name="services.parser.tasks.parse_resume")
def parse_resume_task(resume_id: str):
    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            logger.error("resume_not_found", resume_id=resume_id)
            return

        logger.info("parsing_started", resume_id=resume_id, file=resume.filename)
        
        # Extraction logic
        text = ""
        ext = os.path.splitext(resume.filename)[1].lower()
        if ext == ".pdf":
            with pdfplumber.open(resume.storage_path) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif ext == ".docx":
            doc = docx.Document(resume.storage_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            
        # AI Parsing
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract resume details into JSON."},
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        resume.parsed_data = response.choices[0].message.content
        db.commit()
        logger.info("parsing_complete", resume_id=resume_id)
        
    except Exception as e:
        logger.error("parsing_failed", resume_id=resume_id, error=str(e))
        db.rollback()
    finally:
        db.close()
