from matplotlib.pyplot import ylabel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
from os import path
from PIL import Image
from nltk import tokenize
from nltk import FreqDist
from nltk import corpus
from string import punctuation
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import unidecode
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

# Essa é a tratativa de stopwords ---------------------------------------------------
token_espaco = tokenize.WhitespaceTokenizer() # cria um separador de palavras por espaço

palavras_irrelevantes = nltk.corpus.stopwords.words("portuguese") # traz as stopwords do dicionário português
frase_processada = list()
for opiniao in resenha.text_pt:
    nova_frase = list()
    opiniao = opiniao.lower() # !IMPORTANTE dar lower na string para não falhar nas stopwords
    palavras_texto = token_espaco.tokenize(opiniao) # quebro a opinião (que é uma única string) pelo espaço e insiro em uma lista
    for palavra in palavras_texto: # itero sobre a lista para verificar se o valor do index está na lista de stopwords
        if palavra not in palavras_irrelevantes:
            nova_frase.append(palavra)
    frase_processada.append(' '.join(nova_frase)) # se a palavra não for um stopword, adiciono.

resenha["tratamento_1"] = frase_processada
#--------------------------------------------------------------------


# Essa é a tratativa de pontuação ---------------------------------------------------
pontuacao = list()
for ponto in punctuation: # esse punctuation de string traz todos as pontuações do teclado
    pontuacao.append(ponto)

token_pontuacao = tokenize.WordPunctTokenizer() # cria um separador de palavras por pontuaão
pontuacao_stopwords = pontuacao + palavras_irrelevantes

frase_processada = list()
for opiniao in resenha["tratamento_1"]:
    nova_frase = list()
    palavras_texto = token_pontuacao.tokenize(opiniao)
    for palavra in palavras_texto:
        if palavra not in pontuacao_stopwords:
            nova_frase.append(palavra)
    frase_processada.append(' '.join(nova_frase))

resenha["tratamento_2"] = frase_processada

#--------------------------------------------------------------

# --------------- essa é a tratativa de acentuação ------------
sem_acentos = [unidecode.unidecode(texto) for texto in resenha['tratamento_2']] # List Comprehension
resenha['tratamento_3'] = sem_acentos

#vou repetir o tratamento para retirar as stopwords que não foram removidas com acento
frase_processada = list()
for opiniao in resenha["tratamento_3"]:
    nova_frase = list()
    palavras_texto = token_pontuacao.tokenize(opiniao)
    for palavra in palavras_texto:
        if palavra not in pontuacao_stopwords:
            nova_frase.append(palavra)
    frase_processada.append(' '.join(nova_frase))

resenha["tratamento_3"] = frase_processada

#--------------------------------------------------------------

#---------------------------- tratativa estemização -----------
#para evitar flexões e derivações das palavras, transformando todas num mesmo radical
# http://www.inf.ufrgs.br/~viviane/rslp/index.htm
stemmer = nltk.RSLPStemmer()
frase_processada = list()
for opiniao in resenha["tratamento_3"]:
    nova_frase = list()
    palavras_texto = token_pontuacao.tokenize(opiniao)
    for palavra in palavras_texto:
        if palavra not in pontuacao_stopwords:
            nova_frase.append(stemmer.stem(palavra))
    frase_processada.append(' '.join(nova_frase))

resenha["tratamento_4"] = frase_processada

#---------------------------------------------------------


def classificar_texto(texto, coluna_texto, coluna_classificacao):
    # quebrar em uma sacola de palavras (vetorização)
    vetorizar = TfidfVectorizer(lowercase=False)
    bag_of_words = vetorizar.fit_transform(texto[coluna_texto])

    # quebrando cvs em treino e teste
    treino, teste, classe_treino, classe_teste = train_test_split(bag_of_words, texto[coluna_classificacao],
                                                                  random_state=42)

    # aplicando treino da IA
    regressao_logistica = LogisticRegression()
    regressao_logistica.fit(treino, classe_treino)

    pesos = pd.DataFrame(
        regressao_logistica.coef_[0].T,
        index = vetorizar.get_feature_names()
    )
    print(pesos.nlargest(10, 0))
    print(pesos.nsmallest(10, 0))

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



#print(classificar_texto(resenha,'tratamento_4','classificacao'))
gerar_histograma(resenha,'tratamento_3', 10)
gerar_grafico_linha(resenha,'tratamento_4', 10)
nuvem_palavras_pos(resenha,'tratamento_4')
