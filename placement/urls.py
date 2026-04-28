from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('apply/<int:company_id>/', views.apply_company, name='apply_company'),
    path('add-company/', views.add_company, name='add_company'),
    path('company/<int:company_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('company/<int:company_id>/toggle/', views.toggle_company_status, name='toggle_company_status'),
    path('company/<int:company_id>/', views.company_details, name='company_details'),
    path('company/<int:company_id>/export/', views.export_applicants, name='export_applicants'),
    path('queries/', views.queries_forum, name='queries_forum'),
    path('queries/add/', views.add_query, name='add_query'),
    path('queries/<int:query_id>/answer/', views.answer_query, name='answer_query'),
    path('notifications/read/', views.read_notifications, name='read_notifications'),
]
