from rest_framework import viewsets, permissions
from meetings.models import Meeting
from meetings.serializers import MeetingSerializer
from django.db import models


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(
            models.Q(participants=user) | models.Q(created_by=user)
        ).distinct()
