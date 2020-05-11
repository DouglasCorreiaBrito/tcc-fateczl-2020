from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
        sid = SentimentIntensityAnalyzer()

        print(sid.lexicon_file)
        ss = sid.polarity_scores(self._text)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
        
        print()
        print()

#
#        if self.language == 'pt':
#            #analyse text in PT BR
#            print('')
#        elif self.language == 'en':
#            # analyse text in EN
#            print()
#
#        return "good|bad|neutral"  # analyse text

