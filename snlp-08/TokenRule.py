'''
Created on Jun 30, 2012

@author: wqiu
'''
from BrillRule import BrillRule

class TokenRule(BrillRule):
    '''
    Abstract base class for actural rules, condistions are tuples (start, end , value)
    It checks whether range(start, end) contains value.
    Value is a certain property of token, maybe tag or word
    '''


    def __init__(self, original_tag, replacement_tag, *conditions):
        '''
        Constructor
        '''
        assert self.__class__ != TokenRule, "TokenRule is an abstract base class"
        BrillRule.__init__(self, original_tag, replacement_tag)
        self._conditions = conditions
        for (s, e, v) in conditions:
            if s > e:
                raise ValueError('Condition %s has an invalid range' % ((s, e, v), ))
        
    @staticmethod   
    def extract_property(token):
        assert False, "TokenRule must define extract_property()"
    
    def applies(self, tokens, index):
        if tokens[index][1] != self.original_tag:
            return False
    
        for (start, end , val) in self._conditions:
            s = max(0, index+start)
            e = min(index+end+1, len(tokens))
            
            
            for i in range(s, e):
                if self.extract_property(tokens[i]) == val:
                    break
            else:
                return False
        
        # Every condition checked out, rule is applicable
        return True
    
    def __eq__(self, other):
        return (self is other or 
                (other is not None and  
                 other.__class__ == self.__class__ and 
                 self.original_tag == other.original_tag and 
                 self.replacement_tag == other.replacement_tag and  
                 self._conditions == other._conditions ))
                 
    def __ne__(self, other):
        return not (self == other)
    
    
    def __hash__(self):
        try:
            return self.__hash
        except:
            self.__hash = hash((self.original_tag, self.replacement_tag, self._conditions, self.__class__.__name__))
            return self.__hash