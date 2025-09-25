from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="jobs.index"),
    path("<int:id>/", views.show, name="jobs.show"),
    path("create/", views.create, name="jobs.create"),
    path("manage/", views.manage, name="jobs.manage"),
    path("edit/<int:id>/", views.edit, name="jobs.edit"),
    path("delete/<int:id>/", views.delete, name="jobs.delete"),
]
