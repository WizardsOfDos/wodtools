class FlagException(Exception):
    def __init__(self, flag, text):
        super(FlagException, self).__init__(text)
        self.flag = flag
        self.reason = 'Unknown'


class IllegalFlagException(FlagException):
    def __init__(self, flag, pattern):
        super(IllegalFlagException, self).__init__(flag,
            "Flag '{flag}' does not match the tournaments flag pattern '{pattern}'".format(flag=flag, pattern=pattern))
        self.reason = 'illegalFlag'


class DuplicateFlagException(FlagException):
    def __init__(self, flag):
        super(DuplicateFlagException, self).__init__(flag, "Duplicate flag: '{flag}'".format(flag=flag))
        self.reason = 'duplicateFlag'