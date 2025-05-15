from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as django_login, logout
import json
from .models import *
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'pages/home.html')


def login(request):
    return render(request, 'pages/login.html')


def register(request):
    return render(request, 'pages/register.html')


def pet_register(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'pages/pet_register.html')


@csrf_exempt
def api_pet_reg(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get the current logged-in user's petowner
            try:
                custom_user = request.user
                user = User.objects.filter(email=custom_user.email).first()
                if not user:
                    return JsonResponse({'success': False, 'message': 'User not found'})
                
                petowner = Petowner.objects.get(userid=user)
            except Petowner.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'You must be a pet owner to register a pet'})
            
            # Create the pet
            pet = Pet(
                type=data.get('type'),
                name=data.get('name'),
                breed=data.get('breed'),
                allergy=data.get('allergy'),
                last_visit=data.get('last_visit'),
                test_result=data.get('test_result'),
                vaccine_name=data.get('vaccine_name'),
                vaccine_date=data.get('vaccine_date'),
                ownerid=petowner,
                age=data.get('age')
            )
            pet.save()
            
            return JsonResponse({'success': True, 'message': 'Pet registered successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'})


@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            user_type = data.get('user_type')
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            phone_number = data.get('phone_number')
            address = data.get('address')
            
            # Create regular User
            user = User(
                name=name,
                email=email,
                password=password,
                phone_number=phone_number,
                address=address,
            )
            user.save()
            
            # Create CustomUser for authentication
            custom_user = CustomUser.objects.create_user(
                email=email,
                password=password
            )
            
            # Create specific user type
            if user_type == 'pet_owner':
                Petowner.objects.create(
                    userid=user,
                    emergency_contact=data.get('emergency_contact')
                )
            elif user_type == 'vet':
                Vet.objects.create(
                    userid=user,
                    specialization=data.get('specialization', data.get('emergency_contact'))
                )
            elif user_type == 'daycare':
                Daycare.objects.create(
                    id=user,
                    indoor=data.get('facility', {}).get('indoor', 'No'),
                    pet_type=data.get('pet_types', [''])[0]
                )
            
            # Login the user
            django_login(request, custom_user)
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'})


@csrf_exempt
def login_validation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # Authenticate with CustomUser
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                django_login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid credentials'
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


@login_required
def dashboard(request):
    try:
        # Get the User object based on the CustomUser email
        user = User.objects.filter(email=request.user.email).first()
        if not user:
            return redirect('login')
        
        petowner = Petowner.objects.filter(userid=user).first()
        vet = Vet.objects.filter(userid=user).first()
        daycare = Daycare.objects.filter(id=user).first()
        
        # Initialize variables
        pets = []
        current_appointments = []
        pending_appointments = []
        
        if petowner:
            pets = Pet.objects.filter(ownerid=petowner)
            # Get all appointments for the pet owner
            current_appointments = appointvOwneret.objects.filter(
                ownerid=petowner,
                accepted=True
            )
            
            # Get existing reviews for this pet owner
            existing_reviews = Ownerratesvet.objects.filter(pid=petowner)
            reviewed_vets = set(review.vid.userid.id for review in existing_reviews)
            
            # Mark appointments with review status
            for appointment in current_appointments:
                appointment.has_review = appointment.vid.userid.id in reviewed_vets
        
        elif vet:
            # Get pending appointment requests for vet
            pending_appointments = appointvOwneret.objects.filter(
                vid=vet,
                accepted=False
            )
            # Get current clients (accepted appointments)
            current_appointments = appointvOwneret.objects.filter(
                vid=vet,
                accepted=True
            )
        
        context = {
            'user': user,
            'is_petowner': bool(petowner),
            'is_vet': bool(vet),
            'is_daycare': bool(daycare),
            'petowner': petowner,
            'vet': vet,
            'daycare': daycare,
            'pets': pets,
            'current_appointments': current_appointments,
            'pending_appointments': pending_appointments,
            'notification_count': len(pending_appointments) if vet else 0
        }
        
        return render(request, 'pages/dashboard.html', context)
    except Exception as e:
        print(f"Dashboard error: {e}")
        import traceback
        traceback.print_exc()
        return redirect('login')

def predict_disease_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    symptoms = Symptom.objects.all().order_by('name')
    
    context = {
        'symptoms': symptoms,
    }
    
    return render(request, 'pages/predict_disease.html', context)


@csrf_exempt
def predict_disease(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        symptom_ids = data.get('symptoms', [])
        
        if not symptom_ids:
            return JsonResponse({'error': 'No symptoms provided'}, status=400)
        
        symptom_ids = [int(sid) for sid in symptom_ids]
        
        disease, confidence = predict_disease_algorithm(symptom_ids)
        
        if disease:
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
    disease_scores = {}
    
    symptom_relations = Symptomindicatesdiseases.objects.filter(sid__in=symptom_ids)
    
    if not symptom_relations.exists():
        return None, 0
    
    for relation in symptom_relations:
        disease_id = relation.did.id
        
        score = relation.importance * relation.probablity if relation.importance and relation.probablity else 0
        
        if disease_id in disease_scores:
            disease_scores[disease_id]['score'] += score
            disease_scores[disease_id]['count'] += 1
        else:
            disease_scores[disease_id] = {
                'score': score,
                'count': 1,
                'disease': relation.did
            }
    
    max_score = 0
    best_disease = None
    confidence = 0
    
    for disease_id, data in disease_scores.items():
        avg_score = data['score'] / data['count']
        
        if avg_score > max_score:
            max_score = avg_score
            best_disease = data['disease']
            
            max_possible = 10 * 100
            confidence = min(round((avg_score / max_possible) * 100), 100)
    
    return best_disease, confidence


@login_required
def request_appointment(request):
    try:
        # Get user's pets
        user = User.objects.filter(email=request.user.email).first()
        petowner = Petowner.objects.filter(userid=user).first()
        pets = Pet.objects.filter(ownerid=petowner) if petowner else []
        
        # Get all vets
        vets = Vet.objects.all()
        
        context = {
            'pets': pets,
            'vets': vets
        }
        
        return render(request, 'pages/request_appointment.html', context)
    except Exception as e:
        print(f"Request appointment error: {e}")
        return redirect('dashboard')


@csrf_exempt
def create_appointment_request(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Get current user's petowner
        user = User.objects.filter(email=request.user.email).first()
        petowner = Petowner.objects.get(userid=user)
        
        # Get selected pet and vet
        pet = Pet.objects.get(id=data.get('pet_id'))
        vet = Vet.objects.get(userid__id=data.get('vet_id'))
        
        # Check if appointment already exists
        existing = appointvOwneret.objects.filter(
            petid=pet,
            ownerid=petowner,
            vid=vet
        ).first()
        
        if existing:
            return JsonResponse({
                'success': False,
                'message': 'An appointment request already exists for this pet with this vet'
            })
        
        # Create appointment request (not accepted yet, no fee)
        appointment = appointvOwneret(
            petid=pet,
            ownerid=petowner,
            vid=vet,
            time=data.get('time'),
            date=data.get('date'),
            fee=None,  # No fee until vet accepts
            status='Pending',
            accepted=False
        )
        appointment.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Appointment request sent successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def accept_appointment(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        appointment_id = data.get('appointment_id')
        fee = data.get('fee')
        
        # Get the appointment
        appointment = appointvOwneret.objects.get(petid__id=appointment_id)
        
        # Update appointment
        appointment.accepted = True
        appointment.fee = fee
        appointment.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Appointment accepted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def update_appointment_status(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        appointment_id = data.get('appointment_id')
        status = data.get('status')
        
        # Get the appointment
        appointment = appointvOwneret.objects.get(petid__id=appointment_id)
        
        # Update status  
        appointment.status = status
        appointment.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Status updated to {status} successfully'
        })
        
    except appointvOwneret.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    except Exception as e:
        print(f"Update appointment status error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def add_symptom(request):
    if request.method == 'GET':
        return render(request, 'pages/add_symptom.html')
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            symptom = Symptom(
                name=data.get('name'),
                physical=data.get('physical'),
                behavioural=data.get('behavioural')
            )
            symptom.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Symptom added successfully'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def vet_appointments(request):
    try:
        user = User.objects.filter(email=request.user.email).first()
        vet = Vet.objects.get(userid=user)
        
        # Get pending and accepted appointments
        pending_appointments = appointvOwneret.objects.filter(
            vid=vet,
            accepted=False
        )
        accepted_appointments = appointvOwneret.objects.filter(
            vid=vet,
            accepted=True
        )
        
        context = {
            'pending_appointments': pending_appointments,
            'accepted_appointments': accepted_appointments
        }
        
        return render(request, 'pages/vet_appointments.html', context)
        
    except Exception as e:
        print(f"Vet appointments error: {e}")
        return redirect('dashboard')


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_review(request, appointment_id):
    try:
        # Get the appointment
        appointment = appointvOwneret.objects.get(petid__id=appointment_id)
        
        # Check if user is the pet owner
        user = User.objects.filter(email=request.user.email).first()
        petowner = Petowner.objects.get(userid=user)
        
        if appointment.ownerid != petowner:
            return redirect('dashboard')
        
        # Check if appointment is completed
        if appointment.status != 'Completed':
            return redirect('dashboard')
        
        context = {
            'appointment': appointment
        }
        
        return render(request, 'pages/add_review.html', context)
    except Exception as e:
        return redirect('dashboard')


@csrf_exempt
def submit_review(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Get current user's petowner
        user = User.objects.filter(email=request.user.email).first()
        petowner = Petowner.objects.get(userid=user)
        
        # Get the appointment
        appointment = appointvOwneret.objects.get(petid__id=data.get('appointment_id'))
        
        # Check if user owns this appointment
        if appointment.ownerid != petowner:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        # Create review
        review = Ownerratesvet(
            vid=appointment.vid,
            pid=petowner,
            review=data.get('review'),
            rating=data.get('rating')
        )
        review.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Review submitted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def vet_reviews(request):
    try:
        user = User.objects.filter(email=request.user.email).first()
        vet = Vet.objects.get(userid=user)
        
        # Get all reviews for this vet
        reviews = Ownerratesvet.objects.filter(vid=vet).order_by('-id')
        
        # Calculate average rating
        if reviews:
            avg_rating = sum([r.rating for r in reviews]) / len(reviews)
        else:
            avg_rating = 0
        
        # Debug print
        print(f"Vet: {vet.userid.name}")
        print(f"Number of reviews: {reviews.count()}")
        for review in reviews:
            print(f"Review ID: {review.id}, From: {review.pid.userid.name}, Rating: {review.rating}")
        
        context = {
            'reviews': reviews,
            'avg_rating': round(avg_rating, 1)
        }
        
        return render(request, 'pages/vet_reviews.html', context)
        
    except Vet.DoesNotExist:
        print("Vet not found for user:", request.user.email)
        return redirect('dashboard')
    except Exception as e:
        print(f"Vet reviews error: {e}")
        import traceback
        traceback.print_exc()
        return redirect('dashboard')
# Update the request_appointment view to include ratings
@login_required
def request_appointment(request):
    try:
        # Get user's pets
        user = User.objects.filter(email=request.user.email).first()
        petowner = Petowner.objects.filter(userid=user).first()
        pets = Pet.objects.filter(ownerid=petowner) if petowner else []
        
        # Get all vets with their average ratings
        vets = Vet.objects.all()
        vet_data = []
        
        for vet in vets:
            reviews = Ownerratesvet.objects.filter(vid=vet)
            if reviews:
                avg_rating = sum([r.rating for r in reviews]) / len(reviews)
            else:
                avg_rating = 0
            
            vet_data.append({
                'vet': vet,
                'avg_rating': round(avg_rating, 1),
                'review_count': len(reviews)
            })
        
        context = {
            'pets': pets,
            'vet_data': vet_data
        }
        
        return render(request, 'pages/request_appointment.html', context)
    except Exception as e:
        print(f"Request appointment error: {e}")
        return redirect('dashboard')

@login_required
def vet_reviews(request):
    try:
        user = User.objects.filter(email=request.user.email).first()
        vet = Vet.objects.get(userid=user)
        
        # Get all reviews for this vet
        reviews = Ownerratesvet.objects.filter(vid=vet)
        
        # Calculate average rating
        if reviews:
            avg_rating = sum([r.rating for r in reviews]) / len(reviews)
        else:
            avg_rating = 0
        
        context = {
            'reviews': reviews,
            'avg_rating': round(avg_rating, 1)
        }
        
        return render(request, 'pages/vet_reviews.html', context)
        
    except Exception as e:
        return redirect('dashboard')


def get_vet_reviews(request, vet_id):
    try:
        vet_user = User.objects.get(id=vet_id)
        vet = Vet.objects.get(userid=vet_user)
        reviews = Ownerratesvet.objects.filter(vid=vet)
        
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                'reviewer_name': review.pid.userid.name,
                'rating': review.rating,
                'review': review.review
            })
        
        return JsonResponse({
            'vet_name': vet.userid.name,
            'reviews': reviews_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)