from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from jobs.models import Job
from .models import Application
import json
from .forms import ApplicationForm


@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Prevent duplicate applications
    if Application.objects.filter(job=job, user=request.user).exists():
        messages.info(request, 'You have already applied to this job.')
        return redirect("jobs.show", id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.stage = 'applied'
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect("applications.my_applications")
    else:
        form = ApplicationForm()

    return render(request, "applications/apply.html", {"form": form, "job": job})


@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).select_related('job').order_by('-date_applied')
    return render(request, "applications/my_applications.html", {
        "title": "My Applications",
        "applications": applications
    })


@login_required
def pipeline(request, job_id):
    """Kanban board view for managing applications for a specific job"""
    job = get_object_or_404(Job, id=job_id)

    # Check if user is the recruiter for this job
    if not (job.recruiter == request.user or request.user.is_superuser):
        messages.error(request, 'You do not have permission to view this pipeline.')
        return redirect('jobs.index')

    # Define the 5 stages we want (Rejected first, then Applied, etc.)
    STAGES = [
        ('rejected', 'Rejected'),
        ('applied', 'Applied'),
        ('review', 'Under Review'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
    ]

    # Get all applications for this job, grouped by stage
    applications_by_stage = {}
    for stage_code, stage_name in STAGES:
        applications_by_stage[stage_code] = {
            'name': stage_name,
            'applications': Application.objects.filter(job=job, stage=stage_code).order_by('-date_applied')
        }

    return render(request, "applications/pipeline.html", {
        "template_data": {
            "title": f"Pipeline - {job.title}",
            "job": job,
            "applications_by_stage": applications_by_stage,
            "stage_choices": STAGES
        }
    })


@login_required
@csrf_exempt
@require_POST
def update_application_stage(request, application_id):
    """Update application stage via AJAX"""
    try:
        application = get_object_or_404(Application, id=application_id)

        # Check if user is the recruiter for this job
        if not (application.job.recruiter == request.user or request.user.is_superuser):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = json.loads(request.body)
        new_stage = data.get('stage')

        # Define allowed stages
        ALLOWED_STAGES = ['rejected', 'applied', 'review', 'interview', 'offer']

        if new_stage not in ALLOWED_STAGES:
            return JsonResponse({'error': 'Invalid stage'}, status=400)

        application.stage = new_stage
        application.save()

        return JsonResponse({
            'success': True,
            'stage': new_stage,
            'stage_display': application.get_stage_display()
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_POST
def update_application_notes(request, application_id):
    """Update application notes via AJAX"""
    try:
        application = get_object_or_404(Application, id=application_id)

        # Check if user is the recruiter for this job
        if not (application.job.recruiter == request.user or request.user.is_superuser):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = json.loads(request.body)
        notes = data.get('notes', '')

        application.notes = notes
        application.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
