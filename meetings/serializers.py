from rest_framework import serializers
from meetings.models import Meeting
from users.models import CustomUser
from django.utils import timezone


class MeetingSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    participant_usernames = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username", source="participants"
    )

    class Meta:
        model = Meeting
        fields = [
            "id",
            "title",
            "description",
            "scheduled_at",
            "created_by",
            "created_by_username",
            "participants",
            "participant_usernames",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def validate_scheduled_at(self, value):
        """
        Проверяет, что запланированная встреча не в прошлом. Иначе выбрасывает исключение ValidationError.
        """
        if value < timezone.now():
            raise serializers.ValidationError(
                "Встреча не может быть запланирована в прошлом."
            )
        return value

    def validate(self, data):        
        """
        Проверяет, что запланированное время встречи не пересекается с другим событием
        для каждого участника. Если участник уже занят в это время, выбрасывает исключение ValidationError.
        """

        participants = self.initial_data.get("participants", [])
        for participant_id in participants:
            participant = CustomUser.objects.get(id=participant_id)
            if Meeting.objects.filter(
                participants=participant, scheduled_at=data["scheduled_at"]
            ).exists():
                raise serializers.ValidationError(
                    f"Пользователь {participant.username} уже занят в это время."
                )
        return data
