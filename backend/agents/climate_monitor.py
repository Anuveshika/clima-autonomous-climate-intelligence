from datasources.fires import fetch_fire_data
from datasources.air_quality import fetch_air_quality
from datasources.weather import fetch_weather
from datasources.rivers import fetch_river_levels

from agents.anomaly_agent import detect_anomaly
from agents.causal_agent import infer_cause
from agents.response_agent import generate_response
from agents.validation_agent import validate_prediction
from graphs.climate_graph import ClimateGraph

from state import latest_result
import json
import hashlib

CAUSE_CACHE = {}

def anomaly_fingerprint(snapshot):
    payload = {
        "air": snapshot["air"],
        "fires": snapshot["fires"],
        "weather": snapshot["weather"],
        "rivers": snapshot["rivers"],
        "signals": snapshot.get("anomaly_signals", [])
    }

    blob = json.dumps(payload, sort_keys=True)
    return hashlib.md5(blob.encode()).hexdigest()

async def run_climate_cycle():

    print("\nRunning CLIMA cycle...")

    air = fetch_air_quality()

    coord = air["results"][0]["coordinates"]
    lat = coord["latitude"]
    lon = coord["longitude"]

    fires = fetch_fire_data()
    weather = fetch_weather(lat, lon)
    rivers = fetch_river_levels()

    snapshot = {
        "air": air,
        "fires": fires,
        "weather": weather,
        "rivers": rivers,
        "geo": {"lat": lat, "lon": lon}
    }

    anomaly = detect_anomaly(snapshot)

    #if not anomaly:
    #  print("No anomaly detected.")
    #return

    snapshot["anomaly_signals"] = anomaly["signals"]


    if not anomaly:
        print("No anomaly detected.")
        return

    print("Anomaly detected:", anomaly["type"])
    
    #adding anomaly fingerprint and gemini result cache
    fp = anomaly_fingerprint(snapshot)

    if fp in CAUSE_CACHE:
      print("Using cached Gemini result")
      intelligence = CAUSE_CACHE[fp]
    else:
      intelligence = infer_cause(snapshot)
    if intelligence:
        CAUSE_CACHE[fp] = intelligence


    if not intelligence:
        print("Gemini reasoning failed.")
        return

    print("\n=== INCIDENT INTELLIGENCE ===")
    print(intelligence)

    graph = ClimateGraph()
    graph.build_from_chain(intelligence["causal_chain"])

    print("\n=== CAUSAL GRAPH ===")
    print(graph.to_dict())

    response = generate_response(intelligence)

    print("\n=== RESPONSE PLAN ===")
    print(response)

    validation = validate_prediction(intelligence, snapshot["geo"])

    print("\n=== VALIDATION RESULTS ===")
    print(validation)

    # IMPORTANT: mutate shared dict
    latest_result.clear()
    latest_result.update({
        "intelligence": intelligence,
        "graph": graph.to_dict(),
        "response": response
    })
