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
from cPickle import dump, load


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
    brill_tagger = None
    mle_tagger = None
    try:
        fin = open('mletagger.model', 'rb')
        mle_tagger = load(fin)
        print "MLE tagger loaded"
        fin.close()
    # model doesn't exist
    except IOError:
        print "MLE model not found! Retraining"
        print "Loading training corpus..."
        train_corpus = CorpusReader.readin('train.pos')
        print "Corpus loaded"
        print "Learning MLE tagger..."
        model = MLETagLearner.learn(train_corpus)
        mle_tagger = MLETagger(model)
        print "MLE tagger learned"
        fout = open('mletagger.model', 'wb')
        dump(mle_tagger, fout, -1)
        fout.close()
    
     
    try:
        fin = open('brilltagger.model', 'rb')
        brill_tagger = load(fin)
        print "Brill tagger loaded!"
        fin.close()
    # model doesn't exist
    except IOError:
        print "Brill model not found! Retraining"
        print "Loading training corpus..."
        train_corpus = CorpusReader.readin('train.pos')
        print "Corpus loaded"
        
        
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
        print "Learning new model for brill tagger"
        brill_tagger = trainer.train(train_corpus, 2, 2)
        print "New brill model learned"
        fout = open('brilltagger.model', 'wb')
        dump(brill_tagger, fout, -1)
        fout.close()
    
    test_corpus = CorpusReader.readin('test.pos.txt')
    print "The accuracy of MLE tagger is %f" % evaluate(mle_tagger, test_corpus)
    print "The accuracy of brill tagger is %f" % evaluate(brill_tagger,test_corpus)
    
#    for i in corpus:
#        print mle_tagger.tag(i.get_words())
#        print brill_tagger.tag(i.get_words())
#    
    