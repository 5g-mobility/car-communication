import time
import geocoder
import datetime
import requests
import time
import threading
import sys
import random
import os

class ResponseGenerator:

    def __init__(self):
        self.sunrise = None
        self.sunset = None
        self.visibility = None
        self.precipitation = None
        self.location = None
        self.last_update = None
        self.temp = None

        # TODO
        # the generator needs to have a list with all the coordinates requested
        # only makes request if the coordinate isn't stored

        #self.update_all()


    def update_params(self, location):

        # receives a location
        # answers with a stored message if the location has already been requested

        self.location = location

        self.update_sun()
        self.update_weather()



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

