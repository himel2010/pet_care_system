from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import*


# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def login(request):
    return render(request, 'pages/login.html')

def messenger(request):
    return render(request, 'pages/messenger.html')

def register(request):
    return render(request, 'pages/register.html')

# pages/views.py



@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)

            user_type = data.get('user_type')
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            phone_number = data.get('phone_number')
            address = data.get('address')

            # Insert into database
            user = User(
                name=name,
                email=email,
                password=password,
                phone_number=phone_number,
                address=address,
            )
            
            user.save()
            print("User saved with ID:", user.id)  # Check if this shows a valid ID
            
            if user_type == 'pet_owner':
                new = Petowner(userid = user,
                               emergency_contact = data.get('emergency_contact'))
                
                new.save()
            
            elif user_type == 'vet':
                new = Vet(userid = user, specialization = data.get('emergency_contact'))
                new.save()
                
            elif user_type == 'daycare':
                facility = data.get('facility')
                for key, value in facility.items():
                    
                    if value:
                        facility = key
                        break
                    
                petType = data.get('pet_types')[0]

                new = Daycare(id = user, indoor = facility, pet_type = petType)
                new.save()

            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'})

@csrf_exempt
def predict_disease_page(request):

    # Get all symptoms from the database
    symptoms = Symptom.objects.all().order_by('name')
    
    # Pass symptoms to the template
    context = {
        'symptoms': symptoms,
    }
    
    return render(request, 'pages/predict_disease.html', context)

def predict_disease(request):
    """
    API endpoint to predict disease based on selected symptoms
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        symptom_ids = data.get('symptoms', [])
        
        # Validate that symptom IDs are provided
        if not symptom_ids:
            return JsonResponse({'error': 'No symptoms provided'}, status=400)
        
        # Convert string IDs to integers if needed
        symptom_ids = [int(sid) for sid in symptom_ids]
        
        # Call the prediction algorithm
        disease, confidence = predict_disease_algorithm(symptom_ids)
        
        if disease:
            # Return prediction result
            return JsonResponse({
                'disease': {
                    'id': disease.id,
                    'name': disease.name,
                    'treatment': disease.treatment,
                    'medicine_name': disease.medicine_name,
                    'dosage': disease.dosage
                },
                'confidence': confidence
            })
        else:
            return JsonResponse({'message': 'Not enough symptoms to make a prediction'})
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def predict_disease_algorithm(symptom_ids):

    # Dictionary to store disease scores
    disease_scores = {}
    
    # Get all symptom-disease relationships for the selected symptoms
    symptom_relations = Symptomindicatesdiseases.objects.filter(sid__in=symptom_ids)
    
    # If no relations found, return None
    if not symptom_relations.exists():
        return None, 0
    
    # Calculate score for each disease
    for relation in symptom_relations:
        disease_id = relation.did.id
        
        # Calculate score as importance * probability
        score = relation.importance * relation.probablity if relation.importance and relation.probablity else 0
        
        # Add score to disease total
        if disease_id in disease_scores:
            disease_scores[disease_id]['score'] += score
            disease_scores[disease_id]['count'] += 1
        else:
            disease_scores[disease_id] = {
                'score': score,
                'count': 1,
                'disease': relation.did
            }
    
    # Find the disease with the highest score
    max_score = 0
    best_disease = None
    confidence = 0
    
    for disease_id, data in disease_scores.items():
        # Calculate average score to account for number of symptoms
        avg_score = data['score'] / data['count']
        
        if avg_score > max_score:
            max_score = avg_score
            best_disease = data['disease']
            
            # Calculate confidence as a percentage of the maximum possible score
            # Assuming max importance is 10 and max probability is 100
            max_possible = 10 * 100  # max importance * max probability
            confidence = min(round((avg_score / max_possible) * 100), 100)
    
    return best_disease, confidence


def dashboard(request):
    return render(request, 'pages/dashboard.html')


@csrf_exempt
def login_validation(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process your login validation here
            # Example: Check email/password against database
            email = data.get('email')
            password = data.get('password')
            print(email, password)
            
            try:
                user = User.objects.get(email=email)
                passw = User.objects.get(password = password)
                print(user, passw)
                if user and passw: 
                    return JsonResponse({
                        'success': True,
                        'message': 'Login successful'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid credentials'
                    })
            except Petowner.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'User not found'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Only POST method is allowed'
    }, status=405)