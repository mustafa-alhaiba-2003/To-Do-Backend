from django.db.models.signals import post_save
from django.dispatch import receiver
from django_eventstream import send_event
from .models import NotificationHistory 

@receiver(post_save, sender=NotificationHistory)
def push_notification_count(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        unread_count = NotificationHistory.objects.filter(user=user, is_read=False).count()
        channel_name = f'notifications-{user.id}'
        send_event(channel_name, 'message', {'unread_count': unread_count})