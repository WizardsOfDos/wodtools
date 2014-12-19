import re

from celery.utils.log import get_task_logger

from flgproc import config, app
from flgproc.exceptions import MalformedFlagException


logger = get_task_logger(__name__)


@app.task()
def regex(flag, pattern=config['FLAG_PATTERN']):
    logger.debug("checking flag '{0}' for matching regex pattern".format(flag))
    if re.fullmatch(pattern, flag) is None:
        raise MalformedFlagException(flag, "pattern: '%s'" % pattern)
    return flag


@app.task()
def length(flag, lenght_lower=config['FLAG_LENGTH_MIN'], length_upper=config['FLAG_LENGTH_MIN']):
    logger.debug("checking flag '%s' for length constraints" % flag)
    if not lenght_lower <= len(flag) <= length_upper:
        raise MalformedFlagException(flag, "{length_flag} not within [{lenght_lower}, {length_upper}]".format(
            length_flag=len(flag), lenght_lower=lenght_lower, length_upper=length_upper
        ))
    return flag