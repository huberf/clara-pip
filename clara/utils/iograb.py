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
    port = 3000
    def __init__(self, port):
        ClaraIO.__init__(self)
        #flaskApp = server.app
        self.port = port
        self.flaskApp = app
        self.messageQueue = messageQueue
        self.sessionMessages = sessionMessages
        set_handler(self)
        appThread = Thread(target = self.run)
        appThread.start()

    def run(self):
        # Allow execution on separate thread by removing debug
        self.flaskApp.run(host='0.0.0.0', port=self.port, debug=False)

    def get(self):
        messageReceived = False
        message = { 'text': '', 'session': None }
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
        print(message)
        return message

    def get_response(self, session_id=None):
        if session_id == None:
            if self.responseQueue.empty():
                return { 'text': None, 'session': None }
            else:
                return { 'text': self.responseQueue.get(), 'session': None }
        else:
            try:
                if self.sessionResponses[session_id]:
                    if len(self.sessionResponses[session_id]) > 0:
                        message = self.sessionResponses[session_id].pop()
                        print(message)
                        return { 'text': message, 'session': session_id }
                    else:
                        return { 'text': None, 'session': session_id }
                else:
                    return { 'text': None, 'session': session_id }
            except:
                return { 'text': None, 'session': session_id }

    def put(self, text, session_id=None):
        if session_id == None:
            self.responseQueue.put(text)
        else:
            try:
                self.sessionResponses[session_id] += [text]
            except:
                self.sessionResponses[session_id] = []
                self.sessionResponses[session_id] += [text]
        # r.post(postUrl, { 'message': text })
