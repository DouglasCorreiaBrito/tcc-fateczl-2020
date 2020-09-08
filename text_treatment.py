import unidecode
import re
from nltk import tokenize
from nltk import corpus
from nltk import RSLPStemmer
from string import punctuation


# acentuação -> pontuação -> stopword -> stemização

def pre_processing(text):
    return text.lower()


def treat_accentuation(text):
    return unidecode.unidecode(text)


def treat_punctuation(text):
    tokenizer = tokenize.WordPunctTokenizer()
    return ' '.join(tokenizer.tokenize(text))


def treat_stopwords(text):
    newText = list()
    stopwords = corpus.stopwords.words("portuguese")

    for ponto in punctuation:
        stopwords.append(ponto)

    for word in text.split(' '):
        if word not in stopwords:
            newText.append(word)
    return ' '.join(newText)


def treat_stemming(text):
    stemmer = RSLPStemmer()
    newText = list()
    for word in text.split(' '):
        if word:
            newText.append(stemmer.stem(word))
    return ' '.join(newText)


def treat_user_mention(text):
    regex = '@[\S]+'
    return re.sub(regex, '', text)


def treat_urls(text):
    regex = '((www\.[\S]+)|(https?://[\S]+))'
    return re.sub(regex, '', text)


def treat_all(text):
    if not text:
        return text
    return treat_stemming(
        treat_stopwords(treat_punctuation(treat_accentuation(treat_user_mention(treat_urls(pre_processing(text)))))))


def treat_for_wordcloud(text):
    if not text:
        return text
    return treat_stopwords(treat_punctuation(treat_accentuation(treat_user_mention(treat_urls(pre_processing(text))))))
