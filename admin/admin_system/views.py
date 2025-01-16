from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Attendance, Student, Faculty

@login_required
def dashboard(request):
    user_role = request.user.role
    return render(request, 'admin_pages/dashboard.php', {'role': user_role})

def documentation(request):
    return render(request, 'admin_pages/documentation.php')

def login_view(request, user=None):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    next_url = request.GET.get('next')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect(next_url if next_url else 'dashboard')  # Redirect to 'next' or dashboard
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'admin_pages/index.php', {'next': next_url})

def register(request):
    return render(request, 'admin_pages/register.php')

def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'admin_pages/profile.php')




