from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import tokenize
import pickle
import pandas as pd


def load_brain():
    filename = 'anton_brain.sav'
    loaded_model = LogisticRegression()
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def predict(tweet):

    token_espaco = tokenize.WhitespaceTokenizer()
    palavras_texto = token_espaco.tokenize(tweet)
    brain = load_brain()
    vetorizar = TfidfVectorizer(lowercase=False)
    bag_of_words = vetorizar.fit_transform(palavras_texto)
    df = pd.DataFrame(bag_of_words)
    print(df.shape)

    result = brain.predict(bag_of_words)

    return result