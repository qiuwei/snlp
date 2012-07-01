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


def evaluate(tagger, test_corpus):
    total_num = 0
    error_num = 0
    for sent in test_corpus:
        total_num += len(sent)
        result = tagger.tag(sent.get_words())
        for i in range(len(sent)):
            if result[i][1] != sent.get(i)[1]:
                error_num += 1
    print total_num, error_num
    return float(total_num - error_num) / (total_num)

if __name__ == '__main__':
    train_corpus = CorpusReader.readin('train.pos')
    model = MLETagLearner.learn(train_corpus)
    mle_tagger = MLETagger(model)
    
    test_corpus = CorpusReader.readin('test.pos.txt')
    
    
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
    
    trainer =  BrillTaggerTrainer(mle_tagger, templates)
    brill_tagger = trainer.train(train_corpus, 200, 2)
    
    print "The accuracy of MLE tagger is %f" % evaluate(mle_tagger, test_corpus)
    print "The accuracy of brill tagger is %f" % evaluate(brill_tagger,test_corpus)
    
#    for i in corpus:
#        print mle_tagger.tag(i.get_words())
#        print brill_tagger.tag(i.get_words())
#    
    