import json
import re

def extract_json_from_text(text: str) -> dict:
    try:
        # Remove markdown/code fencing
        text = re.sub(r"^```.*?```$", "", text, flags=re.DOTALL | re.MULTILINE)

        # Match first valid JSON object
        match = re.search(r"\{[\s\S]*?\}", text)
        if not match:
            raise ValueError("No JSON object found in LLM output.")

        return json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"JSON extraction failed: {str(e)}")

def validate_json_response(data: dict):
    if not isinstance(data, dict):
        raise ValueError("Parsed output is not a dictionary.")
    if "summary" not in data or "strategy" not in data:
        raise ValueError("Missing required keys: 'summary' and 'strategy'.")
