from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Attendance, Student, Faculty, Enrollment, Subject, User
import subprocess
import os
from django.conf import settings
import shutil


@login_required
def user_management(request):
    user_role = request.user.role
    user = User.objects.all()
    return render(
        request,
        'admin_pages/management/management.php',
        {'role': user_role, 'users': user},
    )
    
def student_management(request):
    user_role = request.user.role
    students = Student.objects.all()
    return render(
        request,
        'admin_pages/management/management.php',
        {'role': user_role, 'students': students},
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
def add_student(request):
    user_role = request.user.role
    username = request.POST.get('username')
    enrollmentNumber = request.POST.get('enrollment_number')
    faculty = request.POST.get('faculty')

    if username and enrollmentNumber and faculty:
        try:
            if Student.objects.filter(enrollment_number=enrollmentNumber).exists():
                messages.error(request, 'A student with this enrollment number already exists.')
            elif Student.objects.filter(name=username).exists():
                messages.error(request, 'A student with this name already exists.')
            else:
                student = Student.objects.create(
                    name=username,
                    enrollment_number=enrollmentNumber,
                    faculty=faculty,
                    faces=None,
                )
                student.save()
                messages.success(request, 'Student added successfully!')
                return redirect('student')
        except Exception as e:
            messages.error(request, f"Error: {e}")
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'admin_pages/management/add_student.php', {'role': user_role})

@login_required
def edit_student(request, student_id):
    user_role = request.user.role
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        new_name = request.POST.get('username')
        if Student.objects.filter(name=new_name).exclude(id=student_id).exists():
            messages.error(request, 'A student with this name already exists.')
        else:
            student.name = new_name
            student.faculty = request.POST.get('faculty')
            student.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student')
    
    return render(request, 'admin_pages/management/edit_student.php', {'role': user_role, 'student': student})

@login_required
def edit_user(request, user_id):
    user_role = request.user.role
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_name = request.POST.get('username')
        if Student.objects.filter(name=new_name).exclude(id=user_id).exists():
            messages.error(request, 'A user with this name already exists.')
        else:
            user.name = new_name
            user.faculty = request.POST.get('faculty')
            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('management')
    
    return render(request, 'admin_pages/management/edit_user.php', {'role': user_role, 'user': user})

@login_required
def add_faces(request, student_id):
    user_role = request.user.role
    student = get_object_or_404(Student, id=student_id)

    try:
        script_path = r"D:\Git Project\Face-Recognition\webfacesaver.py"
        result = subprocess.run(
            ["python", script_path, str(student.name), str(student.enrollment_number), str(student.faculty)],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            messages.success(request, "Face recognition completed successfully!")
            alert_message = "Face recognition completed successfully!"
        else:
            messages.error(request, f"Error during face recognition: {result.stderr}")
            alert_message = f"Error during face recognition: {result.stderr}"

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        alert_message = f"An error occurred: {str(e)}"

    return render(request, 'admin_pages/management/alert_redirect.php', {'role': user_role, 'alert_message': alert_message})

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

    return redirect('management')

@login_required
def delete_student(request, student_id):
    if request.user.is_authenticated:
        try:
            student = get_object_or_404(Student, id=student_id)
            if student.faces:
                folder_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, student.faces[0]))
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
            student.delete()
            messages.success(request, 'Student deleted successfully.')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    else:
        messages.error(request, 'You are not authorized to perform this action.')

    return redirect('student')
