from django.urls import path
from .views import UserTaskDashboardView

urlpatterns = [
    path('users/dashboard/', UserTaskDashboardView.as_view(), name='user-dashboard'),
]
