/* Notes:
-status column would be like if they are active (in queue or have things checked out) or inactive(nothing checked out) the more in detail info about
their book history is in the manage holds page
-the user info from the row should be sent to the action forms when selected (ex. edit or delete forms)
-direct add user button to add_user.html
-can split up the name into first name and last name columns
 */

let users = [];

async function fetchUsers() {
  try {
    const response = await fetch("/userManage/all-users");
    if (!response.ok) {
      alert("Error getting all users!");
      return;
    }
    users = await response.json();
    users.forEach((user) => {
      // Convert the 'created_on' field into a readable date
      const createdOnDate = new Date(user.created_on);
      const formattedDate = createdOnDate.toLocaleString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
      user.created_on = formattedDate;
    });
    createTable();
  } catch (error) {
    console.error("Error fetching users:", error);
  }
}
  
//create the user table
function createTable() {
  const userTable = document.getElementById('user-table');
  userTable.innerHTML = '';

  users.forEach(user => {
      const row = document.createElement('tr');
      row.id = `${user.email}`;
      row.innerHTML = `
          <td>${user.name}</td>
          <td>${user.email}</td>
          <td>${user.status}</td>
          <td>${user.created_on}</td>
          <td>
              <a href='/userManage/edit-user/${user.email}'>✏️</a>
              <a href="/userManage/delete-user/${user.email}">✖️</a>
          </td>
      `;
      userTable.appendChild(row);
  });
}

// Function to search the books dynamically
function searchUsers() {
  const query = document.getElementById('searchInput').value.toLowerCase();
  if (query === "") {
    // If the query is empty, reset the table
    resetTable();
  } else {
    // Filter users based on name or email
    const filteredUsers = users.filter(user =>
      user.name.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query)
    );
    displayUsers(filteredUsers);
  }
}
  
  // Function to display the list of books as buttons
  function displayUsers(usersToDisplay) {
    const userList = document.getElementById('user-list');
    userList.innerHTML = ''; // Clear the existing search results
  
    if (usersToDisplay.length === 0) {
      userList.innerHTML = '<li class="list-group-item">No user found.</li>';
    } else {
      usersToDisplay.forEach(user => {
        const listItem = document.createElement('li');
        listItem.classList.add('list-group-item');
  
        // Create a button for each user
        const userButton = document.createElement('button');
        userButton.classList.add('btn', 'btn-custom-search', 'w-100', 'p-1');
        userButton.innerHTML = `<p>${user.name} (${user.email})</p>`;
  
        // When the user is clicked, filter the table
        userButton.addEventListener('click', () => {
          filterTable(user);  
        });
  
        listItem.appendChild(userButton);
        userList.appendChild(listItem);
      });
    }
  } 
  
const table = document.getElementById('user-table');
const tableRows = table.querySelectorAll('tr');

function filterTable(user) {
  const query = user.email.toLowerCase(); 
  const tableRows = document.querySelectorAll('#user-table tr'); // Get all rows in the table

  tableRows.forEach(row => {
    const emailCell = row.querySelector('td:nth-child(2)');  // Assuming the email is in the second column
    if (emailCell && emailCell.textContent.toLowerCase().includes(query)) {
      row.style.display = 'table-row'; // Show the matching row
    } else {
      row.style.display = 'none'; // Hide non-matching rows
    }
  });
}

function clearSearchResults() {
    const userList = document.getElementById('user-list');
    userList.innerHTML = ''; 
}

function resetTable(){
    const table = document.getElementById('user-table');
    const tableRows = table.querySelectorAll('tr');
    tableRows.forEach(row => {row.style.display = '' });
}

function addUser(){
  window.location.href = "/userManage/add-user";
}

window.onload = function () {
  fetchUsers();
};