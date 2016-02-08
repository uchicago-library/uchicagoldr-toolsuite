

class LDRError(object):
    message =""
    category = ""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "{}:{}".format(self.category, self.message)

    def get_message(self):
        return self.message

    def get_categoy(self):
        return self.category

class LDRNonFatal(LDRError):
    message = ""
    category = "non-fatal"

    def __init__(self, message):
        self.message = message
        self.category = "non-fatal"

class LDRFatal(LDRError):
    message = ""
    category = "fatal"

    def __init__(self, ex=None):
        if ex is not None:
            self.message = "{}: {}".format(type(ex), str(ex))
            if isinstance(ex, Exception):
                self.message = self.message + ex.__repr__()
        else:
            self.message = message
        self.category = "fatal"