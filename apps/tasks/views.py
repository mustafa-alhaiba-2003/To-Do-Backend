
from django.db.models import Case, When, IntegerField
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import Task
from .serializers import UserTaskSerializer
from .filtres import TaskFilter

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
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomLimitOffsetPagination

    # Search + Filter + Ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter

    # DRF search (?search=...)
    search_fields = ["title", "description"]

    # Ordering (?ordering=... or ?ordering=-...)
    # NOTE: we include "priority_rank" for correct high>medium>low ordering
    ordering_fields = [
        "id",
        "title",
        "status",
        "priority",
        "start_date",
        "due_date",
        "priority_rank",
    ]
    ordering = ["-start_date"]

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)

        qs = qs.annotate(
            priority_rank=Case(
                When(priority="high", then=0),
                When(priority="medium", then=1),
                When(priority="low", then=2),
                default=99,
                output_field=IntegerField(),
            )
        )
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
