from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Job
from .forms import JobForm
from applications.models import Application


def index(request):
    search_term = request.GET.get("search")
    if search_term:
        jobs = Job.objects.filter(title__icontains=search_term)
    else:
        jobs = Job.objects.all()

    template_data = {}
    template_data["title"] = "Jobs"
    template_data["jobs"] = jobs
    return render(request, "jobs/index.html", {"template_data": template_data})


def show(request, id):
    job = get_object_or_404(Job, id=id)

    template_data = {}
    template_data["title"] = job.title
    template_data["job"] = job
    return render(request, "jobs/show.html", {"template_data": template_data})


@login_required
def create(request):
    """Create a new job posting"""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'recruiter':
        raise Http404("Page not found")
    
    template_data = {}
    template_data["title"] = "Post New Job"
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs.manage')
        else:
            template_data['form'] = form
    else:
        template_data['form'] = JobForm()
    
    return render(request, "jobs/create.html", {"template_data": template_data})


@login_required
def edit(request, id):
    """Edit an existing job posting"""
    job = get_object_or_404(Job, id=id)
    
    if not (job.recruiter == request.user or request.user.is_superuser):
        raise Http404("Page not found")
    
    template_data = {}
    template_data["title"] = f"Edit {job.title}"
    template_data["job"] = job
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs.manage')
        else:
            template_data['form'] = form
    else:
        template_data['form'] = JobForm(instance=job)
    
    return render(request, "jobs/edit.html", {"template_data": template_data})


@login_required
def delete(request, id):
    """Delete a job posting"""
    job = get_object_or_404(Job, id=id)
    
    if not (job.recruiter == request.user or request.user.is_superuser):
        raise Http404("Page not found")
    
    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f'Job "{job_title}" deleted successfully!')
        return redirect('jobs.manage')
    
    template_data = {}
    template_data["title"] = f"Delete {job.title}"
    template_data["job"] = job
    return render(request, "jobs/delete.html", {"template_data": template_data})


@login_required
def manage(request):
    """Manage job postings for recruiters"""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'recruiter':
        raise Http404("Page not found")
    
    jobs = Job.objects.filter(recruiter=request.user).order_by('-posted_at')
    
    for job in jobs:
        job.application_count = Application.objects.filter(job=job).count()
    
    template_data = {}
    template_data["title"] = "Manage Jobs"
    template_data["jobs"] = jobs
    return render(request, "jobs/manage.html", {"template_data": template_data})
