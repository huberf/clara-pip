import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

def tokenize(string):
    ignore_words = []
    words = string.split(' ')
    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
