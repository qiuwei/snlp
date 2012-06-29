'''
Created on Jun 30, 2012

@author: wqiu
'''

class BrillTaggerTrainer(object):
    '''
    classdocs
    '''


    def __init__(self, initial_tagger, template):
        '''
        Constructor
        '''
        self.initial_tagger = initial_tagger
        self.template = template
    
    def train(self, corpus, max_error = None, max_rules = None):
        pass

        