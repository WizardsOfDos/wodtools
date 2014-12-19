from celery.utils.log import get_task_logger

from flgproc.submitter.telnet import TelnetSubmitter
from ELconn import event

from flgproc import app

logger = get_task_logger(__name__)
submitter = TelnetSubmitter('127.0.0.1', 5001)


@app.task(ignore_result=True)
def submit_flag(flag):
    result = submitter.send_flag(flag)
    event.add_event_SUBMIT(flag, result)
