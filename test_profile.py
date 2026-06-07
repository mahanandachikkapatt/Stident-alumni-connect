import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_connect.settings')
django.setup()

from accounts.models import User

print("Checking user data in database...")
print("=" * 50)

# Get all users
users = User.objects.all()
print(f"Total users: {users.count()}")

# Check each user's profile data
for user in users:
    print(f"\nUsername: {user.username}")
    print(f"Email: {user.email}")
    print(f"First Name: '{user.first_name}'")
    print(f"Last Name: '{user.last_name}'")
    print(f"Phone: '{user.phone}'")
    print(f"Address: '{user.address}'")
    print(f"Date of Birth: {user.date_of_birth}")
    print(f"Bio: '{user.bio}'")
    print("-" * 30)

# Look for varsha specifically
varsha_user = User.objects.filter(username__icontains='varsha').first()
if varsha_user:
    print(f"\nFound Varsha user:")
    print(f"Username: {varsha_user.username}")
    print(f"Email: {varsha_user.email}")
    print(f"First Name: '{varsha_user.first_name}'")
    print(f"Last Name: '{varsha_user.last_name}'")
    print(f"Phone: '{varsha_user.phone}'")
    print(f"Address: '{varsha_user.address}'")
else:
    print("\nNo user found with 'varsha' in username")
