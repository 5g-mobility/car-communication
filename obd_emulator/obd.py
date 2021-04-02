
"""
Class with the main functionalities
"""
import time
import random
from .commands import commands
from .response_generator import ResponseGenerator
from .OBDResponse import OBDResponse


class OBDEmulator:

    def __init__(self):
        print('Magic connection made with sucess. Ready to emulate')
        self.response_generator = ResponseGenerator()
        self.__last_command = None

    def start_monitoring():
        self.response_generator.update_all()

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
        elif command == commands.AMBIANT_AIR_TEMP:
            return OBDResponse(random.randint(10, 35), command)
        elif command == commands.LIGHT_SENSOR:
            return OBDResponse(self.response_generator.get_light_sensor(), command)
        elif command == commands.FOG_LIGHTS:
            return OBDResponse(self.response_generator.get_fog_light_sensor(), command)
        elif command == commands.RAIN_SENSOR:
            return OBDResponse(self.response_generator.get_rain_sensor(), command)
        elif command == commands.AVG_CONSUMPTION:
            return OBDResponse(random.uniform(5.0, 15.0), command)
        else:
            print('Unknown command')
            return OBDResponse()
        
