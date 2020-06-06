import pickle
from sklearn.linear_model import LogisticRegression
import tbrain
import polyglot
from polyglot.text import Text

class TSentiment:
    def __init__(self, text,language):
        self._text = text
        self._language = language

    @property
    def text(self):
        return self._text

    @property
    def language(self):
        return self._language

    def analyze_feeling(self):

        if ":(" in self._text:
            self._text = "ruim"

        text = Text(self._text, hint_language_code="pt")

        predictionText = ''

        #Adjetivos, adverbios, substantivos, verbos
        allowableTags = ['ADJ', 'ADV', 'NOUN','VERB']

        for word, tag in text.pos_tags:
            if any(allowedTag in tag for allowedTag in allowableTags):
                predictionText += word + ' '

        if predictionText:
            prediction = tbrain.predict(predictionText)
        else:
            prediction = [0]

        pontuacaoFinal = 0

        for pontuacao in prediction:
            pontuacaoFinal += pontuacao

        print(pontuacaoFinal)
        if pontuacaoFinal < -0.5:
            return 'neg'
        elif pontuacaoFinal > 0.5:
            return 'pos'
        else:
            return 'neu'
