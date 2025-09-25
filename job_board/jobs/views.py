from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from .models import Job
from .forms import JobForm, JobFilterForm
from applications.models import Application
from profiles.models import Profile as CandidateProfile, Education, WorkExperience
from profiles.forms import ProfileForm as CandidateProfileForm
from .models import Job

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

@login_required
def create_profile(request):
    # Check if profile already exists
    if CandidateProfile.objects.filter(user=request.user).exists():
        messages.info(request, "You already have a profile.")
        return redirect('jobs.view_profile')

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            # Now that profile has a PK, sync skills via form.save (without altering basic fields)
            form.instance = profile
            form.save(commit=False)
            messages.success(request, "Profile created successfully!")
            return redirect('jobs.view_profile')
    else:
        form = CandidateProfileForm()

    return render(request, "profiles/edit_profile.html", {"form": form})

@login_required
def view_profile(request):
    profile = get_object_or_404(CandidateProfile, user=request.user)
    educations = Education.objects.filter(profile=profile).order_by('-start_date')
    experiences = WorkExperience.objects.filter(profile=profile).order_by('-start_date')
    return render(request, "profiles/profile.html", {"profile": profile, "educations": educations, "experiences": experiences})

@login_required
def edit_profile(request):
    profile = get_object_or_404(CandidateProfile, user=request.user)

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('jobs.view_profile')
    else:
        form = CandidateProfileForm(instance=profile)

    return render(request, "profiles/edit_profile.html", {"form": form})


@login_required
def apply_to_job(request, id):
    # Redirect to canonical applications app route
    return redirect('applications.apply', job_id=id)

