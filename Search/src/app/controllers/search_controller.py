from models.books import *
from typing import List
books = [
        Book(
            title="The Great Adventure",
            author="John Doe",
            genre="Adventure",
            rating=4,
            kidFriendly=True,
            description="A thrilling journey through uncharted territories.",
            format="Hardcover",
            pageNumber=300,
            publisher="Adventure Press",
            status="Available",
            isbn="123-456-7890",
            numOfMins=360,
            numCopies=10
        )
    ]
   
# Get Search query
def retrieve_searchQuery_list(query: str) -> List[Book]:
 
    print(f'controller query: {query}')
    book_by_title = get_books_by_title(query)  # List
    print(f'books by title {book_by_title}')
    book_by_author = get_books_by_author(query)  # List
    book_by_genre = get_books_by_genre(query)  # List
    book_by_publisher = get_books_by_publisher(query)  # List
    '''book_by_title = books
    book_by_author = books
    book_by_genre = books
    book_by_publisher = books'''
    
    # Combine all the lists
    all_books = book_by_title + book_by_author + book_by_genre + book_by_publisher
    print(f'all books:', all_books)
    # Remove duplicates by creating a set based on a unique identifier (e.g., combination of title and isbn)
    unique_books = {tuple(book.model_dump().items()) for book in all_books}  # Create a set of unique book identifiers
    
    # If you want to convert back to a list of dictionaries:
    search_result = [Book(**dict(book)) for book in unique_books]  # Convert back to Book instances
    
    return search_result


def retrieve_popular_books(rating: float) -> List[Book]:
    return get_books_by_rating(rating)  # return popular books list

def retrieve_newest_books() -> List[Book]:
    # return get_latest_releases()  # return newest releases list
    return books