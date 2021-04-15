from enum import Enum

"""
Enumerate with commands available
"""
class commands(Enum):
    RPM = 12
    SPEED = 13
    RUN_TIME = 31 # It returns in seconds
    AMBIENT_AIR_TEMP = 70
    LIGHT_SENSOR = 00
    FOG_LIGHTS = 10
    RAIN_SENSOR = 11
    CO2_EMISSIONS = 90
