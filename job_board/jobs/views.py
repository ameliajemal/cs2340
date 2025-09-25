from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from .models import Job
from .forms import JobForm, JobFilterForm
from applications.models import Application


def index(request):
    qs = Job.objects.all().prefetch_related("skills").order_by("-posted_at")

    form = JobFilterForm(request.GET or None)

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(company__icontains=q) |
                Q(description__icontains=q) |
                Q(location__icontains=q) |
                Q(skills__name__icontains=q)
            )

        location = form.cleaned_data.get("location")
        if location:
            qs = qs.filter(location__icontains=location)

        skills = form.cleaned_data.get("skills")
        if skills:
            for s in skills:
                qs = qs.filter(skills=s)

        desired_min = form.cleaned_data.get("salary_min")
        if desired_min not in (None, ""):
            qs = qs.filter(Q(salary_max__gte=desired_min) | Q(salary_min__gte=desired_min))

        desired_max = form.cleaned_data.get("salary_max")
        if desired_max not in (None, ""):
            qs = qs.filter(Q(salary_min__lte=desired_max) | Q(salary_max__lte=desired_max))

        remote = form.cleaned_data.get("remote")
        if remote == "remote":
            qs = qs.filter(is_remote=True)
        elif remote == "onsite":
            qs = qs.filter(is_remote=False)

        sponsorship = form.cleaned_data.get("sponsorship")
        if sponsorship == "yes":
            qs = qs.filter(provides_sponsorship=True)
        elif sponsorship == "no":
            qs = qs.filter(provides_sponsorship=False)

        qs = qs.distinct()

    template_data = {
        "title": "Job Listings",
        "jobs": qs,
    }
    return render(request, "jobs/index.html", {"template_data": template_data, "filter_form": form})


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
