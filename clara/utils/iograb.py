import requests as r
from threading import Thread
import json
import queue
# Local imports
from .server import app
from .server import messageQueue
from .server import sessionMessages
from .server import set_handler

class ClaraIO:
    def get(self):
        text = input("> ");
        return { 'text': text, 'session': None }

    def put(self, text, session_id=None):
        print(text)

class WebIO(ClaraIO):
    flaskApp = None
    messageQueue = None
    sessionMessages = None
    responseQueue = queue.Queue()
    sessionResponses = {}
    def __init__(self):
        ClaraIO.__init__(self)
        #flaskApp = server.app
        self.flaskApp = app
        self.messageQueue = messageQueue
        self.sessionMessages = sessionMessages
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
        return { 'text': message, 'session': None }

    def get_response(self, session_id=None):
        if session_id == None:
            if self.responseQueue.empty():
                return { 'text': None, 'session': None }
            else:
                return { 'text': self.responseQueue.get(), 'session': None }
        else:
            try:
                if self.responseQueue.empty():
                    return { 'text': None, 'session': session_id }
                else:
                    return { 'text': self.responseQueue.get(), 'session': session_id }
            except:
                sessionResponses[session_id] = queue.Queue()
                return { 'text': None, 'session': session_id }

    def put(self, text, session_id=None):
        if session_id == None:
            self.responseQueue.put(text)
        else:
            try:
                sessionResponses[session_id] += [text]
            except:
                sessionResponses[session_id] = []
                sessionResponses[session_id] += [text]
        # r.post(postUrl, { 'message': text })
