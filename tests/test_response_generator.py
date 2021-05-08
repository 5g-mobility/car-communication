import pytest
from obd_emulator.response_generator import ResponseGenerator
import datetime

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


# deactivated beacause of static coordinates
# test the region code returned when a location is given
# def test_return_region_number(generator):
#     code = generator.get_region_number(("40.74281077429823", "-8.637725758763903"))
    
#     assert code == '3870'

def test_get_region(generator):
    coordinate = generator.get_region(("40.74281077429823", "-8.637725758763903"))

    assert coordinate == ('40.7', '-8.6')

def test_cache(generator):
    generator.update_params(('40.6133935543361', '-8.750542788093933'))

    # verify if the region code was inserted on cache
    assert ('40.6', '-8.7') in generator.cache

    # check if code to first api is working
    assert generator.sunrise is not None

    # check if code to second api is working
    assert generator.temp is not None

    # no requests aswered by cache
    assert generator.requests_answered_by_cache == 0

    generator.update_params(('40.643456900921315', '-8.74092771495921'))

    # verify that cache updated the params
    assert generator.requests_answered_by_cache == 1

    # sunrise was updated correctly
    assert isinstance(generator.sunrise, datetime.datetime)
    
    # temp was updated correctly
    assert isinstance(generator.temp, float)