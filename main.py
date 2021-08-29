from flask import Flask, render_template
import pandas as pd
import os
import json
import logging
import re

app = Flask(__name__, static_folder='/client', static_url_path='/')


def limpar_texto(texto):
    texto = re.sub('\n', '', texto)
    texto = re.sub('@\S+', '', texto)
    texto = re.sub('#\S+', '', texto)
    texto = re.sub(r'https://\S+', '', texto)
    texto = re.sub(r'[^\w\s]', '', texto)

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
