import illustrator
import ttweets
import sys
import time
import illustrator_handler


def spinning_cursor():
    while True:
        for cursor in '||||':
            yield cursor


def load_cli_message():
    spinner = spinning_cursor()
    for _ in range(50):
        sys.stdout.write('\033[94m' + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)


def show_welcome_message():
    print("************************************")
    print("        Bem vindo - POC PLN         ")
    print("************************************")
    print()


def get_search_param():
    q = input('Qual termo deseja buscar? \n')
    print('Conectando ao Twitter ')
    load_cli_message()
    print('Procurando tweets com o termo {} para fazer a análise de sentimentos '.format(q))
    load_cli_message()
    print('\nAqui está o resultado: \n\n')
    time.sleep(0.1)
    ttweets.get_tweets(q)
    return q


def show_graphic_results(q):
    neg, pos = illustrator_handler.get_tweets(q)
    print('Você pode visualizar os arquivos de forma gráfica\n')
    option = int(input('(0) Não,obrigado (1) Visualizar em wordcloud \n'))
    if option == 0:
        print('Obrigado por testar a POC....')
        exit()
    if option == 1:
        sub_option = int(input(
            '(0) Ver wordcloud com as palavras negativas (1) Ver wordcloud com as palavras positivas (2) Ver '
            'wordcloud com todas as palavras'))
        if sub_option == 0:
            illustrator.draw_wordcloud(neg, 'twitter_mask2.png')
        if sub_option == 1:
            illustrator.draw_wordcloud(pos, 'twitter_mask2.png')
        if sub_option == 2:
            print()


show_welcome_message()
query = get_search_param()
show_graphic_results(query)
