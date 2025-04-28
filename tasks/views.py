from django.shortcuts import render
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
        serializer.save(created_by=self.request.user)
        
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assigned_to=user) | Task.objects.filter(created_by=user)
    
    def perform_update(self, serializer):
        task = self.get_object()
        if self.request.user != task.created_by and self.request.user != task.assigned_to:
            raise PermissionDenied("Вы не можете редактировать данную задачу")    
        serializer.save()