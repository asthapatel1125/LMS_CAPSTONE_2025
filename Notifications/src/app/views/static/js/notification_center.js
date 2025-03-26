let availablebooks = []
let dueTodayBooks = [];
let dueSoonBooks = [];

async function fetchTodayReturns() {
  try {
    const response = await fetch('/notif/returns-today');
    if (!response.ok) {
      alert("Error fetching reservations due today.");
    }
    const data = await response.json();
    console.log(data);
    dueTodayBooks = data;

    if (data.length > 0) {
      data.forEach(book => {
        console.log(`Book Name: ${book.title}, ISBN: ${book.isbn}`);
      });
      createTodayTable();
    } else {
      console.log("No books due today.");
    }
  } catch (error) {
    console.error('Error fetching books due today:', error);
  }
}

// Function to fill the due today table rows
function createTodayTable(){
  let i = 1;
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');

  const formattedDate = `${year} / ${month} / ${day}`;

  const dateElement = document.getElementById('date');
  dateElement.textContent = `Date: ${formattedDate}`;

  //for time column add the timestamp (where book.dueDate is)
  dueTodayBooks.forEach(book =>{
      const row = document.createElement('tr');
      row.innerHTML = `
          <td><input type="checkbox" class="selectTodayRow"></td>
          <td>${book.title}</td>
          <td>${book.isbn}</td>
          <td>${book.bookID}</td>
          <td>${book.email}</td>
      `
      document.getElementById('returns-today-table').appendChild(row);
      i++;
      });
}

async function fetchDueSoonReturns() {
  try {
    const response = await fetch('/notif/return-soon');
    if (!response.ok) {
      alert("Error fetching reservations due soon.");
      return;
    }
    
    const data = await response.json();
    console.log(data);
    dueSoonBooks = data;

    if (data.length > 0) {
      data.forEach(book => {
        console.log(`Book Name: ${book.title}, ISBN: ${book.isbn}, Due Date: ${book.expiration_date}`);
      });
      createUpcomingTable();
    } else {
      console.log("No books due soon.");
    }
  } catch (error) {
    console.error('Error fetching books due soon:', error);
  }
}

//maybe just show the holds due within the next three days
function createUpcomingTable(){
  let i = 1;
  dueSoonBooks.forEach(book =>{
      const row = document.createElement('tr');
      row.innerHTML = `
          <td><input type="checkbox" class="selectUpcomingRow"></td>
          <td>${book.title}</td>
          <td>${book.isbn}</td>
          <td>${book.bookID}</td>
          <td>${book.dueDate}</td>
          <td>${book.email}</td>
      `
      document.getElementById('upcoming-returns-table').appendChild(row);
      i++;
      });
}

async function fetchAvailableBooks() {
  try {
    const response = await fetch('/notif/available-now');
    if (!response.ok) {
      alert("Error fetching available books");
    }
    const data = await response.json();
    console.log(data);
    availablebooks = data;

    if (data.length > 0) {
      data.forEach(book => {
        console.log(`Book Name: ${book.title}, ISBN: ${book.isbn}`);
      });
      createAvailableTable();
    } else {
      console.log("No available books.");
    }
  } catch (error) {
    console.error('Error fetching available books:', error);
  }
}

// Function to fill the available table rows
function createAvailableTable(){
  let i = 1;
  availablebooks.forEach(book =>{
      const row = document.createElement('tr');
      row.innerHTML = `
          <td><input type="checkbox" class="selectAvailRow"></td>
          <td>${book.title}</td>
          <td>${book.isbn}</td>
          <td>${book.rating}</td>
          <td>${book.email}</td>
      `
      document.getElementById('available-today-table').appendChild(row);
      i++;
      });
}

// Function to alert when notifcation sent
function notify(tableType){
  if (getCheckedRow(tableType)){
    alert('Notification sent!')
  }
  else {
    alert('Select a row!')
  }
 
}

// Function to get the checked row
function getCheckedRow(tableType) {
  const checkedCheckbox = document.querySelector(`.${tableType}:checked`); 
  if (checkedCheckbox) {
    const row = checkedCheckbox.closest('tr'); 
    return row; 
  }
  return null; 
}

document.addEventListener('DOMContentLoaded', function() {
  fetchTodayReturns();
  fetchDueSoonReturns();
  fetchAvailableBooks();
});
