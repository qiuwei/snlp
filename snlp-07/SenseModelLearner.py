'''
Created on Jun 27, 2012

@author: wqiu
'''
from nltk import SnowballStemmer
import math

class SenseModelLearner(object):
    '''
    classdocs
    '''
    
    @staticmethod 
    def learn(corpus, epsilon=None):
        # set default smooth parameter
        if(epsilon == None):
            epsilon = 0.1
        prior_sense_dist = {}
        total_num_sense = 0
        word_sense_dist = {}
        sense_sum = {}
        snstmr = SnowballStemmer("english")
        #vocabulary = []
        senses = []
        #count all of the sensense
        for instance in corpus:
            sense = instance.get_sense()
            if sense not in senses:
                senses.append(sense)
        # size of vocabulary        
        vsize = 0
        for instance in corpus:
            context = map(lambda x: snstmr.stem(x), instance.get_context().lower().strip().split())
            # count all senses to estimate the distribution of senses
            sense = instance.get_sense()
            total_num_sense += 1
            try:
                prior_sense_dist[sense] += 1
            except KeyError:
                prior_sense_dist[sense] = 1
                    
            #head = instance.get_head_word()
            # count all (word, sense) cooccurece to estimatate the conditional distribution, namely P(word|sense)
            for word in context:
                try:
                    word_sense_dist[(word, sense)] += 1
                #find a new word
                except KeyError:
                    # put it in the matrix
                    vsize += 1
                    word_sense_dist[(word,sense)] = 1 + epsilon
                    # also put it for all other possible senses
                    for s in senses:
                        if s != sense:
                            word_sense_dist[(word, s)] = epsilon
        
        # sum over senses, will be used to calculate the probability
        for k in word_sense_dist.keys():
            try:
                sense_sum[k[1]] += word_sense_dist[k]
            except KeyError:
                sense_sum[k[1]] = 0
                
        for k in word_sense_dist.keys():
            word_sense_dist[k] =  math.log(float(word_sense_dist[k]) / float(sense_sum[k[1]]))
            #print k, word_sense_dist[k]
        #print "========="
        for k in prior_sense_dist.keys():
            prior_sense_dist[k] = math.log(float(prior_sense_dist[k]) / total_num_sense)
            #print prior_sense_dist[k]
            
                
        return (prior_sense_dist,word_sense_dist)


if __name__ == '__main__':
    snstmr = SnowballStemmer("english")
    print snstmr.stem("stemming")
    