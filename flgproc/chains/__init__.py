import traceback

from ELconn import event

from flgproc import app, logger
from flgproc.exceptions import DuplicateFlagException

from flgproc.filter.duplicate import duplicate_elasticsearch
from flgproc.submitter import submit_flag

__all__ = ['dupeCheck_logEvent_submit']


@app.task()
def dupeCheck_logEvent_submit(flag, **add_info):
    try:
        duplicate_elasticsearch(flag)
        event.add_event_ENTRY(flag, **add_info)
        submit_flag.apply_async(args=(flag,))
    except DuplicateFlagException as e:
        event.add_event_DUPLICATE(flag, e.source.name)
    except Exception as e:
        ex = traceback.format_exc()
        event.add_event(flag, exception=ex)
        logger.error(ex)