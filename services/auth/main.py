from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.shared.models import User
from services.shared.database import get_db

app = FastAPI(title="Job Copilot Auth Service")

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/api/v1/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # In production, securely hash the password using Passlib + Argon2
    new_user = User(
        email=user.email,
        password_hash=user.password, # MVP: raw password. Switch to hashed for Phase 2!
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Mock JWT logic for MVP
    return {"access_token": f"mock_jwt_token_for_{new_user.id}", "token_type": "Bearer"}

@app.post("/api/v1/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.password_hash != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
        
    return {"access_token": f"mock_jwt_token_for_{db_user.id}", "token_type": "Bearer"}
