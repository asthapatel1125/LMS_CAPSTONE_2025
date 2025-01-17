// Define a function to handle the form submission
async function handleLoginFormSubmit(event) {
    // Prevent the form from submitting normally (page reload)
    event.preventDefault();
  
    // Get the values of the email and password fields
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const itemData = {email: email, password: password};

    // Get the error message container
    const errorMessage = document.getElementById('errorMessage');
    
    // Clear any previous error message
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';

    // Check if either email or password is empty
    if (email === ''){
      errorMessage.textContent = 'Enter your email';
      errorMessage.style.display = 'block'; // Show error message
    }
    else if (password === ''){
      errorMessage.textContent = 'Enter your password';
      errorMessage.style.display = 'block'; // Show error message
    }
    else {
     /* try {
        // Send the data using fetch API
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"  // Tell FastAPI we are sending JSON
            },
            body: JSON.stringify(itemData)  // Convert the JavaScript object to JSON
        });
        // Parse the response as JSON
        const responseData = await response.json();
        // Display the response message
        document.getElementById("responseMessage").innerText = responseData.message;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("responseMessage").innerText = "An error occurred!";
    }
      // If fields are filled, proceed with the form submission (e.g., logging in)*/
      console.log('Email:', email);
      console.log('Password:', password);
    }
  }
  // Add an event listener for the form submission
  document.getElementById('loginForm').addEventListener('submit', handleLoginFormSubmit);
  