from django.urls import path
from . import views
from . import subject_views
from . import management_views
from . import attendance_views
from . import enrollment_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Attendance URLs
    path('attendance/', attendance_views.attendance, name='attendance'),
    path('attendance_subject/<int:subject_id>/', attendance_views.attendance_subject, name='attendance_subject'),
    path('face_recognition/<int:subject_id>/', attendance_views.face_recognition, name='face_recognition'),
    
    # Management URLs
    path('management/', management_views.user_management, name='management'),
    path('add_user/', management_views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', management_views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', management_views.delete_user, name='delete_user'),
    
    path('student/', management_views.student_management, name='student'),
    path('add_student/', management_views.add_student, name='add_student'),
    path('edit_student/<int:student_id>/', management_views.edit_student, name='edit_student'),
    path('add_faces/<int:student_id>/', management_views.add_faces, name='add_faces'),
    path('delete_student/<int:student_id>/', management_views.delete_student, name='delete_student'),
    
    # Subject URLs
    path('subject/', subject_views.subject, name='subject'),
    path('add_subject/', subject_views.add_subject, name='add_subject'),
    path('delete_subject/<int:subject_id>/', subject_views.delete_subject, name='delete_subject'),
   
    # Enrollment URLs
    path('enrollment/', enrollment_views.enrollment, name='enrollment'),
    path('add_enrollment/<int:student_id>', enrollment_views.add_enrollment, name='add_enrollment'),
    path('delete_enrollment/<int:enrollment_id>', enrollment_views.delete_enrollment, name='delete_enrollment'),
    
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
]
