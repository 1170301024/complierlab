#
class token:
    def __init__(self, lexunit, value=None):
        self.lexunit = lexunit
        self.value=value
    def __str__(self):
        if self.value == None:
            return (self.lexunit)
        else:
            return (self.lexunit, )

