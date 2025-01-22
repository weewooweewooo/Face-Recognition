from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import Attendance, Student, Faculty, Subject, Enrollment

def alert_redirect(request, message, url_name):
    return render(request, 'admin_pages/enrollment/alert_redirect.php', {'alert_message': message, 'redirect_url': url_name})

@login_required
def enrollment(request):
    user_role = request.user.role
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        
        if not student_id:
            messages.error(request, "Student ID is required.")
            return render(request, 'admin_pages/enrollment/enrollment.php', {'role': user_role})

        try:
            student = get_object_or_404(Student, enrollment_number=student_id)
            enrollments = Enrollment.objects.filter(student_id=student.id)
            enrollment_details = []
            
            for enrollment in enrollments:
                subject = get_object_or_404(Subject, id=enrollment.subject_id)
                enrollment_details.append({
                    'enrollment'  : enrollment,
                    'subject_name': subject.name,
                    'subject_code': subject.code,
                })

            return render(
                request,
                'admin_pages/enrollment/enrollment.php',
                {
                    'student': student,
                    'role': user_role,
                    'enrollments': enrollment_details,
                },
            )
        except Exception as e:
            messages.error(request, f"Error fetching enrollment details: {str(e)}")

    return render(request, 'admin_pages/enrollment/enrollment.php', {'role': user_role})

@login_required
def add_enrollment(request, student_id):
    user_role = request.user.role
    enrolled_subjects = Enrollment.objects.filter(student_id=student_id).values_list(
        'subject_id', flat=True
    )
    subjects = Subject.objects.exclude(id__in=enrolled_subjects)

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        if subject_id:
            try:
                Enrollment.objects.create(
                    student_id=student_id,
                    subject_id=subject_id,
                    date_enrolled=now().date(),
                    date_completed=None,
                    status='Enrolled',
                )
                return alert_redirect(request, "Subject enrolled successfully.", 'enrollment')
            except Exception as e:
                messages.error(request, f"Error enrolling subject: {str(e)}")
    
    return render(
        request,
        'admin_pages/enrollment/add_enrollment.php',
        {'role': user_role, 'subjects': subjects, 'student_id': student_id},
    )

@login_required
def delete_enrollment(request, enrollment_id):
    user_role = request.user.role
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id)
            enrollment.delete()
            return alert_redirect(request, "Enrollment deleted successfully.", 'enrollment')
        
        except Exception as e:
            messages.error(request, f"Error deleting enrollment: {str(e)}")
    else:
        messages.error(request, "You are not authorized to delete enrollments.")
        
    return redirect('enrollment')




