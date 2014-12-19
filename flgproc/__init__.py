import os

from celery import Celery
from celery.utils.log import get_task_logger

from flask import Config

from flgproc import config_default

app = Celery()

#: Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'flgproc.celeryconfig')
app.config_from_envvar('CELERY_CONFIG_MODULE')

config = Config(os.path.dirname(os.path.abspath(__file__)))
config.from_object(config_default)
config.from_envvar('flgproc.config', True)

logger = get_task_logger(__name__)