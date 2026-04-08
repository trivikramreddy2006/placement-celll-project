from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='STUDENT')

    def is_student(self):
        return self.role == 'STUDENT'

    def is_teacher(self):
        return self.role == 'TEACHER'

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    branch = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    active_backlogs = models.IntegerField(default=0)
    is_blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.branch}"
