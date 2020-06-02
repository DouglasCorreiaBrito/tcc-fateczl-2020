from wordcloud import WordCloud
from os import path
from PIL import Image
from nltk import tokenize
from nltk import FreqDist
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import os

def draw_wordcloud(list_of_words,name_mask):

    image_mask = _prepare_background_mask(name_mask)

    words_in_the_same_str = ''.join([text for text in list_of_words])

    word_cloud = WordCloud(width=800, height=500, max_font_size=110,
                               collocations=False, mask=image_mask,
                               background_color='white', contour_width=2,
                               contour_color='steelblue').generate(words_in_the_same_str)

    plt.figure(figsize=(10, 7))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def _prepare_background_mask(name_mask):

    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    return np.array(Image.open(path.join(d, name_mask)))


def draw_line_graph(dataframe, df_text_column, num_column):

    words_in_the_same_str = ''.join([texto for texto in dataframe[df_text_column]])

    token_espace = tokenize.WhitespaceTokenizer()
    token_phrase = token_espace.tokenize(words_in_the_same_str)
    frequency = FreqDist(token_phrase)

    # the frequency is a dictionary, convert to data frame
    df_frequencia = pd.DataFrame({'word': list(frequency.keys()), 'frequency': list(frequency.values())})

    plt.figure(figsize=(12, 8))
    ax = sns.lineplot(data=df_frequencia.nlargest(columns='frequency', n=num_column), x='word', y='frequency', color='steelblue')
    ax.set(ylabel='Score')
    plt.show()


def gerar_histograma(dataframe, df_text_column, num_column):

    words_in_the_same_str = ''.join([texto for texto in dataframe[df_text_column]])

    token_espace = tokenize.WhitespaceTokenizer()
    token_phrase = token_espace.tokenize(words_in_the_same_str)
    frequency = FreqDist(token_phrase)

    # the frequency is a dictionary, convert to data frame
    df_frequencia = pd.DataFrame({'word': list(frequency.keys()), 'frequency': list(frequency.values())})

    plt.figure(figsize=(12, 8))
    ax = sns.lineplot(data=df_frequencia.nlargest(columns='frequency', n=num_column), x='word', y='frequency', color='steelblue')
    ax.set(ylabel='Score')
    plt.show()
