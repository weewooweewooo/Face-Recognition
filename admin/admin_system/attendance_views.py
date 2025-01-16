from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import Attendance, Student, Subject, Enrollment
import subprocess


@login_required
def attendance(request):
    user_role = request.user.role
    subject = Subject.objects.all()
    return render(
        request,
        'admin_pages/attendance/attendance.php',
        {'role': user_role, 'subjects': subject},
    )


@login_required
def attendance_subject(request, subject_id):
    user_role = request.user.role
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        enrollments = Enrollment.objects.filter(subject_id=subject_id)
        student_ids = enrollments.values_list('student_id', flat=True)
        students = Student.objects.filter(id__in=student_ids)

        attendance_records = Attendance.objects.filter(subject_id=subject_id)
        attended_students = attendance_records.values_list('student_id', flat=True)

        if request.method == 'POST':
            student_id = request.POST.get('student_id')
            is_checked = request.POST.get('is_checked') == 'true'

            if student_id:
                student_id = int(student_id)

                if is_checked and student_id not in attended_students:
                    Attendance.objects.create(
                        student_id=student_id,
                        subject_id=subject_id,
                        status='Present',
                        created_at=now(),
                    )
                    messages.success(request, "Attendance marked for the student.")
                elif not is_checked and student_id in attended_students:
                    Attendance.objects.filter(
                        student_id=student_id, subject_id=subject_id
                    ).delete()
                    messages.success(request, "Attendance removed for the student.")

            return redirect('attendance_subject', subject_id=subject_id)

        return render(
            request,
            'admin_pages/attendance/attendance_subject.php',
            {
                'role': user_role,
                'subject': subject,
                'students': students,
                'attended_students': attended_students,
            },
        )
    except Exception as e:
        return render(
            request,
            'admin_pages/attendance/attendance_subject.php',
            {
                'role': user_role,
                'error': f"Error fetching attendance details: {str(e)}",
            },
        )


@login_required
def face_recognition(request, subject_id):
    try:
        script_path = r"D:\Git Project\Face-Recognition\webmain.py"
        result = subprocess.run(
            ["python", script_path, str(subject_id)],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            messages.success(request, "Face recognition completed successfully!")
        else:
            messages.error(request, f"Error during face recognition: {result.stderr}")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('attendance_subject', subject_id=subject_id)
