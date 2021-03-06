"""
Django settings for +radio project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re
import sys

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, os.pardir, 'apps')))
sys.path.insert(0, os.path.abspath(os.path.join(
                BASE_DIR, os.pardir, 'vendors')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',

    # third-party apps
    'corsheaders',
    'django_rq',
    'rest_framework',
    'rest_framework_swagger',
    'radiobabel',

    # local apps
    'radio_metadata',
    'radio_players',
    'radio_playlists',
    'radio_queue',
    'radio_users',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'accept',
    'authorization',
    'content-type',
    'origin',
    'x-csrftoken',
    'x-requested-with',
    # Cusom request header objects
    'x_google_auth_token',
    'x_player_auth_token'
)

ROOT_URLCONF = 'radio.urls'

WSGI_APPLICATION = 'radio.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
import dj_database_url

database_url = os.environ.get('LOCAL_DATABASE_URL', None)

DATABASES = {
    'default': dj_database_url.config(
        env="POSTGRESQL_URL",
        default=database_url
    )
}
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
PROJECT_PATH = BASE_DIR
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# Django Rest Framework settings
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'radio.google_oauth.GoogleOauthBackend',
        'radio.player_token_auth.PlayerTokenAuthBackend',
    )
}

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'radio': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

# Django template settings
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(BASE_DIR, os.pardir, 'templates')),
)

# Django RQ configuration
RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
    },
}

SECRET_KEY = os.environ.get('SECRET_KEY', None)

SOUNDCLOUD_CLIENT_ID = os.environ.get('SOUNDCLOUD_CLIENT_ID', None)
SOUNDCLOUD_CLIENT_SECRET = os.environ.get('SOUNDCLOUD_CLIENT_SECRET', None)

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', None)
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', None)

GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID', None)
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get(
    'GOOGLE_OAUTH2_CLIENT_SECRET',
    None
)
domains = os.environ.get('GOOGLE_WHITE_LISTED_DOMAINS', '')
domains = re.findall('([a-z\.]+)', domains)
GOOGLE_WHITE_LISTED_DOMAINS = domains

SWAGGER_SETTINGS = {
    "api_version": '0.1',
    "exclude_namespaces": [],
    "is_authenticated": True,
    "is_superuser": False,
}
