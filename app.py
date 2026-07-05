from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "running", "channel": "@asif92343"})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    return jsonify({"message": "AI Agent is live!", "received": data})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
