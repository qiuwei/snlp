'''
Created on Jun 15, 2012

@author: ehsan
'''
import os
from DataSet import *
from FeatureSelection import *
from string import punctuation
from nltk import wordpunct_tokenize
import matplotlib.pyplot as plt
from Classifier import Perceptron
def featureSelection(path):
     
     
     dataset = DataSet()
     class_name=''
     TrainSet=[]
     for root, dirs,files in os.walk(path):
         #print root
         if dirs==[]:
             if class_name != os.path.basename(root):
                class_name = os.path.basename(root)
                print class_name
                class_count = len(files)
                freq_map={}
                for f in files:
                  temp_set = set()
                  #print class_name , " <--> " ,f
                  with open (os.path.join(root,f),'r')  as fin:
                      lines = fin.readlines()
                      for line in lines:
                          for token in wordpunct_tokenize(line):
                              if token not in punctuation:
                                  temp_set.add(token.lower())
                               
                  for token in temp_set:
                      if freq_map.has_key(token):
                          freq_map[token] = freq_map[token] + 1
                      else:
                          freq_map[token]=1
                                  
                          
                          
                dataset.add_new_class(SNLPClass(class_name, freq_map,class_count))
                          
     return dataset

def classifier_parser(path,features_list):
    class_name=''
    TrainSet=[]
    for root, dirs,files in os.walk(path):
         #print root
         if dirs==[]:
                class_name = os.path.basename(root)
                class_count = len(files)
                
                for f in files:
#                  print f
                  #print class_name , " <--> " ,f
                  with open (os.path.join(root,f),'r')  as fin:
                      lines = fin.readlines()
                      TrainSet.append( (featureCounter(lines, features_list),class_name)      )
    return TrainSet 
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
                    
def runRainbowFeatures(path_train,path_test, path_features, dataset,n=1000,iter_num=5):
    features=[]
    with open(path_features,'r') as f_in:
        for line in f_in:
            features.append(line.split()[1])
    model = Perceptron.train_from_disk(path_train,dataset.get_classes_list() ,features[0:n], iter_num)
    for k,v in model.items():
        print k,v
    print Perceptron.test_from_disk(model, path_test,features[0:n])
        
def runAndreaFeatures(path_train,path_test, path_features, dataset,n=1000,iter_num=5):
    features=[]
    with open(path_features,'r') as f_in:
        for line in f_in:
            for token in line.split():
                features.append(token)
    model = Perceptron.train_from_disk(path_train,dataset.get_classes_list() ,features[0:n], iter_num)
    print Perceptron.test_from_disk(model, path_test,features[0:n])
                 
if __name__=='__main__':
     path_train='20-ng/train'
     path_test='20-ng/test'
     path_rainbow_features='IG100000'
     path_andrea_features = 'features.txt'
     dataset = featureSelection(path_train)
     #feat= dataset.get_features_list()
     #train_set =  classifier_parser(path,feat)
     #model = Perceptron.train_from_disk(path_train,dataset.get_classes_list() ,dataset.get_features_list(), 5)
     #print Perceptron.test_from_disk(model, path_test,dataset.get_features_list())
     #print len(dataset.get_features_list())
     #ig_tuples= FeatureSelector.get_IG_features(dataset)
     #ig_200 = FeatureSelector.get_top_features(ig_tuples,10000)
     runRainbowFeatures(path_train,path_test,path_rainbow_features , dataset,100,2)
     runAndreaFeatures(path_train, path_test, path_andrea_features, dataset,100,5)
     #chi2_tuples = FeatureSelector.get_CHI2_features(dataset)
     #chi2_200 = FeatureSelector.get_top_features(chi2_tuples,1000)
     #for i in range(len(ig_200)):
         #print ig_200[i][0]
     #--------------------------------------------- for i in range(len(ig_200)):
         #---------- print ig_200[i][0], dataset.get_prob_feature2(ig_200[i][0])
     #model = Perceptron.train_from_disk(path_train,dataset.get_classes_list() ,[feat[0] for feat in ig_200], 5)
     #print "\n\n test accuracy ",Perceptron.test_from_disk(model, path_test,[feat[0] for feat in ig_200])    
     #------------- chi2_200 = FeatureSelector.get_top_features(chi2_tuples,200)
     #--------------------------------------------- for i in range(len(ig_200)):
         #----------------------------- print ig_200[i][0],"\t\t",chi2_200[i][0]
#------------------------------------------------------------------------------ 
  
     