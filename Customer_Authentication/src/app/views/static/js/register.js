// Define a function to handle the form submission
async function handleLoginFormSubmit(event) {
    // Prevent the form from submitting normally (page reload)
    event.preventDefault();
  
    // Get the values of the email and password fields
    const fname = document.getElementById('first-name').value;
    const lname = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const repassword = document.getElementById('re-password').value;
    const itemData = {first_name: fname, last_name: lname, email: email, password: password};

    // Get the error message container
    const errorMessage = document.getElementById('errorMessage');
    
    // Clear any previous error message
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';

    // Check if either email or password is empty
    if (fname === ''|| lname === ''|| email === '' || password === ''|| repassword === ''){
      errorMessage.textContent = 'Fill in required fields';
      errorMessage.style.display = 'block'; // Show error message
    }
    else if (password !== repassword) {
        errorMessage.textContent = 'Passwords do not match';
        errorMessage.style.display = 'block'; // Show error message
    }
    else{
      console.log('Email:', email);
      console.log('Password:', password);
    }
  }
  // Add an event listener for the form submission
  document.getElementById('registerForm').addEventListener('submit', handleLoginFormSubmit);
  