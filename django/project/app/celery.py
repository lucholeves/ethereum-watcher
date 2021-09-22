import os
from datetime import timedelta

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config.settings.local")

app = Celery("app")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
beat_max_loop_interval = 5

app.conf.beat_schedule = {
    "update_products": {
        "task": "app.blockchain_eth.tasks.update_blocks",
        "schedule": timedelta(seconds=30),
    },
    "update_transactions": {
        "task": "app.blockchain_eth.tasks.update_transactions",
        "schedule": timedelta(seconds=31),
    },
}
app.conf.timezone = "UTC"
