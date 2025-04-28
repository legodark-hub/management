from django.contrib.auth.models import AbstractUser
from django.db import models

from teams.models import Team


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=50,
        choices=[("admin", "Admin"), ("manager", "Manager"), ("employee", "Employee")],
        default="employee",
    )
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    
    REQUIRED_FIELDS = ["email"]
    
    def __str__(self):
        return self.username