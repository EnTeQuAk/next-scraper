from next_scraper.conf.base import *

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG"},
        "django.request": {
            "handlers": ["console"],
            "propagate": False,
            "level": "ERROR",
        },
        "celery": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
}

CELERY_TASK_ALWAYS_EAGER = False
