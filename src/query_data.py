import pandas as pd
from pathlib import Path
from src.PreProcessingPipeline import BM25_PreProcess

ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = ROOT / "data" / "archive-5" / "archive (2)" / "bbc-news-data.csv"


corpus_df = pd.read_csv(CORPUS_PATH, sep="\t")

print("Columns:", corpus_df.columns.tolist())

if "content" not in corpus_df.columns:
    if "text" in corpus_df.columns:
        corpus_df = corpus_df.rename(columns={"text": "content"})
    else:
        raise KeyError("No 'content' or 'text' column found")

if "title" not in corpus_df.columns:
    corpus_df["title"] = ""

corpus = (
    corpus_df["title"].fillna("").astype(str) + " " +
    corpus_df["content"].fillna("").astype(str)
).str.strip().tolist()

processed_corpus = BM25_PreProcess(
    corpus=corpus,
    set_stemming=True,
    set_lemmatization=False,
    set_stopwords=True
).get_corpus()

query = pd.DataFrame([
    {"query": "stock market interest rates", "category": "business"},
    {"query": "company profits economic growth", "category": "business"},
    {"query": "oil prices global economy", "category": "business"},
    {"query": "bank inflation consumer spending", "category": "business"},
    {"query": "business merger corporate earnings", "category": "business"},

    {"query": "film awards best actor", "category": "entertainment"},
    {"query": "pop music chart success", "category": "entertainment"},
    {"query": "television celebrity interview", "category": "entertainment"},
    {"query": "cinema release box office", "category": "entertainment"},
    {"query": "album launch music industry", "category": "entertainment"},

    {"query": "government election campaign", "category": "politics"},
    {"query": "prime minister policy reform", "category": "politics"},
    {"query": "parliament debate public services", "category": "politics"},
    {"query": "minister resignation political party", "category": "politics"},
    {"query": "tax policy government spending", "category": "politics"},

    {"query": "football team championship win", "category": "sport"},
    {"query": "tennis player grand slam", "category": "sport"},
    {"query": "cricket match captain performance", "category": "sport"},
    {"query": "manager injury squad selection", "category": "sport"},
    {"query": "league title race season", "category": "sport"},

    {"query": "software security internet users", "category": "tech"},
    {"query": "mobile phone technology innovation", "category": "tech"},
    {"query": "computer virus online attack", "category": "tech"},
    {"query": "digital media broadband services", "category": "tech"},
    {"query": "technology company new device", "category": "tech"},
])

query_prepro = BM25_PreProcess(
    corpus=query["query"].tolist(),
    set_stemming=True,
    set_lemmatization=False,
    set_stopwords=True
).get_corpus()