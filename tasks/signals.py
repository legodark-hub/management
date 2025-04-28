from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from scheduler.models import SchedulerEvent
from tasks.models import Task



@receiver(post_save, sender=Task)
def create_scheduler_event_for_task(sender, instance, created, **kwargs):
    if created:
        print(f"CREATED {instance}")
        SchedulerEvent.objects.create(
            event_type="task",
            event_id=instance.id,
            user=instance.assigned_to,
            event_date=instance.deadline,
        )


@receiver(post_save, sender=Task)
def update_scheduler_event_for_task(sender, instance, created, **kwargs):
    if not created:
        SchedulerEvent.objects.filter(event_type="task", event_id=instance.id).update(
            event_date=instance.deadline
        )


@receiver(post_delete, sender=Task)
def delete_scheduler_event_for_task(sender, instance, **kwargs):
        SchedulerEvent.objects.filter(event_type="task", event_id=instance.id).delete()
