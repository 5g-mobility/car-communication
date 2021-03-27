import time
from .commands import commands

"""
Object returned by the query() function
"""
class OBDResponse:
    def __init__(self, value=None, command=None):
        self.value = value
        self.command = command
        self.time = time.time()

    # TODO
    @property
    def unit(self):
        pass

    def is_null(self):
        return self.value is None

    def __str__(self):
        return str(self.value)