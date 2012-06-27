'''
Created on Jun 27, 2012

@author: ehsan
'''
import os
from Sense_Parser import WordSenseParser
from SenseModelLearner import SenseModelLearner
from SenseTagger import SenseTagger

if __name__ == '__main__':
    path = "TWA.sensetagged"
    for root, dirs,files in os.walk(path):
        if dirs==[]:
            for f_name in files:
                with open (os.path.join(root,f_name),'r')  as f_in:
                    data = f_in.read()
                    corpus = WordSenseParser.parse(data)
                    for i in range(len(corpus)):                        
                        st = SenseTagger( SenseModelLearner.learn([corpus[j] for j in range(len(corpus)) if j !=i]))
                        print st.tag(corpus[i].get_context())
                    #for word_sense_instance in word_sense_instance_list:
                    #    print word_sense_instance
            
    