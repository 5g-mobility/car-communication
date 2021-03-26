
"""
Class with the main functionalities
"""
import time
from .commands import commands
from .OBDResponse import OBDResponse

### TODO APAGAR
import random

class OBD:

    def __init__(self):
        print('Magic connection made with sucess. Ready to emulate')
        self.__last_command = None

    def close(self):
        print('Closing connection...')

    """ make query to car """
    def query(self, command):
        self.__last_command = command

        if command == commands.RPM:
            return OBDResponse(random.randint(0, 8000), command)
        elif command == commands.SPEED:
            return OBDResponse(random.randint(0, 150), command)
        elif command == commands.RUN_TIME:
            return OBDResponse(random.randint(0, 60), command)
        elif command == commands.AMBIANT_AIT_TEMP:
            return OBDResponse(random.randint(10, 35), command)
        else:
            print('Unknown command')
            return OBDResponse()
        
        time.sleep(0.5)
        
