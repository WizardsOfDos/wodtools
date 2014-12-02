from celery.utils.log import get_task_logger

from flgproc.tasks import app
from flgproc.exceptions import DuplicateFlagException

logger = get_task_logger(__name__)

LOCAL_FLAG_STORAGE = set()

@app.task()
def duplicate_local(flag, add=True, **kwargs):
    if flag in LOCAL_FLAG_STORAGE:
        raise DuplicateFlagException(flag)
    if add:
        LOCAL_FLAG_STORAGE.add(flag)
    return flag


@app.task()
def duplicate_elasticsearch(flag, add=True, **kwargs):
    logger.error("duplicate checking by elasticsearch is not implemented yet")
    return flag