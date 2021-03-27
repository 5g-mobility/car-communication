import time
import geocoder
import requests
import datetime

class ResponseGenerator:

    def __init__(self):
        self.sunrise = None
        self.sunset = None
        self.weather = None
        self.rain_probability = None
        self.update_sun()
        self.update_weather()
        self.last_update = datetime.datetime.utcnow()

    def update_sun(self):
        g = geocoder.ip('me')
        lat = g.latlng[0]
        lng = g.latlng[1]
        data = self.request_json('https://api.sunrise-sunset.org/json', dict(lat=lat, lng=lng))
        self.sunrise = datetime.datetime.strptime(data['results']['sunrise'], '%I:%M:%S %p')
        self.sunset = datetime.datetime.strptime(data['results']['sunset'], '%I:%M:%S %p')
        print(self.sunrise)
        print(self.sunset)

    def update_weather(self):
        return True

    def get_light_sendor(self):
        return True

    def get_fog_light_sendor(self):
        return True
    
    def get_rain_sendor(self):
        return True

    def request_json(self, url, params):
        resp = requests.get(url=url, params=params)
        return resp.json()

    