import os

from celery import Celery
from celery.utils.log import get_task_logger

#: Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

app = Celery()
app.config_from_envvar('CELERY_CONFIG_MODULE')

logger = get_task_logger(__name__)