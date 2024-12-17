from rest_framework import viewsets, permissions
from meetings.models import Meeting
from meetings.serializers import MeetingSerializer
from django.db import models
from rest_framework.exceptions import PermissionDenied


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Перед созданием объекта встречи проверяет, что текущий пользователь является менеджером и
        что все участники встречи из одной команды. Если не так, то выбрасывает исключение PermissionDenied.
        """
        
        if self.request.user.role != "manager":
            raise PermissionDenied("Вы не являетесь менеджером")
        participants = serializer.validated_data.get("participants")
        for participant in participants:
            if participant.team.admin != self.request.user:
                raise PermissionDenied(
                    "Вы не можете назначить данную встречу участнику другой команды"
                )
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """
        Возвращает набор запросов встреч в зависимости от роли пользователя.

        Если пользователь — менеджер, возвращаются встречи, созданные им.
        Если пользователь — сотрудник, возвращаются встречи, на которые он назначен.
        В противном случае возвращается пустой набор запросов.
        """
        user = self.request.user
        if user.role == "manager":
            return Meeting.objects.filter(created_by=user)
        if user.role == "employee":
            return Meeting.objects.filter(assigned_to=user)
        return Meeting.objects.none()

    def perform_update(self, serializer):
        """
        Перед обновлением объекта встречи проверяет, что текущий пользователь является
        создателем этой встречи. Если не так, то выбрасывает исключение PermissionDenied.
        """
        meeting = self.get_object()
        if self.request.user != meeting.created_by:
            raise PermissionDenied("Вы не можете редактировать данную встречу")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Перед удалением объекта встречи проверяет, что текущий пользователь является
        создателем этой встречи. Если не так, то выбрасывает исключение PermissionDenied.
        """
        if self.request.user != instance.created_by:
            raise PermissionDenied("Вы не можете удалить данную встречу")
        instance.delete()
