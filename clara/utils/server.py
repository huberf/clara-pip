import os
import json
from flask import json
from flask import jsonify
from flask import Flask
from flask import request
import queue

app = Flask(__name__)
messageQueue = queue.Queue()
sessionMessages = {}
handler = None

@app.route("/")
def main():
    return "Personal Clara instance."

@app.route("/converse", methods=['POST'])
@app.route("/api/v1/send/<int:session_id>", methods=['POST'])
def parse_request(session_id=None):
    try:
        text = json.dumps(request.json)
        message = request.json('input')
    except:
        message = request.form['input']
    message = message.lower()
    if session_id == None:
        messageQueue.put(message)
    else:
        try:
            sessionMessages[session_id].put(message)
        except:
            sessionMessages[session_id] = queue.Queue()
            sessionMessages[session_id].put(message)
    return json.dumps({ 'success': True })

@app.route("/getresponse", methods=['GET'])
@app.route("/api/v1/get/<int:session_id>", methods=['GET'])
def handle_retrieval(session_id=None):
    response = handler.get_response(session_id)
    if response == None:
        return '{"message": "None", "new": "false"}'
    else:
        return '{"message": "' + response + '", "new": "true"}'


def set_handler(obj):
    global handler
    handler = obj

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2525))
    app.run(host='0.0.0.0', port=port, debug=True)
