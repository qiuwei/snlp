'''
Created on Jun 30, 2012

@author: wqiu
'''

class BrillTemplate(object):
    '''
    Interface for genertating lists of transformational rules that apply at given sentence positions.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def applicable_rules(self, tokens, i, correct_tag):
        '''
        return a list of transformational rule that would correct the *i* th subtoken's tag in the given token.
        return a list of zero or more rules that would change *tokens*[i][1] to *correct_tag*, if applied to *tokens*[i]
        '''
        raise NotImplementedError()
    