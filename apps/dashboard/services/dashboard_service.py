from apps.user.models import User
from apps.tasks.models import Task
from django.utils import timezone 

class DashboardService:

    def _get_statistics(self):
        total_users_active = User.objects.filter(is_active=True).count()
        total_user_inactive = User.objects.filter(is_active=False).count()
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='completed').count()
        in_progress_tasks = Task.objects.filter(status='in-progress').count()
        overdue_tasks = Task.objects.filter(due_date__lt=timezone.now(), status='in-progress').count()
        return {
            'total_users_active': total_users_active,
            'total_users_inactive': total_user_inactive,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'overdue_tasks': overdue_tasks,
        }
        
    def _get_recent_registered_users(self, limit=3):
        recent_users = User.objects.filter(is_active=True).order_by('-date_joined')[:limit]
        return [{'id': user.id, 'username': user.username, 'email': user.email, 'date_joined': user.date_joined} for user in recent_users]

    def _get_recent_tasks(self, limit=3): 
        recent_tasks = Task.objects.select_related('user').order_by('-start_date')[:limit]
        return [{
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'priority': task.priority,
        } for task in recent_tasks]

    def get_dashboard_data(self):
        data = {}
        data['statistics'] = self._get_statistics()
        data['recent_registered_users'] = self._get_recent_registered_users()
        data['recent_tasks'] = self._get_recent_tasks()
        return data

