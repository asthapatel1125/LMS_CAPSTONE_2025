/* Notes:
-maybe only submit form if any of the fields change
-need to prevent form from submitting if error 
-same logic as admin edit profile (just copied it)
 */

//load initial user information
let user = [];
let newUser = [];

async function getUserInfo() {
    try {
        const user_email = document.getElementById("user_email").innerText;
        const response = await fetch(`/userManage/customer-info/${user_email}`);
        
        if (!response.ok) {
            alert("Error getting the user's information!");
        }
        
        user = await response.json();
        console.log("User Data:", user);
        
        loadUserInfo(user);
        
    } catch (error) {
        console.error("Failed to fetch user info:", error);
    }
}

function loadUserInfo(user){
    userStatus = document.getElementById("status").innerText;

    const firstName = document.getElementById("first-name");
    firstName.value = user.firstName; 

    const lastName = document.getElementById("last-name");
    lastName.value = user.lastName;

    if (userStatus === "Manager"){
        const email = document.getElementById("managerID");
        email.value = user.managerID;

    } else if (userStatus === "Customer"){
        const age = document.getElementById("age");
        age.value = user.age;
    }

    const email = document.getElementById("email");
    email.value = user.email;
}

//reset the form with user info from db
function resetForm(){
    console.log(user);
    loadUserInfo(user);

    const userErrorMessage = document.getElementById('user-error-message');  
    userErrorMessage.style.display = 'none';
}

//check new passwords match when submitting
async function submitUser(event) {
    event.preventDefault(); 
    const formData = new FormData();
    formData.append("firstName", document.getElementById("first-name").value);
    formData.append("lastName", document.getElementById("last-name").value);
    formData.append("email", document.getElementById("email").value);

    userStatus = document.getElementById("status").innerText;
    if (userStatus === "Customer"){
        formData.append("age", document.getElementById("age").value);
    } else if(userStatus === "Manager"){
        formData.append("managerID", document.getElementById("managerID").value);
    }
    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }

    try {
        let username;
        if (userStatus === "Customer"){
            username = user.email;
        } else {
            username = user.managerID;
        }
        const response = await fetch(`/userManage/users/edit-user/${username}`, {
            method: "POST",
            body: formData,
            credentials: "include" // Ensures cookies (manager_login_token) are sent
        });
        
        const result = await response.json();
        alert(result.message);
        
        window.location.href = "/userManage/main";
        
    } catch (error) {
        alert("An error occurred while editing the user.");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    getUserInfo();
    let userStatus = document.getElementById("status").innerText;

    if (userStatus === "Manager") {
        document.getElementById("manager-id-field").style.display = "block";
        document.getElementById("age-field").style.display = "none";
    } else if(userStatus === "Customer"){
        document.getElementById("age-field").style.display = "block";
        document.getElementById("manager-id-field").style.display = "none";
    }
});