from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Attendance, Student, Faculty, Enrollment, Subject, User


@login_required
def user_management(request):
    user_role = request.user.role
    user = User.objects.all()
    return render(
        request,
        'admin_pages/management/management.php',
        {'role': user_role, 'users': user},
    )


@login_required
def add_user(request):
    user_role = request.user.role
    username = request.POST.get('username')
    first_name = request.POST.get('firstName')
    last_name = request.POST.get('lastName')
    password = request.POST.get('password')
    email = request.POST.get('email')
    role = request.POST.get('role')

    if username and first_name and last_name and email and role and password:
        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'A user with this username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists.')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    email=email,
                    role=role,
                    is_staff=1,
                )
                user.save()
                messages.success(request, 'User added successfully!')
                return redirect('management')
        except Exception as e:
            messages.error(request, f"Error: {e}")
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'admin_pages/management/add_user.php', {'role': user_role})


@login_required
def delete_user(request, user_id):
    if request.user.is_authenticated:
        try:
            subject = get_object_or_404(User, id=user_id)
            subject.delete()
            messages.success(request, 'Subject deleted successfully.')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    else:
        messages.error(request, 'You are not authorized to perform this action.')

    return redirect('management')  # Redirect to the subject list view
