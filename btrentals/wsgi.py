"""
WSGI config for btrentals project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btrentals.settings')

application = get_wsgi_application()

try:
    import create_superuser
except Exception as e:
    print(f"Superuser creation skipped or failed: {e}")

