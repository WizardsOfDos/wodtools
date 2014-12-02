from celery.utils.log import get_task_logger

from flgproc.tasks import app

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def printer(flag, *args, **kwargs):
    logger.info("Flag {flag} was submitted with the following args({args}) and kwargs({kwargs})".format(
        flag=flag, args=args, kwargs=kwargs))