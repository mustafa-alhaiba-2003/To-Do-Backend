import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

# No Channels routing needed. Django handles async natively now!
application = get_asgi_application()