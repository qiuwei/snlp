'''
Created on Jun 29, 2012

@author: wqiu
'''

class MLETagger(object):
    '''
    Base tagger, used to give a initial tag for sentence, correction will be based on this result
    '''
    model = None

    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
        
    def _tag_string(self, sentence):
        word_lst = sentence.strip().lower().split()
        pos_lst = []
        for w in word_lst:
            try:
                pos_lst.append((w,self.model[w]))
            except KeyError:
                pos_lst.append((w, 'n'))    
        return pos_lst
    
    def _tag_tokens(self, tokens):
        pos_lst = []
        for w in tokens:
            try:
                pos_lst.append((w, self.model[w]))
            except KeyError:
                pos_lst.append((w,'n'))    
        return pos_lst   

    def tag(self, para):
        if type(para) == list:
            return self._tag_tokens(para)
        else:
            return self._tag_string(para)