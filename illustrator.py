import glob
import random

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
import text_treatment


# arquivo = open('teste.txt', 'r', encoding="utf8")
# unica_string = arquivo.read()
# arquivo.close()

# data = pd.read_csv('Book1.csv')

def bad_color_func(word, font_size, position, orientation, random_state=None,
                   **kwargs):
    return "hsl(0, 75%%, %d%%)" % random.randint(60, 100)


def draw_wordcloud(words_in_the_same_str, name_mask='', positive_flag=True):
    words = text_treatment.treat_for_wordcloud(words_in_the_same_str)

    if positive_flag:
        image_mask = _prepare_background_mask(name_mask)

        word_cloud = WordCloud(width=800, height=500, max_font_size=110,
                               collocations=False, mask=image_mask,
                               background_color='black', contour_width=1,
                               contour_color='steelblue').generate(words)
        plt.figure(figsize=(10, 7))
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.plot(range(10), range(10), '-o')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.axis('off')
        plt.savefig('./static/images/pos_plot.png', bbox_inches=0)

    else:
        image_mask = _prepare_background_mask(name_mask)

        word_cloud = WordCloud(width=800, height=500, max_font_size=110,
                               collocations=False, mask=image_mask,
                               background_color='black', contour_width=1,
                               contour_color='steelblue').generate(words)
        plt.figure(figsize=(10, 7))
        plt.imshow(word_cloud.recolor(color_func=bad_color_func, random_state=3), interpolation='bilinear')
        plt.plot(range(10), range(10), '-o')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.axis('off')
        plt.savefig('./static/images/neg_plot.png', bbox_inches=0)


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
    ax = sns.lineplot(data=df_frequencia.nlargest(columns='frequency', n=num_column), x='word', y='frequency',
                      color='steelblue')
    ax.set(ylabel='Score')
    plt.savefig('/static/images/new_plot.png')


def gerar_histograma(dataframe, df_text_column, num_column):
    words_in_the_same_str = ''.join([texto for texto in dataframe[df_text_column]])
    words_in_the_same_str = text_treatment.treat_for_wordcloud(words_in_the_same_str)
    token_espace = tokenize.WhitespaceTokenizer()
    token_phrase = token_espace.tokenize(words_in_the_same_str)
    frequency = FreqDist(token_phrase)

    # the frequency is a dictionary, convert to data frame
    df_frequencia = pd.DataFrame({'word': list(frequency.keys()), 'frequency': list(frequency.values())})

    plt.figure(figsize=(12, 8))
    ax = sns.barplot(data=df_frequencia.nlargest(columns='frequency', n=num_column), x='word', y='frequency',
                     color='steelblue')
    ax.set(ylabel='Score')
    plt.show()

# draw_wordcloud(unica_string)
# gerar_histograma(data, 'text_pt', 10)
