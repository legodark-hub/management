from rest_framework import serializers

from motivation.models import TaskEvaluation

class TaskEvaluationSerializer(serializers.ModelSerializer):
    evaluator_username = serializers.CharField(source='evaluator.username', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    score = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    
    class Meta:
        model = TaskEvaluation
        fields = [
            'id',
            'task',
            'task_title',
            'evaluator',
            'evaluator_username',
            'score',
            'timeliness',
            'quality',
            'completeness',
            'comments',
            'created_at',
        ]
        read_only_fields = ['evaluator', 'created_at', 'score']
        
        def validate_timeliness(self, value):
            if value < 1 or value > 10:
                raise serializers.ValidationError("Timeliness must be between 1 and 10")
            return value
        
        def validate_quality(self, value):
            if value < 1 or value > 10:
                raise serializers.ValidationError("Quality must be between 1 and 10")
            return value
        
        def validate_completeness(self, value):
            if value < 1 or value > 10:
                raise serializers.ValidationError("Completeness must be between 1 and 10")
            return value