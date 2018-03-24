# This system will supersede the VAR_REGISTRY with more robust data storage and retreival
# So far the system is basically just an encapsulated map but inference is in the works

class KnowledgeGraph:
    registry = {}

    def __init__(self):
        doNothing = True

    def get(self, key):
        try:
            data = self.registry[key]
            return data
        except:
            return None

    def put(self, key, value):
        self.registry[key] = value

    def bulkPut(self, dictionary):
        for key in dictionary:
            self.registry[key] = dictionary[key]

    def getRegistry(self):
        return self.registry
