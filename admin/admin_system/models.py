from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=255)
    enrollment_number = models.CharField(max_length=20, unique=True)
    faculty = models.CharField(max_length=255)
    faces = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.name} ({self.enrollment_number})"

class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    faculty = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - ({self.code}) - {self.faculty}"
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=[('Current', 'Current'), ('Previous', 'Previous')])
    date_enrolled = models.DateField(auto_now_add=True)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.status}"    

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.created_at} - {self.status}"