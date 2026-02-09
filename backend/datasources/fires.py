import json
import os

BASE_DIR = os.path.dirname(__file__)
DUMMY_PATH = os.path.join(BASE_DIR, "dummy", "fires.json")

def fetch_fire_data():
    """
    Loads dummy fire hotspot data.
    """

    with open(DUMMY_PATH, "r") as f:
       return json.load(f)
