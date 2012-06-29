'''
Created on Jun 29, 2012

@author: wqiu
'''

class MLETagLearner(object):
    '''
    learn the MLE tag for each word from corpus, will be used as the model for InitTagger
    '''


#    def __init__(self):
#        '''
#        Constructor
#        '''
#        
    @staticmethod
    def learn(corpus):
        wp_dict = {}
        vocab = {}
        tag_set = []
        for i in corpus:
            for wp in i.get():
                if wp[0] not in vocab.keys():
                    vocab[wp[0]] = None
                if wp[1] not in tag_set:
                    tag_set.append(wp[1])
                try:
                    wp_dict[wp] += 1
                except KeyError:
                    wp_dict[wp] = 1
                    
        for w in vocab.keys():
            max_occur_num = 0
            for t in tag_set:
                try:
                    #find out the most frequent tag
                    if wp_dict[(w,t)] > max_occur_num:
                        vocab[w] = t
                        max_occur_num = wp_dict[(w,t)]
                except KeyError:
                    pass
        return vocab
            