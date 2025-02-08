function previewImage(event) {
    const imagePreview = document.getElementById('imagePreview');
    const file = event.target.files[0];
    
    if (file) {
        // Create a URL for the selected image file
        const reader = new FileReader();
        reader.onload = function() {
            imagePreview.src = reader.result;  // Set the source of the preview image
            imagePreview.style.display = 'block';  // Display the image
        }
        reader.readAsDataURL(file);  // Read the image file as data URL
    }
}

function cancel(){
    location.href = "/catalog/edit_inventory";
}

function clear(){
    document.getElementById("addBookForm").reset();
}

function validateForm() {
    let isValid = true;
    const errorMessage = "This field is required";

    const formFields = document.querySelectorAll('#addBookForm input[required], #addBookForm textarea[required], #addBookForm select[required]');

    formFields.forEach(field => {
        const errorElement = document.getElementById(field.id + "-error");
        
        if (field.tagName.toLowerCase() === "select") {
            if (!field.value || field.value === "" || field.value === "Choose...") {
                isValid = false;
                if (!errorElement) {
                    const error = document.createElement('div');
                    error.id = field.id + "-error";
                    error.classList.add('text-danger', 'mt-2');
                    error.textContent = errorMessage;
                    field.parentElement.appendChild(error);
                }
            } else {
                if (errorElement) {
                    errorElement.remove();
                }
            }
        } else {
            if (!field.value.trim()) {
                isValid = false;
                if (!errorElement) {
                    const error = document.createElement('div');
                    error.id = field.id + "-error";
                    error.classList.add('text-danger', 'mt-2');
                    error.textContent = errorMessage;
                    field.parentElement.appendChild(error);
                }
            } else {
                if (errorElement) {
                    errorElement.remove();
                }
            }
        }
    });

    return isValid;
}

function submitBook(){
    event.preventDefault();
    const formIsValid = validateForm();
    if (formIsValid) {
        alert('Successfully added book!');
        location.href = "/catalog/edit_inventory";
    }
}

document.getElementById("addBookForm").addEventListener("submit", submitBook);