from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mail_sender.settings")

app = Celery("mail_sender")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "periodic-email-sender": {
        "task": "apps.email_scheduler.tasks.periodic_email_sender",
        "schedule": 60,
    },
    "email-log-updater": {
        "task": "apps.email_scheduler.tasks.periodic_email_log_updater",
        "schedule": 60,
    },
}


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
