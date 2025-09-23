from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.title + " - " + self.user.username
