import re

from flgproc.exceptions import IllegalFlagException
from flgproc import conf


def regex(flag, pattern=conf.FLAG_PATTERN):
    if re.fullmatch(pattern, flag) is None:
        raise IllegalFlagException(flag, pattern)
    return flag