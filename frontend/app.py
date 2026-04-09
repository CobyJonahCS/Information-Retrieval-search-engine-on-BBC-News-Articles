from flask import Flask, render_template, request,send_from_directory,jsonify
import os
import sys
sys.path.append('../')

from src.PreProcessingPipeline import BM25_PreProcess

import pandas as pd
from src.models import BM25
from src.models import UnigramLM

#loading our articles hdataset here

# add logic to work on different OS's
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "..", "data", "archive-5", "archive (2)", "bbc-news-data.csv")
df= pd.read_csv(csv_path, sep="\t")

# df = pd.read_csv("../data/archive-5/archive (2)/bbc-news-data.csv",sep="\t")

df['document'] = df['title'] + " " + df ['content']

corpus = df['document'].to_list()
bm_prepro = BM25_PreProcess(corpus=corpus, set_stemming=True, set_lemmatization=False, set_stopwords=True)
processed_corpus = bm_prepro.get_corpus()

# pre procvessing the dataset 

results_out = pd.DataFrame()

"""
use the exact same params to do the dataset preprocess as you do with the query 
these params can change later once we investigate what works well
"""

app = Flask(__name__,template_folder=".")
# point to local dir

@app.route("/")



def home():
    """ just loads the home page """
    return render_template("index.html")


@app.route("/search_api", methods=["GET"]) # constructing get Req to help with search logic
def search():
    query = request.args.get("query", "") 
    model = request.args.get("model", "BM25")
    topN = request.args.get("topN", "10")
    topN = int(topN)


    if model == "BM25":
        query_prepro = BM25_PreProcess(corpus=[query],set_stemming=True,set_lemmatization=False,set_stopwords=True)
        preprocessed_query = query_prepro.get_corpus()[0]

        
        bm25 = BM25(corpus=processed_corpus, k1=1.5, b=1.0) # still yet to tune 
        results = bm25.rank(preprocessed_query) #
        results_out = results.copy().head(topN)
        
        # page_resp = (results_out[['title','content']].to_dict(orient="records"))
        page_resp = (
        results_out[['title', 'content']]
        .rename(columns={"content": "description"})
        .to_dict(orient="records")
                    )
        #issues --> we need a json output ofc but the redirect is getting in the way

        print(results_out)
        return jsonify(page_resp)  ## this bit here is the issue it forces a redirect to the JSON output rather than the page 
        #needs fixing

    if model == "LanguageModel":
        query_prepro = BM25_PreProcess(corpus=[query],set_stemming=True,set_lemmatization=False,set_stopwords=True)
        preprocessed_query = query_prepro.get_corpus()[0]

        uniLM = UnigramLM(corpus=processed_corpus, mu= 500)
        results = uniLM.rank(preprocessed_query) 
        results_out = results.copy().head(topN)
        
        # page_resp = (results_out[['title','content']].to_dict(orient="records"))
        page_resp = (
        results_out[['title', 'content']]
        .rename(columns={"content": "description"})
        .to_dict(orient="records")
                    )
        #issues --> we need a json output ofc but the redirect is getting in the way

        print(results_out)
        return jsonify(page_resp)

    return jsonify([])

    



@app.route("/styles.css")
def styles():
    return send_from_directory(".", "styles.css")

@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")


if __name__ == "__main__":
    app.run(debug=True)
