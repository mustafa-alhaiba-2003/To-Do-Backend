from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format='%Y-%m-%d', input_formats=None , read_only = True)
    due_date = serializers.DateTimeField(format='%Y-%m-%d', input_formats=None)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'start_date', 'due_date', 'priority'
        ]
        read_only_fields = ['id', 'start_date']
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'priority': {'required': False, 'default': 'medium'},
        }

class UserTaskSerializer(TaskSerializer):pass

