'''
Created on Jun 30, 2012

@author: wqiu
'''
from BrillTagger import BrillTagger
from collections import defaultdict

class BrillTaggerTrainer(object):
    '''
    classdocs
    '''


    def __init__(self, initial_tagger, templates):
        '''
        Constructor
        '''
        self._initial_tagger = initial_tagger
        self._templates = templates
    
    def train(self, corpus, max_rules=200, min_score=2):
        '''
        Train Brill Tagger on the corpus
        produce at most *max_rules* transformations, each of which
        reduces the number of errors in the corpus at least *min_score*
        '''
        test_corpus = [self._initial_tagger.tag(sent.get_words()) for sent in corpus]
        
        
        rules = []
        try:
            while len(rules) < max_rules:
                (rule, score, fixscore) = self._best_rule(test_corpus, corpus)
                if rule is None or score < min_score:
                    print 'Insufficient improvement; stopping'
                    break
                else:
                    rules.append(rule)
                    print "A new rule found!"
                    k = 0
                    for sent in test_corpus:
                        k += len(rule.apply(sent))
        except KeyboardInterrupt:
            print "Training stopped manually -- %d rules found" % len(rules)
        
        return BrillTagger(self._initial_tagger, rules)
    
    def _best_rule(self, test_corpus, corpus):
        '''
        Create a dictionary mapping from each tag to a list of the indices
        that have that tag in both test_corpus and corpus
        '''
        
        correct_indices = defaultdict(list)
        for sentnum, sent in enumerate(test_corpus):
            for wordnum, tagged_word in enumerate(sent):
                if tagged_word[1] == corpus[sentnum].get(wordnum)[1]:
                    tag = tagged_word[1]
                    correct_indices[tag].append( (sentnum, wordnum))
                    
        rules = self._find_rules(test_corpus, corpus)
        
        best_rule, best_score, best_fixscore = None, 0, 0
        
        
        for (rule, fixscore) in rules:
            if best_score >= fixscore:
                return best_rule, best_score, best_fixscore
        
        
            score = fixscore
            if rule.original_tag in correct_indices:
                for (sentnum, wordnum) in correct_indices[rule.original_tag]:
                    if rule.applies(test_corpus[sentnum], wordnum):
                        score -= 1
                        if score <= best_score:
                            break
            
            if score > best_score:
                best_rule, best_score, best_fixscore = rule, score, fixscore
        
        return best_rule, best_score, best_fixscore         
    
    def _find_rules(self, test_corpus, corpus):
        '''
        Find all rules that correct at least one token's tag in *test_corpus*.
        '''
        
        error_indices = []
        for sentnum, sent in enumerate(test_corpus):
            for wordnum, tagged_word in enumerate(sent):
                if tagged_word[1] != corpus[sentnum].get(wordnum)[1]:
                    error_indices.append( (sentnum, wordnum) )
        
        rule_score_dict = defaultdict(int)
        for (sentnum, wordnum) in error_indices:
            test_sent = test_corpus[sentnum]
            train_sent = corpus[sentnum].get()
            for rule in self._find_rules_at(test_sent, train_sent, wordnum):
                rule_score_dict[rule] += 1
        
        print "%d candidated rules found in current iteration! " % len(rule_score_dict)
        return sorted(rule_score_dict.items(), key=lambda (rule, score): -score)
    
    def _find_rules_at(self, test_sent, train_sent, i):
        applicable_rules = set()
        
        if test_sent[i][1] != train_sent[i][1]:
            correct_tag = train_sent[i][1]
            for template in self._templates:
                new_rules = template.applicable_rules(test_sent, i, correct_tag)
                applicable_rules.update(new_rules)
        
        return applicable_rules