from meetings.models import Meeting
from scheduler.models import SchedulerEvent
from rest_framework import serializers

from tasks.models import Task


class SchedulerEventSerializer(serializers.ModelSerializer):
    # task_title = serializers.CharField(source="event_id.title", read_only=True)
    event_type_display = serializers.CharField(
        source="get_event_type_display", read_only=True
    )
    task = serializers.SerializerMethodField()
    meeting = serializers.SerializerMethodField()
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = SchedulerEvent
        fields = [
            "id",
            "event_type",
            "event_type_display",
            "event_date",
            "task",
            "meeting",
            "user",
            "user_username",
            "event_type",
            "event_id",
        ]
        read_only_fields = [
            "event_type_display",
            "task",
            "meeting",
            "user",
            "user_username",
        ]

    def get_task(self, obj):
        if obj.event_type == 'task':
            task = Task.objects.filter(id=obj.event_id).first()
            return {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "deadline": task.deadline
            } if task else None
        return None

    def get_meeting(self, obj):
        if obj.event_type == 'meeting':
            meeting = Meeting.objects.filter(id=obj.event_id).first()
            return {
                "id": meeting.id,
                "title": meeting.title,
                "description": meeting.description,
                "scheduled_at": meeting.scheduled_at
            } if meeting else None
        return None
