from rest_framework.routers import DefaultRouter
from scheduler.views import SchedulerViewSet

router = DefaultRouter()
router.register(r"", SchedulerViewSet, basename="scheduler")

urlpatterns = router.urls
