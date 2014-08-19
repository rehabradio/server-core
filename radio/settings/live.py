from .base import *

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
database_url = os.environ.get('DATABASE_URL', None)

DATABASES = {
    'default': dj_database_url.config(
        env="POSTGRESQL_URL",
        default=database_url
    )
}

# Django Caching settings
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_LOCATION', '127.0.0.1:6379:1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'SOCKET_TIMEOUT': 5,
        },
    }
}
