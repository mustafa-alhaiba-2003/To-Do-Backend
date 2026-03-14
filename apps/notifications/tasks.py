# from celery import shared_task
# from django.contrib.auth import get_user_model
# from .services import create_and_send_notification

# User = get_user_model()

# @shared_task
# def send_async_notification(user_id, title, body, data=None):
#     try:
#         user = User.objects.get(id=user_id)
#         create_and_send_notification(user, title, body, data)
#     except User.DoesNotExist:
#         pass