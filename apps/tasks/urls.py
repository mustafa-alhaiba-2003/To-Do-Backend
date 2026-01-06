from django.urls import path
from .views import UserTaskDashboardView , UserTaskViewSet
from rest_framework.routers import DefaultRouter 

router = DefaultRouter()
router.register("user",UserTaskViewSet,basename="user-tasks")

urlpatterns = [
    path('users/dashboard/', UserTaskDashboardView.as_view(), name='user-dashboard'),
]

urlpatterns += router.urls