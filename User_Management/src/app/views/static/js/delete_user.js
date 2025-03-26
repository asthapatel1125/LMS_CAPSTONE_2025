let user = [];

async function getUserInfo() {
    try {
        const user_email = document.getElementById("user_email").innerText;
        const response = await fetch(`/userManage/customer-info/${user_email}`);
        
        if (!response.ok) {
            alert("Error getting the user's information!");
        }
        
        user = await response.json();
        console.log("User Data:", user);
        
        // After getting user data, load it
        loadUserInfo(user);
        
    } catch (error) {
        console.error("Failed to fetch user info:", error);
    }
}

function loadUserInfo(user) {
    userStatus = document.getElementById("status").innerText;

    const firstName = document.getElementById("first-name");
    firstName.textContent = user.firstName; 

    const lastName = document.getElementById("last-name");
    lastName.textContent = user.lastName;

    if (userStatus === "Manager"){
      const managerID = document.getElementById("managerID");
      managerID.textContent = user.managerID;
      const password = document.getElementById("password");
      password.textContent = user.password;
      
    } else if (userStatus === "Customer"){
      const age = document.getElementById("age");
      age.textContent = user.age;
      const password = document.getElementById("password");
      password.textContent = user.password;
    }

    const email = document.getElementById("email");
    email.textContent = user.email;
}

async function deleteUser(event) {
  event.preventDefault();
  try {
    const response = await fetch(`/userManage/users/delete-user/${user.email}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: user.email }),
    });

    if (!response.ok) {
      const result = await response.json()
      alert(result.message);
    } else {
      const result = await response.json()
      alert(result.message);    
    }

    window.location.href = "/userManage/main";
  } catch (error) {
    console.error("Failed to delete user:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
    getUserInfo();
});

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

document.getElementById('delete-profile-form').addEventListener('submit', deleteUser);
