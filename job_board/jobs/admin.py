from django.contrib import admin
from .models import Job, Skill


class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "job_type", "posted_at")
    list_filter = (
        "job_type",
        "is_remote",
        "provides_sponsorship",
        "company",
        "location",
    )
    search_fields = ("title", "company", "description")
    ordering = ["-posted_at"]


class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(Job, JobAdmin)
admin.site.register(Skill, SkillAdmin)
