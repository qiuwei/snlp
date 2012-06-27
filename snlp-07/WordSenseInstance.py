'''
Created on Jun 27, 2012

@author: ehsan
'''

class WordSenseInstance(object):
    '''
    classdocs
    '''
    _head_index = 0
    _head_word = ""
    _context = ""
    _sense = ""

    def __init__(self,head_index ,head_word,context ,sense):
        '''
        Constructor
        '''
        self._head_index = head_index
        self._head_word = head_word
        self._context = context
        self._sense = sense
    def get_head_index (self):
        return self._head_index
    def get_head_word (self):
        return self._head_word
    def get_context (self):
        return self._context
    def get_sense(self):
        return self._sense
    def __str__(self):
        return self._head_word +' by sense:'+self._sense+' appeared in: '+self._context 
        
        