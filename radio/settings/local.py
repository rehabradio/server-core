from .base import *

DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
database_url = os.environ.get('LOCAL_DATABASE_URL', None)

DATABASES = {
    'default': dj_database_url.config(
        env="POSTGRESQL_URL",
        default=database_url
    )
}

# django-debug-toolbar settings
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ('127.0.0.1', '0.0.0.0')
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'radio.utils.debug_toolbar.show_debug_toolbar',
}
