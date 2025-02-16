/* Things that need to be changed
-read from db
-can change alert messages to something else when hold status is changed
-refresh table after each time one of the buttons are selected
-assign each book a copy number
 */
const books = [
    { title: "The Great Gatsby", user: "F. Scott Fitzgerald", holdDate: "2025-02-15", dueDate: "2024-15-2022", isbn:"1", format:"Ebook", status:"Fulfilled"},
    { title: "Moby-Dick", user: "Herman Melville", holdDate: "2025-02-10", dueDate: "na", isbn:"3", format:"Audiobook", status:"Waiting"},
    { title: "The Catcher in the Rye", user: "J.D. Salinger", holdDate: "2025-02-14", dueDate: "2024-15-2022", isbn:"4", format:"Ebook", status:"Fulfilled"},
    { title: "The Catcher in the Rye", user: "J.. Salinger", holdDate: "2025-02-14", dueDate: "2024-15-2022", isbn:"4", format:"Ebook", status:"Fulfilled"},
    { title: "To Kill a Mockingbird", user: "Harper Lee", holdDate: "2025-01-21", dueDate: "na", isbn:"5", format:"Ebook", status:"Waiting"}
  ];

function createTable(){
    let i = 1;
    books.forEach(book =>{
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><input type="checkbox" class="selectRow"></td>
            <th scope="row">${i}</th>
            <td>${book.title}</td>
            <td>${book.isbn}</td>
            <td>${book.copyid}</td>
            <td>${book.user}</td>
            <td>${book.holdDate}</td>
            <td>${book.dueDate}</td>
            <td>${book.status}</td>
        `
        document.getElementById('book-table').appendChild(row);
        i++;
        });
}

createTable();

$(document).ready(function() {
    // Select or deselect a single row checkbox
    $(".selectRow").click(function() {
      var row = $(this).closest("tr");
  
      // Uncheck all other checkboxes and remove 'selected' class from other rows
      $(".selectRow").not(this).prop("checked", false).closest("tr").removeClass("selected");
  
      // If the clicked row checkbox is checked, highlight the row
      if ($(this).prop("checked")) {
        row.addClass("selected");
      } else {
        row.removeClass("selected");
      }
    });
});

// Get all the filter checkboxes
const filterCheckboxes = document.querySelectorAll('.form-check-input');
const searchInput = document.getElementById('searchInput');
let filterOpt = '';

// Function to ensure only one filter is selected at a time
function restrictSingleFilterSelection() {
  filterCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', function() {
      if (this.checked) {
        // Update the filterOpt when a checkbox is selected
        filterOpt = this.value;
        console.log('Selected filter:', filterOpt);

        // Uncheck other checkboxes
        filterCheckboxes.forEach((otherCheckbox) => {
          if (otherCheckbox !== this) {
            otherCheckbox.checked = false; 
          }
        });
      } else {
        if (!isAnyFilterSelected()) {
          filterOpt = ''; 
          console.log('No filter selected');
        }
      }
      toggleSearchInput(); 
    });
  });
}

// Function to check if any filter is selected
function isAnyFilterSelected() {
  let isSelected = false;
  filterCheckboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      isSelected = true;
    }
  });
  return isSelected;
}

// Function to enable or disable the search input based on filter selection
function toggleSearchInput() {
  if (isAnyFilterSelected()) {
    searchInput.disabled = false;
  } else {
    searchInput.disabled = true;
  }
}

// Initialize the filter restriction and enable/disable search input
restrictSingleFilterSelection();
toggleSearchInput();


filterCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener('change', toggleSearchInput); 
});

toggleSearchInput(); 
restrictSingleFilterSelection();

// Function to search the books dynamically
function searchBooks() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    if (query === "") {
        // If query is empty, hide the search list
        clearSearchResults();
        selectedBook = null;
        
    } else {
        if (filterOpt === 'isbn'){
            const filteredBooks = [];
            books.forEach(book => {
                if (!filteredBooks.includes(book.isbn) && book.isbn.toLowerCase().includes(query)){
                    filteredBooks.push(book.isbn)
                }
            }); 
            console.log(filteredBooks);
            displayIsbn(filteredBooks);         
        }
        else if (filterOpt === 'title'){
            const filteredBooks = [];
            books.forEach(book => {
                if (!filteredBooks.includes(book.title) && book.title.toLowerCase().includes(query)){
                    filteredBooks.push(book.title)
                }
            }); 
            console.log(filteredBooks);
            displayTitle(filteredBooks);        
        }
        else if (filterOpt === 'user'){
            const filteredBooks = [];
            books.forEach(book => {
                if (!filteredBooks.includes(book.user) && book.user.toLowerCase().includes(query)){
                    filteredBooks.push(book.user)
                }
            }); 
            console.log(filteredBooks);
            displayUser(filteredBooks);           
        } 
        else if (filterOpt === 'holdDate'){
            const filteredBooks = [];
            books.forEach(book => {
                if (!filteredBooks.includes(book.holdDate) && book.holdDate.toLowerCase().includes(query)){
                    filteredBooks.push(book.holdDate)
                }
            }); 
            console.log(filteredBooks); 
            filterTableByDate(filteredBooks, 'holdDate') 
        }
        else if (filterOpt === 'dueDate'){
            const filteredBooks = [];
            books.forEach(book => {
                if (!filteredBooks.includes(book.dueDate) && book.dueDate.toLowerCase().includes(query)){
                    filteredBooks.push(book.dueDate)
                }
            }); 
            console.log(filteredBooks); 
            filterTableByDate(filteredBooks, 'dueDate') 
        }
    }
  }
  
  // Function to display the list of books based on isbn
  function displayTitle(titlesToDisplay) {
    const searchList = document.getElementById('bookList');
    searchList.innerHTML = ''; // Clear the existing list
    if (titlesToDisplay.length === 0) {
        searchList.innerHTML = '<li class="list-group-item">No entries found.</li>';
    } else {
        titlesToDisplay.forEach(title => {
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            
            // Create a button for each book
            const itemButton = document.createElement('button');
            itemButton.classList.add('btn', 'btn-custom-search', 'w-100');
            itemButton.innerHTML = `<p align="left">${title}</p>`;
            
            itemButton.addEventListener('click', () => {
                filterTable(title, 'title');  
                clearSearchResults(); 
            });
            listItem.appendChild(itemButton);
            searchList.appendChild(listItem);
        });
    }
  }
  
  // Function to display the list of books based on title
  function displayIsbn(isbnToDisplay) {
    const searchList = document.getElementById('bookList');
    searchList.innerHTML = ''; // Clear the existing list
    if (isbnToDisplay.length === 0) {
        searchList.innerHTML = '<li class="list-group-item">No entries found.</li>';
    } else {
        isbnToDisplay.forEach(isbn => {
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            
            // Create a button for each book
            const itemButton = document.createElement('button');
            itemButton.classList.add('btn', 'btn-custom-search', 'w-100');
            itemButton.innerHTML = `<p align="left">${isbn}</p>`;
            
            itemButton.addEventListener('click', () => {
                filterTable(isbn, 'isbn');  
                clearSearchResults(); 
            });
            listItem.appendChild(itemButton);
            searchList.appendChild(listItem);
        });
    }
  }

// Function to display the list of books based on user
function displayUser(usersToDisplay) {
    const searchList = document.getElementById('bookList');
    searchList.innerHTML = ''; // Clear the existing list
    if (usersToDisplay.length === 0) {
        searchList.innerHTML = '<li class="list-group-item">No entries found.</li>';
    } else {
        usersToDisplay.forEach(user => {
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            
            // Create a button for each book
            const itemButton = document.createElement('button');
            itemButton.classList.add('btn', 'btn-custom-search', 'w-100');
            itemButton.innerHTML = `<p align="left">${user}</p>`;
            
            itemButton.addEventListener('click', () => {
                filterTable(user, 'user');  
                clearSearchResults(); 
            });
            listItem.appendChild(itemButton);
            searchList.appendChild(listItem);
        });
    }
} 

function filterTableByDate(dateToDisplay, dateType) {
    const searchList = document.getElementById('bookList');
    searchList.innerHTML = ''; // Clear the existing list
    if (dateToDisplay.length === 0) {
        searchList.innerHTML = '<li class="list-group-item">No entries found.</li>';
    } else {
        dateToDisplay.forEach(date => {
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            
            // Create a button for each book
            const itemButton = document.createElement('button');
            itemButton.classList.add('btn', 'btn-custom-search', 'w-100');
            itemButton.innerHTML = `<p align="left">${date}</p>`;
            
            itemButton.addEventListener('click', () => {
                filterTable(date, dateType);  
                clearSearchResults(); 
            });
            listItem.appendChild(itemButton);
            searchList.appendChild(listItem);
        });
    }
}

function resetTable(){
    const table = document.getElementById('book-table');
    const tableRows = table.querySelectorAll('tr');
    tableRows.forEach(row => {row.style.display = '' });
}


function clearSearchResults() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; 
}

const table = document.getElementById('book-table');
const tableRows = table.querySelectorAll('tr');

function filterTable(book, filter){
    const query = book.toLowerCase();
    tableRows.forEach(row => {
        const cells = row.querySelectorAll('td');
        console.log(cells);
        if (filter === 'user'){
            shouldDisplay = cells[4].textContent.toLowerCase().includes(query);
            console.log(cells[4].textContent.toLowerCase());
            row.style.display = shouldDisplay ? '' : 'none';
        }
        else if (filter === 'isbn'){
            shouldDisplay = cells[2].textContent.toLowerCase().includes(query);
            console.log(cells[2].textContent.toLowerCase());
            row.style.display = shouldDisplay ? '' : 'none';
        }
        else if (filter === 'title'){
            console.log(query);
            shouldDisplay = cells[1].textContent.toLowerCase().includes(query);
            console.log(cells[1].textContent.toLowerCase());
            row.style.display = shouldDisplay ? '' : 'none';
        }
        else if (filter === 'holdDate'){
            console.log(query);
            shouldDisplay = cells[5].textContent.toLowerCase().includes(query);
            console.log(cells[5].textContent.toLowerCase());
            row.style.display = shouldDisplay ? '' : 'none';            
        }
        else if (filter === 'dueDate'){
            console.log(query);
            shouldDisplay = cells[6].textContent.toLowerCase().includes(query);
            console.log(cells[6].textContent.toLowerCase());
            row.style.display = shouldDisplay ? '' : 'none';            
        }
    });
    console.log(book);
}

// Function to get the checked row
function getCheckedRow() {
    const checkedCheckbox = document.querySelector('.selectRow:checked'); 
    if (checkedCheckbox) {
      const row = checkedCheckbox.closest('tr'); 
      return row; 
    }
    return null; 
  }
  
//Function for backend stuff
function fulfillHold(action) {
    const checkedRow = getCheckedRow(); // Get the checked row
  
    if (!checkedRow) {
      alert("Please select a row.");
      return;
    }
    alert("Fulfilling hold");
    console.log("Fulfilling row:", checkedRow);
    createTable(); //refreshed table
}

function cancelHold(action) {
    const checkedRow = getCheckedRow(); // Get the checked row
  
    if (!checkedRow) {
      alert("Please select a row.");
      return;
    }
    alert("Cancelling hold");
    console.log("Cancelling row:", checkedRow);
    createTable(); //refreshed table
}

function extendHold(action) {
    const checkedRow = getCheckedRow(); // Get the checked row
    if (!checkedRow) {
      alert("Please select a row.");
      return;
    }
    alert("Extending hold");
    console.log("Extending row:", checkedRow);
    createTable(); //refreshed table
}