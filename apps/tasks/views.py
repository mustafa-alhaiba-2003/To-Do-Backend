from rest_framework import generics, permissions, status , viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .models import Task
from .serializers import TaskSerializer , UserTaskSerializer
from .pagination import CustomLimitOffsetPagination
from django.utils import timezone

class UserTaskDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        now = datetime.now()
        tasks = Task.objects.filter(user=user)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status="completed").count()
        in_progress_tasks = tasks.filter(status="in-progress").count()
        overdue_tasks = tasks.filter(due_date__lt=now, status="in-progress").count()

        recent_tasks = tasks.order_by('-start_date')[:5]
        recent_tasks_list = TaskSerializer(recent_tasks, many=True).data

        return Response({
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "overdue_tasks": overdue_tasks,
            "recent_tasks": recent_tasks_list
        }, status=status.HTTP_200_OK)


class UserTaskViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)    
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, 
            start_date=timezone.now()
        )

    def perform_update(self, serializer):
        serializer.save(
            user=self.request.user
        )