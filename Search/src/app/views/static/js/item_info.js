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
    ],
    copies: 5
};

const title = document.getElementById("book-title");
title.textContent = '📖' + itemData.title;

document.getElementById("book-cover").innerHTML = `<img src="/static/images/hungergames.jpg" class="book-cover img-fluid" alt="..." >`

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
        </div>  `
    document.getElementById('commentsList').appendChild(card);
    });

const holdButton = document.getElementById('hold-button');
const waitButton = document.getElementById('waitlist-button');

if (itemData.copies === 0){
    holdButton.disabled = true;
    waitButton.disabled = false;
}
else {
    holdButton.disabled = false;
    waitButton.disabled = true;
}

//get number of stars
function getStars(review){
    rating = '';
    for (let i = 1; i <= review; i++) {
        rating+='⭐';
    }
    console.log(rating);
    return rating;
}

function getRating(itemData){
    let totalRating = 0;
    itemData.reviews.forEach(review => {
        totalRating += review.rating;
    });
    const avgRating = (totalRating / itemData.reviews.length).toFixed(1);
    return avgRating;
}

