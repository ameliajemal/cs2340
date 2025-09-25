from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from .models import UserProfile
from jobs.models import Job
from applications.models import Application

def is_recruiter(user):
    """Check if user is a recruiter"""
    try:
        return user.userprofile.role == 'recruiter'
    except UserProfile.DoesNotExist:
        return False

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def dashboard(request):
    """Recruiter dashboard with pipelines overview"""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'recruiter':
        raise Http404("Page not found")
    
    # Get all jobs posted by this recruiter with application counts
    jobs = Job.objects.filter(recruiter=request.user).order_by('-posted_at')
    
    # Add pipeline data for each job
    for job in jobs:
        applications = Application.objects.filter(job=job)
        job.total_applications = applications.count()
        
        # Count applications by stage
        job.stage_counts = {}
        STAGES = [
            ('rejected', 'Rejected'),
            ('applied', 'Applied'),
            ('review', 'Under Review'),
            ('interview', 'Interview'),
            ('offer', 'Offer'),
        ]
        for stage_code, stage_name in STAGES:
            count = applications.filter(stage=stage_code).count()
            job.stage_counts[stage_code] = {
                'name': stage_name,
                'count': count
            }
    
    template_data = {
        "title": "Recruiter Dashboard",
        "jobs": jobs
    }
    return render(request, "accounts/dashboard.html", {"template_data": template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})