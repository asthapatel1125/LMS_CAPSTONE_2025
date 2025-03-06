from controllers.token import *
from models.books import *

def handle_add_book(title: str, isbn: str, author: str, genre: str, rating: float,
                    kidFriendly: bool, description: str, format: str, pageNumber: int, 
                    numCopies: int, publisher: str, status: str):
    book = get_book(isbn)
    if book is None:
        return create_book(Book(title=title, isbn=isbn, author=author, genre=genre, rating=rating,
                kidFriendly=kidFriendly, description=description, format=format, pageNumber=pageNumber, 
                numCopies=numCopies, publisher=publisher, status=status))
    return "Error"

def handle_modify_book(title: str, isbn: str, author: str, genre: str, numCopies: int, description: str, kidFriendly: bool, format: str, pageNumber: int, publisher: str, status: str):
    book = get_book(isbn)
    if book is not None:
        updates = {"title": title, "isbn": isbn, "author": author, "genre": genre, "numCopies": numCopies,
                    "description": description, "kidFriendly": kidFriendly, "format": format, "pageNumber": pageNumber,
                    "publisher": publisher, "status": status}
        update_occurred = False
        for field, new in updates.items():
            if getattr(book, field) != new:
                update_method = globals().get(f"update_{field}")
                if update_method:
                    response = update_method(book.isbn, new)
                    print(f"\n\n{response}\n\n")
                    if response:
                        update_occurred = True
        return update_occurred
    return False

    