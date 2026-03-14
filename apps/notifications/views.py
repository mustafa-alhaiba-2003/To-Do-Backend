from apps.tasks import pagination
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FCMDevice, NotificationHistory
from .serializers import FCMDeviceSerializer, NotificationSerializer 
from apps.tasks.pagination import CustomLimitOffsetPagination

class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FCMDeviceSerializer
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        if self.request.user.role == "admin":
            return FCMDevice.objects.all()
        return FCMDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        FCMDevice.objects.update_or_create(
            user=self.request.user,
            registration_token=serializer.validated_data['registration_token'],
            defaults={'is_active': True}
        )

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        if self.request.user.role == "admin":
            return NotificationHistory.objects.all()
        return NotificationHistory.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({"status": "Notifications marked as read."})