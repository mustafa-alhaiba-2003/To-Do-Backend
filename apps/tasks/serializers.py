from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format='%Y-%m-%d', input_formats=None)
    due_date = serializers.DateTimeField(format='%Y-%m-%d', input_formats=None)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'start_date', 'due_date', 'priority'
        ]
        read_only_fields = ['id', 'start_date']