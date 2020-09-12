class Result:
    def __init__(self, id, user, text, sentiment, favorites, retweets, createdat):
        self._id = id
        self._user = user
        self._text = text
        self._sentiment = sentiment
        self._favorites = favorites
        self._retweets = retweets
        self._createdat = createdat

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._user

    @property
    def text(self):
        return self._text

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def favorites(self):
        return self._favorites

    @property
    def retweets(self):
        return self._retweets

    @property
    def createdat(self):
        #return format(self._createdat, "%d/%m/%Y")
        return self._createdat
