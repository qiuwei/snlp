'''
Created on Jun 30, 2012

@author: wqiu
'''
from collections import defaultdict

class BrillTagger(object):
    '''
    Brill tagger implementation
    '''
    
    def __init__(self, init_tagger, rules):
        self._init_tagger = init_tagger
        self._rules = tuple(rules)
        
    def rules(self):
        return self._rules
    
    def _tag_tokens(self, tokens):
        tagged_tokens = self._init_tagger.tag(tokens)
        
        tag_to_positions = defaultdict(set)
        for i, (token, tag) in enumerate(tagged_tokens):
            tag_to_positions[tag].add(i)
        
        for rule in self._rules:
            positions = tag_to_positions.get(rule.original_tag, [])
            changed = rule.apply(tagged_tokens, positions)
            
            for i in changed:
                tag_to_positions[rule.original_tag].remove(i)
                tag_to_positions[rule.replacement_tag].add(i)
                
        return tagged_tokens
    
    def _tag_string(self, sentence):
        tokens = sentence.strip().lower().split()
        return self._tag_tokens(tokens)
        
    def tag(self, param):
        if type(param) == list:
            return self._tag_tokens(param)
        else:
            return self._tag_string(param)
    
