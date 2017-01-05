import os
from unipath import Path
from decouple import config
from dj_database_url import parse as db_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'agazeta.urls'

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            [os.path.join(BASE_DIR, 'templates')],
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
)


WSGI_APPLICATION = 'agazeta.wsgi.application'


DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        cast=db_url
    )
}


AUTH_PASSWORD_VALIDATORS = (
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttribute'
        'SimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLength'
        'Validator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPassword'
        'Validator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPassword'
        'Validator',
    },
)

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
FORCE_SSL = config('FORCE_SSL', default=True, cast=bool)
SECURE_SSL_REDIRECT = FORCE_SSL
SESSION_COOKIE_SECURE = FORCE_SSL
CSRF_COOKIE_SECURE = FORCE_SSL
SSLIFY_DISABLE = not FORCE_SSL

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

STATIC_ROOT = 'static'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
    os.path.join(BASE_DIR, 'staticfiles'),
]

LOGIN_URL = '/login/'
