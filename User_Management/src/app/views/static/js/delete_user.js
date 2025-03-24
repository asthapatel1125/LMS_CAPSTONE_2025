const testUser =     {
    firstName: "John",
    lastName: "Doe",
    age: "13",
    status: "Active",
    createdOn: "2022-03-15",
    email: "john.doe@example.com",
    password: "hello"
};

document.addEventListener("DOMContentLoaded", () => {
    loadUserInfo(testUser);
});

function loadUserInfo(user){
    const firstName = document.getElementById("first-name");
    firstName.textContent = user.firstName; 

    const lastName = document.getElementById("last-name");
    lastName.textContent = user.lastName;

    const age = document.getElementById("age");
    age.textContent = user.age;

    const email = document.getElementById("email");
    email.textContent = user.email;

    const password = document.getElementById("password");
    password.textContent = user.password;
}

//maybe it returns back to the main user page
function deleteUser(event){
    alert("Deleting user");
}

document.getElementById('delete-profile-form').addEventListener('submit', deleteUser);