class FlagException(Exception):
    def __init__(self, flag, text):
        super(FlagException, self).__init__(text)
        self.flag = flag
        self.reason = 'Unknown'


class MalformedFlagException(FlagException):
    def __init__(self, flag, constraint_notes=None):
        text = "Flag '{flag}' does not match the constraints on flag format".format(flag=flag)
        if constraint_notes is not None:
            text = "{text} ({constraint_notes})".format(text=text, constraint_notes=constraint_notes)
        super(MalformedFlagException, self).__init__(flag, text)
        self.reason = 'malformedFlag'


class DuplicateFlagException(FlagException):
    def __init__(self, flag, src):
        super(DuplicateFlagException, self).__init__(flag, "Duplicate flag: '{flag}'".format(flag=flag))
        self.reason = 'duplicateFlag'
        self.source = src