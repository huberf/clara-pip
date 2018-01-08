import os
from flask import json
from flask import jsonify
from flask import Flask
from flask import request
import queue

app = Flask(__name__)
messageQueue = queue.Queue()

@app.route("/")
def main():
    return "Personal Clara instance."

@app.route("/converse", methods=['POST'])
def parse_request():
    try:
        text = json.dumps(request.json)
        message = request.json['input']
    except:
        message = request.form['input']
    message = message.lower()
    messageQueue.put(message)
    return { 'success': True }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2525))
    app.run(host='0.0.0.0', port=port, debug=True)
