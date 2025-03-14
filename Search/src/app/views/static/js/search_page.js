let selectedBook = null;
let searchResults = []; // Store search results globally

document.addEventListener("DOMContentLoaded", function() {
    fetchPopularBooks();
    fetchNewestBooks();
    
    // Add event listener for the search button
    const searchButton = document.getElementById('searchButton');
    searchButton.addEventListener('click', handleSearchButtonClick);

    // Monitor input changes to display suggestions dynamically
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', searchBooks);
});

// Function to fetch popular books from the backend
async function fetchPopularBooks() {
    try {
        const response = await fetch("/search/popular");
        const data = await response.json();
        
        if (data.popular_books) {
            displayBooksForCarousel(data.popular_books, "popularCarouselInner");
        } else {
            console.error('No popular books found in the response');
        }
    } catch (error) {
        console.error("Error fetching popular books:", error);
    }
}

// Function to fetch newest books from the backend
async function fetchNewestBooks() {
    try {
        const response = await fetch("/search/newest");
        const data = await response.json();
        
        if (data.newest_books) {
            displayBooksForCarousel(data.newest_books, "newestCarouselInner");
        }
    } catch (error) {
        console.error("Error fetching newest books:", error);
    }
}

// Function to search books dynamically when "Search" input changes
async function searchBooks() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    
    if (query === "") {
        clearSearchResults();
        selectedBook = null;
        document.getElementById('bookDetails').innerHTML = '';
    } else {
        try {
            const response = await fetch(`/search/searchQuery?query=${encodeURIComponent(query)}`, {
                method: "GET",
                headers: { "Content-Type": "application/json" }
            });

            if (response.ok) {
                const data = await response.json();
                
                // Store the results globally for later use
                if (data.books && data.books.length > 0) {
                    searchResults = data.books;
                    displaySearchResults(searchResults);
                } else {
                    clearSearchResults();
                    const bookList = document.getElementById('bookList');
                    bookList.innerHTML = '<li class="list-group-item">No books found.</li>';
                }
            } else {
                clearSearchResults();
                const bookList = document.getElementById('bookList');
                bookList.innerHTML = '<li class="list-group-item">Error fetching books.</li>';
            }
        } catch (error) {
            console.error("Error searching for books:", error);
            clearSearchResults();
            const bookList = document.getElementById('bookList');
            bookList.innerHTML = '<li class="list-group-item">Error fetching books.</li>';
        }
    }
}

// Handle search button click - Redirect to search result page
function handleSearchButtonClick() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    console.log(query);
    
    if (query) {
        // Set the redirect URL dynamically using setAttribute
        const searchUrl = `/search/search_result_page?query=${encodeURIComponent(query)}`;
        window.location.setAttribute('href', searchUrl); // Using setAttribute for setting the location.href
    }
}



// Function to display books as search results (but not redirect yet)
function displaySearchResults(books) {
    console.log(books)
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; // Clear previous results

    books.forEach(book => {
        const listItem = document.createElement('li');
        listItem.classList.add('list-group-item');
        listItem.textContent = `${book.title} by ${book.author}`;
        listItem.onclick = function() {
          window.location.href = `/search/book_info?isbn=${book.isbn}`;
        };
        
        bookList.appendChild(listItem);
      });
}

// Function to clear the search results
function clearSearchResults() {
    document.getElementById('bookList').innerHTML = '';
}

// Function to display books in a carousel
function displayBooksForCarousel(booksToDisplay, carouselId) {
    const carouselInner = document.getElementById(carouselId);
    carouselInner.innerHTML = '';  // Clear existing content

    const chunkedBooks = chunkBooks(booksToDisplay, 5);

    chunkedBooks.forEach((chunk, index) => {
        const carouselItem = createCarouselItem(chunk, index);
        carouselInner.appendChild(carouselItem);
    });
}

// Helper function to group books into chunks
function chunkBooks(booksToDisplay, size) {
    const result = [];
    for (let i = 0; i < booksToDisplay.length; i += size) {
        result.push(booksToDisplay.slice(i, i + size));
    }
    return result;
}

// Function to create a carousel item with book images
function createCarouselItem(bookChunk, index) {
    const carouselItem = document.createElement('div');
    carouselItem.classList.add('carousel-item');
    if (index === 0) {
        carouselItem.classList.add('active');
    }

    const carouselItemInner = document.createElement('div');
    carouselItemInner.classList.add('row');

    bookChunk.forEach(book => {
        const bookCard = document.createElement('div');
        bookCard.classList.add('col-2', 'mb-4');

        const card = document.createElement('div');
        card.classList.add('card');

        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        const bookImage = document.createElement('img');
        bookImage.src = book.imageUrl;
        bookImage.classList.add('card-img-top');
        bookImage.alt = `${book.title} cover image`;

        cardBody.appendChild(bookImage);
        card.appendChild(cardBody);
        bookCard.appendChild(card);
        carouselItemInner.appendChild(bookCard);
    });

    carouselItem.appendChild(carouselItemInner);
    return carouselItem;
}

document.getElementById('searchButton').addEventListener('click', function(event) {
    const query = document.getElementById('searchInput').value.toLowerCase();
    if (!query) {
        event.preventDefault(); // Stop form submission if the query is empty
        return;
    }
    
    document.getElementById('hiddenSearchInput').value = query; // Set the hidden input value
});