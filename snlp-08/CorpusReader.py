'''
Created on Jun 29, 2012

@author: wqiu
'''
from Instance import Instance

class CorpusReader(object):
    '''
    class to read in corpus from text file, store it simply as list
    '''

#    def __init__(selfparams):
#        '''
#        Constructor
#        '''
        
    @staticmethod
    def readin(file_name):
        corpus = []
        with open(file_name, 'r') as fin:
            current_ln = fin.readline()
            while current_ln != '':
                #print current_ln
                context = current_ln
                pos = fin.readline()
                corpus.append(Instance(context, pos))
                fin.readline() #skip the blank line
                current_ln = fin.readline()
        return corpus

if __name__=='__main__':
    corpus = CorpusReader.readin('train.pos.txt')
    for i in corpus:
        print i
