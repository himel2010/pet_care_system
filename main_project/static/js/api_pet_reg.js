// Only this one listener is enough
document.getElementById('pet-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const form = e.target;
    const data = {
        type: form.type.value,
        name: form.name.value,
        breed: form.breed.value,
        allergy: form.allergy.value,
        last_visit: form.last_visit.value,
        test_result: form.test_result.value,
        vaccine_name: form.vaccine_name.value,
        vaccine_date: form.vaccine_date.value,
        age: parseInt(form.age.value),
        OwnerID: form.OwnerID.value
    };

    fetch('api_pet_reg/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        alert(result.message);
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
