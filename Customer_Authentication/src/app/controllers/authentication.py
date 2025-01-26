from controllers.token import *
from controllers.email_verif_code import *
from models.customers import *

def verify_user(email: str, password: str):
    user = get_user(email)
    if not user or user.password != password:
        return False
    return True

# Logic for handling login
def handle_login(email: str, pword: str):
    if verify_user(email, pword):
        token = create_jwt(email)
        return token
    else:
        return None

# Logic for handling registration
def handle_registration(fname: str, lname: str, email: str, password: str, age: int):
    user = get_user(email)
    if user is None:
        return create_user(Customer(firstName=fname, lastName=lname, email=email, password=password, 
                                    address=Address(streetAddress="", city="", state="", country=""), 
                                    age=age))
    return "Error"  
    
# Logic for handling forgot password
def handle_forgot_password(email: str):
    user = get_user(email)
    if user is None:
        return False
    return True

def handle_reset_password(request: Request, first_pass: str, second_pass: str):
    verif_email = get_verif_email(request)
    if first_pass == second_pass:
        change_password(verif_email, first_pass)
        return True
    return False
    
    