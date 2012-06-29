'''
Created on Jun 29, 2012

@author: wqiu
'''

class Instance(object):
    '''
    instance in the corpus, stored as a list of tuple(word, pos)
    '''
    result = None
    
    def __init__(self, context, pos = None):
        '''
        Constructor
        '''
        cntxt_lst = context.strip().lower().split()
        if pos != None:
            pos_lst = pos.strip().lower().split()
        
        self.result = len(cntxt_lst) * [None]
        for i in range(len(cntxt_lst)):
            self.result[i] = [cntxt_lst[i], pos_lst[i]]
    
    def __str__(self):
        s = ""
        for i in self.result:
            s = s + " " + i[0] + "/" + i[1]
        return s[1:]
    
    # get the context of instance.
    # if index is specified then return (word, pos) at specific position
    # else return the whole list
    def get(self, idx = None):
        if idx != None:
            return self.result[idx]
        else:
            return self.result 
        
        