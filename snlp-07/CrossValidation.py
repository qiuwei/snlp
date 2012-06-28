'''
Created on Jun 27, 2012

@author: wqiu
'''
from SenseTagger import SenseTagger
from MFSTagger import MFSTagger
from SenseModelLearner import SenseModelLearner

class CrossValidation(object):
    
    @staticmethod
    # search best epsilon in epsilon range provided by user
    def evalutate(corpus, epsilon_range = None):
        best_accuracy = 0.0
        best_accuracy_ms = 0.0
        best_ep = 0
        correct_num = 0
        for ep in epsilon_range:
            correct_num = 0
            correct_num_ms = 0
            for i in range(len(corpus)):                        
                model = SenseModelLearner.learn([corpus[j] for j in range(len(corpus)) if j !=i], ep)
                st = SenseTagger(model)
                mst = MFSTagger(model[0])
                tag = st.tag(corpus[i].get_context())
                tag_ms = mst.tag(corpus[i].get_context())
                if (tag == corpus[i].get_sense()):
                    correct_num += 1
                if (tag_ms == corpus[i].get_sense()):
                    correct_num_ms += 1
            accuracy = float(correct_num) / float(len(corpus))
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_ep = ep 
            
            accuracy_ms = float(correct_num_ms) / float(len(corpus))
            if accuracy_ms > best_accuracy_ms:
                best_accuracy_ms = accuracy_ms
                
        
        return (best_accuracy, best_ep, best_accuracy_ms)
