import clara
import requests as r
import os
from flask import json
from flask import jsonify
from flask import Flask
from flask import request

app = Flask(__name__)

telegram_key = ''

@app.route("/")
def main():
    return "Personal Clara instance."

@app.route("/new-message", methods=['POST'])
def handle_message():
    message = request.json
    brain.get_response(message['text'].lower())
    data = {
            'chat_id': message['chat']['id'],
            'text': 'Test'
            }
    url = 'https://api.telegram.org/' + telegram_key + '/sendMessage'
    r.post('', data)
    return 'Thanks!'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2525))
    app.run(host='0.0.0.0', port=port, debug=True)
