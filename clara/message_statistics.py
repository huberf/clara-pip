import hashlib
import json

class MessageStats:
    log = {}
    file_name = ""
    def __init__(self, file_name):
        self.file_name = file_name

    def generate_message_hash(self, message):
        m = hashlib.md5()
        m.update(message.encode("utf-8"))
        digest = str(m.digest())
        return digest

    def log_occurence(self, message):
        key_hash = self.generate_message_hash(message)
        try:
            self.log[key_hash] += 1
        except:
            self.log.update({key_hash: 1})

    def retrieve_occurences(self, message):
        key_hash = self.generate_message_hash(message)
        try:
            return log[key_hash]
        except:
            return 0

    def save_log(self):
        raw_log = json.dumps(self.log)
        log_file = open(self.file_name, 'w')
        log_file.write(raw_log)

    def load_log(self):
        log_file = open(self.file_name)
        raw_log = log_file.read()
        log = json.loads(raw_log)
