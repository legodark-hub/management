from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    assigned_to_username = serializers.CharField(
        source="assigned_to.username", read_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "assigned_to",
            "created_by",
            "deadline",
            "created_at",
            "updated_at",
            "created_by_username",
            "assigned_to_username",
        ]
        read_only_fields = ["created_by" ,"created_at", "updated_at"]
