import os
import django
from django.conf import settings
from decouple import config

# Configure Django settings
settings.configure(
    DEBUG=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='church_cms_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
)

django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("✅ Django connected successfully!")
        print(f"PostgreSQL version: {version[0][:60]}...")
        
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        print(f"Connected to database: {db_name[0]}")
except Exception as e:
    print(f"❌ Connection failed: {e}")