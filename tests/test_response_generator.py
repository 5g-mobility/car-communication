import pytest
from obd_emulator.response_generator import ResponseGenerator

@pytest.fixture
def generator():
    return ResponseGenerator()

# test update sun method
def test_update_sun(generator):
    """ fail if the api returns a code different from OK"""
	
    generator.update_params(("52.52364029919217", "13.400111802078426"))

    response = generator.update_sun()
    assert response['status'] == 'OK'
    assert response['results']['sunrise'] is not None
    assert response['results']['sunset'] is not None


# test update weather method
def test_fog_lights(generator):
    """ There isn\'t any param that can be used to check the integrity of the response
        so, this test just checks if the response arrives and has the
        necessary params that allows the update
    """
    generator.update_params(("52.52364029919217", "13.400111802078426"))

    response = generator.update_weather()
    assert  response['data'][0]['vis'] is not None
    assert  response['data'][0]['precip'] is not None

# test geocoder
# def test_geocoder(generator):
#     assert generator.get_location().status == 'OK'
