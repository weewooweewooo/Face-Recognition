from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Attendance, Student, Faculty, Enrollment, Subject

@login_required
def subject(request):
    user_role = request.user.role
    subjects = Subject.objects.all()
    return render(
        request,
        'admin_pages/subject/subject.php',
        {'subjects': subjects, 'role': user_role},
    )

@login_required
def add_subject(request):
    user_role = request.user.role
    if request.method == 'POST':
        name = request.POST['courseName']
        code = request.POST['courseCode']
        faculty = request.POST['faculty']

        if name and code and faculty:
            try:
                if Subject.objects.filter(name=name).exists():
                    messages.error(request, 'A subject with this name already exists.')
                elif Subject.objects.filter(code=code).exists():
                    messages.error(request, 'A subject with this code already exists.')
                else:
                    Subject.objects.create(name=name, code=code, faculty=faculty)
                    messages.success(request, 'Course added successfully')
                    return redirect('subject')
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'admin_pages/subject/add_subject.php', {'role': user_role})

@login_required
def delete_subject(request, subject_id):
    if request.user.is_authenticated:
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            subject.delete()
            messages.success(request, 'Subject deleted successfully.')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    else:
        messages.error(request, 'You are not authorized to perform this action.')

    return redirect('subject')  # Redirect to the subject list view
