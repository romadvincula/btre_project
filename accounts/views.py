from email import message
import re
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        # get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords match
        if not password == password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('register')

        # check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is already in use')
            return redirect('register')

        # create new user
        user = User.objects.create_user(username=username, 
            password=password, 
            email=email, 
            first_name=first_name,
            last_name=last_name)
        user.save()

        # login user after registration
        auth.login(request, user)
        messages.success(request, f'Registration successful, logged in as {username}')

        return redirect('index')

    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

        auth.login(request,user)
        messages.success(request, 'You are now logged in')
        
        return redirect('dashboard')

    else:
        if request.user.is_authenticated:
            messages.error(request, 'Already logged in')
            return redirect('dashboard')
            
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You have logged out')

        return redirect('index')

    else:
        return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/dashboard.html')
    
    else:
        return redirect('login')