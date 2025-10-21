from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/1")

celery = Celery(
    "coffee_api",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BACKEND_URL,
)

celery.conf.beat_schedule = {
    "delete-unverified-users-every-day": {
        "task": "app.tasks.cleanup.delete_unverified_users",
        "schedule": 60 * 60 * 24,  # every 24 hours
    }
}
celery.conf.timezone = "UTC"
