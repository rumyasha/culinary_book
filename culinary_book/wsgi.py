"""
WSGI config for culinary_book project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culinary_book.settings')

# This application is used for running the project with WSGI servers like Gunicorn
application = get_wsgi_application()