from rest_framework import viewsets, permissions

from motivation.models import TaskEvaluation
from motivation.serializers import TaskEvaluationSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

class TaskEvaluationViewSet(viewsets.ModelViewSet):
    queryset = TaskEvaluation.objects.all()
    serializer_class = TaskEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        if task.created_by != self.request.user:
            raise PermissionDenied("Вы не можете оценить данную задачу")
        serializer.save(evaluator=self.request.user)
        
    def perform_update(self, serializer):
        evaluation = self.get_object()
        if evaluation.evaluator != self.request.user:
            raise PermissionDenied("Вы не можете редактировать данную оценку")
        serializer.save()
        
    def get_queryset(self):
        if self.request.user.role == "manager":
            return TaskEvaluation.objects.filter(evaluator=self.request.user)
        if self.request.user.role == "employee":
            return TaskEvaluation.objects.filter(task__assigned_to=self.request.user)
        return TaskEvaluation.objects.none()

    @action(detail=False, methods=["get"], url_path="average-score")
    def average_score(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        evaluations = self.get_queryset()
        if start_date and end_date:
            evaluations = evaluations.filter(created_at__range=[start_date, end_date])

        total_score = 0
        count = evaluations.count()

        for evaluation in evaluations:
            total_score += (
                evaluation.timeliness + evaluation.quality + evaluation.completeness
            ) / 3

        average_score = total_score / count if count > 0 else 0
        return Response({"average_score": round(average_score, 2)})