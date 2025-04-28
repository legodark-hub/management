from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from scheduler.models import SchedulerEvent
from .models import Meeting


@receiver(post_save, sender=Meeting)
def create_scheduler_event_for_meeting(sender, instance, created, **kwargs):
    if created:
        SchedulerEvent.objects.create(
            event_type="meeting",
            event_id=instance.id,
            user=instance.created_by,
            event_date=instance.scheduled_at,
        )


@receiver(m2m_changed, sender=Meeting.participants.through)
def create_calendar_events_for_participants(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for participant_id in pk_set:
            participant = instance.participants.model.objects.get(id=participant_id)
            SchedulerEvent.objects.create(
                event_type="meeting",
                event_id=instance.id,
                user=participant,
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
    SchedulerEvent.objects.filter(event_type="meeting", event_id=instance.id).delete()
