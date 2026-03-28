
import math
import numpy as np # not used as of yet could probably help give a bit of a speed up but might not be important
import pandas as pd # for our dataset

class BM25:

    def __init__(self,corpus,k1,b):
        """ K1 and b are our parameters, these can be tuned later on 
            we assume our corpus is already pre processed using the pipleline module we made

            here is just super useful defenitions and constants we need to use
        
        """
        
        self.corpus = corpus # corpus 
        
        #IR Model params 
        self.k1 = k1
        self.b = b 
        self.N = len(corpus)

        #doc norms
        self.doc_lens = [len(article) for article in corpus]
        self.avgdl = ((1/self.N) * (sum(self.doc_lens)))

        self.bow_collection = set(word for doc in self.corpus for word in doc) #ibr i didnt even need this in the end, lowkey overthinked this 
        self.df = pd.read_csv("../data/archive(5)/archive (2)/bbc-news-data.csv",sep="\t")# used for mainly output
        
        #super slow though, could use some form of memoization to speed up ?

        #add a cache to track the IDF score per each term  probably help with the run time a tad

    def _IDF(self,term):
        #computes the ID on a per term basis 

        nt = 0 
        for article in self.corpus:
            if term in article:
                nt +=1


        idf_val = math.log(((self.N - nt +0.5) / (nt + 0.5)))

        return idf_val
        

    def _TF(self,term,article):
        """ just returns Term frequency according to BM25"""

        f = article.count(term)
        return (f) * (self.k1 +1 ) / (f + self.k1 * (1-self.b+self.b * (len(article)/(self.avgdl))))
        

    def _Score(self,article,query):
        """ computes the sore for an individual article in the corpus"""

        term_scores = []

        for term in query:
            term_scores.append(self._IDF(term) * (self._TF(term=term,article=article)))


        return (sum(term_scores))

    def rank(self,query):
        """ returns the results by appending scores to the df 
            orders by most relevant 
        """

        scores = []

        for article in self.corpus:
            scores.append(self._Score(article=article,query=query))
        self.df['scores'] = scores
        return self.df.sort_values("scores",ascending=False)


