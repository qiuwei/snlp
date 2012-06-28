'''
Created on Jun 27, 2012

@author: ehsan
'''
import os
from SenseParser import WordSenseParser
from SenseModelLearner import SenseModelLearner
from SenseTagger import SenseTagger
from CrossValidation import CrossValidation
import math

def seq(start, stop, step=1):
    n = int(math.floor((stop - start)/float(step)))
    if n >= 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([start]) 
    
if __name__ == '__main__':
    path = "TWA.sensetagged"
    for root, dirs,files in os.walk(path):
        if dirs==[]:
            for f_name in files:
                with open (os.path.join(root,f_name),'r')  as f_in:
                    data = f_in.read()
                    corpus = WordSenseParser.parse(data)
                    print CrossValidation.evalutate(corpus, seq(0.1, 0.2))

           
    