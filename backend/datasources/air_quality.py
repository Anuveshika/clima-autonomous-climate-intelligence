import json
import os

BASE_DIR = os.path.dirname(__file__)
PATH = os.path.join(BASE_DIR, "dummy", "air_quality.json")

def fetch_air_quality():
   with open(PATH) as f:
       return json.load(f)

#import requests

#def fetch_air_quality():

#    url = "https://api.openaq.org/v2/latest?limit=25"

#    try:
#        return requests.get(url, timeout=30).json()
#    except:
#       return {}
