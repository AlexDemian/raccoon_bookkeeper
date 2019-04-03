import os
from conf import settings_secret
from .settings_secret import SECRET_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = ['*']
BASE_URL = 'http://www.raccoonbooker.com'


REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
BROKER_URL = 'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT)
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = BROKER_URL

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = settings_secret.EMAIL_USERNAME
EMAIL_HOST_PASSWORD = settings_secret.EMAIL_PASSWORD
EMAIL_PORT = 587

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Booker',
    'Auth',
    'UserConfs',
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

AUTH_USER_MODEL = 'Auth.User'
ROOT_URLCONF = 'conf.urls'
LOGIN_URL = 'auth/signin_form'
STATIC_URL = 'templates/static/'
STATIC_ROOT = 'templates/static/'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, "static/templates")],
        'APP_DIRS': True,
        'OPTIONS':
            {
                'environment': 'conf.jinja2_conf.environment',
                'context_processors': [
                    'django.contrib.messages.context_processors.messages',
                    'django.contrib.auth.context_processors.auth'
                ]
            },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'raccoon',
        'USER': settings_secret.DATABASE_USER,
        'PASSWORD': settings_secret.DATABASE_PASSWORD,
        'HOST': 'db',
        'PORT': '5432',
    }
}


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




