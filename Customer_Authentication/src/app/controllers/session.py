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

@router.post("/create-session")
async def create_user_session(username: str):
    session_id = create_session(username)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

@router.get("/validate-session")
async def validate_user_session(session_id: Optional[str] = Depends(lambda: None)):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ID is required",
        )
    session = get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )
    return {"username": session["username"]}

@router.post("/delete-session")
async def delete_user_session(session_id: Optional[str] = Depends(lambda: None)):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID is required",
        )
    delete_session(session_id)
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_id")
    return response
