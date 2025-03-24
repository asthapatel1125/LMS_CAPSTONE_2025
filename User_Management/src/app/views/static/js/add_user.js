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


//function to check if email was changed and if so checked if the email is already registered
function checkUserExists(){
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

//function to check passwords match
function checkPasswords(){
    const pass = document.getElementById("password");
    const newPass = document.getElementById("re-password");
    console.log(pass.value); 

    if (pass.value !== newPass.value) { //check the rentered password
        const passErrorMessage = document.getElementById('passwordErrorMessage');  
        passErrorMessage.textContent = 'Passwords do not match';  
        passErrorMessage.style.display = 'block';  
    } else {
        const passErrorMessage = document.getElementById('passwordErrorMessage');
        passErrorMessage.style.display = 'none';  
    }  
}

//error handling before submission
function checkSubmission(event){
    event.preventDefault(); 
    checkPasswords();
    checkUserExists();
}

//clear any password or user exist errors when refresh form
function clearErrors(){
    const passErrorMessage = document.getElementById('passwordErrorMessage');
    passErrorMessage.style.display = 'none';

    const userErrorMessage = document.getElementById('user-error-message');  
    userErrorMessage.style.display = 'none';
    
    
}
document.getElementById('user-register-form').addEventListener('submit', checkSubmission);
