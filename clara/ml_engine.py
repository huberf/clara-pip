# General 3rd party library imports
import json
import os

# Specific 3rd party library imports
from os import listdir

# Local imports
try:
    from utils import convo_reader
except ModuleNotFoundError:
    from clara.utils import convo_reader

# ML specific library imports
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
import random

# Config load
configFile = open('config.json')
raw_data = configFile.read()
data = json.loads(raw_data)

ROOT_CACHE = None

def strip_punctuations(val):
    return val.strip('.').strip('?').strip('!')

def tokenize(string):
    ignore_words = []
    words = string.split(' ')
    words = [stemmer.stem(strip_punctuation(w.lower())) for w in words if w not in ignore_words]
    return words

def _load_convos():
    # Load all conversations
    convo = []
    convoFiles = listdir(data['convo_dir'])
    for i in convoFiles:
        if i.endswith('.json'):
            convoFile = open(data['convo_dir'] + i)
            raw_data = convoFile.read()
            convo += json.loads(raw_data)
        elif i.endswith('.convo'):
            # Process the loose file format
            convoFile = open(data['convo_dir'] + i)
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
    node_count = 16
    net = tflearn.fully_connected(net, node_count) # First hidden layer
    net = tflearn.fully_connected(net, node_count) # Second hidden layer
    net = tflearn.fully_connected(net, len(list(ROOT_CACHE['replies'].keys())), activation='softmax')
    net = tflearn.regression(net)

    # Define model and setup tensorboard
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    return model

def train_model(model, epochs):
    train_x = []
    train_y = []
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
    f = open('dev_logs/train.log', 'w')
    f.write(json.dumps(train_x))
    f.write('\n')
    f.write(json.dumps(train_y))
    model.fit(train_x, train_y, n_epoch=epochs, batch_size=10, show_metric=True)#, callbacks=[cp_callback])
    model.save('neural_model')

def out_to_reply(out):
    max_i = 0
    max_val = out[0]
    for i in range(1,len(out)):
        if out[i] > max_val:
            max_val = out[i]
            max_i = i
    reply = list(ROOT_CACHE['replies'].keys())[max_i]
    reply_val = json.loads(reply)
    return reply_val

if __name__ == '__main__':
    print("Caching tokens...")
    cache_tokens()
    #load_cache()
    choice = input("train model? [y/n] ")
    if choice[0] == 'y':
        print("Building model...")
        model = build_model()
        print("Training model...")
        train_model(model, 200)
        print("Testing model...")
        tokens = string_to_root_array("What are you up to?")
        out = list(model.predict([tokens]))
        print(out)
        print(out_to_reply(out[0]))
        tokens = string_to_root_array("What is the convo file type?")
        out = list(model.predict([tokens]))
        print(out)
        print(out_to_reply(out[0]))
    else:
        #model = tf.keras.models.load_model('neural_model')
        with tf.Session() as sess:
            new_saver = tf.train.import_meta_graph('neural_model.meta')
            new_saver.restore(sess, tf.train.latest_checkpoint('./'))
    print("Ready for input...")
    while True:
        text = input("> ")
        tokens = string_to_root_array(text)
        out = list(model.predict([tokens]))
        print(out)
        print(out_to_reply(out[0])[0]['text']) # Simply print first reply
