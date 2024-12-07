from django.db import models

from tasks.models import Task
from users.models import CustomUser

# Create your models here.
class SchedulerEvent(models.Model):
    event_type = models.CharField(max_length=50, choices=[('task', 'Task')])
    event_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='scheduler_events')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_date = models.DateTimeField()
    
    def __str__(self):
        return f'Event for task {self.event_id.title} on {self.event_date}'
