import os
import json
from flask import json
from flask import jsonify
from flask import Flask
from flask import request
import queue

app = Flask(__name__)
messageQueue = queue.Queue()
handler = None

@app.route("/")
def main():
    return "Personal Clara instance."

@app.route("/converse", methods=['POST'])
def parse_request():
    try:
        text = json.dumps(request.json)
        message = request.json('input')
    except:
        message = request.form['input']
    message = message.lower()
    messageQueue.put(message)
    return json.dumps({ 'success': True })

@app.route("/getresponse", methods=['GET'])
def handle_retrieval():
    return handler.get_response()

def set_handler(obj):
    global handler
    handler = obj

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2525))
    app.run(host='0.0.0.0', port=port, debug=True)
