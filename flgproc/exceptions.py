class IllegalFlagException(Exception):
    def __init__(self, flag, pattern):
        super(IllegalFlagException, self).__init__(
            "Flag '{flag}' does not match the tournaments flag pattern '{pattern}'".format(flag=flag, pattern=pattern))


class DuplicateFlagException(Exception):
    def __init__(self, flag):
        super(DuplicateFlagException, self).__init__("Duplicate flag: '{flag}'".format(flag))