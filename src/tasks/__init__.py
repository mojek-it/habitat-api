# This makes the Celery app instance discoverable as 'src.tasks.app'
from .celery import app

__all__ = ("app",)
