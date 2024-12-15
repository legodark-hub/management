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
        if self.request.user.role != "manager":
            raise PermissionDenied("Вы не являетесь менеджером")
        participants = serializer.validated_data.get("participants")
        for participant in participants:
            if participant.team != self.request.user.team:
                raise PermissionDenied(
                    "Вы не можете назначить данную встречу участнику другой команды"
                )
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == "manager":
            return Meeting.objects.filter(created_by=user)
        if user.role == "employee":
            return Meeting.objects.filter(assigned_to=user)
        return Meeting.objects.none()

    def perform_update(self, serializer):
        meeting = self.get_object()
        if self.request.user != meeting.created_by:
            raise PermissionDenied("Вы не можете редактировать данную встречу")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.created_by:
            raise PermissionDenied("Вы не можете удалить данную встречу")
        instance.delete()
