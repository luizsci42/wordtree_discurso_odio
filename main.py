from flask import Flask, render_template
from flask_cors import CORS
import pandas as pd
import os
import json
import logging
import re
import nltk

app = Flask(__name__, static_folder='/client', static_url_path='/')
CORS(app)


def limpar_texto(texto: str) -> str:
    """
    Método para limpar o texto
    """
    pontuacao = r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    stop_words = []

    # Removendo as URLs
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    # Removendo os elementos HTML
    texto = re.sub(r'<.*?>', '', texto)
    # Removendo a pontuação
    for x in texto.lower():
        if x in pontuacao:
            texto = texto.replace(x, "")
    # convertendo o texto para letras minúsculas
    texto = texto.lower()
    # removendo as stopwords
    texto = ' '.join([word for word in texto.split() if word not in stop_words])
    # removendo os espaços em branco
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/consultar/')
@app.route('/consultar/<bigrama>')
def consultar(bigrama=''):
    path = 'res/discurso_odio.csv'
    df_tweets = pd.read_csv(path, error_bad_lines=False)
    df_tweets['Texto'] = df_tweets.apply(lambda row: limpar_texto(row['Texto']), axis=1)

    stopwords = nltk.corpus.stopwords.words('portuguese')
    tweets = list(df_tweets['Texto'])
    tweets = [palavra for palavra in tweets if not palavra.lower() in stopwords]

    if bigrama != '':
        logging.info('Consultando a palavra: ' + bigrama)
        bigrama = bigrama.replace('_', ' ')
        # busca apenas as postagens que possuem o bigrama
        tweets = [post for post in tweets if (post.__contains__(bigrama))]
    else:
        # tweets = [post for post in tweets if (post.__contains__('jacarezinho'))]
        tweets = [post for post in tweets if (post.__contains__('pretos'))]

    logging.info('Quantidade de postagens: ', len(tweets))
    posts = {'Post': tweets}
    posts_json = json.dumps(posts, ensure_ascii=False)
    return posts_json


@app.route('hatepeech/')
def index_hatespeech():
    return render_template('hatespeech.html')


@app.route('hatespeech/<palavra>')
def hatespeech(palavra=''):
    path = 'res/posts_perfis.csv'
    df_tweets = pd.read_csv(path, error_bad_lines=False)
    df_tweets['Texto'] = df_tweets.apply(lambda row: limpar_texto(row['Texto']), axis=1)

    stopwords = nltk.corpus.stopwords.words('portuguese')
    tweets = list(df_tweets['Texto'])
    tweets = [palavra for palavra in tweets if not palavra.lower() in stopwords]

    if bigrama != '':
        logging.info('Consultando a palavra: ' + bigrama)
        bigrama = bigrama.replace('_', ' ')
        # busca apenas as postagens que possuem o bigrama
        tweets = [post for post in tweets if (post.__contains__(bigrama))]
    else:
        # tweets = [post for post in tweets if (post.__contains__('jacarezinho'))]
        tweets = [post for post in tweets if (post.__contains__('pretos'))]

    logging.info('Quantidade de postagens: ', len(tweets))
    posts = {'Post': tweets}
    posts_json = json.dumps(posts, ensure_ascii=False)

    return posts_json


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
