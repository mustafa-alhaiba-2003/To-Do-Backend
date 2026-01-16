from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a default admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the admin user', default='admin')
        parser.add_argument('--email', type=str, help='Email for the admin user', default="admin@gmail.com")
        parser.add_argument('--password', type=str, help='Password for the admin user', default='adminpassword')

    def handle(self, *args, **options):
        from apps.user.models import User

        username = options['username']
        email = options['email']
        password = options['password']

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role = 'admin'
        )
        self.stdout.write(self.style.SUCCESS(f'Admin {username} ,email: {email} and password: {password} created successfully.'))