# Django settings for the CRM (webcrm/settings.py), set up to run in Docker
# with the MySQL service from docker-compose.yml.

import sys
from pathlib import Path
from datetime import datetime as dt
from django.utils.translation import gettext_lazy as _

# Load the default settings shipped with each CRM app
from crm.settings import *          # NOQA
from common.settings import *       # NOQA
from tasks.settings import *        # NOQA
from voip.settings import *         # NOQA
from .datetime_settings import *    # NOQA

# ---- Django settings ---- #

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# To get new value of key use code:
# from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key())
SECRET_KEY = 'j1c=6$s-dh#$ywt@(q4cm=j&0c*!0x!e-qm6k1%yoliec(15tn'

# Host names the CRM can be reached on. Add your own domain here.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'codespace-dev.k3p.dev']
# HTTPS addresses allowed to submit forms (needed when the CRM is behind a proxy)
CSRF_TRUSTED_ORIGINS=['https://codespace-dev.k3p.dev']

# Database connection
DATABASES = {
    'default': {
        # for MySQl
        'ENGINE': 'django.db.backends.mysql',
        'PORT': '3306',

        # for PostgreSQL
        # "ENGINE": "django.db.backends.postgresql",
        # 'PORT': '5432',   # for PostgreSQL

        # Must match the MySQL service in docker-compose.yml.
        # HOST is 'db', the name of the database service.
        'NAME': 'crm_db',
        'USER': 'crm_user',
        'PASSWORD': 'crmpass',
        'HOST': 'db',
    }
}

# Outgoing mail (SMTP) server used to send CRM emails
EMAIL_HOST = '<specify host>'   # 'smtp.example.com'
EMAIL_HOST_PASSWORD = '<specify password>'
EMAIL_HOST_USER = 'crm@example.com'
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = 'CRM: '
EMAIL_USE_TLS = True

# Sender addresses for error reports and normal emails
SERVER_EMAIL = 'test@example.com'
DEFAULT_FROM_EMAIL = 'test@example.com'

# People who receive error reports
ADMINS = [("<Admin1>", "<admin1_box@example.com>")]   # specify admin

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Treat URLs typed into forms without a scheme as https://
FORMS_URLFIELD_ASSUME_HTTPS = True

# Internationalization
# Default language and the languages users can switch to
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('ar', 'Arabic'),
    ('cs', 'Czech'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('he', 'Hebrew'),
    ('hi', 'Hindi'),
    ('id', 'Indonesian'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('nl', 'Nederlands'),
    ('pl', 'Polish'),
    ('pt-br', 'Portuguese'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
    ('vi', 'Vietnamese'),
    ('zh-hans', 'Chinese'),
]

TIME_ZONE = 'UTC'   # specify your time zone

# Enable translations
USE_I18N = True

# Store dates and times in UTC and convert them for display
USE_TZ = True

# Folders that hold translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Page users are sent to when they need to log in
LOGIN_URL = '/admin/login/'

# Application definition
INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # CRM apps
    'crm.apps.CrmConfig',
    'massmail.apps.MassmailConfig',
    'analytics.apps.AnalyticsConfig',
    'help',
    'tasks.apps.TasksConfig',
    'chat.apps.ChatConfig',
    'voip',
    'common.apps.CommonConfig',
    'settings'
]

# Code that runs on every request and response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.utils.usermiddleware.UserMiddleware'
]

# Module with the main URL routes
ROOT_URLCONF = 'webcrm.urls'

# How HTML templates are found and rendered
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Entry point used by WSGI web servers
WSGI_APPLICATION = 'webcrm.wsgi.application'

# Password validation
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Uploaded files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Folder with sample data used by tests
FIXTURE_DIRS = ['tests/fixtures']

# Keep flash messages in the user's session
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ID of this site for the django.contrib.sites app
SITE_ID = 1

# HTTPS and security headers
SECURE_HSTS_SECONDS = 0  # set to 31536000 for the production server
# Set all the following to True for the production server
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_PRELOAD = False
# Only allow the CRM to be shown in frames on the same site
X_FRAME_OPTIONS = "SAMEORIGIN"

# Hide the development server warning in the console
DJANGO_RUNSERVER_HIDE_WARNING = True

# ---- CRM settings ---- #

# For more security, replace the url prefixes
# with your own unique value.
SECRET_CRM_PREFIX = '123/'
SECRET_ADMIN_PREFIX = '456-admin/'
SECRET_LOGIN_PREFIX = '789-login/'

# Specify ip of host to avoid importing emails sent by CRM
CRM_IP = "127.0.0.1"

# Reply-To address added to emails sent by the CRM
CRM_REPLY_TO = ["'Do not reply' <crm@example.com>"]

# List of addresses to which users are not allowed to send mail.
NOT_ALLOWED_EMAILS = []

# List of applications on the main page and in the left sidebar.
APP_ON_INDEX_PAGE = [
    'tasks', 'crm', 'analytics',
    'massmail', 'common', 'settings'
]
# Models shown for each app on the main page
MODEL_ON_INDEX_PAGE = {
    'tasks': {
        'app_model_list': ['Task', 'Memo']
    },
    'crm': {
        'app_model_list': [
            'Request', 'Deal', 'Lead', 'Company',
            'CrmEmail', 'Payment', 'Shipment'
        ]
    },
    'analytics': {
        'app_model_list': [
            'IncomeStat', 'RequestStat'
        ]
    },
    'massmail': {
        'app_model_list': [
            'MailingOut', 'EmlMessage'
        ]
    },
    'common': {
        'app_model_list': [
            'UserProfile', 'Reminder'
        ]
    },
    'settings': {
        'app_model_list': [
            'PublicEmailDomain', 'StopPhrase'
        ]
    }
}

# Country VAT value
VAT = 0    # %

# 2-Step Verification Credentials for Google Accounts.
#  OAuth 2.0
CLIENT_ID = ''
CLIENT_SECRET = ''
OAUTH2_DATA = {
    'smtp.gmail.com': {
        'scope': "https://mail.google.com/",
        'accounts_base_url': 'https://accounts.google.com',
        'auth_command': 'o/oauth2/auth',
        'token_command': 'o/oauth2/token',
    }
}
# Hardcoded dummy redirect URI for non-web apps.
REDIRECT_URI = ''

# Credentials for Google reCAPTCHA.
GOOGLE_RECAPTCHA_SITE_KEY = ''
GOOGLE_RECAPTCHA_SECRET_KEY = ''

# Look up visitor countries by IP address (needs a GeoIP database)
GEOIP = False
GEOIP_PATH = MEDIA_ROOT / 'geodb'

# For user profile list
SHOW_USER_CURRENT_TIME_ZONE = False

# Text shown for records without a name
NO_NAME_STR = _('Untitled')

# For automated getting currency exchange rate
LOAD_EXCHANGE_RATE = False
LOADING_EXCHANGE_RATE_TIME = "6:30"
LOAD_RATE_BACKEND = ""  # "crm.backends.<specify_backend>.<specify_class>"

# Ability to mark payments through a representation
MARK_PAYMENTS_THROUGH_REP = False

# Site headers
SITE_TITLE = 'CRM'
ADMIN_HEADER = "ADMIN"
ADMIN_TITLE = "CRM Admin"
INDEX_TITLE = _('Main Menu')

# Allow mailing
MAILING = True

# This is copyright information. Please don't change it!
COPYRIGHT_STRING = f"Django-CRM. Copyright (c) {dt.now().year}"
PROJECT_NAME = "Django-CRM"
PROJECT_SITE = "https://github.com/DjangoCRM/django-crm/"


# Settings used only when running "python manage.py test"
TESTING = sys.argv[1:2] == ['test']
if TESTING:
    SECURE_SSL_REDIRECT = False
    LANGUAGE_CODE = 'en'
    LANGUAGES = [('en', ''), ('uk', '')]
