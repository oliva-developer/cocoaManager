"""
Django settings for apis project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a=a_3b@_@1!$l-hcs=7*!n(qix6_1@7m!f0w8vdf6yt^e($8(@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# JAZZMIN CONFIG
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "OliSYS",
    "site_header": "OliSYS",
    "site_brand": "liSYS",
    "site_logo": "logo.jpg",
    "login_logo": "logo.jpg",
    "login_logo_dark": "logo.jpg",
    "welcome_sign": 'Bienvenido(a) a Productora de Cacao "ALVAREZ EIRL"',
    "copyright": "OliSYS EIRL",
    "site_logo_classes": "img-thumbnail",
    "user_avatar": "avatar",
    "custom_css": "css/custom_admin.css",
    "hide_models": ["apis_.PurchaseDetail", "apis_.WorkingDayResource", "apis_.Kpi"],
    "hide_apps": ["django_plotly_dash"],
    "icons": {
        "apis_.Article": "fa-solid fa-tag",
        "apis_.Collaborator": "fa-solid fa-user-tie",
        "apis_.Provider": "fa-solid fa-truck-arrow-right",
        "apis_.Workshop": "fa-solid fa-toolbox",
        "apis_.Customer": "fa-solid fa-handshake-simple",
        "apis_.Purchase": "fa-solid fa-cart-shopping",
        "apis_.ToolMaintenance": "fa-solid fa-screwdriver-wrench",
        "apis_.CustomUser": "fa-solid fa-user",
        "apis_.WorkingDay": "fas fa-calendar-check",
        "apis_.Task": "fas fa-list-check",
        "apis_.SaleProduct": "fa-solid fa-money-bill-trend-up",
        "apis_.Kpi": "fa-solid fa-chart-simple",
    },
    "order_with_respect_to": [
        "apis_.SaleProduct",
        "apis_.WorkingDay",
        "apis_.Purchase",
        "apis_.ToolMaintenance",
        "apis_.Collaborator",
        "apis_.Workshop",
        "apis_.Customer",
        "apis_.Task",
        "apis_.Article",
        "apis_.Provider",
        "apis_.CustomUser",
        "apis_.Kpi",
    ],
    # "custom_links": {
    #     "apis_": [{
    #             "name": "Artículos",
    #             "url": "/admin/apis_/article/",
    #             "icon": "fas fa-product",
    #             # "permissions": ["books.view_book"]     
    #         },
    #     ]
    # },
}

JAZZMIN_UI_TWEAKS = {
    "theme" : "lux"
}

AUTH_USER_MODEL = "apis_.CustomUser"
# Application definition
X_FRAME_OPTIONS = 'SAMEORIGIN'
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apis_',
    'django_plotly_dash',
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

ROOT_URLCONF = 'apis.urls'

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

WSGI_APPLICATION = 'apis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cocoamanager',
        'USER': 'root',
        'PASSWORD': 'aldair821',
        'HOST': 'localhost',  # Cambia si tu base de datos está en otro servidor
        'PORT': '3306',  # Puerto predeterminado de MySQL
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
