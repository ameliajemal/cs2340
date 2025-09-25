from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]
    list_filter = ["role"]
    search_fields = ["user__username", "user__email"]


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profile"
    fk_name = "user"


def _ensure_groups():
    """Ensure our default groups exist so admin actions can assign them."""
    for g in ["Regular", "Moderator", "Admin"]:
        Group.objects.get_or_create(name=g)


@admin.action(description="Deactivate selected users")
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Reactivate selected users")
def reactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Assign role: Regular")
def make_regular(modeladmin, request, queryset):
    _ensure_groups()
    regular = Group.objects.get(name="Regular")
    moderator = Group.objects.get(name="Moderator")
    admin_g = Group.objects.get(name="Admin")
    for user in queryset:
        user.groups.remove(moderator, admin_g)
        user.groups.add(regular)


@admin.action(description="Assign role: Moderator")
def make_moderator(modeladmin, request, queryset):
    _ensure_groups()
    regular = Group.objects.get(name="Regular")
    moderator = Group.objects.get(name="Moderator")
    admin_g = Group.objects.get(name="Admin")
    for user in queryset:
        user.groups.remove(regular, admin_g)
        user.groups.add(moderator)


@admin.action(description="Assign role: Admin (group)")
def make_admin_group(modeladmin, request, queryset):
    _ensure_groups()
    regular = Group.objects.get(name="Regular")
    moderator = Group.objects.get(name="Moderator")
    admin_g = Group.objects.get(name="Admin")
    for user in queryset:
        user.groups.remove(regular, moderator)
        user.groups.add(admin_g)


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ("username", "email", "is_active", "is_staff", "display_groups", "display_account_role")
    actions = [deactivate_users, reactivate_users, make_regular, make_moderator, make_admin_group]

    def display_groups(self, obj):
        return ", ".join(obj.groups.values_list("name", flat=True)) or "—"
    display_groups.short_description = "Groups"

    def display_account_role(self, obj):
        try:
            return obj.userprofile.role
        except UserProfile.DoesNotExist:
            return "(none)"
    display_account_role.short_description = "Account Role"


# Re-register the User admin with our customization
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
