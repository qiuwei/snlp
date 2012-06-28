'''
Created on Jun 27, 2012

@author: ehsan
'''
from bs4 import  BeautifulSoup
from WordSenseInstance import WordSenseInstance

class WordSenseParser(object):
    '''
    classdocs
    '''

    @staticmethod
    def parse(data):
        
        word_sense_instance_list =[]
        soup = BeautifulSoup(data)
        for instanceTag in soup.find_all('instance'):
            sense = instanceTag.find('answer').attrs['senseid'].split('%')[1]
            head_word =  instanceTag.find('answer').attrs['senseid'].split('%')[0]
            contextTag = instanceTag.find('context')
            context = contextTag.get_text().strip()
            head_index = context.find(head_word) 
            wordSenseInstance = WordSenseInstance(head_index, head_word, context, sense)
            word_sense_instance_list.append(wordSenseInstance)
            
        
        return word_sense_instance_list 
    
       