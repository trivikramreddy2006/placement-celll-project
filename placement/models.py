from django.db import models
from accounts.models import User

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    application_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    max_backlogs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Application(models.Model):
    STATUS_CHOICES = (
        ('APPLIED', 'Applied'),
        ('REJECTED', 'Rejected'),
        ('SELECTED', 'Selected'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'company')

    def __str__(self):
        return f"{self.student.username} - {self.company.name}"

class Query(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    answered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='answered_queries')
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.question[:50]}..."

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.recipient.username}: {self.message}"
