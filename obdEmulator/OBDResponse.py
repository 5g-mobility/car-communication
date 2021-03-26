"""
Object returned by the query() function
"""
class OBDResponse:
    def __init__(self, value=None, command=None, message=None, time=None):
        self.value = value
        self.command = command
        self.message = message
        self.time = time

    def is_null(self):
        if self.value is None:
            return True