from fastapi import HTTPException, status
from controllers.token import *
from models.customers import *

SECRET_KEY = "lms2025"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def verify_user(email: str, password: str):
    user = get_user(email)
    if not user or user.password != password:
        return False
    return True

# Logic for handling login
def handle_login(email: str, pword: str):
    if verify_user(email, pword):
        token = create_jwt("FastAPI", email, ACCESS_TOKEN_EXPIRE_MINUTES)
        return token
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

# Logic for handling registration
def handle_registration(fname: str, lname: str, email: str, password: str, age: int):
    user = get_user(email)
    if user is None:
        return create_user(Customer(firstName=fname, lastName=lname, email=email, password=password, 
                                    address=Address(streetAddress="", city="", state="", country=""), 
                                    age=age))
    raise HTTPException(status_code=400, detail="Email already registered")    
    
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

#-----------------JWT TOKEN VALIDATION------------------

"""
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
"""