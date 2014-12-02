from celery import chain
from celery.utils.log import get_task_logger

from flgproc.tasks import app
from flgproc.filter.matching import regex
from flgproc.filter.duplicate import duplicate_local, duplicate_elasticsearch
from flgproc.submitter.demo import printer

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def inpython_collector(flag, **flagargs):
    """
    In this example, the collector decides completely the route of the flag.
    It takes a flag and arbitrary arguments, passes them through local, and then remote filter
    :param flag:
    :param flagargs:
    :return:
    """
    logger.info("receiving flag '{0}' for processing".format(flag))

    """
    first call the simple checks locally and stop if they throw an exception
    """
    try:
        duplicate_local(flag)
        regex(flag)
    except Exception as e:
        logger.error("Stopping flag submission because some check threw an exception: %s" % e)
        return

    """
    If the checks did not throw exceptions, put flag in remote processing.
    This is doing some other checks eg and then submitting the flag.
    But don't wait for result in the end!

    In this example the ignore_result is redundant as the task is already delcared this way.
    But we keep it as an example
    """
    chain(duplicate_elasticsearch.s(flag) | printer.subtask( kwargs=flagargs, options={"ignore_result": True}))()