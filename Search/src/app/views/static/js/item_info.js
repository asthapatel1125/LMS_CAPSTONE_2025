// Get the ISBN from the URL
//const urlParams = new URLSearchParams(window.location.search);
//const isbn = urlParams.get('isbn');
document.addEventListener("DOMContentLoaded", function() {
    // Get the search query from the URL
    console.log("Inside Book_info.js");
    const urlParams = new URLSearchParams(window.location.search);
    const isbn = urlParams.get("isbn") || ""; // Default to empty string if no query is provided
    console.log(isbn)
    // Fetch books based on the query (initial load)
    fetchBooks(isbn);

    // Assign the search query to a global variable or store it for later use
    window.searchQuery = query;
});

function fetchBooks(isbn) {
    // Fetch the book information based on the ISBN
    fetch(`/search/book_info/${isbn}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch book data');
            }
            return response.json();
        })
        .then(itemData => {
            // Pass the data to the displayBookInfo function
            displayBookInfo(itemData.book_info);
        })
        .catch(error => console.error('Error fetching book info:', error));
}


function displayBookInfo(itemData) {
    const title = document.getElementById("book-title");
    title.textContent = '📖 ' + itemData.title;

    document.getElementById("book-cover").innerHTML = `<img src="${itemData.coverImage}" class="book-cover img-fluid" alt="Book Cover">`;

    document.getElementById("main-book-info").innerHTML = `
        <h6 class="card-title">${itemData.author}</h6>
        <p class="card-text">Rating: ${getRating(itemData)}</p>
        <p class="card-text">${itemData.synopsis}</p>
        <p class="card-text">Copies Available: ${itemData.copies}</p>`;

    document.getElementById("book-info").innerHTML = `
        <p class="card-text">ISBN: ${itemData.isbn}</p>
        <p class="card-text">Format: ${itemData.format}</p>
        <p class="card-text">Genre(s):</p>
        <p class="card-text">Book Length:</p>
        <p class="card-text">Publisher:</p>
        <p class="card-text">Release Date: ${itemData.year}</p>`;

    itemData.reviews.forEach(review => {
        const card = document.createElement('div');
        card.innerHTML = `
            <div class="card mt-3 mb-3">
                <div class="card-body">
                    <h5 class="card-title">${review.user}</h5>
                    <p class="card-text">${getStars(review.rating)} </p>
                    <p class="card-text">${review.text}</p>
                </div>
            </div>`;
        document.getElementById('commentsList').appendChild(card);
    });

    const holdButton = document.getElementById('hold-button');
    const waitButton = document.getElementById('waitlist-button');

    if (itemData.copies === 0) {
        holdButton.disabled = true;
        waitButton.disabled = false;
    } else {
        holdButton.disabled = false;
        waitButton.disabled = true;
    }
}

// Get number of stars for review
function getStars(review) {
    let rating = '';
    for (let i = 1; i <= review; i++) {
        rating += '⭐';
    }
    return rating;
}

// Get the average rating for the book
function getRating(itemData) {
    let totalRating = 0;
    itemData.reviews.forEach(review => {
        totalRating += review.rating;
    });
    const avgRating = (totalRating / itemData.reviews.length).toFixed(1);
    return avgRating;
}