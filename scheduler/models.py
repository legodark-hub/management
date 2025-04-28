from django.db import models

from users.models import CustomUser

# Create your models here.
class SchedulerEvent(models.Model):
    EVENT_TYPES = [
        ('task', 'Task'),
        ('meeting', 'Meeting'),
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_id = models.PositiveIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_date = models.DateTimeField()
    
    def __str__(self):
        return f'{self.get_event_type_display()} on {self.event_date}'
