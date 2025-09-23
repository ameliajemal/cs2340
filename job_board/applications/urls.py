from django.urls import path
from . import views

urlpatterns = [
    # This URL is for applying to a specific job.
    # e.g., /applications/5/apply/
    path("<int:job_id>/apply/", views.apply_to_job, name="applications.apply"),
    # This URL is for viewing the current user's applications.
    # e.g., /applications/
    path("", views.my_applications, name="applications.my_applications"),
]
