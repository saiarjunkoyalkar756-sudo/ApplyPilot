import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
# Default to the Docker Compose development database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://jobcopilot:devpassword@localhost:5432/jobcopilot_dev")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
