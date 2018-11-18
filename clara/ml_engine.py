# General 3rd party library imports
import json

# Specific 3rd party library imports
from os import listdir

# Local imports
from utils import convo_reader

# ML specific library imports
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

# Config load
configFile = open('config.json')
raw_data = configFile.read()
data = json.loads(raw_data)

ROOT_CACHE = None

def tokenize(string):
    ignore_words = []
    words = string.split(' ')
    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
    return words

def _load_convos():
    # Load all conversations
    convo = []
    convoFiles = listdir(data['convo_dir'])
    for i in convoFiles:
        if i.endswith('.json'):
            convoFile = open('convos/' + i)
            raw_data = convoFile.read()
            convo += json.loads(raw_data)
        elif i.endswith('.convo'):
            # Process the loose file format
            convoFile = open('convos/' + i)
            raw_data = convoFile.read()
            convo += convo_reader.convert_to_json(raw_data)
    return convo

def cache_tokens():
    global ROOT_CACHE
    convo = _load_convos()
    # Now get all contexts and tokens
    all_roots = {}
    all_replies = {}
    for i in convo:
        all_replies[json.dumps(i['replies'])] = 0 # Make JSON representations of replies
        for j in i['replies']:
            temp = tokenize(j['text'])
            for q in temp:
                all_roots[q] = 0 # dummy value
        for j in i['starters']:
            temp = tokenize(j)
            for q in temp:
                all_roots[q] = 0 # dummy value
    # Now we generate an index for every node
    roots = list(all_roots.keys())
    save_map = {}
    for i in range(len(roots)):
        save_map[roots[i]] = i
    replies = list(all_replies.keys())
    reply_map = {}
    for i in range(len(replies)):
        reply_map[replies[i]] = i
    ROOT_CACHE = { 'count': len(roots), 'roots': save_map, 'replies': reply_map }
    string = json.dumps(ROOT_CACHE)
    cache_file = open('root_cache.json', 'w')
    cache_file.write(string)

def load_cache():
    global ROOT_CACHE
    cache_file = open('root_cache.json', 'r')
    contents = cache_file.read()
    ROOT_CACHE = json.loads(contents)

def string_to_root_array(string):
    if ROOT_CACHE == None:
        load_cache()
    tokens = tokenize(string)
    to_return = []
    for i in range(ROOT_CACHE['count']):
        to_return += [0]
    for i in tokens:
        try:
            index = ROOT_CACHE['roots'][i]
            to_return[index] = 1
        except:
            print("Root is not in collection:", i)
    return to_return

def build_model():
    # reset underlying graph data
    tf.reset_default_graph()
    # Build neural network
    net = tflearn.input_data(shape=[None, len(list(ROOT_CACHE['roots'].keys()))])
    net = tflearn.fully_connected(net, 8) # First hidden layer
    net = tflearn.fully_connected(net, 8) # Second hidden layer
    net = tflearn.fully_connected(net, len(list(ROOT_CACHE['replies'].keys())), activation='softmax')
    net = tflearn.regression(net)

    # Define model and setup tensorboard
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    return model

def train_model(model, epochs):
    train_x = [] # TODO: Setup examples
    train_y = [] # TODO: Setup examples
    convo = _load_convos()
    for i in convo:
        reply_match = json.dumps(i['replies']) # Make JSON representations of replies
        for j in i['starters']:
            train_x += [ string_to_root_array(j) ] # Convert to model input
            y_in = []
            # Convert to reply to vector with only applicable reply equal to 1
            for q in range(len(list(ROOT_CACHE['replies'].keys()))):
                if q == ROOT_CACHE['replies'][reply_match]:
                    y_in += [1]
                else:
                    y_in += [0]
            train_y += [ y_in ]
    model.fit(train_x, train_y, n_epoch=epochs, batch_size=8, show_metric=True)

if __name__ == '__main__':
    print("Caching tokens...")
    cache_tokens()
    #load_cache()
    print("Building model...")
    model = build_model()
    print("Training model...")
    train_model(model, 100)
    print("Testing model...")
    tokens = string_to_root_array("What are you up to?")
    print(tokens)
    print(model.predict([tokens]))
    tokens = string_to_root_array("What is the convo file type?")
    print(tokens)
    print(model.predict([tokens]))
