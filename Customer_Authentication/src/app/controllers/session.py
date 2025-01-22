from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from uuid import uuid4
from datetime import datetime
from typing import Optional

router = APIRouter()
sessions = {}

SESSION_EXPIRATION_TIME = 3600

def create_session(email: str) -> str:
    session_id = str(uuid4())
    sessions[session_id] = {
        "email": email,
        "created_at": datetime.utcnow(),
    }
    return session_id

def get_session(session_id: str) -> Optional[dict]:
    session = sessions.get(session_id)
    if session:
        if (datetime.utcnow() - session["created_at"]).total_seconds() > SESSION_EXPIRATION_TIME:
            del sessions[session_id]
            return None
        return session
    return None

def delete_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]