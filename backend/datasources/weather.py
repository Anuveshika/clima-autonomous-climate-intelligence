import json
import os

BASE_DIR = os.path.dirname(__file__)
PATH = os.path.join(BASE_DIR, "dummy", "weather.json")

def fetch_weather(lat=None, lon=None):
    with open(PATH) as f:
       return json.load(f)

#import requests

#def fetch_weather(lat, lon):

#   url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=rain,wind_speed_10m"

#   try:
#       return requests.get(url, timeout=30).json()
#   except:
#       return {}
