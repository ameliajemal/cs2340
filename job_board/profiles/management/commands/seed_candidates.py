from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from jobs.models import Skill
from profiles.models import Profile, ProfileSkill, Project


class Command(BaseCommand):
    help = "Seed sample candidate profiles, skills, and projects for testing the recruiter search"

    def handle(self, *args, **options):
        # Ensure some skills exist
        skill_names = ["Python", "Django", "React", "SQL", "Java", "Mobile"]
        skills = {name: Skill.objects.get_or_create(name=name)[0] for name in skill_names}
        self.stdout.write(self.style.SUCCESS(f"Ensured skills: {', '.join(skills.keys())}"))

        # Create or update a few candidate users
        candidates = [
            {
                "username": "alice",
                "first_name": "Alice",
                "last_name": "Nguyen",
                "location": "Atlanta, GA",
                "headline": "CS student and Django enthusiast",
                "bio": "Built several course projects in Django and REST APIs.",
                "skills": ["Python", "Django", "SQL"],
                "projects": [
                    ("Campus Events App", "A Django app to list and RSVP campus events", ""),
                    ("Recipe API", "REST API using Django REST Framework and Postgres", ""),
                ],
            },
            {
                "username": "bob",
                "first_name": "Bob",
                "last_name": "Lee",
                "location": "Remote",
                "headline": "Frontend developer",
                "bio": "React and mobile web projects.",
                "skills": ["React", "Java", "Mobile"],
                "projects": [
                    ("Todo PWA", "Offline-first PWA built with React", ""),
                    ("Campus Maps", "Mobile-friendly maps with routing", ""),
                ],
            },
        ]

        for cand in candidates:
            user, _ = User.objects.get_or_create(
                username=cand["username"],
                defaults={"first_name": cand["first_name"], "last_name": cand["last_name"]},
            )
            # ensure applicant role
            UserProfile.objects.get_or_create(user=user, defaults={"role": "applicant"})

            profile, _ = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "headline": cand["headline"],
                    "bio": cand["bio"],
                    "location": cand["location"],
                },
            )
            # Update details on repeated runs
            profile.headline = cand["headline"]
            profile.bio = cand["bio"]
            profile.location = cand["location"]
            profile.save()

            # Attach skills (clear then add)
            ProfileSkill.objects.filter(profile=profile).delete()
            for s in cand["skills"]:
                ProfileSkill.objects.create(profile=profile, skill=skills[s])

            # Seed projects (clear then add)
            profile.projects.all().delete()
            for name, desc, url in cand["projects"]:
                Project.objects.create(profile=profile, name=name, description=desc, url=url)

        self.stdout.write(self.style.SUCCESS("Seeded sample candidates successfully."))