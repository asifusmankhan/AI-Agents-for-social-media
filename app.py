from flask import Flask, jsonify, request
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/")
def home():
    return jsonify({"status": "running", "channel": "@asif92343"})

@app.route("/test")
def test():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return jsonify({"key_found": True, "preview": key[:14]})
    return jsonify({"key_found": False, "error": "No API key found"})

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        res = jsonify({"status": "ok"})
        res.headers.add("Access-Control-Allow-Origin", "*")
        res.headers.add("Access-Control-Allow-Headers", "Content-Type")
        res.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return res
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        res = jsonify({"result": message.content[0].text})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res
    except Exception as e:
        res = jsonify({"error": str(e)})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
