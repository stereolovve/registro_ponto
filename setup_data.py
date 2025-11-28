import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ponto_system.settings')
django.setup()

from django.contrib.auth.models import User
from timesheet.models import UserProfile

# Create Supervisor
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    UserProfile.objects.create(user=u, role='supervisor', hourly_rate=50.00)
    print("Supervisor created: admin/admin")

# Create Employee
if not User.objects.filter(username='func').exists():
    u = User.objects.create_user('func', 'func@example.com', 'func')
    UserProfile.objects.create(user=u, role='employee', hourly_rate=20.00)
    print("Employee created: func/func")