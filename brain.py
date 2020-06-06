from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import tokenize
import pickle
import pandas as pd
import text_treatment
from os import path

def load_brain():
    filename = 'anton_brain.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def load_vectorizer():
    filename = 'anton_vectorizer.sav'
    vectorizer = pickle.load(open(filename, 'rb'))
    return vectorizer

def predict(tweet):
    token_espaco = tokenize.WhitespaceTokenizer()
    palavras_texto = token_espaco.tokenize(text_treatment.treat_all(tweet))
    brain = load_brain()
    vetorizar = load_vectorizer()
    bag_of_words = vetorizar.transform(palavras_texto)
    result = brain.decision_function(bag_of_words)
    
    return result
