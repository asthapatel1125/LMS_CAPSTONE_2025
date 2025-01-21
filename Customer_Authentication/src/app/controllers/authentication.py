from fastapi import HTTPException, status
import jwt
from controllers.session import create_session, delete_session
from models.customers import *

SECRET_KEY = "lms2025"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def verify_user(email: str, password: str):
    user = await get_user(email)
    if not user or user["password"] != password:
        return False
    return True

# Logic for handling login
async def handle_login(email: str, pword: str):
    if await verify_user(email, pword):
        session_id = create_session(email)
        print('I AM IN HANDLE LOGIN')
        return session_id
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

# Logic for handling logout
def handle_logout(session_id: str):
    delete_session(session_id)

# Logic for handling registration
def handle_registration(username: str, email: str, password: str, confirm_password: str):
    if username in mock_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    mock_users_db[username] = {"username": username, "password": password, "email": email}

# Logic for handling forgot password
def handle_forgot_password(email: str):
    for user in mock_users_db.values():
        if user["email"] == email:
            # Simulate sending a reset link (replace with actual email logic)
            return {"message": f"A reset link has been sent to {email}"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Email not found"
    )

# Logic for validating JWT token
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return {"message": "Token is valid", "username": username}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
