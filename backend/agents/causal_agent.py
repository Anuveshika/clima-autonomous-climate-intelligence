import json
import re
import time
import random
from gemini.client import call_gemini
from gemini.climate_prompts import ROOT_CAUSE_PROMPT


def extract_json(text):
    text = text.replace("```json", "").replace("```", "")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group() if match else None


def infer_cause(snapshot, max_retries=3):

    prompt = ROOT_CAUSE_PROMPT.format(
        air=snapshot["air"],
        fires=snapshot["fires"],
        weather=snapshot["weather"],
        rivers=snapshot["rivers"],
        geo=snapshot["geo"],
        signals=snapshot.get("anomaly_signals", [])
    )

    for attempt in range(max_retries):
        try:
            raw = call_gemini(prompt)

            print("\n--- RAW GEMINI RESPONSE ---")
            print(raw)

            json_text = extract_json(raw)
            if not json_text:
                raise ValueError("No JSON found in Gemini output")

            return json.loads(json_text)

        except Exception as e:
            wait = (2 ** attempt) + random.uniform(0.5, 1.5)
            print(f"Gemini failed (attempt {attempt+1}), retrying in {round(wait,1)}s...")
            time.sleep(wait)

    print("Gemini permanently failed after retries.")
    return None
