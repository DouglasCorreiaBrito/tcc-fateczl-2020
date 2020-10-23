import brain


class Sentiment:
    def __init__(self, text, language):
        self._text = text
        self._language = language

    @property
    def text(self):
        return self._text

    @property
    def language(self):
        return self._language

    def analyze_feeling(self):
        if self._language not in 'pt_BR':
            return 'olan'
        if ":(" in self._text:
            self._text = "ruim"

        prediction = brain.predict(self._text)
        pontuacaoFinal = 0
        list_punct = []

        for pontuacao in prediction:
            list_punct.append(pontuacao)
            pontuacaoFinal += pontuacao
        #print('score por palavra', list_punct)
        #print('score final da frase',pontuacaoFinal)
        if pontuacaoFinal < -0.5:
            #print(pontuacaoFinal)
            return 'neg'
        elif pontuacaoFinal > 0.5:
            #print(pontuacaoFinal)
            return 'pos'
        else:
            #print(pontuacaoFinal)
            return 'neu'
