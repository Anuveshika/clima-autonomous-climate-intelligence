import json
import os

BASE_DIR = os.path.dirname(__file__)
PATH = os.path.join(BASE_DIR, "dummy", "rivers.json")

def fetch_river_levels():
    with open(PATH) as f:
        return json.load(f)

#import requests

#def fetch_river_levels():
#    url = "https://waterservices.usgs.gov/nwis/iv/?format=json"

#   try:
#       return requests.get(url, timeout=30).json()
#    except:
#       return {}
