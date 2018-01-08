import requests as r
import json
import queue
# Local imports
from .server import app

class ClaraIO:
    def get(self):
        text = input("> ");
        return text

    def put(self, text):
        print(text)

class WebIO(ClaraIO):
    flaskApp = None
    def __init__(self):
        ClaraIO.__init__(self)
        #flaskApp = server.app
        flaskApp = app
        port = 3000
        flaskApp.run(host='0.0.0.0', port=port, debug=True)

    def get(self):
        messageReceived = False
        message = ""
        if not messageReceived:
            messsage = flaskApp.messageQueue.get()
            if not message == None:
                messageReceived = True
        '''
        while not messageReceived:
            contents = json.loads(r.get(getUrl).text)
            if contents['hasMessage'] == True:
                message = contents['message']
                messageReceived = True
        '''
        return message

    def put(self, text):
        # r.post(postUrl, { 'message': text })
        print(text)
