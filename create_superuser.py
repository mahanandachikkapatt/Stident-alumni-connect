import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_connect.settings')
django.setup()

from accounts.models import User

# Create superuser
if not User.objects.filter(is_superuser=True).exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='ADMIN'
    )
    print(f"Superuser created: {admin.username}")
else:
    print("Superuser already exists")
