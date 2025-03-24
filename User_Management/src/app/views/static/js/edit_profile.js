/* Notes:
-maybe only submit form if any of the fields change
-need to prevent form from submitting if error 
-same logic as admin edit profile (just copied it)
 */

const users = [
    {
      firstName: "John",
      lastName:  "Doe",
      status: "Active",
      createdOn: "2022-03-15",
      email: "john.doe@example.com"
    },
    {
      firstName: "Jane",
      lastName : "Smith",
      status: "Inactive",
      createdOn: "2021-07-22",
      email: "jane.smith@example.com"
    },
    {
      firstName: "Alice",
      lastName : "Johnson",
      status: "Active",
      createdOn: "2023-01-10",
      email: "alice.johnson@example.com"
    },
    {
      firstName: "Bob",
      lastName: "Brown",
      status: "Active",
      createdOn: "2020-05-30",
      email: "bob.brown@example.com"
    },
    {
      firstName: "Charlie",
      lastName: "Lee",
      status: "Active",
      createdOn: "2024-02-05",
      email: "charlie.lee@example.com"
    },
    {
      firstName: "Diana",
      lastName:  "Prince",
      status: "Inactive",
      createdOn: "2021-09-17",
      email: "diana.prince@example.com"
    }
  ];

const testUser =     {
    firstName: "John",
    lastName: "Doe",
    age: "13",
    status: "Active",
    createdOn: "2022-03-15",
    email: "john.doe@example.com",
    password: "hello"
};

//load initial user information
document.addEventListener("DOMContentLoaded", () => {
    loadUserInfo(testUser);
});

function loadUserInfo(user){
    const firstName = document.getElementById("first-name");
    firstName.value = user.firstName; 

    const lastName = document.getElementById("last-name");
    lastName.value = user.lastName;

    const age = document.getElementById("age");
    age.value = user.age;

    const email = document.getElementById("email");
    email.value = user.email;

    const password = document.getElementById("password");
    password.value = user.password;

    const rePassword = document.getElementById("re-password");
    rePassword.value = '';
}

//reset the form with user info from db
function resetForm(){
    console.log(testUser);
    loadUserInfo(testUser);
    //clear error messages
    const passErrorMessage = document.getElementById('passwordErrorMessage');
    passErrorMessage.style.display = 'none';
    const userErrorMessage = document.getElementById('user-error-message');  
    userErrorMessage.style.displayt = 'none';
}

//check if password has been changed
function checkPass(user){
    pass = document.getElementById("password");
    if (pass.value !== user.password){
        console.log(pass.value);
        console.log(user.password);
        const rePass = document.getElementById("re-password");
        rePass.required = true;
        return true;
    }  
}

//function to check if email was changed and if so checked if the email is already registered
function checkUserExists(users){
    const email = document.getElementById("email");
    if (email.value !== testUser){
        users.forEach(user => {
            if (email.value === user.email){
                const userErrorMessage = document.getElementById('user-error-message');  
                userErrorMessage.textContent = 'User already exists!';  
                userErrorMessage.style.display = 'block';
            }
        });
    }
}

//check new passwords match when submitting
function submitUser(event) {
    event.preventDefault(); 
    
    const pass = document.getElementById("password");
    const newPass = document.getElementById("re-password");
    console.log(pass.value); 

    if (pass.value !== testUser.password){ //if password was changed
        if (pass.value !== newPass.value) { //check the rentered password
            const passErrorMessage = document.getElementById('passwordErrorMessage');  
            passErrorMessage.textContent = 'Passwords do not match';  
            passErrorMessage.style.display = 'block';  
        } else {
            const passErrorMessage = document.getElementById('passwordErrorMessage');
            passErrorMessage.style.display = 'none';  
        }
    }
    else { //remove the error message if no change
        const passErrorMessage = document.getElementById('passwordErrorMessage');
        passErrorMessage.style.display = 'none';
    }
    
    checkUserExists(users);
    console.log(newPass.value); 
}

document.getElementById('update-form').addEventListener('submit', submitUser);
