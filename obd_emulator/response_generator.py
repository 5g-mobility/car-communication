import time
import geocoder
import requests
import datetime
import threading

class ResponseGenerator:

    def __init__(self):
        self.sunrise = None
        self.sunset = None
        self.visibility = None
        self.precipitation_rate = None
        self.location = None
        self.last_update = None
        self.update_all()
    
    def update_all(self):
        g = geocoder.ip('me')
        self.location = g.latlng
        self.update_sun()
        self.update_weather()
        self.last_update = datetime.datetime.utcnow()
        # Updates every hour
        threading.Timer(3600, self.update_all).start()

    def update_sun(self):
        data = self.request_json('https://api.sunrise-sunset.org/json', dict(lat=self.location[0], lng=self.location[1], formatted=0))
        self.sunrise = datetime.datetime.strptime(data['results']['sunrise'], '%Y-%m-%dT%H:%M:%S+00:00')
        self.sunset = datetime.datetime.strptime(data['results']['sunset'], '%Y-%m-%dT%H:%M:%S+00:00')

    def update_weather(self):
        data = self.request_json('https://api.weatherbit.io/v2.0/current', dict(lat=self.location[0], lon=self.location[1], key = "ef58b324228248f6a49385a2d6cd58f8"))
        self.visibility = data['data'][0]['vis']
        self.precipitation_rate = data['data'][0]['precip']

    def get_light_sensor(self):
        now = datetime.datetime.utcnow()
        if now < self.sunrise:
            return True
        return False

    def get_fog_light_sensor(self):
        if self.visibility <= 1:
            return True
        return False
    
    def get_rain_sensor(self):
        if self.precipitation_rate > 0:
            return True
        return False

    def request_json(self, url, params):
        resp = requests.get(url=url, params=params)
        return resp.json()

    