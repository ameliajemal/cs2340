from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Create test users with different roles'

    def handle(self, *args, **options):
        # Create test applicant
        applicant_user, created = User.objects.get_or_create(
            username='test_applicant',
            defaults={'email': 'applicant@test.com'}
        )
        if created:
            applicant_user.set_password('testpass123')
            applicant_user.save()
            UserProfile.objects.create(user=applicant_user, role='applicant')
            self.stdout.write(self.style.SUCCESS('Created test applicant user'))
        else:
            self.stdout.write(self.style.WARNING('Test applicant user already exists'))

        # Create test recruiter
        recruiter_user, created = User.objects.get_or_create(
            username='test_recruiter',
            defaults={'email': 'recruiter@test.com'}
        )
        if created:
            recruiter_user.set_password('testpass123')
            recruiter_user.save()
            UserProfile.objects.create(user=recruiter_user, role='recruiter')
            self.stdout.write(self.style.SUCCESS('Created test recruiter user'))
        else:
            self.stdout.write(self.style.WARNING('Test recruiter user already exists'))

        self.stdout.write(self.style.SUCCESS('Test users created successfully!'))
        self.stdout.write('Applicant: test_applicant / testpass123')
        self.stdout.write('Recruiter: test_recruiter / testpass123')
