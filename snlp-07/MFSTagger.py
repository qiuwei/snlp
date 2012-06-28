'''
Created on Jun 28, 2012

@author: wqiu
'''
from nltk import SnowballStemmer

class MFSTagger(object):
    '''
    most frequent sense Tagger, will be used as baseline system
    '''


    def __init__(self, model):
        '''
        Constructor
        '''
        self.prior_sense_dist = model
        self.snstmr = SnowballStemmer("english")
    
    def tag(self, sentence):
        context = map(lambda x: self.snstmr.stem(x), sentence.lower().strip().split())
        predict_sense = "init"
        prob = float('-inf')
        for candi_sense in self.prior_sense_dist.keys():
            #print candi_sense
            current_prob = self.prior_sense_dist[candi_sense]
            if current_prob > prob:
                predict_sense = candi_sense
                #update the probability
                prob = current_prob
        return predict_sense
