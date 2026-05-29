"""Management command to create admin user if it doesn't exist."""
from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **options):
        if CustomUser.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists'))
            return

        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@church.com',
            password='Admin@123',
            first_name='Admin',
            last_name='User',
            role='super_admin',
        )
        self.stdout.write(self.style.SUCCESS(f'✅ Admin user created: {admin.username}'))
        self.stdout.write(f'   Password: Admin@123')
