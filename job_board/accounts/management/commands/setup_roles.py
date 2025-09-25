from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

from jobs.models import Job
from applications.models import Application
from profiles.models import Profile, Project


class Command(BaseCommand):
    help = "Create default Groups (Regular, Moderator, Admin) and assign sensible permissions. Optionally creates a demo admin user."

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-demo-admin",
            action="store_true",
            help="Create a demo site admin account (username: site_admin, password: admin123)",
        )

    def handle(self, *args, **options):
        # Ensure groups
        regular_group, _ = Group.objects.get_or_create(name="Regular")
        moderator_group, _ = Group.objects.get_or_create(name="Moderator")
        admin_group, _ = Group.objects.get_or_create(name="Admin")

        # Resolve content types
        job_ct = ContentType.objects.get_for_model(Job)
        app_ct = ContentType.objects.get_for_model(Application)
        profile_ct = ContentType.objects.get_for_model(Profile)
        project_ct = ContentType.objects.get_for_model(Project)

        # Helper to fetch perms by codename
        def perms(ct, codenames):
            return list(Permission.objects.filter(content_type=ct, codename__in=codenames))

        # Regular: no additional perms beyond defaults (authenticated behavior)
        regular_perms = []
        regular_group.permissions.set(regular_perms)

        # Moderator: can view and delete Applications (e.g., remove abusive content), and view Profiles/Projects
        moderator_perms = []
        moderator_perms += perms(app_ct, ["view_application", "change_application", "delete_application"])  # moderate applications
        moderator_perms += perms(profile_ct, ["view_profile"])  # view candidate profiles in admin
        moderator_perms += perms(project_ct, ["view_project"])  # view candidate projects in admin
        moderator_group.permissions.set(moderator_perms)

        # Admin group: broad management of jobs, applications, profiles/projects
        admin_perms = []
        admin_perms += perms(job_ct, ["add_job", "change_job", "delete_job", "view_job"])
        admin_perms += perms(app_ct, ["add_application", "change_application", "delete_application", "view_application"])
        admin_perms += perms(profile_ct, ["add_profile", "change_profile", "delete_profile", "view_profile"])
        admin_perms += perms(project_ct, ["add_project", "change_project", "delete_project", "view_project"])
        admin_group.permissions.set(admin_perms)

        self.stdout.write(self.style.SUCCESS("Groups and permissions configured: Regular, Moderator, Admin."))

        if options.get("with_demo_admin"):
            user, created = User.objects.get_or_create(username="site_admin", defaults={"email": "admin@example.com"})
            if created:
                user.set_password("admin123")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS("Demo admin created: site_admin / admin123"))
        else:
            self.stdout.write("Tip: run with --with-demo-admin to create a demo superuser as well.")
