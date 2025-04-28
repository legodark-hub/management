from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from teams.models import Team
from users.models import CustomUser

class CustomUserCreateSerializer(UserCreateSerializer):
    invitation_code = serializers.UUIDField(required=False, write_only=True)
    
    class Meta(UserCreateSerializer.Meta): 
        model = CustomUser   
        fields = ['id', 'username', 'email', 'password', 'role', 'invitation_code']
        
    def validate_invitation_code(self, value):
        print(f"VALIDATION {value}")
        if not Team.objects.filter(invitation_code=value).exists():
                raise serializers.ValidationError("Неверный код приглашения")
        return value
    
    def perform_create(self, validated_data):
        print(f"PERFORM CREATE {validated_data}")
        invitation_code = validated_data.pop('invitation_code', None)
        user = CustomUser.objects.create_user(**validated_data)
        if invitation_code:
            team = Team.objects.get(invitation_code=invitation_code)
            user.team = team
            user.save()
        return user
    
    def validate(self, attrs):
        invitation_code = attrs.pop('invitation_code', None)
        if invitation_code:
            if not Team.objects.filter(invitation_code=invitation_code).exists():
                raise serializers.ValidationError("Неверный код приглашения")
            attrs['team'] = Team.objects.get(invitation_code=invitation_code)
        return attrs
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    # def create(self, validated_data):
    #     print(f"CREATE {validated_data}")
    #     invitation_code = validated_data.pop('invitation_code', None)
    #     user = super().create(validated_data)
    #     if invitation_code:
    #         team = Team.objects.get(invitation_code=invitation_code)
    #         user.team = team
    #         user.save()
    #     return user
        
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'team')
    