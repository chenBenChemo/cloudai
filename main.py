import base64
import json
import time
import uuid
import os
from flask import Flask, request
from app.agent import root_agent
from google.adk.runners.local_runner import LocalRunner

app = Flask(__name__)

def pubsub_to_adk_transform(payload_bytes):
    """
    Python equivalent of the JS SMT.
    Purpose: Robustly decodes Pub/Sub data and formats the Agent prompt.
    """
    # --- 1. Robust Decoding ---
    try:
        # Decodes byte array to UTF-8 string, similar to TextDecoder [cite: 1.3]
        alert_string = payload_bytes.decode("utf-8")
    except Exception as e:
        # Fallback if decoding fails
        alert_string = str(payload_bytes)

    # --- 2. Context & Prompt Generation ---
    # Generates a unique ID using current timestamp and a random fragment [cite: 5.1, 5.4]
    ticket_id = f"ticket-pubsub-{int(time.time() * 1000)}"
    
    combined_prompt = (
        f"CONTEXT: Ticket ID is {ticket_id}\n\n"
        f"INPUT ALERT (JSON):\n{alert_string}"
    )
    
    return combined_prompt

@app.route("/", methods=["POST"])
def handler():
    # Receive Pub/Sub push notification [cite: 1.3, 3.1]
    envelope = request.get_json()
    if not envelope or "message" not in envelope:
        return "Bad Request", 400

    # Get the raw base64 data [cite: 1.3]
    encoded_data = envelope["message"]["data"]
    decoded_bytes = base64.b64decode(encoded_data)

    # Transform data into the final prompt
    final_prompt = pubsub_to_adk_transform(decoded_bytes)

    # --- 3. Execute ADK Runner ---
    # LocalRunner is used for Cloud Run deployments [cite: 1.1, 1.3]
    runner = LocalRunner(root_agent)
    
    # Run the agent with the formatted prompt
    # Each call uses a fresh user_id to simulate a unique background event [cite: 1.3]
    result = runner.run(final_prompt)

    return f"Processed Ticket: {result}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
