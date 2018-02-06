import requests as r
from threading import Thread
import json
import queue
# Local imports
from .server import app
from .server import messageQueue
from .server import set_handler

class ClaraIO:
    def get(self):
        text = input("> ");
        return text

    def put(self, text):
        print(text)

class WebIO(ClaraIO):
    flaskApp = None
    messageQueue = None
    responseQueue = queue.Queue()
    def __init__(self):
        ClaraIO.__init__(self)
        #flaskApp = server.app
        self.flaskApp = app
        self.messageQueue = messageQueue
        set_handler(self)
        appThread = Thread(target = self.run)
        appThread.start()

    def run(self):
        port = 3000
        # Allow execution on separate thread by removing debug
        self.flaskApp.run(host='0.0.0.0', port=port, debug=False)

    def get(self):
        messageReceived = False
        message = ""
        if not messageReceived:
            message = self.messageQueue.get()
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

    def get_response(self):
        return self.responseQueue.get()

    def put(self, text):
        self.responseQueue.put(text)
        # r.post(postUrl, { 'message': text })
