from controllers.token import *
from models.books import *
from models.reservations import *

def handle_get_available_books():
    recent = get_recently_available()
    waiting = get_waiting_users()
    
    available_books = []
    
    for i in range(len(recent)):
        if recent[i]['isbn'] == waiting[i]['isbn']:
            available_books.append(
                {"title": get_book_title(waiting[i]['isbn']), 
                 "isbn": waiting[i]['isbn'], 
                 "rating": get_book_rating(waiting[i]['isbn']), 
                 "email": waiting[i]['user_email']}
                )
    return available_books
        
def handle_return_books_today():
    holds = get_due_today()
    due_today = []
    
    for i in range(len(holds)):
        due_today.append({
            "title": get_book_title(holds[i]['isbn']),
            "isbn": holds[i]['isbn'],
            "bookID": holds[i]['book_id'],
            "email": holds[i]["user_email"]
        })
    return due_today
    
def handle_return_books_soon():
    holds = get_due_soon()
    due_soon = []
    
    for i in range(len(holds)):
        due_date = holds[i]['expiration_date'].strftime('%m/%d/%Y')
        
        due_soon.append({
            "title": get_book_title(holds[i]['isbn']),
            "isbn": holds[i]['isbn'],
            "bookID": holds[i]['book_id'],
            "dueDate": due_date,
            "email": holds[i]["user_email"]
        })
    return due_soon        
