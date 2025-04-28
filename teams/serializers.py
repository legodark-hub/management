from rest_framework import serializers

from teams.models import Team
from users.models import CustomUser

class TeamSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin.username', read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'admin', 'admin_username', 'invitation_code', 'created_at']
        read_only_fields = ['admin', 'created_at']
        
class AddUserToTeamSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, email):
        """
        Проверяет, что указанный email соответствует существующему пользователю.
        Если пользователь не существует, выбрасывает исключение ValidationError.
        """
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        return email
    
    def add_user(self, team, email):
        """
        Добавляет пользователя в указанную команду, если он еще не состоит в другой.

        Если пользователь уже состоит в команде, выбрасывает исключение ValidationError.
        В противном случае, назначает пользователя в указанную команду и сохраняет изменения.
        """

        user = CustomUser.objects.get(email=email)
        if user.team:
            raise serializers.ValidationError("Пользователь уже в команде")
        user.team = team
        user.save()
        return user