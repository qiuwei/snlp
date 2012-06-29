'''
Created on Jun 15, 2012

@author: ehsan
'''

from sets import  Set
from copy import deepcopy
class SNLPClass(object):
    class_count=0
    class_name=""
    features_freq_map={}
    def __init__(self,class_name,features_freq_map, class_count ):
        self.class_count = class_count
        self.features_freq_map = features_freq_map
        self.class_name = class_name
    def get_class_count(self):
        return self.class_count
    def get_features_freq_map(self):
        return self.features_freq_map
    def get_class_name(self):
        return self.class_name    
        
class DataSet(object):
    '''
    classdocs
    '''
    
    freq_map = {}
    class_counts_map={}
    feature_counts_map={}
    sum_of_classes=0.0
    sum_of_features=0.0
    def __init__(self):
        '''
        Constructor
        '''
    def add_new_class(self, snlp_class ):
        #consistency should be checked later
        self.sum_of_classes += snlp_class.get_class_count()
        
        self.class_counts_map[snlp_class.get_class_name()]=snlp_class.get_class_count()
        self.freq_map[snlp_class.get_class_name()] = snlp_class
        
        for feature,count in snlp_class.get_features_freq_map().items():
            self.sum_of_features = self.sum_of_features + count
            if self.feature_counts_map.has_key(feature):
                self.feature_counts_map[feature]= self.feature_counts_map[feature] + count
                self.sum_of_features = self.sum_of_features + count
            else:
                self.feature_counts_map[feature]=count
                
        
        
    def get_features_list(self ):
        return self.feature_counts_map.keys()
    
    def get_classes_list(self):
        return self.class_counts_map.keys()
    
        
    def get_prob_feature(self, feature_name ):
        # n(documents have t) / n(documents)
        if self.sum_of_classes!=0:
            return self.get_count_feature(feature_name)/self.sum_of_classes
        else:
            return 0.0
    def get_prob_feature2(self, feature_name ):
        prob=0.0
        for class_name in self.get_classes_list():
            #print (feature_name , class_name , self.get_cond_prob_feature_class(feature_name, class_name))
            prob += self.get_cond_prob_feature_class(feature_name, class_name) * self.get_prob_class(class_name)   
        return prob    
    def get_prob_class(self, class_name):
        if self.sum_of_classes!= 0 :
            return self.get_count_class(class_name)/self.sum_of_classes
        else:
            return 0.0    
            
    def get_cond_prob_feature_class(self,feature_name,class_name):
        if self.class_counts_map.has_key(class_name):
            class_count = self.class_counts_map[class_name]
            return self.get_joint_count_feature(feature_name, class_name, True, True)/float(class_count)
        else:
            return 0
    def get_cond_prob_class_feature(self,feature_name,class_name, pf):
        (A,B,C,D)=self.get_joint_count_feature2(feature_name, class_name)
        N=A+B+C+D
        
        if pf==1:
            return ( A/N , 0 )
        else:
            return ( (A/N) / pf , (C/N) / (1 - pf )  )
    def get_cond_prob_class_feature2(self,feature_name,class_name, pf): 
        pc = self.get_prob_class(class_name)
        ptc = self.get_cond_prob_feature_class(feature_name, class_name)
        
        if (pf==0):
            return (0, pc * (1-ptc) / (1-pf))
        elif (pf==1):
            return (pc * ptc / pf , 0)
        else:
            return (pc * ptc / pf , pc * (1-ptc) / (1-pf) )
   
        
      
    def get_features_count_map(self):
        return self.feature_counts_map
    def get_joint_count_feature2(self, feature_name, class_name):
       
       
        snlp_class = self.freq_map[class_name]
        features_map = snlp_class.get_features_freq_map()
        total_features_class_count = sum(features_map.values())
        if features_map.has_key(feature_name):
             A = features_map[feature_name]
        else:
             A = 0.0
          
     
        B = self.feature_counts_map[feature_name] - A 
        
        C = total_features_class_count - A
        
        D = self.sum_of_features - (A+B+C)
        
        return (A,B,C,D)         
    def get_joint_count_feature(self, feature_name, class_name, feature_appeared, class_appeared):
        
        if feature_appeared==True and class_appeared==True:
             #print 1
             if self.freq_map.has_key(class_name):
                 snlp_class = self.freq_map[class_name]
                 features_map = snlp_class.get_features_freq_map()
                 
                 if features_map.has_key(feature_name):
                     return features_map[feature_name]
                 else:
                     return 0.0
             else:
                 return 0.0    
             
        
        elif feature_appeared==True and class_appeared==False:
            #print 2
            feature_class_count=0.0
            if self.freq_map.has_key(class_name):
                 snlp_class = self.freq_map[class_name]
                 features_map = snlp_class.get_features_freq_map()
                 if features_map.has_key(feature_name):
                     feature_class_count = features_map[feature_name]
            if self.feature_counts_map.has_key(feature_name):
                return self.feature_counts_map[feature_name] - feature_class_count 
            
            
        
        elif feature_appeared==False and class_appeared==True:
            #print 3
            feature_class_count=0.0
            total_features_class_count=0.0
            if self.freq_map.has_key(class_name):
                 snlp_class = self.freq_map[class_name]
                 features_map = snlp_class.get_features_freq_map()
                 total_features_class_count = sum(features_map.values())
                 if features_map.has_key(feature_name):
                     feature_class_count = features_map[feature_name]
            return total_features_class_count - feature_class_count
        
        elif feature_appeared==False and class_appeared==False:
           # print 4
            sums = 0.0
            #===================================================================
            # for cn in self.get_classes_list():
            #    for fn in self.get_features_list():
            #        if cn!=class_name and fn!=feature_name:
            #            sums += self.get_joint_count_feature(fn, cn, True, True)
            #===================================================================
            
            sums = self.sum_of_features - (self.get_joint_count_feature(feature_name, class_name, True, True)\
                                            +self.get_joint_count_feature(feature_name, class_name, True, False)\
                                            +self.get_joint_count_feature(feature_name, class_name, False, True))
            return sums        
            
    
    def get_count_feature(self,feature_name):
        if self.feature_counts_map.has_key(feature_name):
            return self.feature_counts_map[feature_name]
        else:
            return 0.0
    
    
    def get_count_class(self,class_name):
        if self.class_counts_map.has_key(class_name):
            return self.class_counts_map[class_name]
        else:
            return 0.0
            
        
    def get_subset_dataset(self,feature_subset):
        subset_dataset = DataSet()
        for snlp_class in self.freq_map.values():
            new_features_freq_map = deepcopy(snlp_class.get_features_freq_map())
            for feature_name in snlp_class.get_features_freq_map().keys():
                if feature_name not in feature_subset:
                    new_features_freq_map.pop(feature_name)
            new_snlp_class = \
                SNLPClass(snlp_class.get_class_name(), new_features_freq_map, snlp_class.get_class_count())
            subset_dataset.add_new_class(new_snlp_class)  
        return subset_dataset  
                                      
