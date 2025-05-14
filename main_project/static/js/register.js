document.addEventListener('DOMContentLoaded', function() {
    // Show/hide conditional fields based on user type
    document.getElementById('userType').addEventListener('change', function() {
        const userType = this.value;
        
        // Hide all conditional fields first
        document.getElementById('petOwnerFields').style.display = 'none';
        document.getElementById('vetFields').style.display = 'none';
        document.getElementById('daycareFields').style.display = 'none';
        
        // Show the relevant fields based on user type
        if (userType === 'pet_owner') {
            document.getElementById('petOwnerFields').style.display = 'block';
        } else if (userType === 'vet') {
            document.getElementById('vetFields').style.display = 'block';
        } else if (userType === 'daycare') {
            document.getElementById('daycareFields').style.display = 'block';
        }
    });
    
    // Trigger change event to show appropriate fields on page load
    document.getElementById('userType').dispatchEvent(new Event('change'));
    
    // Form validation
    document.getElementById('registerForm').addEventListener('submit', function(event) {
        event.preventDefault();
        
        let isValid = true;
        
        // Validate email
        const email = document.getElementById('email').value;
        if (!email.includes('@') || !email.includes('.')) {
            document.getElementById('emailError').style.display = 'block';
            isValid = false;
        } else {
            document.getElementById('emailError').style.display = 'none';
        }
        
        // Validate phone number (basic validation)
        const phone = document.getElementById('phoneNumber').value;
        if (phone.length < 10) {
            document.getElementById('phoneError').style.display = 'block';
            isValid = false;
        } else {
            document.getElementById('phoneError').style.display = 'none';
        }
        
        // Validate password
        const password = document.getElementById('password').value;
        if (password.length < 6) {
            document.getElementById('passwordError').style.display = 'block';
            isValid = false;
        } else {
            document.getElementById('passwordError').style.display = 'none';
        }
        
        // Validate password confirmation
        const confirmPassword = document.getElementById('confirmPassword').value;
        if (password !== confirmPassword) {
            document.getElementById('confirmPasswordError').style.display = 'block';
            isValid = false;
        } else {
            document.getElementById('confirmPasswordError').style.display = 'none';
        }
        
        // If form is valid, collect data and submit
        if (isValid) {
            const userType = document.getElementById('userType').value;
            
            // Basic user data
            const formData = {
                user_type: userType,
                name: document.getElementById('firstName').value,
                address: document.getElementById('address').value,
                phone_number: phone,
                email: email,
                password: password
            };
            
            // Add conditional fields based on user type
            if (userType === 'pet_owner') {
                formData.emergency_contact = 
                    document.getElementById('emergencyPhone').value 
                ;
            } else if (userType === 'vet') {
                formData.specialization = document.getElementById('vetSpecialization').value;
                formData.qualification = document.getElementById('vetQualification').value;
                formData.experience = document.getElementById('vetExperience').value;
            } else if (userType === 'daycare') {
                formData.facility = {
                    indoor: document.getElementById('indoor').checked,
                    outdoor: document.getElementById('outdoor').checked,
                    overnight: document.getElementById('overnight').checked
                };
                
                // Collect pet types
                const petTypes = [];
                document.querySelectorAll('input[name="petType[]"]:checked').forEach(checkbox => {
                    petTypes.push(checkbox.value);
                });
                formData.pet_types = petTypes;

            }
            
            console.log('Registration data to be sent to backend:', formData);
            
            // Get CSRF token from the form
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Send registration data to Django backend
            fetch('/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Account created successfully! You can now log in.');
                    console.log('hi')
                    window.location.href = document.querySelector('.login_page').getAttribute('href');
                } else {
                    alert(data.message || 'Registration failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during registration. Please try again.');
            });
        }
    });
});