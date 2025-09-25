from django.contrib import admin
from .models import Profile, ProfileSkill, Project, Education, WorkExperience


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "headline", "location")
    search_fields = ("user__username", "user__first_name", "user__last_name", "location")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "profile")
    search_fields = ("name", "description", "profile__user__username")


admin.site.register(ProfileSkill)
admin.site.register(Education)
admin.site.register(WorkExperience)