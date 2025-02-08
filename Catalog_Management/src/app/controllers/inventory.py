from controllers.token import *
from models.books import *

def handle_add_book(title: str, isbn: str, author: str, genre: str, rating: float,
                    kidFriendly: bool, description: str, format: str, pageNumber: int, 
                    bookID: str, publisher: str, status: str):
    book = get_book(isbn)
    if book is None:
        return create_book(Book(title=title, isbn=isbn, author=author, genre=genre, rating=rating,
                kidFriendly=kidFriendly, description=description, format=format, pageNumber=pageNumber, 
                bookID=bookID, publisher=publisher, status=status))
    return "Error"