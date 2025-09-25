from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import Application


@login_required
def apply_to_job(request, job_id):
    job = Job.objects.get(id=job_id)
    application, created = Application.objects.get_or_create(
        job=job, user=request.user
    )
    return redirect("jobs.show", id=job_id)


@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user)
    template_data = {"title": "My Applications", "applications": applications}
    return render(
        request, "applications/my_applications.html", {"template_data": template_data}
    )
