from django.db import models
from users.models import CustomUser


# Create your models here.
class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scheduled_at = models.DateTimeField()  # Время проведения встречи
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="created_meetings",
    )
    participants = models.ManyToManyField(CustomUser, related_name="meetings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meeting: {self.title} at {self.scheduled_at}"
