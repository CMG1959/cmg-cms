"""
Django settings for CIMC project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Moved over to bitbucket for now

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#95@a0qici=2*%n&4zh#k%ecmkvn@(i$8gwhn5qq6=$vw#9fp@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jquery',
    'bootstrap3',
    'mathfilters',
    'dashboard',
    'employee',
    'equipment',
    'home',
    'inspection',
    'mobile_views',
    'molds',
    'part',
    'production_and_mold_history',
    'startupshot',
    'supplier',
    'rest_framework',)

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

ROOT_URLCONF = 'CIMC.urls'

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

WSGI_APPLICATION = 'CIMC.wsgi.application'

config_dict = json.load(open('config.json'))
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'NAME': 'CIMC_DB',
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': '127.0.0.1',
#         'PORT': '',
#         'USER': 'mcaro',
#         'PASSWORD': '1959Cmg1',
#
#     },
DATABASES = {
        'default': config_dict['default_database'],
        },
    # DATABASES = {
    #             'default': {
    #                 'NAME': 'CIMC_DB',
    #                 'ENGINE': 'sql_server.pyodbc',
    #                 'HOST': 'dmi5vh1dpk.database.windows.net',
    #                 'PORT' :'1433',
    #                 'USER': 'mcaro@dmi5vh1dpk',
    #                 'PASSWORD': '1959Cmg1',
    #                 'OPTIONS': {
    #                     'driver': 'SQL Server Native Client 11.0',
    #                 },
    #             },
    # 'mattec': {
    #     'NAME': 'MATTEC',
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': '127.0.0.1',
    #     'PORT' :'1433',
    #     'USER': 'mcaro',
    #     'PASSWORD': '1959Cmg1',
    #     'OPTIONS': {
    #         'driver': 'SQL Server Native Client 11.0',
    #     },
    # }
}
#     DATABASES = {
#             'default': {
#                 'NAME': 'CIMC_DB',
#                 'ENGINE': 'sql_server.pyodbc',
#                 'HOST': '127.0.0.1',
#                 'PORT' :'1433',
#                 'USER': 'mcaro',
#                 'PASSWORD': '1959Cmg1',
#                 'OPTIONS': {
#                     'driver': 'SQL Server Native Client 11.0',
#                 },
#             },
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'  # You may find this is already defined as such.
STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
STATIC_ROOT = "C:\CIMC_static"

STATICFILES_DIRS = (
    STATIC_PATH,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


#### SETTINGS FOR SESSIONS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

BOOTSTRAP3 = {
    # The URL to the jQuery JavaScript file
    'jquery_url': 'external/jquery/jquery.js',

    # The Bootstrap base URL
    'base_url': 'external/bootstrap/',
}
