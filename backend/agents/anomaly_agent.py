def detect_anomaly(snapshot):

    anomalies = []

    air = snapshot["air"]["results"][0]
    fires = snapshot["fires"]
    rivers = snapshot["rivers"]
    weather = snapshot["weather"]

    # ---- AQI SAFE EXTRACTION ----
    series = air.get("pm25", [])
    pm25 = series[-1] if series else 0

    if pm25 > 180:
        anomalies.append("AIR_POLLUTION")

    # ---- FIRE CLUSTER ----
    if len(fires) >= 2:
        anomalies.append("WILDFIRE_CLUSTER")

    # ---- FLOOD ----
    for r in rivers:
      if isinstance(r, dict) and r.get("alert"):
        anomalies.append("FLOOD_RISK")


    # ---- WEATHER ----
    if weather.get("temperature", 0) > 40:
        anomalies.append("HEATWAVE")

    if weather.get("rainfall", 0) > 50:
        anomalies.append("EXTREME_RAIN")

    if anomalies:
        return {
            "type": "COMPOUND_EVENT",
            "signals": list(set(anomalies))
        }

    return None
