from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.user.views import AuthViewSet, MyProfileViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'profile', MyProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]

