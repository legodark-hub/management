from djoser.serializers import UserCreateSerializer, UserSerializer

from users.models import CustomUser

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta): 
        model = CustomUser   
        fields = ('id', 'username', 'email', 'password', 'role', 'team')
        
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'team')
    