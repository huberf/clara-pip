from random import randint
import random
from Levenshtein import distance
from os import listdir
import json
from threading import Thread
from time import sleep
import re
# Import interface for basic convo file
from .utils import convo_reader
from .message_statistics import MessageStats
from .utils import sentiment
from .utils import iograb

# Setup global objects
myIO = iograb.ClaraIO()
#myIO = iograb.WebIO()

# Config load
configFile = open('config.json')
raw_data = configFile.read()
data = json.loads(raw_data)
null_response = "None"
try:
    null_response = data["null_response"]
except:
    null_response = "None"


# Emotion load
emotionFile = open('emotions.json')
raw_data = emotionFile.read()
emotions = json.loads(raw_data)
emotionFile.close()

# Append all conversation response around distributed conversation files
# This allows one to "plug-in" new responses and have them centralized together
convo = []
convoDir = data['convo_dir']
convoFiles = listdir(data['convo_dir'])
for i in convoFiles:
    if i.endswith('.json'):
        convoFile = open(convoDir + i)
        raw_data = convoFile.read()
        convo += json.loads(raw_data)
    elif i.endswith('.convo'):
        # Process the loose file format
        convoFile = open(convoDir + i)
        raw_data = convoFile.read()
        convo += convo_reader.convert_to_json(raw_data)

# Var Setup
VAR_REGISTRY = {}
def build_registry():
    global VAR_REGISTRY, convo
    VAR_REGISTRY = {
            "user_name": data['user']['name'],
            "name": data['name'],
            "response_count": len(convo),
            "user_hobby": data['user']['hobby'],
            "favorite_food": data['food'],
            "happy_level": emotions['happy'],
            "stress_level": emotions['stress'],
            "animosity": emotions['animosity']
            }
    feelings = json.load(open('feelings.json'))
    for i in feelings:
        VAR_REGISTRY[i['name']] = i['val']
        # Add diagnostic info
        convo += [ {
            "starters": [ i['name'] + " level", "What is your " + i['name'] + "level?"],
            "replies": [{ "text": "My " + i['name'] + " level is {" + i['name'] + "}." }]
            }]

build_registry()

def punctuation_stripper(statement):
    toRemove = ['.', '!', '?']
    punctuate = None
    for i in toRemove:
        if not statement.find(i) == -1:
            punctuate = i
        statement = statement.strip(i)
    return {"text": statement, "punctuation": punctuate}

def handle_modifiers(modifiers):
    for i in modifiers:
        try:
            VAR_REGISTRY[i['name']] += i['val']
        except:
            doNothing = True

def calc_qualifiers(qualifier):
    registryValue = VAR_REGISTRY[qualifier['name']]
    try:
        if registryValue > qualifier['$gt']:
            return True
        else:
            return False
    except:
        # Not a greater than qualifier
        doNothing = True
    try:
        if registryValue == qualifier['$eq']:
            return True
        else:
            return False
    except:
        # Not an equal to qualifier
        doNothing = True
    try:
        if registryValue < qualifier['$lt']:
            return True
        else:
            return False
    except:
        # Not a less than qualifier
        doNothing = True
    # Legacy qualifier types
    try:
        if registryValue == qualifier['val']:
            return True
        else:
            return False
    except:
        # Not a less than qualifier
        doNothing = True
    # if supplied info doesn't fit any of the above qualifier types reject
    return False

# Pick a random option from supplied reply list using weights
def random_pick_weighted(reply_options):
    weights = list(map(lambda e: e['weight'], reply_options))
    indexes = list(range(0, len(reply_options)))
    # Generates a list with a single entry containing a value randomly picked with proper weight
    choices_list = random.choices(indexes, weights=weights, k=1)
    picked_index = choices_list[0]
    slimmed_reply = reply_options[picked_index]
    return slimmed_reply

def get_response(input):
    sentimentValues = sentiment.assess(input)
    # Remove currently useless characters
    stripped = punctuation_stripper(input)
    input = stripped["text"]
    punctuation = stripped["punctuation"]
    possibilities = []
    for i in convo:
        for a in i['starters']:
            val = distance(input, a)
            if len(input)/(val+1) > 1.5:
                reply_options = []
                for b in i['replies']:
                    should_add = False
                    try:
                        to_test = b['qualifiers']
                        for z in to_test:
                            if calc_qualifiers(z):
                                should_add = True
                            else:
                                do_nothing = True
                    except:
                        should_add = True
                    if should_add:
                        to_add = {'text': b['text']}
                        try:
                            to_add['image'] = b['image']
                        except:
                            to_add['image'] = 'None'
                        try:
                            to_add['modifiers'] = b['modifiers']
                        except:
                            to_add['modifiers'] = []
                        try:
                            to_add['weight'] = b['weight']
                        except:
                            to_add['weight'] = 1
                        reply_options += [to_add]
                slimmed_reply = random_pick_weighted(reply_options)
                possibilities.append({
                    'val': val,
                    'response': slimmed_reply['text'],
                    'image': slimmed_reply['image'],
                    'weight': slimmed_reply['weight'],
                    'modifiers': slimmed_reply['modifiers']
                    })
    min = 10000000000
    response = 'None'
    image = 'None'
    modifiers = []
    # print(possibilities)
    for i in possibilities:
        if i['val'] < min:
            response = i['response']
            image = i['image']
            modifiers = i['modifiers']
            min = i['val']
    handle_modifiers(modifiers)
    toReturn = {'message': response.format(**VAR_REGISTRY), 'image': image}
    return toReturn

input_queue = []
def threaded_input():
    while True:
        if len(input_queue) == 0:
            input_queue.append(myIO.get());

ticker = 0
events = json.load(open('events.json'))
for i in range(len(events)):
    metric = events[i]['metric']
    val = VAR_REGISTRY[metric]
    events[i]['last'] = val
def event_check():
    global ticker
    ticker += 1
    for i in range(len(events)):
        metric = events[i]['metric']
        val = VAR_REGISTRY[metric]
        if events[i]['type'] == '$gt':
            if val > events[i]['level'] and events[i]['last'] < val:
                myIO.put(events[i]['response'])
        elif events[i]['type'] == '$lt':
            if val < events[i]['level'] and events[i]['last'] > val:
                myIO.put(events[i]['response'])
        events[i]['last'] = val

def run():
    logFile = open('log.txt', 'a')
    secureLogger = MessageStats("secure_log.json")
    secureLogger.load_log()
    myIO.put("Booting...")
    ioThread = Thread(target = threaded_input)
    myIO.put("{} online.".format(data['name']))
    ioThread.start()
    terminated = False
    while not terminated:
        event_check()
        if len(input_queue) > 0:
            statement = input_queue[0]
            del input_queue[0]
            response = get_response(statement.lower())
            if not response['message'] == 'None':
                myIO.put(response['message'])
            else:
                myIO.put(null_response)
            secureLogger.log_occurence(response['message'])
            ender = '\n'
            logFile.write('Q: ' + statement + ender)
            if not response == None:
                logFile.write('R: ' + response['message'] + ender)
            else:
                logFile.write('R: None' + ender)
            if statement == "quit":
                terminated = True
        sleep(0.1)
    emotionFile = open('emotions.json', 'w')
    emotionFile.write(json.dumps(emotions))
    emotionFile.close()
    secureLogger.save_log()

if __name__ == "__main__":
    run()
