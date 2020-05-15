from matplotlib.pyplot import ylabel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from os import path
from PIL import Image
from nltk import tokenize
from nltk import FreqDist
from nltk import corpus
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import nltk

resenha = pd.read_csv('imdb-reviews-pt-br.csv')
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_columns', 999)

# adicionando uma coluna numérica no dataset para poder trabalhar com o SKLearn
swap: {
    'neg': 0,
    'pos': 1
}
classificacao = resenha['sentiment'].replace(['neg', 'pos'], [0, 1])
resenha['classificacao'] = classificacao

palavras_irrelevantes = nltk.corpus.stopwords.words('portuguese')
token_espaco = tokenize.WhitespaceTokenizer()

palavras_irrelevantes = nltk.corpus.stopwords.words("portuguese")

frase_processada = list()
for opiniao in resenha.text_pt:
    nova_frase = list()
    palavras_texto = token_espaco.tokenize(opiniao)
    for palavra in palavras_texto:
        if palavra not in palavras_irrelevantes:
            nova_frase.append(palavra)
    frase_processada.append(' '.join(nova_frase))

resenha["tratamento_1"] = frase_processada

def classificar_texto(texto, coluna_texto, coluna_classificacao):
    # quebrar em uma sacola de palavras (vetorização)
    vetorizar = CountVectorizer(max_features=50)
    bag_of_words = vetorizar.fit_transform(texto[coluna_texto])

    # quebrando cvs em treino e teste
    treino, teste, classe_treino, classe_teste = train_test_split(bag_of_words, texto[coluna_classificacao],
                                                                  random_state=42)

    # aplicando treino da IA
    regressao_logistica = LogisticRegression()
    regressao_logistica.fit(treino, classe_treino)

    # retorna a acurácia do IA
    return round(regressao_logistica.score(teste, classe_teste) * 100, 2)


def nuvem_palavras_neg(texto, coluna_texto):
    twitter_mask = preparar_mascara_twitter()

    texto_negativo = texto.query("sentiment == 'neg'")
    todas_palavras = ''.join([texto for texto in texto_negativo[coluna_texto]])

    nuvem_palavras = WordCloud(width=800, height=500, max_font_size=110, collocations=False, mask=twitter_mask,
                               background_color='white', contour_width=2, contour_color='steelblue').generate(
        todas_palavras)
    plt.figure(figsize=(10, 7))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def nuvem_palavras_pos(texto, coluna_texto):
    twitter_mask = preparar_mascara_twitter()

    texto_positivo = texto.query("sentiment == 'pos'")
    todas_palavras = ''.join([texto for texto in texto_positivo[coluna_texto]])

    nuvem_palavras = WordCloud(width=800, height=500, max_font_size=110, collocations=False, mask=twitter_mask,
                               background_color='white', contour_width=2, contour_color='steelblue').generate(
        todas_palavras)
    plt.figure(figsize=(10, 7))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def preparar_mascara_twitter():
    # preparando a mascara de imagem do twitter
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    # Read the whole text.
    return np.array(Image.open(path.join(d, "twitter_mask2.png")))


def gerar_grafico_linha(texto, coluna_texto,
                        qtd_colunas):  # função que gera um gráfico de pareto onde x = palavra  e y = fi de x

    todas_palavras = ''.join([texto for texto in texto[coluna_texto]])

    # tokenizando os dados (contando número de vezes em que uma palavra aparece)
    token_espaco = tokenize.WhitespaceTokenizer()
    token_frase = token_espaco.tokenize(todas_palavras)
    frequencia = FreqDist(token_frase)

    # a frequencia é um dicionário, vou converter em data frame
    df_frequencia = pd.DataFrame({'palavra': list(frequencia.keys()), 'frequencia': list(frequencia.values())})

    # plotando a contagem de palavras num gráfico
    plt.figure(figsize=(12, 8))
    ax = sns.lineplot(data=df_frequencia.nlargest(columns='frequencia', n=qtd_colunas), x='palavra', y='frequencia',
                      color='steelblue')
    ax.set(ylabel='Contagem')
    plt.show()


def gerar_histograma(texto, coluna_texto,
                     qtd_colunas):  # função que gera um gráfico de pareto onde x = palavra  e y = fi de x

    todas_palavras = ''.join([texto for texto in texto[coluna_texto]])

    # tokenizando os dados (contando número de vezes em que uma palavra aparece)
    token_espaco = tokenize.WhitespaceTokenizer()
    token_frase = token_espaco.tokenize(todas_palavras)
    frequencia = FreqDist(token_frase)

    # a frequencia é um dicionário, vou converter em data frame
    df_frequencia = pd.DataFrame({'palavra': list(frequencia.keys()), 'frequencia': list(frequencia.values())})

    # plotando a contagem de palavras num gráfico
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(data=df_frequencia.nlargest(columns='frequencia', n=qtd_colunas), x='palavra', y='frequencia',
                     color='steelblue')
    ax.set(ylabel='Contagem')
    plt.show()

#print(classificar_texto(resenha,'tratamento_1','classificacao'))
#gerar_histograma(resenha,'tratamento_1',20)
nuvem_palavras_pos(resenha,'tratamento_1')


