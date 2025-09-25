from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="jobs.index"),
    path("<int:id>/", views.show, name="jobs.show"),
    path("create/", views.create, name="jobs.create"),
    path("manage/", views.manage, name="jobs.manage"),
    path("edit/<int:id>/", views.edit, name="jobs.edit"),
    path("delete/<int:id>/", views.delete, name="jobs.delete"),
    path("profile/create/", views.create_profile, name="jobs.create_profile"),
    path("profile/", views.view_profile, name="jobs.view_profile"),
    path("profile/edit/", views.edit_profile, name="jobs.edit_profile"),
    path("<int:id>/apply/", views.apply_to_job, name="jobs.apply"),
]
