import socket

from celery.utils.log import get_task_logger
from ELconn import event

from flgproc import app

logger = get_task_logger(__name__)
_UDPSOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

@app.task(ignore_result=True)
def printer(flag, *args, **kwargs):
    logger.info("Flag {flag} was submitted with the following args({args}) and kwargs({kwargs})".format(
        flag=flag, args=args, kwargs=kwargs))
    event.add_event_SUBMIT(flag, 'DUMMY')


@app.task(ignore_result=True)
def send_udp(flag, host='127.0.0.1', port=4223, msg=None):
    if msg is None:
        msg = "{flag}\n"
    DATA=msg.format(flag=flag)
    logger.debug("sending flag '{data}' to ({host}, {port})".format(data=DATA, host=host, port=port))
    _UDPSOCK.sendto(bytes(DATA, 'utf-8'), (host, port))