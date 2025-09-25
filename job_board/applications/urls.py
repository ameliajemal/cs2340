from django.urls import path
from . import views

urlpatterns = [
    path("<int:job_id>/apply/", views.apply_to_job, name="applications.apply"),
    path("", views.my_applications, name="applications.my_applications"),
]
