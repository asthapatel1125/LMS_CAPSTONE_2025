document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const isbn = urlParams.get("isbn") || ""; // Default to empty string if no isbn is provided

    // Fetch book data based on the query (initial load)
    fetchBooks(isbn);


    // Set up wishlist button
    let wishButton = document.getElementById('wishlist-button');
    wishButton.addEventListener('click', function() {
        addToWishlist(isbn);
    });
});

async function fetchBooks(isbn) {
    try {
        const response = await fetch(`/search/book_info/${isbn}`);
        if (!response.ok) {
            throw new Error('Failed to fetch book data');
        }
        const itemData = await response.json();

        try {
            const coverResponse = await fetch(`/search/serve-book-cover/${isbn}`);
            if (coverResponse.ok) {
                let blob = await coverResponse.blob();
                let coverBlob = new Blob([blob], { type: "image/jpg" });
                let blobUrl = URL.createObjectURL(coverBlob);
                itemData.coverImage = blobUrl;
            } else {
                itemData.coverImage = "/search/static/images/error.png";
            }
        } catch (coverError) {
            console.error(`Error fetching cover for ISBN: ${isbn}`, coverError);
            itemData.coverImage = "/search/static/images/error.png";
        }
        
        displayBookInfo(itemData);
        
        // Fetch reviews
        fetchReviews(isbn);
    } catch (error) {
        console.error('Error fetching book info:', error);
    }
}

function displayBookInfo(itemData) {
    const title = document.getElementById("book-title");
    title.textContent = '📖 ' + itemData.title;
    document.getElementById("book-cover").innerHTML = `<img src="${itemData.coverImage}" class="book-cover img-fluid" alt="Book Cover">`;

    document.getElementById("main-book-info").innerHTML = `
        <h6 class="card-title">${itemData.author}</h6>
        <p class="card-text">Rating: ${itemData.rating}</p>
        <p class="card-text">${itemData.description}</p>
        <p class="card-text">Copies Available: ${itemData.numCopies}</p>`;

    let bookDetails = `
        <p class="card-text">ISBN: ${itemData.isbn}</p>
        <p class="card-text">Format: ${itemData.format}</p>
        <p class="card-text">Genre: ${itemData.genre}</p>`;

    if (itemData.format === "eBook") {
        bookDetails += `<p class="card-text">Page Numbers: ${itemData.pageNumber}</p>`;
    }
    if (itemData.format === "Audio") {
        bookDetails += `<p class="card-text">Number of Minutes: ${itemData.numOfMins}</p>`;
    }
    bookDetails += `
        <p class="card-text">Publisher: ${itemData.publisher}</p>
        <p class="card-text">Status: ${itemData.status}</p>`;

    document.getElementById("book-info").innerHTML = bookDetails;

    const holdButton = document.getElementById('hold-button');
    let wishButton = document.getElementById('wishlist-button');
    holdButton.disabled = false;
    wishButton.disabled = false;

    if (itemData.numCopies <= 0) {
        holdButton.disabled = true;
    } else if(itemData.status === "Not Available"){
        holdButton.disabled = true;
    }
}

async function fetchReviews(isbn) {
    try {
        // Pass the ISBN as a query parameter in the URL
        const response = await fetch(`/search/retrieve-reviews?isbn=${isbn}`, {
            method: "GET",
            headers: {"Content-Type": "application/json"}
        });

        if (!response.ok) {
            throw new Error('Failed to fetch reviews');
        }

        const reviewData = await response.json();
        displayReviews(reviewData.reviews);
    } catch (error) {
        console.error('Error fetching reviews:', error);
    }
}


function displayReviews(reviews) {
    const commentsList = document.getElementById('commentsList');
    commentsList.innerHTML = ''; // Clear any existing reviews
    reviews.forEach(review => {
        const card = document.createElement('div');
        card.innerHTML = `
            <div class="card mt-3 mb-3">
                <div class="card-body">
                    <h5 class="card-title">${review.user}</h5>
                    <p class="card-text">${getStars(review.rating)} </p>
                    <p class="card-text">${review.review_text}</p>
                    <p class="card-text">${review.created_at} </p>
                </div>
            </div>`;
        commentsList.appendChild(card);
    });
}

// Get number of stars for review
function getStars(rating) {
    let stars = '';
    for (let i = 1; i <= rating; i++) {
        stars += '⭐';
    }
    return stars;
}

function addToWishlist(isbn) {
    fetch(`/search/add-to-wishlist`, {
        method: "POST",
        credentials: "include",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ isbn: isbn })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error("Error adding to wishlist:", error);
    });
}
