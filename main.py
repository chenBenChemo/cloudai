import base64, json, os
from flask import Flask, request
from app.agent import root_agent
from google.adk.runners.local_runner import LocalRunner

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handler():
    envelope = request.get_json()
    payload = base64.b64decode(envelope["message"]["data"]).decode("utf-8")
    data = json.loads(payload)

    runner = LocalRunner(root_agent)
    result = runner.run(f"Process complaint for Order {data['order_id']} and image {data.get('image_uri')}")
    return result, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
