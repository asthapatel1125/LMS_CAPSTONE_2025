let selectedBook = null;
let books = [];

async function fetchBooks() {
    try {
        const response = await fetch('/catalog/books/');
        if (response.ok) {
            const bookData = await response.json();
            books = bookData;
            displayBooks(books);
        } else {
            console.error('Error fetching books:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function searchBooks() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    if (query === "") {
        clearSearchResults();
        selectedBook = null;
        document.getElementById('bookDetails').style.display = 'none';
        document.getElementById('modifyBookForm').style.display = 'none';
        modifyButtonDisable();
    } else {
        const filteredBooks = books.filter(book =>
            book.title.toLowerCase().includes(query) ||
            book.author.toLowerCase().includes(query) ||
            book.isbn.toLowerCase().includes(query)
        );
        displayBooks(filteredBooks);
    }
}

function displayBooks(booksToDisplay) {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = '';
    booksToDisplay.forEach(book => {
        const listItem = document.createElement('li');
        listItem.classList.add('list-group-item');
        const bookButton = document.createElement('button');
        bookButton.classList.add('btn', 'btn-custom-search', 'w-100', 'p-1');
        bookButton.innerHTML = `<h5>${book.title}</h5> <p>By: ${book.author}</p>`;
        bookButton.addEventListener('click', () => {
            selectedBook = book;
            displayBookDetails(book);
            const modifyBookForm = document.getElementById('bookDetailsForm');
            if (modifyBookForm) {
                modifyBookForm.style.display = 'none';
            } else {
                console.error('bookDetailsForm not found');
            }
            clearSearchResults();
            modifyButtonEnable();
        });
        listItem.appendChild(bookButton);
        bookList.appendChild(listItem);
    });
}

function displayBookDetails(book) {
    const bookDetailsDiv = document.getElementById('bookDetails');
    bookDetailsDiv.innerHTML = `
        <h5>${book.title}</h5>
        <p><strong>Author:</strong> ${book.author}</p>
        <p><strong>ISBN:</strong> ${book.isbn}</p>
        <p><strong>Genre:</strong> ${book.genre}</p>
        <p><strong>Rating:</strong> ${book.rating} ⭐</p>
        <p><strong>Description:</strong> ${book.description}</p>
        <p><strong>Kid Friendly:</strong> ${book.kidFriendly ? "Yes" : "No"}</p>
        <p><strong>Format:</strong> ${book.format}</p>
        <p><strong>Page Number:</strong> ${book.pageNumber}</p>
        <p><strong>Publisher:</strong> ${book.publisher}</p>
        <p><strong>Status:</strong> ${book.status}</p>
        <button class="btn btn-custom-size mt-2" onclick="openModifyForm()">Modify</button>
    `;
    document.getElementById('bookDetails').style.display = 'block';
}

function openModifyForm() {
    const modifyBookForm = document.getElementById('bookDetailsForm');
    const bookDeets = document.getElementById('bookDetails');

    if (modifyBookForm) {
        modifyBookForm.style.display = 'block';
        populateModifyForm(selectedBook);
    } else {
        console.error('bookDetailsForm not found');
    }

    if (bookDeets){
        bookDeets.style.display = "none";
    }
}

function populateModifyForm(book) {
    document.getElementById('title').value = book.title;
    document.getElementById('author').value = book.author;
    document.getElementById('isbn').value = book.isbn;
    document.getElementById('genre').value = book.genre;
    document.getElementById('rating').value = book.rating;
    document.getElementById('description').value = book.description;
    document.getElementById('kidFriendly').checked = book.kidFriendly;
    document.getElementById('format').value = book.format;
    document.getElementById('pageNumber').value = book.pageNumber;
    document.getElementById('publisher').value = book.publisher;
    document.getElementById('status').value = book.status;
}

function modifyButtonEnable() {
    const modifyButton = document.getElementById('modifyButton');
    modifyButton.disabled = false;
}

function modifyButtonDisable() {
    const modifyButton = document.getElementById('modifyButton');
    modifyButton.disabled = true;
}

function clearSearchResults() {
    const modifyBookForm = document.getElementById("modifyBookForm");
    if (modifyBookForm) {
        modifyBookForm.reset();
    } else {
        console.error('modifyBookForm not found');
    }
}

window.onload = function() {
    modifyButtonDisable();
    fetchBooks();
}

function validateForm() {
    let isValid = true;
    const errorMessage = "This field is required";

    const formFields = document.querySelectorAll('#modifyBookForm input[required], #modifyBookForm textarea[required], #modifyBookForm select[required]');

    formFields.forEach(field => {
        const errorElement = document.getElementById(field.id + "-error");

        if (field.tagName.toLowerCase() === "select") {
            if (!field.value || field.value === "" || field.value === "Choose...") {
                isValid = false;
                if (!errorElement) {
                    const error = document.createElement('div');
                    error.id = field.id + "-error";
                    error.classList.add('text-danger', 'mt-2');
                    error.textContent = errorMessage;
                    field.parentElement.appendChild(error);
                }
            } else {
                if (errorElement) {
                    errorElement.remove();
                }
            }
        } else {
            if (!field.value.trim()) {
                isValid = false;
                if (!errorElement) {
                    const error = document.createElement('div');
                    error.id = field.id + "-error";
                    error.classList.add('text-danger', 'mt-2');
                    error.textContent = errorMessage;
                    field.parentElement.appendChild(error);
                }
            } else {
                if (errorElement) {
                    errorElement.remove();
                }
            }
        }
    });

    return isValid;
}

function modifyBook(event) {
    event.preventDefault();
    const formIsValid = validateForm();
    if (formIsValid) {
        const formData = new FormData(document.getElementById("modifyBookForm"));
        const data = Object.fromEntries(formData.entries());
        data.kidFriendly = document.getElementById("kidFriendly").checked;
        
        fetch('/catalog/modify-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.status === 409) {
                fetchBooks();
                return response.json().then(result => {
                    alert(result.detail);
                });
            } else if (response.ok) {
                alert("Book modified successfully!");
                document.getElementById("modifyBookForm").reset();
                window.location.href = "/catalog/modify-item";
            } else {
                fetchBooks();
                alert("An unexpected error occurred.");
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function cancel(){
    fetchBooks();
    document.getElementById("modifyBookForm").reset();
  }

function back(){
    window.location.href = "/catalog/edit_inventory";
}

document.querySelector("#modifyButton").addEventListener("click", modifyBook);