'''
Created on Jun 27, 2012

@author: wqiu
'''
from SenseTagger import SenseTagger
from SenseModelLearner import SenseModelLearner

class CrossValidation(object):
    
    @staticmethod
    # search best epsilon in epsilon range provided by user
    def evalutate(corpus, epsilon_range = None):
        best_accuracy = 0.0
        best_ep = 0
        correct_num = 0
        for ep in epsilon_range:
            correct_num = 0
            for i in range(len(corpus)):                        
                st = SenseTagger( SenseModelLearner.learn([corpus[j] for j in range(len(corpus)) if j !=i], ep))
                tag = st.tag(corpus[i].get_context())
                if (tag == corpus[i].get_sense()):
                    correct_num += 1
            accuracy = float(correct_num) / float(len(corpus))
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_ep = ep 
        
        return (best_accuracy, best_ep)
