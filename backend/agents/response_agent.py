import json
import re
from gemini.client import call_gemini


def extract_json(text):
    text = text.replace("```json", "").replace("```", "")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group() if match else None


RESPONSE_PROMPT = """
You are CLIMA Response Planner.

Incident:
{incident}

Causal Chain:
{chain}

Impact:
{impact}

Return STRICT JSON ONLY:

{{
 "severity":"",
 "citizen_advisory":"",
 "mitigation_steps":[],
 "gov_brief":""
}}
"""

def generate_response(intelligence):

    raw = call_gemini(RESPONSE_PROMPT.format(
        incident=intelligence.get("incident_type"),
        chain=intelligence.get("causal_chain"),
        impact=intelligence.get("impact")
    ))

    json_text = extract_json(raw)
    if not json_text:
        return None

    return json.loads(json_text)
