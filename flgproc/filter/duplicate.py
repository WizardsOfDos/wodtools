from collections import deque

from celery.utils.log import get_task_logger

from flgproc import config, app
from flgproc.exceptions import DuplicateFlagException

import ELconn.event

logger = get_task_logger(__name__)

LOCAL_FLAG_STORAGE = deque(maxlen=config.DUPFLAG_DEQUEU_MAXLEN)


@app.task()
def duplicate_local(flag, add=True, **kwargs):
    logger.debug("checking flag '{0}' for local duplicates".format(flag))
    if flag in LOCAL_FLAG_STORAGE:
        raise DuplicateFlagException(flag)
    if add:
        LOCAL_FLAG_STORAGE.append(flag)
    return flag


@app.task()
def duplicate_elasticsearch(flag, add=True, **kwargs):
    logger.debug("checking flag '{0}' for duplicates in elasticsearch".format(flag))
    if ELconn.event.get_events_count_ENTRY(flag) > 0:
        raise DuplicateFlagException(flag)
    return flag