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
        if self.language == 'pt':
            #analyse text in PT BR
            print('')
        elif self.language == 'en':
            # analyse text in EN
            print()

        return "good|bad|neutral"  # analyse text

