'''
Created on Jun 30, 2012

@author: wqiu
'''
from BrillTemplate import BrillTemplate

class TokenTemplate(BrillTemplate):
    '''
    A brill template that generates a list of ''TokenRule'' that apply at a
    given sentence position
    
    Generate all rules that:
    
    - use the given brill rule class
    - use the given list of boundaries as the start and end
    - are applicable to the given token
    '''
    
    def __init__(self, rule_class, *boundaries):
        self._rule_class = rule_class
        self._boundaries = boundaries
        for (s, e) in boundaries:
            if s>e:
                raise ValueError('Boundary %s has an invalid range'% ((s, e),))
    
    
    def applicable_rules(self, tokens, index, correct_tag):
        # already correct, not rules possible
        if tokens[index][1] == correct_tag:
            return []
        
        applicable_conditions = [self._applicable_conditions(tokens, index, start, end) for (start, end) in self._boundaries]
        
        
        # Find all combinations of applicable conditions
        condition_combos = [[]]
        for conditions in applicable_conditions:
            condition_combos = [old_conditions + [new_condition]
                                for old_conditions in condition_combos
                                for new_condition in conditions]
        
        return [self._rule_class(tokens[index][1], correct_tag, *conds)
                for conds in condition_combos]
    
    
    def _applicable_conditions(self, tokens, index, start, end):
        '''
        return a list of all tuples of (start, end, value), such that property value of at least one token
        between *index+start* and *index+end* (inclusive) is *value*
        '''
        conditions = []
        s = max(0, index+start)
        e = min(index+end+1, len(tokens))
        for i in range(s, e):
            value = self._rule_class.extract_property(tokens[i])
            conditions.append( (start, end, value) )
        return conditions
        
        
    