from datasources.air_quality import fetch_air_quality
from datasources.weather import fetch_weather

def validate_prediction(intelligence, geo):
    """
    Compares Gemini prediction with observed outcomes.
    Returns error metrics + suggested adjustments.
    """

    # Fetch "observed" data (dummy replay in your case)
    air = fetch_air_quality()

    # Grab first PM2.5 reading as observed value
    observed_pm25 = None
    try:
        for r in air["results"]:
            for m in r["measurements"]:
                if m["parameter"] == "pm25":
                    observed_pm25 = m["value"]
                    break
    except Exception:
        observed_pm25 = None

    # Simple heuristic: expected severity from Gemini
    predicted_impact = intelligence.get("impact", "UNKNOWN")

    # Map impact → expected PM2.5 range (very rough)
    expected_ranges = {
        "LOW": (0, 100),
        "MEDIUM": (100, 200),
        "HIGH": (200, 500)
    }

    expected_min, expected_max = expected_ranges.get(predicted_impact, (0, 500))

    error = 0.0
    if observed_pm25 is not None:
        if observed_pm25 < expected_min:
            error = (expected_min - observed_pm25) / expected_min
        elif observed_pm25 > expected_max:
            error = (observed_pm25 - expected_max) / expected_max
        else:
            error = 0.05  # small nominal error if within band

    # Suggest adjustments (symbolic — you’ll log these)
    adjustments = []

    if error > 0.2:
        adjustments.append("Increase weight of AQI anomaly detection")
        adjustments.append("Increase confidence calibration")

    result = {
        "observed_pm25": observed_pm25,
        "predicted_impact": predicted_impact,
        "error_percent": round(error * 100, 2),
        "suggested_adjustments": adjustments
    }

    return result
