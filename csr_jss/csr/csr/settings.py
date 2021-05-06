"""
Django settings for csr project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r^6=v^da!3(64pzygit-s%sb9&eu_3r9#at%^nl3&z^b3q4_4z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Generated by using cryptography module
CRYPT_KEY = "EYuHD5qgQg9tdw-Pc88v3yK0myk17UmylIJ0dq-S6XM="


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'import_export',
    'accounts',
    'eprotocol',
    'ckeditor',
    'audits',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'csr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
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

WSGI_APPLICATION = 'csr.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'


IMPORT_EXPORT_USE_TRANSACTIONS = False

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'csr_jss',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DATA_UPLOAD_MAX_NUMBER_FIELDS = 102400
DATA_UPLOAD_MAX_MEMORY_SIZE = 100000000


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

#For Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# For logging
path, PROJECT_NAME = os.path.split(BASE_DIR)
LOG_FILES = ['info','error']
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        LOG_FILES[0]+'_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename' : str(BASE_DIR)+'/'+'media'+'/logs/'+LOG_FILES[0]+'.log',
            'formatter': 'verbose',
            'filters': ['require_debug_true']
        },
    'PP_'+LOG_FILES[0]+'_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename' : str(BASE_DIR)+'/'+'media'+'/logs/'+LOG_FILES[0]+'.log',
            'formatter': 'verbose', 
            'filters': ['require_debug_false'],
        },
        LOG_FILES[1]+'_log': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename' : str(BASE_DIR)+'/'+'media'+'/logs/'+LOG_FILES[1]+'.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        LOG_FILES[0]: {
            'handlers': [LOG_FILES[0]+'_log','PP_'+LOG_FILES[0]+'_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        LOG_FILES[1]: {
            'handlers': [LOG_FILES[1]+'_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    
    },
}