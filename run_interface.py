import glob
import os
import time

from flask import Flask, render_template, request

import illustrator
import ttweets
import get_charts

app = Flask(import_name=__name__)

@app.route('/')
def home():
    description = 'Insira um termo de pesquisa para descobrir o sentimento das pessoas em relação a ele no Twitter.'
    return render_template('index.html', title='Twitter Sentimentalizer',
                           description=description,
                           readed_tweets=get_charts.readed_tweets(),
                           good_tweets=get_charts.good_tweets(),
                           bad_tweets=get_charts.bad_tweets(),
                           neu_tweets=get_charts.neutral_tweets(),
                           top_terms=get_charts.top_tweets(),
                           total_searchs = get_charts.total_searchs())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/devs')
def devs():
    return render_template('devs.html')


@app.route('/results', methods=['POST'])
def result():
    term_search = request.form['search']
    try:
        tweets, pos, neg = ttweets.get_tweets(term_search)
        files = glob.glob('./static/images/*')
        for f in files:
            os.remove(f)
        illustrator.draw_wordcloud(neg, 'twitter_mask2.png', False)
        illustrator.draw_wordcloud(pos, 'twitter_mask2.png', True)
        description = 'Aqui está o que encontramos:'
        time.sleep(3)
        return render_template('results.html', title='Resultados',
                               tweets=tweets, description=description,
                               url1='./static/images/neg_plot.png',
                               url2='./static/images/pos_plot.png')
    except:
        return render_template('error.html', term=term_search)

# port = int(os.environ.get('PORT', 33507))
# app.run(debug=True, port=port)
