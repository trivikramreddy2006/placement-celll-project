from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('apply/<int:company_id>/', views.apply_company, name='apply_company'),
    path('add-company/', views.add_company, name='add_company'),
    path('company/<int:company_id>/applicants/', views.view_applicants, name='view_applicants'),
]
