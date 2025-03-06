/* Things that prob need to be changed
- when you click on a button on the dynamic search it redirects straight to the book page information
- if you click on the search button beside the search bar it redirects to the search results page
 */
// Sample book data
const books = [
    { title: "The Great Gatsby", author: "F. Scott Fitzgerald", genre: "Fiction", description: "A story about the American Dream in the Jazz Age." },
    { title: "1984", author: "George Orwell", genre: "Dystopian", description: "A totalitarian regime controls everything in a dystopian society." },
    { title: "Moby-Dick", author: "Herman Melville", genre: "Adventure", description: "A sailor's obsession with hunting the elusive white whale, Moby-Dick." },
    { title: "The Catcher in the Rye", author: "J.D. Salinger", genre: "Fiction", description: "A disillusioned teenager's story of rebellion and growing up." },
    { title: "To Kill a Mockingbird", author: "Harper Lee", genre: "Fiction", description: "A young girl's perspective on racial injustice in the American South." }
  ];
  
  let selectedBook = null;
  
  // Function to search the books dynamically
  function searchBooks() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    if (query === "") {
        // If query is empty, hide the search list
        clearSearchResults();
        selectedBook = null;
        document.getElementById('bookDetails').innerHTML = '';
        deleteButtonDisable();
    } else {
        const filteredBooks = books.filter(book => 
            book.title.toLowerCase().includes(query) ||
            book.author.toLowerCase().includes(query) ||
            book.genre.toLowerCase().includes(query)
        );
        displayBooks(filteredBooks);
    }
  }
  
  // Function to display the list of books as buttons
  function displayBooks(booksToDisplay) {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; // Clear the existing list
    if (booksToDisplay.length === 0) {
        bookList.innerHTML = '<li class="list-group-item">No books found.</li>';
    } else {
        booksToDisplay.forEach(book => {
          const listItem = document.createElement('li');
          listItem.classList.add('list-group-item');
          
          // Create a button for each book
          const bookButton = document.createElement('button');
          bookButton.classList.add('btn', 'btn-custom-search', 'w-100');
          bookButton.innerHTML = `<p align="left">${book.title} - ${book.author} (${book.genre})</p>`;
          
          bookButton.addEventListener('click', () => {
              displayBookDetails(book);  
              clearSearchResults(); 
              deleteButtonEnable();
          });
          
          // Append the button to the list item
          listItem.appendChild(bookButton);
          bookList.appendChild(listItem);
        });
    }
  }
  
  function clearSearchResults() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; 
  }