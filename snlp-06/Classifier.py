'''
Created on Jun 15, 2012

@author: ehsan
'''
import os
from string import punctuation
from nltk import wordpunct_tokenize

class Perceptron(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def __prcp_argmax(w_map, input_list):
        #very bad way to initialize maxf
        maxf=-1000000000
        maxy=""
        for y,w in w_map.items():
#          print 'w= ',w  
          f= sum([w[index]*input_list[index] for index in range(len(input_list))])
          if f>maxf:
              maxy=y
              maxf=f
        return maxy
    @staticmethod
    def __w_update(w_y,w_yhat,vector):
        new_w_y = [w_y[index]+vector[index] for index in range(len(vector)) ]
        new_w_yhat = [w_yhat[index]-vector[index] for index in range(len(vector)) ]
        return (new_w_y , new_w_yhat)
    #input_data [(list,class_name)]
    @staticmethod
    def train_from_disk(path_to_dataset,list_unique_classes,features_subset,max_iter_num=5):
       
        #print "uniq classes= ",list_unique_classes
        dim_size = len(features_subset)
        #print "dimension ", dim_size
        
        w_map=dict(zip(list_unique_classes,[[0 for d in range(dim_size)]       for v in range(len(list_unique_classes))]))
        #print "w_map:" ,w_map
        iter_num=0
        for iter in range(max_iter_num):
            print '\n\n-------------******------------\n\nTraining iteration:',iter_num
            iter_num += 1
            accuracy_iter=0.0
            all_documents_number=0.0
            for root, dirs,files in os.walk(path_to_dataset):

                if dirs==[]:
                    class_name = os.path.basename(root)
                    print class_name
                    accuracy_class=0.0
                    class_count = len(files)
                    for f in files:
                        with open (os.path.join(root,f),'r')  as fin:
                            all_documents_number += 1.0
                            lines = fin.readlines()
                            datum= (Perceptron.featureCounter(lines, features_subset),class_name)
                            y = datum[1]
                            y_hat = Perceptron.__prcp_argmax(w_map, datum[0])
                            if y!=y_hat:
                                (w_y , w_yhat) = Perceptron.__w_update(w_map[y],w_map[y_hat],datum[0])
                                w_map[y]=w_y
                                w_map[y_hat]=w_yhat
                            else:
                                accuracy_class +=1.0
                                accuracy_iter +=1.0
                    print "class train accuracy", accuracy_class/len(files),"\n\n"          
            print "\n iteration train accuracy", accuracy_iter/all_documents_number,"\n\n"
        return w_map
    @staticmethod   
    def featureCounter(lines, features_list ):
     feat = dict(zip(features_list,[0 for v in range(len(features_list))]))
     token_set=set()
     for line in lines:
            for token in wordpunct_tokenize(line):
                if token not in punctuation :
                    token_set.add(token)
     for token in token_set:
         if feat.has_key(token):
              feat[token]=1
    
     return feat.values()    
    @staticmethod
    def train(input_data,features_subset,iter_num=5):
        list_unique_classes = list(set([datum[1] for datum in input_data]))
        #print "uniq classes= ",list_unique_classes
        dim_size = len(features_subset)
        #print "dimension ", dim_sized
        
        w_map=dict(zip(list_unique_classes,[[0 for d in range(dim_size)]  for v in range(len(list_unique_classes))]))
        #print "w_map:" ,w_map
        for iter in range(iter_num):
            accuracy=0
            print 'Training iteration:',iter_num
            for datum in input_data:
                y = datum[1]
                y_hat = Perceptron.__prcp_argmax(w_map, datum[0])
                if y!=y_hat:
                    (w_y , w_yhat) = Perceptron.__w_update(w_map[y],w_map[y_hat],datum[0])
                    w_map[y]=w_y
                    w_map[y_hat]=w_yhat
                else:
                    accuracy+=1    
        return w_map
    
    @staticmethod
    def eval (w_map,datum):
        y = datum[1]
        y_hat = Perceptron.__prcp_argmax(w_map, datum[0])
        return y_hat
          
    @staticmethod
    def test(w_map, input_data):      
        accuracy=0.0
        for datum in input_data:
            y = datum[1]
            y_hat = Perceptron.__prcp_argmax(w_map, datum[0])
            if y==y_hat:
                accuracy +=1.0
        return accuracy/len(input_data)
            
    @staticmethod
    def test_from_disk(w_map, path_to_dataset, features_subset):      
        accuracy=0.0
        num_instances = 0.0
        for root, dirs,files in os.walk(path_to_dataset):
                all_documents_number=0.0
                
                if dirs==[]:
                    class_name = os.path.basename(root)
                    accuracy_class = 0.0
                    class_count = len(files)
                    for f in files:
                        num_instances += 1
                        with open (os.path.join(root,f),'r')  as fin:
                            lines = fin.readlines()
                            datum= (Perceptron.featureCounter(lines, features_subset),class_name)
                            y = datum[1]
                            y_hat = Perceptron.__prcp_argmax(w_map, datum[0])
                            if y==y_hat:
                                accuracy +=1.0
                                accuracy_class += 1.0
                    print class_name ,"test accuracy", accuracy_class/len(files),"\n\n"     
        return accuracy/num_instances       
          
          
          
          
          
          
          
          
          
            
            
        