from django.urls import path
from . import views
from . import subject_views
from . import management_views
from . import attendance_views
from . import enrollment_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('documentation/', views.documentation, name='documentation'),
    
    # Attendance URLs
    path('attendance/', attendance_views.attendance, name='attendance'),
    path('attendance_subject/<int:subject_id>', attendance_views.attendance_subject, name='attendance_subject'),
    
    # Management URLs
    path('management/', management_views.user_management, name='management'),
    path('add_user/', management_views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', management_views.delete_user, name='delete_user'),
    
    # Subject URLs
    path('subject/', subject_views.subject, name='subject'),
    path('add_subject/', subject_views.add_subject, name='add_subject'),
    path('delete_subject/<int:subject_id>/', subject_views.delete_subject, name='delete_subject'),
   
    # Enrollment URLs
    path('enrollment/', enrollment_views.enrollment, name='enrollment'),
    path('add_enrollment/<int:student_id>', enrollment_views.add_enrollment, name='add_enrollment'),
    path('delete_enrollment/<int:enrollment_id>', enrollment_views.delete_enrollment, name='delete_enrollment'),
    
    
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
