/*
Things that prob need to be changed:
-the keys used to access the dict elements
-the values given to each of the filter tags in html to match values in db
-adding the img link when creating the card
*/

//using this for testing
const books = [
    { title: "The Great Gatsby", author: "F. Scott Fitzgerald", genre: "Romance", description: "A story about the American Dream in the Jazz Age.", isbn:"1", format:"Ebook", copies:"1", kidFriendly: "true", rating:'4'},
    { title: "1984", author: "George Orwell", genre: "Mystery", description: "A totalitarian regime controls everything in a dystopian society.", isbn:"2", format:"Ebook", copies:"0", kidFriendly: "false", rating:'1'},
    { title: "Moby-Dick", author: "Herman Melville", genre: "Adventure", description: "A sailor's obsession with hunting the elusive white whale, Moby-Dick.", isbn:"3", format:"Audiobook", copies:"3", kidFriendly: "false", rating:'3'},
    { title: "The Catcher in the Rye", author: "J.D. Salinger", genre: "Fiction", description: "A disillusioned teenager's story of rebellion and growing up.", isbn:"4", format:"Ebook", copies:"0", kidFriendly: "true", rating:'1'},
    { title: "To Kill a Mockingbird", author: "Harper Lee", genre: "Fiction", description: "A young girl's perspective on racial injustice in the American South.", isbn:"5", format:"Ebook", copies:"5", kidFriendly: "true", rating:'2'}
  ];

//stuff to change is the image source and putting the copies available instead genre
//show all the initial search results
books.forEach(book => {
    const card = document.createElement('div');
    card.innerHTML = `
            <div class="card w-100 m-2" value=${book.isbn}>
                <div class="row g-0 p-1">
                    <!-- Image on the left -->
                    <div class="col-2 d-flex justify-content-center align-items-center">
                        <img src="/static/images/hungergames.jpg" class="book-cover img-fluid" alt="..." >
                    </div>
                    <!-- Text on the right -->
                    <div class="col-10">
                        <h5 class="card-header">${book.title}</h5>
                        <div class="card-body">
                          <h6 class="card-title">${book.author}</h6>
                          <p class="card-text">Copies Available: ${book.genre}</p>
                          <button type="submit" class="btn btn-custom-size px-5">Place Hold</button>
                        </div>
                    </div> 
                </div>
            </div>  `
    document.getElementById('bookCardContainer').appendChild(card);
    });


//function to apply all the filters
function applyFilters() {
    const filteredBooks = books;
    updatedFilter = filterGenre(filteredBooks);
    updatedFilter = filterFormat(updatedFilter);
    updatedFilter = filterAvailability(updatedFilter);
    updatedFilter = filterAudience(updatedFilter);
    updatedFilter = filterRating(updatedFilter);
    console.log("Filtered books", updatedFilter);
   
    const filteredIsbnBooks = getISBN(updatedFilter);
    showFilteredCards(filteredIsbnBooks);
}

//display the filtered cards
function showFilteredCards(books) {
    const searchContainer = document.getElementById('bookCardContainer'); 
    const allBooks = searchContainer.querySelectorAll('.card');
    
    allBooks.forEach(card => {
        const bookIsbn = card.getAttribute('value');
        if (books.includes(bookIsbn)) {
            card.style.display = 'block'; 
        } else {
            card.style.display = 'none';
        }
    });
}

//function to get the value for multi valued filters
function getCheckedBoxes(form_id) {
    const checkboxes = document.querySelectorAll(form_id);
    const checkedValues = [];
    
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            checkedValues.push(checkbox.value); 
        }
    });

    console.log('Checked values:', checkedValues);
    return checkedValues;
}

//function to filtre by genre
function filterGenre(filteredBooks) {
    const checkedGenres = getCheckedBoxes('#collapseThree .form-check-input');
    const updatedFilter = filteredBooks.filter(book => {
        if (checkedGenres.length === 0) return true;
        return checkedGenres.includes(book.genre);
    });
    console.log('Filtered by Genre: ', updatedFilter);
    return updatedFilter;
}

//function to filter between ebook and audiobook
function filterFormat(filteredBooks){
    const checkedFormat = getCheckedBoxes('#collapseTwo .form-check-input');
    const updatedFilter = filteredBooks.filter(book => {
        if (checkedFormat.length === 0) return true;
        return checkedFormat.includes(book.format);
    });
    console.log('Filtered by Genre: ', updatedFilter);
    return updatedFilter;
}

//filter based on availability
function filterAvailability(filteredBooks){
    const checkedAvail = getCheckedBoxes('#collapseOne .form-check-input');
    const updatedFilter = filteredBooks.filter(book => {
        if (checkedAvail.length === 0) return true;
        return book.copies>0;
    });
    console.log('Filtered by Availability: ', updatedFilter);
    return updatedFilter;
}

//filter based on audience 
function filterAudience(filteredBooks){
    const checkedAudience = getCheckedBoxes('#collapseFour .form-check-input');
    const updatedFilter = filteredBooks.filter(book => {
        if (checkedAudience.length === 0) return true;
        return checkedAudience.includes(book.kidFriendly);
    });
    console.log('Filtered by Audience: ', updatedFilter);
    return updatedFilter;
}

//filter based on rating
function filterRating(filteredBooks){
    const checkedRating = getCheckedBoxes('#collapseFive .form-check-input');
    const updatedFilter = filteredBooks.filter(book => {
        if (checkedRating.length === 0) return true;
        return checkedRating.includes(book.rating);
    });
    console.log('Filtered by Rating: ', updatedFilter);
    return updatedFilter;
}

//function to get isbn of all filtered books
function getISBN(filterBooks){
    const filteredIsbn = [];
    filterBooks.forEach(book =>{
        filteredIsbn.push(book.isbn);
    });
    return filteredIsbn;
}
 