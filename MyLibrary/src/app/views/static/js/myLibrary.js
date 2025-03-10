document.addEventListener("DOMContentLoaded", function () {
    loadHolds();
    loadCheckedOutBooks();
    loadWishlist();
});

// Holds Data
function loadHolds() {
    const holdsData = [
        { title: "The Great Gatsby", position: 2 },
        { title: "1984", position: 5 },
        { title: "Brave New World", position: 3 }
    ];
    const holdsTable = document.getElementById("holdsTable");
    holdsTable.innerHTML = "";
    holdsData.forEach((hold) => {
        let row = `<tr class="book-row"><td>${hold.title}</td><td class="queue-position">${hold.position}</td></tr>`;
        holdsTable.innerHTML += row;
    });
}

// Checked Out Books Data
let checkedOutData = [
    { title: "To Kill a Mockingbird", daysLeft: 10 },
    { title: "The Catcher in the Rye", daysLeft: 3 },
    { title: "Moby Dick", daysLeft: 7 }
];

function loadCheckedOutBooks() {
    const checkedOutTable = document.getElementById("checkedOutTable");
    checkedOutTable.innerHTML = "";
    checkedOutData.forEach((book) => {
        let row = `<tr class="book-row"><td>${book.title}</td><td>${book.daysLeft} days</td></tr>`;
        checkedOutTable.innerHTML += row;
    });
}

// Wishlist Data
function loadWishlist() {
    const wishlistData = ["Moby Dick", "Pride and Prejudice", "War and Peace"];
    const wishlist = document.getElementById("wishlist");
    wishlist.innerHTML = "";
    wishlistData.forEach((book) => {
        let listItem = `<li class="list-group-item wishlist-item">${book}</li>`;
        wishlist.innerHTML += listItem;
    });
}

// Add to Wishlist
function addToWishlist() {
    const newBook = prompt("Enter book title to add to wishlist:");
    if (newBook) {
        const wishlist = document.getElementById("wishlist");
        let listItem = `<li class="list-group-item wishlist-item">${newBook}</li>`;
        wishlist.innerHTML += listItem;
    }
}

// Filter Books by Name
function filterBooks() {
    let filter = document.getElementById("bookFilter").value.toLowerCase();
    let bookRows = document.querySelectorAll(".book-row");

    bookRows.forEach(row => {
        let bookTitle = row.cells[0].textContent.toLowerCase();
        row.style.display = bookTitle.includes(filter) ? "" : "none";
    });
}

// Sort Checked Out Books by Due Date
function sortByDueDate() {
    checkedOutData.sort((a, b) => a.daysLeft - b.daysLeft);
    loadCheckedOutBooks();
}
