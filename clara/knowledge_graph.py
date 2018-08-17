# This system will supersede the VAR_REGISTRY with more robust data storage and retreival
# So far the system is basically just an encapsulated map but inference is in the works

class KnowledgeGraph:
    registry = {}
    connections = {}
    valueToClass = {}
    classToValue = {}

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

    def classify(self, value):
        try:
            return self.valueToClass[value]
        except:
            return []

    def addClassification(self, value, classification):
        try:
            self.valueToClass[value] += [classification]
        except:
            self.valueToClass[value] = [classification]
        try:
            self.classToValue[classification] += [value]
        except:
            self.classToValue[classification] = [value]

    def classMembers(self, classification):
        try:
            return self.classToValue[classification]
        except:
            return []

    # Specialized context functionality
    context_graph = {}

    def updateContext(self):
        for i in self.context_graph.keys():
            self.context_graph[i] += 1 # Move context recency one step into the past

    def newContext(self, value):
        try:
            self.context_graph[value] = 0
        except:
            self.context_graph[value] = 0 # Never seen before

    def contextSeparation(self, name):
        try:
            return self.context_graph[name]
        except:
            return float('infinity')

    def loadContext(self, context_map):
        self.context_graph = context_map

    def dumpContext(self):
        return self.context_graph

if __name__ == '__main__':
    knowledge = KnowledgeGraph()
    knowledge.addClassification('The Expanse', 'TV Show')
    knowledge.addClassification('The Expanse', 'Best Show')
    print('The Expanse is a ', ', '.join(knowledge.classify('The Expanse')))
    print('The best shows are', ', '.join(knowledge.classMembers('Best Show')))

