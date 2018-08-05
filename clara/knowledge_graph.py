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

if __name__ == '__main__':
    knowledge = KnowledgeGraph()
    knowledge.addClassification('The Expanse', 'TV Show')
    knowledge.addClassification('The Expanse', 'Best Show')
    print('The Expanse is a ', ', '.join(knowledge.classify('The Expanse')))
    print('The best shows are', ', '.join(knowledge.classMembers('Best Show')))

