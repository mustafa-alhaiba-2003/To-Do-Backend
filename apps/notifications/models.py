# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FCMDevice(models.Model):
    user = models.ForeignKey(User, related_name='fcm_devices', on_delete=models.CASCADE)
    registration_token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Device for {self.user.username}"

class NotificationHistory(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    data_payload = models.JSONField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title