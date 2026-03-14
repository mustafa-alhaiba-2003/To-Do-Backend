# notifications/serializers.py
from rest_framework import serializers
from .models import FCMDevice, NotificationHistory

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ['id','registration_token', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_active', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationHistory
        fields = ['id', 'title', 'body', 'data_payload', 'is_read', 'created_at']
        read_only_fields = ['id', 'title', 'body', 'data_payload', 'created_at']