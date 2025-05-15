# main_project/pages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pet_register/', views.pet_register, name='pet_register'),
    path('predict/', views.predict_disease_page, name='predict_disease_page'),
    
    # API endpoints
    path('api/register/', views.api_register, name='api_register'),
    path('api_pet_reg/', views.api_pet_reg, name='api_pet_reg'),
    path('predict_disease/', views.predict_disease, name='predict_disease'),
    path('login_validation/', views.login_validation, name='login_validation'),
    
    # Updated appointment views
    path('request_appointment/', views.request_appointment, name='request_appointment'),
    path('create_appointment_request/', views.create_appointment_request, name='create_appointment_request'),
    path('accept_appointment/', views.accept_appointment, name='accept_appointment'),
    path('update_appointment_status/', views.update_appointment_status, name='update_appointment_status'),
    path('vet_appointments/', views.vet_appointments, name='vet_appointments'),
    
    # Other views
    path('add_symptom/', views.add_symptom, name='add_symptom'),
    path('logout/', views.logout_view, name='logout'),
    path('add_review/<int:appointment_id>/', views.add_review, name='add_review'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('vet_reviews/', views.vet_reviews, name='vet_reviews'),
    path('vet_reviews/', views.vet_reviews, name='vet_reviews'),
    path('get_vet_reviews/<int:vet_id>/', views.get_vet_reviews, name='get_vet_reviews'),

]