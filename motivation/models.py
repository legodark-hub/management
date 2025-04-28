from django.db import models

from tasks.models import Task
from users.models import CustomUser

# Create your models here.
class TaskEvaluation(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='evaluation')
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='evaluated_tasks')
    timeliness = models.PositiveSmallIntegerField()
    quality = models.PositiveSmallIntegerField()
    completeness = models.PositiveSmallIntegerField()
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def score(self):
        return (self.timeliness + self.quality + self.completeness) / 3
            
    def __str__(self):
        return f"Evaluation for task {self.task.title} by {self.evaluator.username}"