'''
Created on Jun 30, 2012

@author: wqiu
'''

class BrillRule(object):
    '''
    classdocs
    '''


    def __init__(self, original_tag, replacement_tag):
        '''
        Constructor
        '''
        assert self.__class__ != BrillRule, "BrillRule is an abstract base class"
        
        
        self.original_tag = original_tag
        self.replacement_tag = replacement_tag
        
        
    def apply(self, tokens, positions=None):
        if positions is None:
            positions = range(len(tokens))
            
        change = [i for i in positions if self.applies(tokens, i)]
        
        for i in change:
            tokens[i] = (tokens[i][0], self.replacement_tag)
        
        return change
    
    def applies(self, tokens, index):
        assert False, "Brill rules must define applies()"
    
    def __eq__(self):
        assert False, "Brill rules must be comparable"
    
    def __ne__(self):
        assert False, "Brill rules must be comparable"
        
    def __hash__(self):
        assert False, "Brill rules must be hashable"