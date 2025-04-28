from tasks.views import TasksViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"", TasksViewSet, basename="task")

urlpatterns = router.urls
