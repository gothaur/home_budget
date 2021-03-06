"""
Django settings for home_budget project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from celery.schedules import crontab
from django.urls import reverse_lazy

import os

from decouple import (
    config,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    # 'rest_framework',
    'api.apps.ApiConfig',
    'auth_ex',
    'budget',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'home_budget.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'budget.context_processor.add_entry_form',
                'budget.context_processor.date',
                'budget.context_processor.filter_forms',
                'budget.context_processor.sidebars',
                'budget.context_processor.version',
            ],
        },
    },
]

WSGI_APPLICATION = 'home_budget.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
}

LOGIN_URL = reverse_lazy('auth_ex:login')
LOGIN_REDIRECT_URL = reverse_lazy('index')

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
AUTH_USER_MODEL = 'auth_ex.User'

# SECURE_SSL_REDIRECT = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']


# CELERY_BROKER_URL = 'redis://h:p25bde47f0ecf0de18acd3bb60fa34eeecf29c741bc4266f791751693bbb2ee2d@ec2-52-202-177-173.compute-1.amazonaws.com:13899'
# CELERY_BEAT_SCHEDULE = {
#     'print-every-10-seconds': {
#         'task': 'budget.tasks.print_message_to_console',
#         'schedule': crontab(day_of_month=2),
#     },
# }
CELERY_BROKER_URL = 'amqp://localhost'
# CELERY_BEAT_SCHEDULE = {
#     '2nd-day-monthly-reports': {
#         'task': 'budget.tasks.email_monthly_report',
#         'schedule': 10.0,
#         'args': '',
#     },
# }
# CELERY_TIMEZONE = 'Europe/Warsaw'
