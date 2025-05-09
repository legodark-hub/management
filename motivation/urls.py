from rest_framework.routers import DefaultRouter

from motivation.views import TaskEvaluationViewSet

router = DefaultRouter()
router.register(r"", TaskEvaluationViewSet, basename="evaluation")

urlpatterns = router.urls