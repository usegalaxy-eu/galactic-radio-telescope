from base.settings import *  # noqa

import os
import random
import string

import raven

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('/tmp/django_secret'):
    with open('/tmp/django_secret', 'w') as handle:
        handle.write("".join([random.SystemRandom().choice(string.digits + string.punctuation) for i in range(100)]))

with open('/tmp/django_secret', 'r') as handle:
    SECRET_KEY = handle.read()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', None) == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
CORS_ORIGIN_WHITELIST = os.environ.get('DJANGO_CORS_ORIGINS', '').split(',')


# Application definition

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

if 'RAVEN_DSN' in os.environ:
    RAVEN_CONFIG = {
        'dsn': os.environ['RAVEN_DSN'],
        'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
    }
else:
    RAVEN_CONFIG = {}
