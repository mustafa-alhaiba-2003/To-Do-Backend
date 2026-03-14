import os
import firebase_admin
from firebase_admin import credentials
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notifications'

    def ready(self):
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'secrets.json')
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)