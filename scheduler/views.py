from rest_framework import viewsets, permissions

from scheduler.models import SchedulerEvent
from scheduler.serializers import SchedulerEventSerializer


# Create your views here.
class SchedulerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchedulerEvent.objects.all()
    serializer_class = SchedulerEventSerializer
    permission_classes = [permissions.IsAuthenticated]
        
    def get_queryset(self):
        user = self.request.user
        queryset = SchedulerEvent.objects.filter(user=user)
        
        event_type = self.request.query_params.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
            
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(event_date__range=[start_date, end_date])
        
        return queryset