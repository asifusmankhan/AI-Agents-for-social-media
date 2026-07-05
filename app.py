from flask import Flask, jsonify, request
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route('/')
def home():
    return jsonify({"status": "running", "channel": "@asif92343"})

@app.route('/test')
def test():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return jsonify({"key_found": True, "preview": key[:14]})
    else:
        return jsonify({"key_found": False, "error": "No API key found in environment"})

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    try:
        data = request.json
        prompt = data.get('prompt', '')
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        response = jsonify({"result": message.content[0].text})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as
