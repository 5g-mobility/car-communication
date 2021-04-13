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

	assert r.value >= 0 and r.value <= 3600

# test air temperature
def test_AIR_TEMP(obd):
	r = obd.query(commands.AMBIANT_AIR_TEMP)

	assert r.value >= -20 and r.value <= 50

# test average consumption
def test_AVG_CONSUMPTION(obd):
	r = obd.query(commands.AVG_CONSUMPTION)

	assert r.value >= 5.0 and r.value <= 15.0

# test unknown command
def test_Unknown_Command(obd):
	# using an unknown command raises a AttributeError exception
	# at the commands enumerate
	with pytest.raises(AttributeError):
		obd.query(commands.UNKNOWN)