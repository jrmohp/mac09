from django.db import models

# Create your models here.
from django.db import models
from user.models import teamdata  # Import the teamdata model

class Checkin(models.Model):
    team = models.ForeignKey(teamdata, on_delete=models.CASCADE)  # ForeignKey to teamdata
    annexure1 = models.BooleanField(default=False)
    annexure2 = models.BooleanField(default=False)
    annexure3 = models.BooleanField(default=False)
    faculty_accompanied = models.BooleanField(default=False)
    team_members_present = models.IntegerField(default=0)
    check_in_time = models.DateTimeField(auto_now_add=True)
