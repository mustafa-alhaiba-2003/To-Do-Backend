from django.db import models

class Task(models.Model):
    TITLE_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in-progress')
    start_date = models.DateTimeField(auto_now_add = True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=TITLE_CHOICES, default='medium')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
