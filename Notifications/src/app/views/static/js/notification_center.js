let books = []

// Function to fill the due today table rows
function createTodayTable(){
  let i = 1;
  const date = document.getElementById('date');
  date.textContent = 'Date: 2025/03/20';

  //for time column add the timestamp (where book.dueDate is)
  books.forEach(book =>{
      const row = document.createElement('tr');
      row.innerHTML = `
          <td><input type="checkbox" class="selectTodayRow"></td>
          <td>${book.title}</td>
          <td>${book.isbn}</td>
          <td>${book.copyid}</td>
          <td>${book.dueDate}</td>
          <td>${book.user}</td>
      `
      document.getElementById('returns-today-table').appendChild(row);
      i++;
      });
}

//maybe just show the holds due within the next three days
function createUpcomingTable(){
  let i = 1;
  books.forEach(book =>{
      const row = document.createElement('tr');
      row.innerHTML = `
          <td><input type="checkbox" class="selectUpcomingRow"></td>
          <td>${book.title}</td>
          <td>${book.isbn}</td>
          <td>${book.copyid}</td>
          <td>${book.dueDate}</td>
          <td>${book.user}</td>
      `
      document.getElementById('upcoming-returns-table').appendChild(row);
      i++;
      });
}

// Function to fill the available table rows
function createAvailableTable(){
  let i = 1;
  books.forEach(book =>{
      const row = document.createElement('tr');
      row.innerHTML = `
          <td><input type="checkbox" class="selectAvailRow"></td>
          <td>${book.title}</td>
          <td>${book.isbn}</td>
          <td>${book.copyid}</td>
          <td>${book.user}</td>
      `
      document.getElementById('upcoming-returns-table').appendChild(row);
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
createTodayTable()

// Function to get the checked row
function getCheckedRow(tableType) {
  const checkedCheckbox = document.querySelector(`.${tableType}:checked`); 
  if (checkedCheckbox) {
    const row = checkedCheckbox.closest('tr'); 
    return row; 
  }
  return null; 
}

