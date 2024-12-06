import uuid
from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    admin = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='admin_team')
    created_at = models.DateTimeField(auto_now_add=True)
    invitation_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.name
