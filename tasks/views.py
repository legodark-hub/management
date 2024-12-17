from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from tasks.models import Task
from .serializers import TaskSerializer


# Create your views here.
class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Перед созданием задачи проверяет, что текущий пользователь является
        менеджером и что участник, на которого назначается задача, находится
        в команде, которой управляет менеджер. Если не так, то выбрасывает
        исключение PermissionDenied.
        """        
        if self.request.user.role != "manager":
            raise PermissionDenied("Вы не являетесь менеджером")

        assigned_to = serializer.validated_data.get("assigned_to")
        if assigned_to.team.admin != self.request.user:
            raise PermissionDenied(
                "Вы не можете назначить данную задачу участнику другой команды"
            )
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """
        Возвращает набор задач в зависимости от роли пользователя.

        Если пользователь - менеджер, возвращаются задачи, созданные им.
        Если пользователь - сотрудник, возвращаются задачи, на которые он назначен.
        В противном случае возвращается пустой набор задач.
        """
        user = self.request.user
        if user.role == "manager":
            return Task.objects.filter(created_by=user)
        if user.role == "employee":
            return Task.objects.filter(assigned_to=user)
        return Task.objects.none()

    def perform_update(self, serializer):
        """
        Перед обновлением задачи проверяет, что текущий пользователь является
        создателем задачи. Если не так, то выбрасывает исключение PermissionDenied.
        """
        task = self.get_object()
        if self.request.user != task.created_by:
            raise PermissionDenied("Вы не можете редактировать данную задачу")
        serializer.save()
        
    def partial_update(self, request, *args, **kwargs):
        """
        Частичное обновление задачи.

        Позволяeт менеджеру обновлять любые поля задачи, а сотруднику - только поле 'status'.
        """
        task = self.get_object()
        if self.request.user != task.assigned_to:
            if 'status' in request.data:
                return super().partial_update(request, *args, **kwargs)
            else:
                raise PermissionDenied(
                    "Сотрудник может изменять только статус своей задачи."
                )
        return super().partial_update(request, *args, **kwargs)
        
    def perform_destroy(self, instance):
        """
        Перед удалением задачи проверяет, что текущий пользователь является
        создателем задачи. Если не так, то выбрасывает исключение PermissionDenied.
        """
        if self.request.user != instance.created_by:
            raise PermissionDenied("Вы не можете удалить данную задачу")
        instance.delete()
