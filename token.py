#
class Token:
    def __init__(self, code, attr=None):
        self.code = code
        self.attr = attr

    def __str__(self):
        if self.attr is None:
            return ("<%s>" %self.code)
        else:
            return ("<%s, %s>" %(self.code, self.attr))

