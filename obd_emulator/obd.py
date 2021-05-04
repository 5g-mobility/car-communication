
"""
Class with the main functionalities
"""
import time
import random
import datetime
from .commands import commands
from .response_generator import ResponseGenerator
from .OBDResponse import OBDResponse



class OBDEmulator:

    def __init__(self, generator):
        print('Magic connection made with sucess. Ready to emulate')
        self.init_time = datetime.datetime.now()
        self.response_generator = generator
        self.__last_command = None

    def update_location(self, location):
        pass
        # self.response_generator.update_params(location)

    def close(self):
        print('Closing connection...')

    """ make query to car """
    def query(self, command, location=None):
        self.__last_command = command

        if command == commands.RPM:
            return OBDResponse(random.randint(0, 8000), command)
        elif command == commands.SPEED:
            return OBDResponse(random.randint(0, 175), command)
        elif command == commands.RUN_TIME:
            return OBDResponse(divmod((datetime.datetime.now()-self.init_time).total_seconds(), 60)[1], command)
        elif command == commands.AMBIENT_AIR_TEMP:
            # return OBDResponse(self.response_generator.get_ambient_air_temp(), command)
            return OBDResponse(20, command)
        elif command == commands.LIGHT_SENSOR:
            # self.response_generator.get_light_sensor()
            return OBDResponse(True, command)
        elif command == commands.FOG_LIGHTS:
            # self.response_generator.get_fog_light_sensor()
            return OBDResponse(False, command)
        elif command == commands.RAIN_SENSOR:
            # self.response_generator.get_rain_sensor()
            return OBDResponse(False, command)
        elif command == commands.CO2_EMISSIONS:
            return OBDResponse(random.uniform(60, 300), command)
        else:
            print('Unknown command')
            return OBDResponse()
        
