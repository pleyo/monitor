"""
Django settings for fromedwin project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        environment= os.getenv('SENTRY_ENVIRONMENT', 'undefined'),
        integrations=[
            DjangoIntegration(),
        ],
    )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
FORCE_HTTPS = False
if os.environ.get('FORCE_HTTPS') == '1' or os.environ.get('FORCE_HTTPS', '').lower() == 'true':
    FORCE_HTTPS = True 

DOMAIN = os.environ.get('DOMAIN')
PORT = os.environ.get('PORT')
WEBAUTH_USERNAME = os.environ.get('WEBAUTH_USERNAME')
WEBAUTH_PASSWORD = os.environ.get('WEBAUTH_PASSWORD')

IS_SERVICE_DOWN_SCRAPE_INTERVAL_SECONDS = 60
IS_SERVICE_DOWN_TRIGGER_OUTRAGE_MINUTES = 5
# Run Lighthouse every 60 minutes
LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES = int(os.environ.get('LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES', 60))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS = ['*']

USE_X_FORWARDED_HOST = True

CSRF_TRUSTED_ORIGINS = [
    f'https://{os.environ.get("DOMAIN")}',
    f'https://*.{os.environ.get("DOMAIN")}',
    f'https://core.com',
    f'https://*.core.com',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'static'),
]

# Was returning 413 on report upload.
DATA_UPLOAD_MAX_MEMORY_SIZE = 10*1024*1024 # (10Mb instead of default 2.5Mb)

if os.environ.get('STORAGE') == 'S3':
    # aws settings
    AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
    S3_USE_SIGV4 = False
    AWS_S3_SIGNATURE_VERSION = "s3"
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=3600'}
    AWS_S3_FILE_OVERWRITE = True
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# Application definition

# TAILWIND SETTINGS
TAILWIND_APP_NAME = 'theme' # Tailwind theme
INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    # Tailwind
    'theme',
    'tailwind',
    'django_browser_reload',
    # App
    'administration',
    'availability',
    'dashboard',
    'incidents',
    'core',
    'notifications',
    'performances',
    'settings',
    'projects',
    'website',
    'status',
    'workers',
    # Statistics
    'django_prometheus',
    # Authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    # Django cleanup needs to be last !
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = (
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
    'core.middleware.project_required',
    'settings.middleware.set_timezone',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
)

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database confugration using environment variable DATABASES_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {}
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django_prometheus.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_EMAIL_VERIFICATION = 'none'

CONTACT_NAME = os.environ.get('CONTACT_NAME', 'FromEdwin')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'no-reply@core.com')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')

if os.environ.get('EMAIL_BACKEND_CONSOLE') == 'True' or not EMAIL_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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


SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
        ],
    }
}

HEARTBEAT_INTERVAL = 10 # client will call server every HEARTBEAT_INTERVAL seconds.

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1


"""
    Generate webhook url used by alert manager yml file
"""
ALERTMANAGER_WEBHOOK_URL = ''
if FORCE_HTTPS:
    ALERTMANAGER_WEBHOOK_URL += 'https://'
else:
    ALERTMANAGER_WEBHOOK_URL += 'http://'

if DOMAIN == 'localhost' or DOMAIN == None:
    ALERTMANAGER_WEBHOOK_URL += 'host.docker.internal'
else:
    ALERTMANAGER_WEBHOOK_URL += DOMAIN

if PORT and PORT != '80' and PORT != '443':
    ALERTMANAGER_WEBHOOK_URL += f':{PORT}'
ALERTMANAGER_WEBHOOK_URL += '/alert/'

# Define freemium specs
FREEMIUM_PROJECTS = 3
FREEMIUM_AVAILABILITY = 1
FREEMIUM_PERFORMANCE = 3
