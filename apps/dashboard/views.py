from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

#services 
from apps.dashboard.services.dashboard_service import DashboardService
from apps.dashboard.permissions import IsAdminUser



class AdminViewSet(ViewSet):
    permission_classes = [IsAdminUser]
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        data = DashboardService().get_dashboard_data()
        return Response(data)