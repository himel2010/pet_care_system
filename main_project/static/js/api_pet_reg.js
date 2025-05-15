// main_project/static/js/api_pet_reg.js
document.getElementById('pet-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const form = e.target;
    const data = {
        type: form.type.value,
        name: form.name.value,
        breed: form.breed.value,
        allergy: form.allergy.value || '',
        last_visit: form.last_visit.value || null,
        test_result: form.test_result.value || '',
        vaccine_name: form.vaccine_name.value || '',
        vaccine_date: form.vaccine_date.value || null,
        age: parseInt(form.age.value)
    };

    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api_pet_reg/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const messageDiv = document.getElementById('response-message');
        messageDiv.textContent = result.message;
        messageDiv.style.color = result.success ? 'green' : 'red';
        
        if (result.success) {
            form.reset();
        }
    })
    .catch(error => {
        const messageDiv = document.getElementById('response-message');
        messageDiv.textContent = 'Error: ' + error;
        messageDiv.style.color = 'red';
    });
});