import os

from corsheaders.defaults import default_headers

from celery.schedules import crontab

SITE_BASE_URL = "https://weed-ai.sydney.edu.au"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "upload")
THUMBNAILS_DIR = os.path.join(BASE_DIR, "thumbnails")
REPOSITORY_DIR = os.path.join(BASE_DIR, "repository", "ocfl")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "download")
CVAT_DATA_DIR = os.path.join(BASE_DIR, "cvat_data")

TUS_UPLOAD_DIR = os.path.join(BASE_DIR, "tus_upload")
TUS_DESTINATION_DIR = os.path.join(BASE_DIR, "tus_dir", "data")
TUS_FILE_NAME_FORMAT = "keep"
TUS_EXISTING_FILE = "overwrite"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("ENV", "PROD") == "DEV"

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
AUTH_USER_MODEL = "weedid.WeedidUser"
SESSION_COOKIE_NAME = "weedai_sessionid"

# TUS headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-request-id",
    "x-http-method-override",
    "upload-length",
    "upload-offset",
    "tus-resumable",
    "upload-metadata",
    "upload-defer-length",
    "upload-concat",
]


# Scale file size of upload limit up to 30 MB
MAX_IMAGE_SIZE = 1024 * 1024 * 30
MAX_VOC_SIZE = 1024 * 100
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_IMAGE_SIZE
# Avoid permissions bug, see https://github.com/django-cms/django-filer/issues/1031
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_IMAGE_SIZE

# Application definition

# SMTP config

# Default for SEND_EMAIL is true - set it to false iff it's the
# string "false" (case insensitive)
SEND_EMAIL = os.environ.get("SEND_EMAIL", "").lower() != "false"
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.sydney.edu.au")
SMTP_PORT = os.environ.get("SMTP_PORT", 25)
FROM_EMAIL = os.environ.get("FROM_EMAIL", "Weed-AI <weed-ai.app@sydney.edu.au>")

# The tus upload endpoint is http://tus:1080/tus/files, but for it to work we
# need to proxy the level above that, so TUS_SERVER is http://tus:1080/tus/
# Note that this requires tusd to be launched with -base-path /tus/files as the
# default is /files

TUS_SERVER = os.environ.get("TUS_SERVER", "http://tus:1080/tus/")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "weedid",
    "django_celery_results",
    "django_celery_beat",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB", "reactivesearch"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": "db",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "mystatic")
STATIC_URL = "/mystatic/"

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"

GIT_REMOTE_PATH = os.environ.get("GIT_REMOTE_PATH")
DVC_REMOTE_PATH = os.environ.get("DVC_REMOTE_PATH")

CELERY_BEAT_SCHEDULE = {
    "regular-versioned-backup": {
        "task": "weedid.tasks.backup_repository_changes",
        "schedule": crontab(minute="0", hour="*/3"),
    },
}

IMAGE_HASH_MAPPING_URL = os.environ.get("IMAGE_HASH_MAPPING_URL", "")
