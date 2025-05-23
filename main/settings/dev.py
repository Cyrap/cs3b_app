from .base import *
from datetime import timedelta

# Security
SECRET_KEY = 'django-insecure-_5-d+r21rz%2%zw$!iqde1v^+rx-c!oa^y%enwmr4bg)k(7eaz'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '*']
CORS_ALLOW_ALL_ORIGINS = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cyrap_app',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',
    'http://127.0.0.1:3001',
    'http://localhost:3009',
    'http://127.0.0.1:3009',
    "http://localhost:43249",
    "http://127.0.0.1:43249",
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',
    'http://127.0.0.1:3001',
    "http://localhost:43249",
    "http://127.0.0.1:43249",
]

# ustga