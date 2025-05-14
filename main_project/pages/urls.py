from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('messenger/', views.messenger, name = 'messenger'),
    path('api/register/', views.api_register, name='api_register'),
    path('predict/', views.predict_disease_page, name='predict_disease_page'),
    path('predict_disease/', views.predict_disease, name='predict_disease'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('login_validation/', views.login_validation, name='login_validation'),

]
