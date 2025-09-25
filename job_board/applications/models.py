from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Application(models.Model):
    STAGE_CHOICES = [
        ('rejected', 'Rejected'),
        ('applied', 'Applied'),
        ('review', 'Under Review'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
    ]
    
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='applied')
    notes = models.TextField(blank=True, null=True, help_text="Internal notes for recruiters")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job.title + " - " + self.user.username
