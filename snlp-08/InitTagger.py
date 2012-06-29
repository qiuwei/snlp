'''
Created on Jun 29, 2012

@author: wqiu
'''

class InitTagger(object):
    '''
    Base tagger, used to give a initial tag for sentence, correction will be based on this result
    '''
    model = None

    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
        
    def tag(self, sentence):
        word_lst = sentence.strip().lower().split()
        pos_lst = []
        for w in word_lst:
            try:
                pos_lst.append(self.model[w])
            except KeyError:
                pos_lst.append('noun')    
        return pos_lst
        