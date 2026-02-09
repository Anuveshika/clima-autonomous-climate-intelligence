import os
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini(prompt):

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(
        f"{url}?key={GEMINI_API_KEY}",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=60
    )

    print("\n=== RAW HTTP STATUS ===")
    print(response.status_code)

    print("\n=== FULL GEMINI RESPONSE ===")
    print(response.text)

    try:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return ""
