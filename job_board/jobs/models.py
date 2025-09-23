from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    JOB_TYPE_CHOICES = [
        (FULL_TIME, "Full-Time"),
        (PART_TIME, "Part-Time"),
        (CONTRACT, "Contract"),
        (INTERNSHIP, "Internship"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)

    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE_CHOICES, default=FULL_TIME
    )
    salary_min = models.PositiveIntegerField(
        null=True, blank=True, help_text="Minimum yearly salary in USD"
    )
    salary_max = models.PositiveIntegerField(
        null=True, blank=True, help_text="Maximum yearly salary in USD"
    )
    is_remote = models.BooleanField(
        default=False, help_text="Is this a fully remote position?"
    )
    provides_sponsorship = models.BooleanField(
        default=False, help_text="Does this position offer visa sponsorship?"
    )

    skills = models.ManyToManyField(Skill, blank=True)

    # Timestamps
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
