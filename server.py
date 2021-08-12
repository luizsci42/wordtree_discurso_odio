from flask import Flask, render_template
from flask_cors import CORS
import pandas as pd
import os
import json

app = Flask(__name__, static_folder='/client', static_url_path='/')
CORS(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/consultar/')
@app.route('/consultar/<bigrama>')
def consultar(bigrama=''):
    path = 'res/posts_perfis_policiais.csv'
    df_tweets = pd.read_csv(path, error_bad_lines=False)
    tweets = list(df_tweets['Text'])

    if bigrama != '':
        bigrama = bigrama.replace('_', ' ')
        # busca apenas as postagens que possuem o bigrama
        tweets = [post for post in tweets if (post.__contains__(bigrama))]
    else:
        tweets = [post for post in tweets if (post.__contains__('jacarezinho'))]

    posts = {'Post': tweets}
    posts_json = json.dumps(posts, ensure_ascii=False)
    return posts_json


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)
