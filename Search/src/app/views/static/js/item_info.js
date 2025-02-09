document.addEventListener("DOMContentLoaded", function () {
    // Simulated backend data
    const itemData = {
        coverImage: "https://via.placeholder.com/150",
        title: "The Great Gatsby",
        author: "F. Scott Fitzgerald",
        year: "1925",
        isbn: "ASDBU1273712UGFSD",
        format: "EPUB",
        synopsis: "The Great Gatsby, F. Scott Fitzgerald’s third book, stands as the supreme achievement of his career. First published by Scribner in 1925, this quintessential novel of the Jazz Age has been acclaimed by generations of readers. The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan is an exquisitely crafted tale of America in the 1920s.",
        reviews: [
            { user: "Alice", rating: 5, text: "Loved it! A timeless classic." },
            { user: "Bob", rating: 4, text: "Great book with deep themes." },
            { user: "Charlie", rating: 3, text: "Interesting but not my style." }
        ]
    };

    // Populate item display
    document.getElementById("item-cover").src = itemData.coverImage;
    document.getElementById("item-info").innerHTML = `
        <h2>${itemData.title}</h2>
        <p><strong>Author:</strong> ${itemData.author}</p>
        <p><strong>Published:</strong> ${itemData.year}</p>
        <p><strong>ISBN: </strong>${itemData.isbn}</p>
        <p><strong>Format: </strong>${itemData.format}</p>
    `;

    // Populate synopsis
    document.getElementById("item-synopsis").textContent = itemData.synopsis;

    // Populate reviews and calculate average rating
    let totalRating = 0;
    const reviewsList = document.getElementById("reviews-list");
    itemData.reviews.forEach(review => {
        totalRating += review.rating;
        const reviewElement = document.createElement("div");
        reviewElement.classList.add("review");
        reviewElement.innerHTML = `<strong>${review.user}:</strong> ⭐ ${review.rating} - ${review.text}`;
        reviewsList.appendChild(reviewElement);
    });

    const avgRating = (totalRating / itemData.reviews.length).toFixed(1);
    document.getElementById("average-rating").innerHTML = `⭐ ${avgRating}`;
});
