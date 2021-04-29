import pytest
from obd_emulator.response_generator import ResponseGenerator

@pytest.fixture
def generator():
    return ResponseGenerator()

# test update sun method
def test_sunrise_sunset_api(generator):
    """ fail if the api returns a code different from OK"""
	
    generator.update_params(("52.52364029919217", "13.400111802078426"))

    response = generator.update_sun()
    assert response['status'] == 'OK'
    assert response['results']['sunrise'] is not None
    assert response['results']['sunset'] is not None


# test update weather method
def test_openweather_api(generator):
    """ There isn\'t any param that can be used to check the integrity of the response
        so, this test just checks if the response arrives and has the
        necessary params that allows the update
    """
    generator.update_params(("40.8586", "-8.6251"))

    response = generator.update_weather()
    print(response)
    
    assert response['cod'] == 200
    assert response['visibility'] is not None
    assert response['main']['temp'] is not None

# test geocoder
# def test_geocoder(generator):
#     assert generator.get_location().status == 'OK'
