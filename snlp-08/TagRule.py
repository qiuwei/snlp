'''
Created on Jun 30, 2012

@author: wqiu
'''
from TokenRule import TokenRule

class TagRule(TokenRule):
    '''
    classdocs
    '''


    @staticmethod 
    def extract_property(token):
        ''':return: The given token's tag'''
        return token[1]
        