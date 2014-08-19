"""
WSGI config for rehabradio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

environment = os.environ.get('ENVIRONMENT', 'LOCAL')
if environment == 'LOCAL':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radio.settings.local')
elif environment == 'LIVE':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radio.settings.live')


from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
