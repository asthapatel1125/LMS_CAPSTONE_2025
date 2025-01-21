async function resetPassword(event){
    event.preventDefault();
    const new_password = document.getElementById('password').value;
    const re_entered_password = document.getElementById('re-password').value;
    const itemData = {password: new_password};
  
    const passErrorMessage = document.getElementById('passwordErrorMessage');
  
    passErrorMessage.style.display = 'none';
    passErrorMessage.textContent = '';
  
    if (new_password === '' || re_entered_password ===''){
      passErrorMessage.textContent = 'Enter required fields';
      passErrorMessage.style.display = 'block'; // Show error message      
    }
    else if (new_password !== re_entered_password){
      passErrorMessage.textContent = 'Passwords do not match';
      passErrorMessage.style.display = 'block'; // Show error message   
    }
    else {
      console.log("Password", new_password);
    }
  }

  document.getElementById('reset-password-form').addEventListener('submit', resetPassword);