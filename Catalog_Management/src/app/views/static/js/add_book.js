let authourCount = 1;

// Handle the click event of the "+" button to add new fields
document.getElementById('add-authour').addEventListener('click', function() {
    authourCount++;
    const fieldContainer = document.getElementById('field-container');

    // Create new field
    const newField = document.createElement('div');
    newField.classList.add('form-group', 'mb-3');
    newField.id = 'authour-' + authourCount;

    // Add label, input, and remove button for the new field
    newField.innerHTML = `
        <label for="input-${authourCount}"></label>
        <input type="text" class="form-control" id="input-${authourCount}" name="input-${authourCount}">
        <button type="button" class="btn btn-remove-size btn-sm mt-2 remove-field" data-field="authour-${authourCount}">Remove</button>
    `;

    // Append the new field to the field container
    fieldContainer.appendChild(newField);
});

// Delegate the remove button click event to handle dynamic removal
document.getElementById('field-container').addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('remove-field')) {
        // Get the field ID and remove the corresponding field
        const fieldId = e.target.getAttribute('data-field');
        const fieldToRemove = document.getElementById(fieldId);
        fieldToRemove.remove();
    }
});

// Initialize input mask for phone number
const phoneInput = document.getElementById('isbn-num');
const im = new Inputmask('999-99-99999-99-9');
im.mask(phoneInput);

function toggleFormat() {
    const reasonField = document.getElementById('num-pages');
    const reasonSelect = document.getElementById('book-format');
    if (reasonSelect.value === 'Book' || reasonSelect.value === 'eBook') {
        reasonField.setAttribute('placeholder', 'Number of pages'); // Make field required
    } else {
        reasonField.setAttribute('placeholder', 'Number of minutes'); // Remove required attribute
    }
}

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
    location.href = "edit_inventory.html";
}

function submitBook(){
    alert('Successfully added book!');
}