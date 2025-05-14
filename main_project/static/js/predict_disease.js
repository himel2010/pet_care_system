document.addEventListener('DOMContentLoaded', function() {
    // Get references to elements
    const predictBtn = document.getElementById('predict-btn');
    const resultsContainer = document.getElementById('results');
    const predictionResult = document.getElementById('prediction-result');
    
    // Add event listener to predict button
    predictBtn.addEventListener('click', function() {
        // Get all checked symptoms
        const checkedSymptoms = document.querySelectorAll('input[name="symptoms"]:checked');
        
        // Validate that at least one symptom is selected
        if (checkedSymptoms.length === 0) {
            alert('Please select at least one symptom to predict a disease.');
            return;
        }
        
        // Create an array of selected symptom IDs
        const selectedSymptoms = Array.from(checkedSymptoms).map(checkbox => checkbox.value);
        
        // Show loading state
        predictBtn.disabled = true;
        predictBtn.textContent = 'Predicting...';
        
        // Send the data to the backend
        fetch('/predict_disease/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                symptoms: selectedSymptoms
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display results
            displayResults(data);
            
            // Reset button state
            predictBtn.disabled = false;
            predictBtn.textContent = 'Predict Disease';
            
            // Show results container
            resultsContainer.style.display = 'block';
            
            // Scroll to results
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was a problem with the prediction. Please try again.');
            
            // Reset button state
            predictBtn.disabled = false;
            predictBtn.textContent = 'Predict Disease';
        });
    });
    
    // Function to display prediction results
    function displayResults(data) {
        if (!data.disease) {
            predictionResult.innerHTML = '<p>Not enough symptoms to make a prediction. Please select more symptoms.</p>';
            return;
        }
        
        // Create HTML for the prediction result
        let resultHTML = `
            <div class="prediction-card">
                <h4>Most Likely Disease: ${data.disease.name}</h4>
                <p><strong>Confidence:</strong> ${data.confidence}%</p>
                
                <div class="disease-details">
                    <h5>Treatment</h5>
                    <p>${data.disease.treatment}</p>
                    
                    <h5>Recommended Medicine</h5>
                    <p>${data.disease.medicine_name} (Dosage: ${data.disease.dosage})</p>
                </div>
                
                <div class="disclaimer">
                    <p><em>Note: This is only a prediction based on symptoms. Please consult a veterinarian for proper diagnosis and treatment.</em></p>
                </div>
            </div>
        `;
        
        predictionResult.innerHTML = resultHTML;
    }
    
    // Function to get CSRF token from cookies
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
});

// Additional styles for the results
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .prediction-card {
            padding: 15px;
        }
        
        .prediction-card h4 {
            color: #3a7bd5;
            margin-top: 0;
            margin-bottom: 10px;
        }
        
        .disease-details {
            margin-top: 15px;
        }
        
        .disease-details h5 {
            color: #555;
            margin-bottom: 5px;
        }
        
        .disclaimer {
            margin-top: 20px;
            font-size: 13px;
            color: #777;
        }
    `;
    document.head.appendChild(style);
});
