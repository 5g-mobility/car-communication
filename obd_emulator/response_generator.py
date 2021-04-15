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
        self.precipitation_rate = None
        self.location = None
        self.last_update = None
        self.temp = None
        self.update_all()
    
    def update_all(self):
        self.get_location()
        self.update_sun()
        self.update_weather()
        self.last_update = datetime.datetime.now()
        # Updates every hour
        if 'ENVIRONMENT' in os.environ and os.environ.get('ENVIRONMENT') == 'github-actions':
            pass
        else:
            t = threading.Timer(3600, self.update_all)
            # allows the thread to be stoped
            t.daemon = True
            t.start()

    # update the location using geocoder
    def get_location(self):
        g = geocoder.ip('me')
        self.location = g.latlng

        return g


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

            data = self.request_json('https://api.weatherbit.io/v2.0/current', dict(lat=self.location[0], lon=self.location[1], key = "ef58b324228248f6a49385a2d6cd58f8"))
            times += 1

        self.visibility = data['data'][0]['vis']
        self.precipitation_rate = data['data'][0]['precip']
        self.temp = data['data'][0]['temp']

        return data

    def get_light_sensor(self):
        now = datetime.datetime.now()
        if now < self.sunset and now > self.sunrise:
            return True
        else:
            return False
        
        return False

    def get_fog_light_sensor(self):
        if self.visibility <= 1:
            return True
        return False
    
    def get_rain_sensor(self):
        if self.precipitation_rate > 0:
            return True
        return False

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

