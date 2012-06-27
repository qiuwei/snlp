'''
Created on Jun 27, 2012

@author: wqiu
'''
from nltk import SnowballStemmer

class SenseTagger(object):
    
    prior_sense_dist = {}
    word_sense_dist = {}
    
    def __init__(self, model):
        self.prior_sense_dist = model[0]
        self.word_sense_dist = model[1]
        self.snstmr = SnowballStemmer("english")
    
    def tag(self, sentence):
        context = map(lambda x: self.snstmr.stem(x), sentence.lower().strip().split())
        predict_sense = "init"
        prob = float('-inf')
        for candi_sense in self.prior_sense_dist.keys():
            #print candi_sense
            current_prob = self.prior_sense_dist[candi_sense]
            #print current_prob
            #print '--------'
            for word in context:
                try:
                    current_prob += self.word_sense_dist[(word, candi_sense)]  
                    #print current_prob
                except KeyError:
                    pass
            #print current_prob, prob
            if current_prob > prob:
                predict_sense = candi_sense
                #update the probability
                prob = current_prob
        
        return predict_sense

if __name__ == '__main__':
    pass
        