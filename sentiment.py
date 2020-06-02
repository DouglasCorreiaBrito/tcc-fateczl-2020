
import brain

class Sentiment:
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

        prediction = brain.predict(self._text)

        count_zero = 0
    
        for entry in prediction:
            if entry == 0:
                count_zero += 1
        
        if count_zero > len(prediction) / 2:
            return 'neg'
        elif count_zero < len(prediction) / 2:
            return 'pos'
        else:
            return 'neu'

