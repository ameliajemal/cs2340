from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'stage', 'date_applied', 'updated_at')
    list_filter = ('stage', 'date_applied', 'job__company')
    search_fields = ('user__username', 'job__title', 'job__company')
    readonly_fields = ('date_applied', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('job', 'user', 'stage')
        }),
        ('Additional Information', {
            'fields': ('notes', 'date_applied', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
