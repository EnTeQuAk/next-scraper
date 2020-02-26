import os

import environ
from kombu import Queue

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "..", "..")

SECRET_KEY = "na2p&yexkp-g83$2m^&b!r+a%nv2ci1!d9vh^a_7h!hv*7&h79"

SITE_ID = 1

DEBUG = True

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Asyncronous worker support
    "celery",
    # For our REST Api
    "rest_framework",
    # next_scraper apps
    "next_scraper",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "next_scraper.urls"

WSGI_APPLICATION = "next_scraper.wsgi.application"

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

DATABASES = {"default": env.db_url(default="psql://scraper:@db/scraper")}

# Run all views in a transaction unless they are decorated not to.
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Pool our database connections up for 300 seconds
DATABASES["default"]["CONN_MAX_AGE"] = 300

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Celery
BROKER_URL = "redis://localhost:6379"

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/1")

CELERY_TASK_IGNORE_RESULT = False

# Just so that this won't be forgotten, see
# http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html#caveats
# for details.
BROKER_TRANSPORT_OPTIONS = {"fanout_prefix": True, "fanout_patterns": True}

# Force always eager to be False (it's by default but here for documentation)
CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = False

# Track started tasks. This adds a new STARTED state once a task
# is started by the celery worker.
CELERY_TRACK_STARTED = True

CELERY_IMPORTS = ("next_scraper.tasks.scraper",)

CELERY_QUEUES = (
    Queue("default", routing_key="default"),
    Queue("celery", routing_key="celery"),
)

# Make our `LOGGING` configuration the only truth and don't let celery
# overwrite it.
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# Don't log celery log-redirection as warning (default).
# We manage our logging through `django.conf.settings.LOGGING` and
# want that to be our first-citizen config.
CELERY_REDIRECT_STDOUTS_LEVEL = "INFO"
