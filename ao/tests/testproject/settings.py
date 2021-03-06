import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = ')&b+%f!0%x37!z4-5bns-^6c_k67cb^!pcs!ahmb#)($+ys)j$'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'ao',
    'ao.msazure',
    'ao.upcloud',
)

MIDDLEWARE = (
    # 'ao.middlewares.ProxyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'ao.admin.middlewares.AdminAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'ao.tests.testproject.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ao.tests.testproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

APPEND_SLASH = False

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'ao.core.views.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (),
}

try:
    __import__('imp').find_module('django_extensions')
    INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)
except ImportError:
    pass
