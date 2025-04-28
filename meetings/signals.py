from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from scheduler.models import SchedulerEvent
from .models import Meeting


@receiver(post_save, sender=Meeting)
def create_scheduler_event_for_meeting(sender, instance, created, **kwargs):
    if created:
        for participant in instance.participants.all():
            SchedulerEvent.objects.create(
                event_type="meeting",
                event_id=instance.id,
                user=participant,
                event_date=instance.scheduled_at,
            )
        SchedulerEvent.objects.create(
            event_type="meeting",
            event_id=instance.id,
            user=instance.created_by,
            event_date=instance.scheduled_at,
        )


@receiver(post_save, sender=Meeting)
def update_scheduler_event_for_meeting(sender, instance, created, **kwargs):
    if not created:
        SchedulerEvent.objects.filter(
            event_type="meeting", event_id=instance.id
        ).update(event_date=instance.scheduled_at)


@receiver(post_delete, sender=Meeting)
def delete_scheduler_event_for_meeting(sender, instance, **kwargs):
        SchedulerEvent.objects.filter(
            event_type="meeting", event_id=instance.id
        ).delete()
