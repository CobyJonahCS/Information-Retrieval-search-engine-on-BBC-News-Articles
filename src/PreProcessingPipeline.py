import string 
import nltk
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.corpus import stopwords
import re

# nltk.download('wordnet')

class BM25_PreProcess:

    def __init__(self,corpus,set_stemming,set_lemmatization,set_stopwords):
        """ Experiment with different pre processing 
        Pre Processing must be the exact same as what we use for the query this is very important
        """
        self.corpus = corpus
        self.set_stemming = set_stemming
        self.set_lemmatization = set_lemmatization
        self.set_stopwords = set_stopwords
        pass

    def _preprocess (self):

        """ This function does the actual heavy liftinf 
            Removes punctuation, lowercases everything ,stems 
            lemmatizes and optionally removes stop words. 

            not sure if stemming, lemmatization or stop words is really neccesary. 
            we can see as we go along 
        """
        
        
        #gets rid of punc and lowercases
        #also removes special characters too

        init_corpus = [article.lower() for article in self.corpus]
        init_corpus = [article.translate(str.maketrans('', '', string.punctuation)) for article in init_corpus]
        init_corpus = [re.sub(r'\W', ' ',article) for article in init_corpus]

        init_corpus = [article.split(" ") for article in init_corpus] # tokenises corpus

        #all optional params here 
        if self.set_stopwords:
            nltk.download('wordnet') # grabs stop words lists incase its needed
            stop_words_ref = set(stopwords.words('english'))
            init_corpus = [[word for word in article if word not in stop_words_ref] for article in init_corpus]
        if self.set_stemming: 
            stemmer = PorterStemmer()
            init_corpus = [[stemmer.stem(word) for word in article] for article in init_corpus]
        if self.set_lemmatization: 
            lemmatizer = WordNetLemmatizer()
            init_corpus = [[lemmatizer.lemmatize(word) for word in article] for article in init_corpus]

        processed_corpus = init_corpus
        

        return processed_corpus
    def get_corpus(self):
        """ simple getter for fully processed corpus now"""
        return self._preprocess()

