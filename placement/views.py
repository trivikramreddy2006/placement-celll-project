from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, Application
from accounts.models import StudentProfile
import csv
from django.http import HttpResponse

@login_required
def dashboard_redirect(request):
    if request.user.is_teacher():
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')

@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect('dashboard')
    
    student_profile = request.user.student_profile
    active_companies = Company.objects.filter(is_active=True).order_by('-created_at')
    past_companies = Company.objects.filter(is_active=False).order_by('-created_at')
    applications = Application.objects.filter(student=request.user).values_list('company_id', flat=True)
    
    context = {
        'active_companies': active_companies,
        'past_companies': past_companies,
        'applied_company_ids': applications,
        'profile': student_profile
    }
    return render(request, 'placement/student_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        return redirect('dashboard')
    
    companies = Company.objects.all().order_by('-created_at')
    context = {
        'companies': companies
    }
    return render(request, 'placement/teacher_dashboard.html', context)

@login_required
def apply_company(request, company_id):
    if request.method == 'POST' and request.user.is_student():
        company = get_object_or_404(Company, id=company_id, is_active=True)
        profile = request.user.student_profile
        
        if profile.is_blacklisted:
            messages.error(request, "You cannot apply because you are blacklisted.")
            return redirect('student_dashboard')
            
        if profile.active_backlogs > company.max_backlogs:
            messages.error(request, f"You exceed the maximum backlogs allowed ({company.max_backlogs}).")
            return redirect('student_dashboard')
            
        if profile.cgpa < company.min_cgpa:
            messages.error(request, f"You do not meet the minimum CGPA requirement ({company.min_cgpa}).")
            return redirect('student_dashboard')
            
        application, created = Application.objects.get_or_create(student=request.user, company=company)
        
        if 'resume' in request.FILES:
            application.resume = request.FILES['resume']
            application.save()
            
        messages.success(request, f"Successfully applied to {company.name}.")
    return redirect('company_details', company_id=company.id)

@login_required
def add_company(request):
    if not request.user.is_teacher():
        return redirect('dashboard')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        link = request.POST.get('application_link')
        min_cgpa = request.POST.get('min_cgpa')
        max_backlogs = request.POST.get('max_backlogs')
        
        Company.objects.create(
            name=name,
            description=description,
            application_link=link,
            min_cgpa=min_cgpa,
            max_backlogs=max_backlogs,
            is_active=True
        )
        messages.success(request, "Company added successfully.")
        return redirect('teacher_dashboard')
        
    return render(request, 'placement/add_company.html')

@login_required
def view_applicants(request, company_id):
    if not request.user.is_teacher():
        return redirect('dashboard')
        
    company = get_object_or_404(Company, id=company_id)
    applications = Application.objects.filter(company=company).select_related('student', 'student__student_profile')
    
    return render(request, 'placement/view_applicants.html', {'company': company, 'applications': applications})

@login_required
def toggle_company_status(request, company_id):
    if not request.user.is_teacher():
        return redirect('dashboard')
        
    if request.method == 'POST':
        company = get_object_or_404(Company, id=company_id)
        company.is_active = not company.is_active
        company.save()
        status_text = "active" if company.is_active else "closed"
        messages.success(request, f"Company '{company.name}' marked as {status_text}.")
        
    return redirect('teacher_dashboard')

@login_required
def company_details(request, company_id):
    if not request.user.is_student():
        return redirect('dashboard')
        
    company = get_object_or_404(Company, id=company_id)
    profile = request.user.student_profile
    has_applied = Application.objects.filter(student=request.user, company=company).exists()
    
    is_eligible = not profile.is_blacklisted and profile.active_backlogs <= company.max_backlogs and profile.cgpa >= company.min_cgpa
    
    context = {
        'company': company,
        'has_applied': has_applied,
        'is_eligible': is_eligible,
        'profile': profile
    }
    return render(request, 'placement/company_details.html', context)

@login_required
def export_applicants(request, company_id):
    if not request.user.is_teacher():
        return redirect('dashboard')
        
    company = get_object_or_404(Company, id=company_id)
    applications = Application.objects.filter(company=company).select_related('student', 'student__student_profile')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{company.name}_applicants.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Branch', 'CGPA', 'Active Backlogs', 'Applied At', 'Resume Link'])
    
    for app in applications:
        resume_link = ""
        if app.resume:
            resume_link = request.build_absolute_uri(app.resume.url)
            
        writer.writerow([
            app.student.username,
            app.student.email,
            app.student.student_profile.branch,
            app.student.student_profile.cgpa,
            app.student.student_profile.active_backlogs,
            app.applied_at.strftime("%Y-%m-%d %H:%M"),
            resume_link
        ])
        
    return response
