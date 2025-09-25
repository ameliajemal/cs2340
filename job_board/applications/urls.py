from django.urls import path
from . import views

urlpatterns = [
    path("<int:job_id>/apply/", views.apply_to_job, name="applications.apply"),
    path("", views.my_applications, name="applications.my_applications"),
    path("pipeline/<int:job_id>/", views.pipeline, name="applications.pipeline"),
    path("update-stage/<int:application_id>/", views.update_application_stage, name="applications.update_stage"),
    path("update-notes/<int:application_id>/", views.update_application_notes, name="applications.update_notes"),
]
