import os

from config.env import BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))


ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])


# Application definition

LOCAL_APPS = []

THIRD_PARTY_APPS = [
    "django_filters",
{%- if cookiecutter.use_celery == 'y' and cookiecutter.use_beat == 'y'  %}
    "django_celery_beat",
{%- endif %}

{%- if cookiecutter.use_drf == "y" %}
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
{%- endif %}

]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *LOCAL_APPS,
    *THIRD_PARTY_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    {% if cookiecutter.use_drf == "y" -%}
    "corsheaders.middleware.CorsMiddleware",
    {%- endif %}
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {"default": env.db("DATABASE_URL")}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

from config.settings.email import * # noqa

{% if cookiecutter.use_drf == "y" %}
from config.settings.cors import *  # noqa
from config.settings.rest import *  # noqa
from config.settings.swagger import *  # noqa
{% endif %}

{% if cookiecutter.use_celery == "y" and cookiecutter.use_beat == "y" %}
from config.settings.beat import *  # noqa
{% endif %}

{% if cookiecutter.use_celery == "y" %}
from config.settings.celery import *  # noqa
{% endif %}

{% if cookiecutter.use_simple_jwt == "y" and cookiecutter.use_jwt == 'y' %}
from config.settings.jwt import *  # noqa
{% endif %}

{% if cookiecutter.use_cache == "y" %}
from config.settings.cache import *  # noqa
{% endif %}