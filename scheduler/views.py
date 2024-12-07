from rest_framework import viewsets, permissions

from scheduler.models import SchedulerEvent
from scheduler.serializers import SchedulerEventSerializer


# Create your views here.
class SchedulerViewSet(viewsets.ModelViewSet):
    queryset = SchedulerEvent.objects.all()
    serializer_class = SchedulerEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        user = self.request.user
        return SchedulerEvent.objects.filter(user=user)