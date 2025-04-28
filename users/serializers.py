from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from teams.models import Team
from users.models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    invitation_code = serializers.UUIDField(required=False, write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ["id", "username", "email", "password", "invitation_code"]

    def validate_invitation_code(self, value):
        """
        Проверяет, что указанный код приглашения соответствует существующей команде.
        Если команда не существует, выбрасывает исключение ValidationError.
        """
        if not Team.objects.filter(invitation_code=value).exists():
            raise serializers.ValidationError("Неверный код приглашения")
        return value

    def validate(self, attrs):
        """
        Если пользователь передал код приглашения, то он
        добаляется в словарь validated_data. Если код приглашения
        не существует, выбрасывает исключение ValidationError.
        """
        invitation_code = attrs.pop("invitation_code", None)
        if invitation_code:
            if not Team.objects.filter(invitation_code=invitation_code).exists():
                raise serializers.ValidationError("Неверный код приглашения")
            attrs["team"] = Team.objects.get(invitation_code=invitation_code)
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ("id", "username", "email", "role", "team")
        
class RoleChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["role"]
        
    def validate_role(self, value):
        """
        Проверяет, что указанная роль является корректной.
        Если роль не является корректной, выбрасывает исключение ValidationError.
        """
        if value not in ["manager", "employee"]:
            raise serializers.ValidationError("Неправильная роль")
        return value
