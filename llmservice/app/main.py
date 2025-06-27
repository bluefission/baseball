import os
import logging
from datetime import datetime
from flask import Flask, request, send_file, jsonify, Response
from dotenv import load_dotenv
import torch
import io
import json
import re
import base64
import requests
import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from inference.llama_infer import run_generate_response
from huggingface_hub import login, HfApi
from utils.json_extractor import extract_json_from_text, validate_json_response
from concurrent.futures import ThreadPoolExecutor

print("🔍 sys.path:", sys.path)

# Create a logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Format log filename with timestamp
log_file = f"logs/run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Clear existing Flask/Werkzeug logging handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging
logging.basicConfig(
    filename=log_file,
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# print("Setup Logging")
# Optional: also show logs on the console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

logging.info("🚀 Script started")

# print("Assign Constants")
HF_TOKEN = os.getenv("HF_TOKEN")
DEVICE = os.getenv("DEVICE", "cuda")

# login(HF_TOKEN)
# print("Hugging Face")
logging.info("Starting HuggingFace login")
api = HfApi(token=HF_TOKEN)
# print("Getting the user")
logging.info("Calling whoami()")
try:
    user = api.whoami()
    # print("User verified")
    # logging.info(f"HF user verified: {user}")
except Exception as e:
    # print("Login error")
    logging.warning(f"Hugging Face whoami() failed or timed out: {str(e)}")
    user = {"name": "unknown"}
# logging.info(f"Logged in as: {user}")


# logging.info("Model loaded.")
# torch.set_grad_enabled(False)
# torch.backends.cudnn.benchmark = True
# generator._model = generator._model.to(memory_format=torch.channels_last).half()


# We'll be using this later like
#   future = executor.submit(generate_response, request.json)
# in the summary path...
# executor = ThreadPoolExecutor(max_workers=2)

def is_prompt_invalid(prompt: str) -> bool:
    # prompt is not zero length
    if not prompt or len(prompt.strip()) == 0:
        return True
    return False

app = Flask(__name__)

@app.before_request
def log_request_start():
    request.start_time = datetime.now()

@app.after_request
def log_request_end(response):
    duration = (datetime.now() - request.start_time).total_seconds()
    logging.info(f"Request to {request.path} took {duration:.2f}s and returned {response.status}")
    return response

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Inference API is running"})

@app.route("/summary", methods=["POST"])
def summary():
    try:
        data = request.get_json()

        prompt = data.get("prompt")
        summary = ""

        if not prompt:
            logging.info(f"Missing 'prompt' in request")
            output = jsonify({"error": "Missing 'prompt' in request"})
            if isinstance(output, Response):
                try:
                    logging.info("Returning response payload: " + json.dumps(output.get_json(), indent=2))
                except Exception as e:
                    logging.warning(f"Could not serialize response: {e}")
            else:
                try:
                    logging.info("Returning response: " + json.dumps(output, indent=2))
                except Exception as e:
                    logging.warning(f"Failed to log output: {e}")

            return output, 400;

        # in /summary
        if is_prompt_invalid(prompt):
            logging.warning(f"Detected empty or malformed prompt:\n{prompt}")
            return jsonify({
                "summary": "No Summary Generated",
                "strengths": "",
                "weaknesses": "",
                "strategy": "",
            }), 200

        # Step 1: Run LLaMA inference (with retry if needed)
        attempts = 2
        llm_output = ""
        parsed = None

        # if reassess:
        #     summary 

        for attempt in range(attempts):
            logging.info(f"Attempt {attempt+1}: Generating LLM output...")
            llm_output = run_generate_response(prompt)
            logging.info(f"LLM raw output:\n{llm_output}")
            try:
                # parsed = extract_json_from_text(llm_output)
                # parsed = json.dumps(llm_output)
                parsed = llm_output
                logging.info(f"Extracted JSON: {parsed}")
                validate_json_response(parsed)
                break
            except Exception as e:
                logging.debug(f"Attempt {attempt + 1} failed to parse LLM output:")
                logging.debug(f"Raw output:\n{llm_output}")
                logging.debug(f"Error: {str(e)}")

                if attempt == attempts - 1:
                    logging.exception("Error occurred in /summary route:")
                    output = jsonify({
                        "error": f"Failed to extract valid JSON: {str(e)}",
                        "llm_output": llm_output
                    })
                    if isinstance(output, Response):
                        try:
                            logging.info("Returning response payload ❓: " + json.dumps(output.get_json(), indent=2))
                        except Exception as e:
                            logging.warning(f"Could not serialize response: {e}")
                    else:
                        try:
                            logging.info("Returning response: " + json.dumps(output, indent=2))
                        except Exception as e:
                            logging.warning(f"Failed to log output: {e}")

                    return output, 500

                # Retry with correction-based feedback
                correction_instruction = f"""
You previously responded with the following incorrect output, which could not be parsed as valid JSON:
{llm_output}

Correct it now. You must respond ONLY with a single-line JSON object in this exact format:
{{"summary": "...", "strategy": "..."}}

No markdown. No explanations. No example formatting. Just the JSON. Retry:
""".strip()
                prompt += "\n\n" + correction_instruction

        # if not parsed.get("summary") or not parsed.get("strategy"):
        if "summary" not in parsed or "strategy" not in parsed:
            logging.info(f"Indeterminate response (missing summary or strategy)")
            output = jsonify({
                "summary": "No Summary Generated",
                "strengths": "",
                "weaknesses": "",
                "strategy": "",
            })
            if isinstance(output, Response):
                try:
                    logging.info("Returning response payload 👎🏽: " + json.dumps(output.get_json(), indent=2))
                except Exception as e:
                    logging.warning(f"Could not serialize response: {e}")
            else:
                try:
                    logging.info("Returning response: " + json.dumps(output, indent=2))
                except Exception as e:
                    logging.warning(f"Failed to log output: {e}")

            return output, 200

        summary = parsed.get("summary", "")
        strengths = parsed.get("strengths", "")
        weaknesses = parsed.get("weaknesses", "")
        strategy = parsed.get("strategy", "")

        output = jsonify({
            "summary": summary,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "strategy": strategy,
        })

        # for right now, forego the audio
        return output, 200

    except Exception as e:
        logging.exception("Error occurred in /summary route:")
        output = jsonify({"error": str(e)})
        if isinstance(output, Response):
            try:
                logging.info("Returning response payload ❌: " + json.dumps(output.get_json(), indent=2))
            except Exception as e:
                logging.warning(f"Could not serialize response: {e}")
        else:
            try:
                logging.info("Returning response: " + json.dumps(output, indent=2))
            except Exception as e:
                logging.warning(f"Failed to log output: {e}")

        return output, 500

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        logging.exception("Unhandled exception occurred:")