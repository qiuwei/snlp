'''
Created on Jun 29, 2012

@author: wqiu
'''
from CorpusReader import CorpusReader
from MLETagLearner import MLETagLearner
from MLETagger import MLETagger
from TokenTemplate import TokenTemplate
from TagRule import TagRule
from BrillTaggerTrainer import BrillTaggerTrainer

if __name__ == '__main__':
    corpus = CorpusReader.readin('train.pos.txt')
    model = MLETagLearner.learn(corpus)
    it = MLETagger(model)
    
    
    templates = [
                 TokenTemplate(TagRule, (-1, -1)),
                 TokenTemplate(TagRule, (1, 1)),
                 TokenTemplate(TagRule, (-2, -1)),
                 TokenTemplate(TagRule, (1, 2)),
                 TokenTemplate(TagRule, (-3, -1)),
                 TokenTemplate(TagRule, (1, 3)),
                 TokenTemplate(TagRule, (-1, -1), (1,1)),
                 TokenTemplate(TagRule, (-1, -1), (2,2)),
                 TokenTemplate(TagRule, (-2, -2), (1,1)),
                 ]
    
    trainer =  BrillTaggerTrainer(it, templates)
    brill_tagger = trainer.train(corpus, 200, 1)
    
    