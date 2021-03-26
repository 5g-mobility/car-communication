
"""
Class with the main functionalities
"""
import time
from .commands import commands

class OBD:

    def __init__(self):
        print('Magic connection made with sucess. Ready to emulate')
        self.__last_command = None

    def close(self):
        print('Closing connection...')

    """ make query to car """
    def query(self, command):
        if command == commands.RPM:
            print('rpm')
            return 'rpm'
        elif command == commands.SPEED:
            print('speed')
            return 'speed'
        elif command == commands.RUN_TIME:
            print('run_time')
            return 'run_time'
        elif command == commands.AMBIANT_AIT_TEMP:
            print('ambient_air_temp')
            return 'ambient_ait_temp'
        else:
            print('Unknown command')
        
        time.sleep(0.5)
        
