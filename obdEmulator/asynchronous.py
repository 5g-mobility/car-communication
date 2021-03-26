
import time
import threading
from .obd import OBD

""" class to make asynchronous querys """
class Async(OBD):

    def __init__(self, delay_cmds=0.25):
        super().__init__()
        self.thread = None
        self.__commands = {}
        self.__callbacks = {}
        self.__running = False
        self.__was_running = False
        self.__delay_cmds = delay_cmds