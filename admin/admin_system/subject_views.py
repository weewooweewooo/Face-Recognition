from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Attendance, Student, Faculty, Enrollment, Subject

def alert_redirect(request, message, url_name):
    return render(request, 'admin_pages/subject/alert_redirect.php', {'alert_message': message, 'redirect_url': url_name})

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
                    return alert_redirect(request, 'Course added successfully', 'subject')
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
            enrollments = Enrollment.objects.filter(subject_id=subject_id)
            if enrollments.exists():
                enrollments.delete()
            subject.delete()
            return alert_redirect(request, 'Subject and associated enrollments deleted successfully.', 'subject')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    else:
        messages.error(request, 'You are not authorized to perform this action.')


@login_required
def edit_subject(request, subject_id):
    user_role = request.user.role
    user = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        new_name = request.POST.get('courseName')
        if Subject.objects.filter(name=new_name).exclude(id=subject_id).exists():
            messages.error(request, 'A subject with this name already exists.')
        else:
            user.name = new_name
            user.code = request.POST.get('courseCode')
            user.faculty = request.POST.get('faculty')
            user.save()
            return alert_redirect(request, 'Subject updated successfully!', 'subject')
        
    return render(request, 'admin_pages/subject/edit_subject.php', {'role': user_role, 'subject': user})

