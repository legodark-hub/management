from scheduler.models import SchedulerEvent
from rest_framework import serializers


class SchedulerEventSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source="event_id.title", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = SchedulerEvent
        fields = [
            "id",
            "task_title",
            "event_date",
            "user",
            "user_username",
            "event_type",
            "event_id",
        ]
        read_only_fields = ["user", "user_username"]
