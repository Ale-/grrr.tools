"""
Django settings for GRRR
"""

import os
from django.utils.translation import ugettext_lazy as _

#
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.abspath( os.path.dirname(__file__) )
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ENV_PATH, '..', 'static')
PROJECT_STATIC_FOLDER = 'grrr'
STATICFILES_DIRS = [
    ( PROJECT_STATIC_FOLDER, STATIC_ROOT + '/' + PROJECT_STATIC_FOLDER + '/' ),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ENV_PATH, '..', 'media')
MAINTENANCE_IGNORE_URLS = (
    r'^/admin/.*',
    r'^/login$',
)
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/mi-cuenta'
LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
REGISTRATION_AUTO_LOGIN = True

# Name of site in the document title
DEFAULT_HTML_TITLE = 'GRRR Tools'
DEFAULT_HTML_DESCRIPTION = _('Grupo para la reutilización y redistribución de recursos.')

# Sites ID
SITE_ID = 1

#
# Application definition
#

CONTRIB_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maintenancemode',
    'djgeojson',
    'leaflet',
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
    'star_ratings',
    'captcha'
]

PROJECT_APPS = [
    'apps.models',
    'apps.users',
    'apps.api',
    'apps.views',
    'apps.utils',
]

INSTALLED_APPS = CONTRIB_APPS + PROJECT_APPS

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

ROOT_URLCONF = 'grrr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.users.context_processors.unseen_messages',
                'apps.utils.context_processors.site_info_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'grrr.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('es', _('Español')),
    ('en', _('Inglés')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# LEAFLET
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (40.4115, -3.7076),
    'DEFAULT_ZOOM'  : 5,
    'MIN_ZOOM'      : 3,
    'MAX_ZOOM'      : 18,
    'TILES'         : [('toner', 'https://api.mapbox.com/styles/v1/ale/cj3rpgd2n00142slekpjya98f/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWxlIiwiYSI6ImpKQ2dnekEifQ.GjyY2X3Wa6pgoHTPOrUBdA', {
                        'attribution': '<a href="https://www.mapbox.com/about/maps/" target="_blank">© Mapbox</a> <a href="http://www.openstreetmap.org/about/" target="_blank">© OpenStreetMap</a>' })],
}

# CKEDITOR
# CKEDITOR_UPLOAD_PATH = "/inline-images/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'width'  : '100%',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Image' ],
            ['RemoveFormat', 'Source']
        ]
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL  = "/static/admin/js/vendor/jquery/jquery.min.js"

TWITTER_NOTIFICATIONS = False

#
# Import private settings
#
from .private_settings import *
