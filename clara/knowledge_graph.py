# This system will supersede the VAR_REGISTRY with more robust data storage and retreival
# So far the system is basically just an encapsulated map but inference is in the works

class KnowledgeGraph:
    registry = {}
    connections = {}

    def __init__(self):
        doNothing = True

    def get(self, key):
        try:
            data = self.registry[key]
            return data
        except:
            try:
                connection = self.connections[key]
                response = ""
                for i in connection:
                    if i['type'] == 'connection':
                        response += self.registry[i['name']]
                    elif i['type'] == 'string':
                        response += self.registry[i['text']]
                return response
            except:
                return None
    
    def addConnection(self, key, fields):
        self.registry[key] = fields

    def put(self, key, value):
        self.registry[key] = value

    def bulkPut(self, dictionary):
        for key in dictionary:
            self.registry[key] = dictionary[key]

    def getRegistry(self):
        return self.registry
