import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_management.settings')
django.setup()

from accounts.models import CustomUser
from django.contrib.auth.models import Group, Permission

# Create admin user
admin, created = CustomUser.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@church.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'super_admin',
        'is_staff': True,
        'is_superuser': True,
    }
)

if created:
    admin.set_password('Admin@123')
    admin.save()
    print(f"✅ Superuser 'admin' created successfully!")
    print(f"   Email: {admin.email}")
    print(f"   Password: Admin@123")
else:
    print(f"⚠️  User 'admin' already exists (not modified)")

print(f"\nTotal users in database: {CustomUser.objects.count()}")
