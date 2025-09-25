from django.shortcuts import render
from django.db.models import Q
from .models import Profile
from .forms import CandidateSearchForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import UserProfile


@login_required
def search_candidates(request):
    template_data = {"title": "Search Candidates"}

    # Only recruiters can access this view
    try:
        if request.user.userprofile.role != "recruiter":
            return HttpResponseForbidden("Only recruiters can search candidates.")
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden("Only recruiters can search candidates.")

    form = CandidateSearchForm(request.GET or None)
    profiles = Profile.objects.select_related("user").prefetch_related(
        "profileskill_set__skill", "projects"
    )

    if form.is_valid():
        skills = form.cleaned_data.get("skills")
        location = form.cleaned_data.get("location")
        project_keywords = form.cleaned_data.get("project_keywords")

        if skills and skills.exists():
            profiles = profiles.filter(profileskill__skill__in=skills)

        if location:
            profiles = profiles.filter(location__icontains=location)

        if project_keywords:
            kw = project_keywords
            profiles = profiles.filter(
                Q(projects__name__icontains=kw) |
                Q(projects__description__icontains=kw) |
                Q(projects_text__icontains=kw)  # free-text projects field on Profile
            )

        profiles = profiles.distinct()

    context = {
        "template_data": template_data,
        "form": form,
        "profiles": profiles,
    }

    return render(request, "profiles/search.html", context)

