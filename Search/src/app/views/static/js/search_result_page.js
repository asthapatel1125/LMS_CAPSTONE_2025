document.addEventListener("DOMContentLoaded", function() {
    // Get the search query from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get("query") || ""; // Default to empty string if no query is provided
    // Assign the search query to a global variable or store it for later use
    window.searchQuery = query;
    document.addEventListener("DOMContentLoaded", function() {
    // Get the search query from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get("query") || ""; // Default to empty string if no query is provided
    // Assign the search query to a global variable or store it for later use
    console.log("Search Result Page - Query Entered:", query);

    window.searchQuery = query;
    // Fetch books based on the query (initial load)
    fetchBooks(query);
});
    // Fetch books based on the query (initial load)
    fetchBooks(query);
});

// Function to fetch books from the backend based on the search query
async function fetchBooks(query) {
    try {
        const response = await fetch(`/search/searchQuery?query=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.message) {
            // Display no results message if no books found
            document.getElementById('bookCardContainer').innerHTML = `<div>No books found matching your search.</div>`;
        } else {
            // Display the books
            displayBooks(data.books);
        }
    } catch (error) {
        console.error("Error fetching search results:", error);
    }
}

// Function to display books as clickable buttons that lead to item_info.html
function displayBooks(books) {
    const bookCardContainer = document.getElementById('bookCardContainer');
    bookCardContainer.innerHTML = ''; // Clear any existing cards

    if (books && books.length === 0) {
        bookCardContainer.innerHTML = `<div>No books found matching your criteria.</div>`;
        return;
    }

    books.forEach(book => {
        const card = document.createElement('div');
        card.classList.add("col-12", "col-md-6", "col-lg-4", "my-3");

        // Create a button for each book that links to the book info page
        const bookButton = document.createElement('button');
        bookButton.classList.add('btn', 'btn-outline-dark', 'w-100');
        bookButton.setAttribute('onclick', `window.location.href='/search/book_info?isbn=${book.isbn}'`);

        bookButton.innerHTML = `
            <div class="card w-100">
                <div class="row g-0 p-1">
                    <!-- Image on the left -->
                    <div class="col-2 d-flex justify-content-center align-items-center">
                        <img src="${book.imageUrl}" class="book-cover img-fluid" alt="...">
                    </div>
                    <!-- Text on the right -->
                    <div class="col-10">
                        <h5 class="card-header">${book.title}</h5>
                        <div class="card-body">
                          <h6 class="card-title">Author: ${book.author}</h6>
                          <h6 class="card-title">Genre: ${book.genre}</h6>
                          <h6 class="card-title">Format: ${book.format}</h6>
                          <h6 class="card-title">Status: ${book.status}</h6>
                          <button type="submit" class="btn btn-custom-size px-5">Place Hold</button>
                        </div>
                    </div> 
                </div>
            </div>
        `;

        bookCardContainer.appendChild(bookButton);
    });
}

// Function to apply all the filters and send to the backend
function applyFilters() {
    // Get the current search query from the URL (this is your query parameter)
    const searchQuery = window.searchQuery || new URLSearchParams(window.location.search).get("query") || "";    // Collecting filter values
    const genreFilters = getCheckedBoxes('#collapseThree .form-check-input');
    const formatFilters = getCheckedBoxes('#collapseTwo .form-check-input');
    const availabilityFilters = getCheckedBoxes('#collapseOne .form-check-input');
    const audienceFilters = getCheckedBoxes('#collapseFour .form-check-input');
    const ratingFilters = getCheckedBoxes('#collapseFive .form-check-input');

    // Display loading indicator
    const bookCardContainer = document.getElementById('bookCardContainer');
    bookCardContainer.innerHTML = `<div>Loading...</div>`;  // Show loading text

    // Sending filter data and search query to the backend
    fetch('/search/filter_books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            searchQuery: searchQuery,  // Include the query from the URL
            genres: genreFilters,
            formats: formatFilters,
            availability: availabilityFilters,
            audience: audienceFilters,
            ratings: ratingFilters,
        }),
    })
    .then(response => response.json())
    .then(filteredBooks => {
        // Clear the container and display the filtered books
        displayBooks(filteredBooks);
    })
    .catch(error => {
        console.error('Error:', error);
        bookCardContainer.innerHTML = `<div>Error fetching books. Please try again later.</div>`;  // Display error message
    });
}

// Function to get the checked checkbox values
function getCheckedBoxes(form_id) {
    const checkboxes = document.querySelectorAll(form_id);
    const checkedValues = [];

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            checkedValues.push(checkbox.value);
        }
    });

    return checkedValues;
}
