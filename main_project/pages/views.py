from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def login(request):
    return render(request, 'pages/login.html')

def messenger(request):
    return render(request, 'pages/messenger.html')
