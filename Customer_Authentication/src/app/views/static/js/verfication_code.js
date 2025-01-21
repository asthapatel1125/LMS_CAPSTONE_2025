async function verifCode(event) {
    //function to send entered verification code to backend
    event.preventDefault();
    const verif_code = document.getElementById('verif-code').value;
    const verifErrorMessage = document.getElementById('errorMessage');
    
    // Clear any previous error message
    verifErrorMessage.style.display = 'none';
    verifErrorMessage.textContent = '';
  
    if (verif_code === ''){
      verifErrorMessage.textContent = 'Enter verification code';
      verifErrorMessage.style.display = 'block'; // Show error message    
    }else{
        console.log("Verification code", verif_code);      
    }
  }

  document.getElementById('verif-code-form').addEventListener('submit', verifCode);