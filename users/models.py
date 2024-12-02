from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=50,
        choices=[("admin", "Admin"), ("manager", "Manager"), ("employee", "Employee")],
    )
    team = models.CharField(max_length=50, null=True)
    
    REQUIRED_FIELDS = ["email"]
    
    def __str__(self):
        return self.username