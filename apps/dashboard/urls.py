from apps.dashboard.views import AdminViewSet
from rest_framework.routers import DefaultRouter

from todo import urls

router = DefaultRouter()
router.register(r'', AdminViewSet, basename='admin')

urlpatterns = []
urlpatterns += router.urls