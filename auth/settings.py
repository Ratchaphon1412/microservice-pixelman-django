"""
Django settings for auth project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from .base import *
from .vault import *
from .rest import *
from .jwt import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETE_KEY_SERVICE['data']['data']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SECRETE_KEY_SERVICE['data']['data']['DEBUG']

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rolepermissions",
    "user",
    "middleware",
    "infrastructure",
    "django_password_validators",
    "django_password_validators.password_history",
    "corsheaders"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# Role Permission
ROLEPERMISSIONS_MODULE = 'auth.roles'

# CORS
CORS_ALLOWED_ORIGINS=True
CORS_ALLOWED_ORIGINS=[
    "http://localhost:3000",
    "*"
]

ROOT_URLCONF = "auth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "auth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": SECRETE_KEY_SERVICE['data']['data']['ENGINE'],
        "NAME": SECRETE_KEY_SERVICE['data']['data']['DB_NAME'],
        "USER": SECRETE_KEY_SERVICE['data']['data']['DB_USER'],
        "PASSWORD": SECRETE_KEY_SERVICE['data']['data']['DB_PASSWORD'],
        "HOST": SECRETE_KEY_SERVICE['data']['data']['DB_HOST'],
        "PORT": SECRETE_KEY_SERVICE['data']['data']['DB_PORT'],
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django_postgres_vault',
#         'NAME': SECRETE_KEY_SERVICE['data']['data']['DB_NAME'],
#         'HOST': SECRETE_KEY_SERVICE['data']['data']['DB_HOST'],
#         'PORT': SECRETE_KEY_SERVICE['data']['data']['DB_PORT'],
#         'VAULT_ADDR': env('VAULT_URI'),
#         'VAULT_TOKEN': env('VAULT_TOKEN'),
#         'VAULT_ROLE_NAME': env('VAULT_DB_ROLE'),
#         'VAULT_DB_MOUNT_POINT': env('VAULT_DB_PATH'),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

# If you want, you can change the default hasher for the password history.
# DPV_DEFAULT_HISTORY_HASHER = 'django_password_validators.password_history.hashers.HistoryHasher'

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTION": {
            "user_attributes": ["email", "username", "first_name", "last_name", "phone"]
        }
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        'NAME': 'django_password_validators.password_history.password_validation.UniquePasswordsValidator',
        'OPTIONS': {
            # How many recently entered passwords matter.
            # Passwords out of range are deleted.
            # Default: 0 - All passwords entered by the user. All password hashes are stored.
            'last_passwords': 5  # Only the last 5 passwords entered by the user
        }
    },
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
            'min_length_digit': 1,

            'min_length_special': 1,
            'min_length_lower': 1,
            'min_length_upper': 1,

            'special_characters': "~!@#$%^&*()_+{}\":;'[]"
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "TH-th"

TIME_ZONE = "Asia/Bangkok"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# URL Frontend
BASE_URL_FRONTEND=SECRETE_KEY_SERVICE['data']['data']['BASE_URL_FRONTEND']

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
