"""
Django settings for timetracker project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None)

# Only use default secret key if DEBUG is turned on
if SECRET_KEY is None and DEBUG:
    SECRET_KEY = 'secret'

allowed_host_string = os.environ.get('DJANGO_ALLOWED_HOSTS', None)
if allowed_host_string:
    ALLOWED_HOSTS = allowed_host_string.split(',')
else:
    ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'crispy_forms',

    # Custom Apps
    'account',
    'core',
    'vms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'timetracker.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'timetracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# We assume that the provided credentials are for a Postgres DB. If the
# appropriate credentials are not provided, we fall back to the local
# sqlite DB.

DB_HOST = os.environ.get('DJANGO_DB_HOST', 'localhost')
DB_NAME = os.environ.get('DJANGO_DB_NAME')
DB_PASSWORD = os.environ.get('DJANGO_DB_PASSWORD')
DB_PORT = os.environ.get('DJANGO_DB_PORT', '5432')
DB_USER = os.environ.get('DJANGO_DB_USER')

if all((DB_HOST, DB_USER, DB_PASSWORD, DB_PORT)):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',     # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',               # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',              # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',             # noqa
    },
]


# Custom User Model

AUTH_USER_MODEL = 'account.User'


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT', None)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_ROOT', None)


# Login/Logout URLs

LOGIN_REDIRECT_URL = 'vms:dashboard'
LOGIN_URL = 'account:login'
LOGOUT_REDIRECT_URL = 'home'


# Settings for generating slugs.

########################################################################
#                                WARNING                               #
########################################################################
# Do not modify the values here unless strictly necessary. If these    #
# values are changed, a migration has to be made on the database to    #
# ensure that the max lengths of the slug fields are correct.          #
########################################################################

# The number of characters to generate to guarantee uniqueness of the
# slug.
SLUG_KEY_LENGTH = 6

# The maximum number of characters to use from the slugified value.
SLUG_LENGTH = 50

# The complete slug is composed of the slug and slug key, joined by a
# hyphen.
SLUG_LENGTH_TOTAL = SLUG_KEY_LENGTH + SLUG_LENGTH + 1


# Crispy Forms

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Logging Configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Root logger
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        # App specific loggers
        'account': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'vms': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
