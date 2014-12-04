import re

from celery.utils.log import get_task_logger

from flgproc import conf
from flgproc.tasks import app
from flgproc.exceptions import MalformedFlagException


logger = get_task_logger(__name__)


@app.task()
def regex(flag, pattern=conf.FLAG_PATTERN):
    logger.debug("checking flag '{0}' for matching regex pattern".format(flag))
    if re.fullmatch(pattern, flag) is None:
        raise MalformedFlagException(flag, "pattern: '%s'" % pattern)
    return flag