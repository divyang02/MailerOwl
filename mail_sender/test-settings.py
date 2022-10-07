from .settings import *

ENV = "testing"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mail_sender",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "",
    },
    "readonly": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mail_sender",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "",
    },
}

SECRET_KEY = "testing-key"

CELERY_TASK_ALWAYS_EAGER = True