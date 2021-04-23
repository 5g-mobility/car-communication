import pytest

from obd_emulator.obd import OBDEmulator
from obd_emulator.commands import commands
from obd_emulator import OBDResponse

@pytest.fixture
def obd():
    return OBDEmulator()

# test rpm
def test_RPM(obd):
    r = obd.query(commands.RPM)

    assert r.value >= 0 and r.value <= 8000

# test speed
def test_SPEED(obd):
	r = obd.query(commands.SPEED)

	assert r.value >= 0 and r.value <= 300

# test run_time
def test_RUN_TIME(obd):
	r = obd.query(commands.RUN_TIME)

	assert r.value >= 0

# test air temperature
def test_AIR_TEMP(obd):
	obd.update_location(("52.52364029919217", "13.400111802078426"))
	r = obd.query(commands.AMBIENT_AIR_TEMP)

	assert r.value >= -20 and r.value <= 50

# test light sensor
def test_Light_Sensor(obd):
	obd.update_location(("52.52364029919217", "13.400111802078426"))
	r = obd.query(commands.LIGHT_SENSOR)

	assert r.value == True or r.value == False

# test fog light sensor
def test_Fog_Lights(obd):
	obd.update_location(("52.52364029919217", "13.400111802078426"))
	r = obd.query(commands.FOG_LIGHTS)

	assert r.value == True or r.value == False

# test Rain sensor
def test_Rain_Sensor(obd):
	obd.update_location(("52.52364029919217", "13.400111802078426"))
	r = obd.query(commands.RAIN_SENSOR)

	assert r.value == True or r.value == False

# test co2 emissions
def test_CO2_EMISSIONS(obd):
	obd.update_location(("52.52364029919217", "13.400111802078426"))
	r = obd.query(commands.CO2_EMISSIONS)

	assert r.value >= 60 and r.value <= 300

# test unknown command
def test_Unknown_Command(obd):
	# using an unknown command raises a AttributeError exception
	# at the commands enumerate
	with pytest.raises(AttributeError):
		obd.query(commands.UNKNOWN)