'''
Created on Jun 29, 2012

@author: wqiu
'''
from CorpusReader import CorpusReader
from MLETagLearner import MLETagLearner
from MLETagger import MLETagger

if __name__ == '__main__':
    corpus = CorpusReader.readin('train.pos.txt')
    model = MLETagLearner.learn(corpus)
    it = MLETagger(model)
    pos_result = it.tag("what push push")
    for p in pos_result:
        print p
    
    