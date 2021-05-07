import time
import datetime
import requests
import time
import sys
import random
import os

from geopy.geocoders import Nominatim

class ResponseGenerator:

    def __init__(self):
        self.sunrise = None
        self.sunset = None
        self.visibility = None
        self.precipitation = None
        self.location = None
        self.last_update = None
        self.temp = None

        # the generator needs to have a dictionary with all the coordinates requested
        # only makes request if the coordinate isn't stored

        # coordinates : (timestamp, sun_api_response, weather_api_response)
        self.cache = {}
        self.geolocator = Nominatim(user_agent="OBD2_Generator")
        self.requests_answered_by_cache = 0


    def update_params(self, location):

        self.location = location
        # receives a location
        # if the location was already requested and it hasn't passed 5 minutes since the last update
        # the answer will be computed using stored responses from api
        
        # TODO verify if the number of requests to this api is to much
        # and if errors do not occur
        region = self.get_region_number(location)

        if not region in self.cache or (time.time() - self.cache[region][0]) > 300: # 5 minutes = 300 seconds
            # else
            # make a request to the api
            # save the information on cache
            
            self.cache[region] = (time.time() , self.update_sun(), self.update_weather())
            return

        # update params on this object with the response stored on cache
        self.update_params_with_cache(region)
        self.requests_answered_by_cache += 1

    def update_sun(self):
        times = 0
        data = None
        while not data:
            if times == 3:
                sys.exit('Couldn\'t refresh params. Api not working')

            data = self.request_json('https://api.sunrise-sunset.org/json', dict(lat=self.location[0], lng=self.location[1], formatted=0))
            times += 1
        
        self.sunrise = datetime.datetime.strptime(data['results']['sunrise'], '%Y-%m-%dT%H:%M:%S+00:00')
        self.sunset = datetime.datetime.strptime(data['results']['sunset'], '%Y-%m-%dT%H:%M:%S+00:00')

        return data

    def update_weather(self):
        times = 0
        data = None
        while not data:
            if times == 3:
                sys.exit('Couldn\'t refresh params. Api not working')
            # http://api.openweathermap.org/data/2.5/weather?lat=36.1659&lon=-86.7844&appid=00ae9df8c755778aea621c4543cf6b25&units=metric
            data = self.request_json('http://api.openweathermap.org/data/2.5/weather',
                                            dict(lat=self.location[0],
                                                lon=self.location[1],
                                                appid="00ae9df8c755778aea621c4543cf6b25",
                                                units="metric"))
            times += 1

        self.visibility = data['visibility']
        
        try:
            # if the rain field exists on the response it means that it is raining
            self.precipitation = data['rain']['1h']
        except KeyError:
            # otherwise, it is not raining
            self.precipitation = None

        self.temp = data['main']['temp']

        return data

    def get_light_sensor(self):
        now = datetime.datetime.now()
        if now < self.sunset and now > self.sunrise:
            return True
        else:
            return False
        
        return False

    def get_fog_light_sensor(self):
        # this measure comes in meters, so we are considering that if a person
        # can not see more than 300 meters forward, in that case there is fog

        return self.visibility <= 300
    
    def get_rain_sensor(self):
        return True if self.precipitation else False

    def get_ambient_air_temp(self):
        max = self.temp + 1.5
        min = self.temp - 1.5
        return random.uniform(min, max)

    def request_json(self, url, params):
        try:
            resp = requests.get(url=url, params=params)
        except requests.exceptions.RequestException:
            return None

        if resp.status_code != 200:
            return None
        
        return resp.json()

    def get_region_number(self, location):
        try:
            address = self.geolocator.reverse(f'{location[0]}, {location[1]}').address
        except Exception as e:
            print(f'Error finding region: {e}')
            return
        
        # return the first 4 digits of the postal code
        return address.split(',')[-2].strip().split('-')[0]

    def update_params_with_cache(self, region):
        cache_data = self.cache[region]
        self.sunrise = datetime.datetime.strptime(cache_data[1]['results']['sunrise'], '%Y-%m-%dT%H:%M:%S+00:00')
        self.sunset = datetime.datetime.strptime(cache_data[1]['results']['sunset'], '%Y-%m-%dT%H:%M:%S+00:00')

        self.visibility = cache_data[2]['visibility']

        try:
            # if the rain field exists on the response it means that it is raining
            self.precipitation = cache_data[2]['rain']['1h']
        except KeyError:
            # otherwise, it is not raining
            self.precipitation = None

        self.temp = cache_data[2]['main']['temp']
