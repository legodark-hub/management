from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from teams.models import Team
from teams.serializers import AddUserToTeamSerializer, TeamSerializer
from users.models import CustomUser


# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Перед созданием команды проверяет, что текущий пользователь является менеджером.
        Если не так, то выбрасывает исключение PermissionDenied.
        """

        if self.request.user.role != "manager":
            raise PermissionDenied("Вы не являетесь менеджером")
        serializer.save(admin=self.request.user)

    def get_queryset(self):
        """
        Возвращает набор объектов Team, которые текущий пользователь может видеть.
        Если текущий пользователь является суперпользователем, возвращает все команды.
        В противном случае возвращает только команды, в которых текущий пользователь является администратором.
        """
        if self.request.user.is_superuser:
            return Team.objects.all()
        return Team.objects.filter(admin=self.request.user)

    def perform_update(self, serializer):
        """
        Перед обновлением информации о команде проверяет, что текущий пользователь является
        администратором команды. Если не так, то выбрасывает исключение PermissionDenied.
        """
        if self.request.user != serializer.instance.admin:
            raise PermissionDenied("Вы не являетесь администратором данной команды")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Перед удалением команды проверяет, что текущий пользователь является
        администратором команды. Если не так, то выбрасывает исключение PermissionDenied.
        """
        if self.request.user != instance.admin:
            raise PermissionDenied("Вы не являетесь администратором данной команды")
        instance.delete()
        
    @action(
        detail=True,
        methods=["get"],
        url_path="members",
    )
    def get_members(self, request, pk=None):
        """
        Возвращает список участников команды в виде JSON-ответа.

        Для вызова этого метода необходимо, чтобы текущий пользователь
        был аутентифицирован. Метод возвращает список словарей, где каждый
        словарь содержит информацию об одном участнике команды, включая
        идентификатор, имя пользователя, email и роль.
        """

        team = self.get_object()
        members = team.members.all()
        members_data = [
            {
                "id": member.id,
                "username": member.username,
                "email": member.email, 
                "role": member.role,
            }
            for member in members
        ]
        return Response({
            "members": members_data,
        })

    @action(
        detail=True,
        methods=["post"],
        url_path="add-user",
        permission_classes=[permissions.IsAuthenticated],
    )
    def add_user(self, request, pk=None):
        """
        Добавляет пользователя в указанную команду.

        Для вызова этого метода необходимо, чтобы текущий пользователь
        был аутентифицирован и являлся администратором команды. Метод
        возвращает ответ в формате JSON, содержащий сообщение о
        результате операции.
        """
        team = self.get_object()
        if request.user != team.admin:
            raise PermissionDenied("Вы не являетесь администратором данной команды")
        serializer = AddUserToTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.add_user(team, serializer.validated_data["email"])
        return Response(
            {
                "message": f"Пользователь {user.email} успешно добавлен в команду {team.name}"
            }
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path="remove-user/(?P<user_id>[^/.]+)",
        permission_classes=[permissions.IsAuthenticated],
    )
    def remove_user(self, request, pk=None, user_id=None):
        """
        Удаляет пользователя из указанной команды.

        Для вызова этого метода необходимо, чтобы текущий пользователь
        был аутентифицирован и являлся администратором команды.
        Метод возвращает ответ в формате JSON, содержащий сообщение о
        результате операции.
        """
        team = self.get_object()
        if request.user != team.admin:
            raise PermissionDenied("Вы не являетесь администратором данной команды")
        try:
            user = CustomUser.objects.get(id=user_id, team=team)
            user.team = None    
            user.save()
            return Response({"message": f"Пользователь {user.email} успешно удален из команды {team.name}"})
        except CustomUser.DoesNotExist:
            raise PermissionDenied("Пользователь не найден в данной команде")