'''
Created on Jun 15, 2012

@author: ehsan
'''
import math
class FeatureSelector(object):
   @staticmethod
   def compute_information_gain(dataset, feature_name):
             
             return  FeatureSelector.__class_entropy(dataset) + \
                     FeatureSelector.__left_right_entropy3(dataset, feature_name)
   
   @staticmethod
   def __class_entropy(dataset):
       entropy = 0.0
       for class_name in dataset.get_classes_list():
           prob = dataset.get_prob_class(class_name)
           if prob != 0:
               entropy = entropy + prob * math.log(prob)
       return -1.0 * entropy 
   
   @staticmethod
   def __left_right_entropy(dataset, feature_name):
       pf = dataset.get_prob_feature(feature_name)
      
       first_sum = 0.0
       sec_sum = 0.0
       A = 0
       B = 0
       for class_name in dataset.get_classes_list():
           pc = dataset.get_prob_class(class_name)
           ptc = dataset.get_cond_prob_feature_class(feature_name, class_name)
           if ptc != 0:
               A += pc * ptc * math.log(pc * ptc / pf) 
           if ptc != 1:
               B += pc * (1 - ptc) * math.log(pc * (1 - ptc) / (1 - pf))
       #========================================================================
       # if pf==0:
       #    print "khak bar sar, prob featuere sefre"
       # elif pf==1:    
       #    print "khak bar sar, prob featuere yeke"
       #    print feature_name,B
       #========================================================================
       return A + B
   @staticmethod
   def __left_right_entropy2(dataset, feature_name):
       pf = dataset.get_prob_feature2(feature_name)
      
       first_sum = 0.0
       sec_sum = 0.0
     
       for class_name in dataset.get_classes_list():
           ct, ctp = dataset.get_cond_prob_class_feature(feature_name, class_name, pf)
           if ct == 0:
               continue
           else:
               first_sum += ct * math.log(ct)
           
           if ctp == 0:
               continue
           else:
               sec_sum += ctp * math.log(ctp)

       return pf * first_sum + (1 - pf) * sec_sum
   @staticmethod
   def __left_right_entropy3(dataset, feature_name):
       pf = dataset.get_prob_feature(feature_name)
       #print (feature_name, pf)
       first_sum = 0.0
       sec_sum = 0.0
       #print "\n\n",feature_name, " ", pf
       for class_name in dataset.get_classes_list():
           pct , pct_not = dataset.get_cond_prob_class_feature2(feature_name, class_name, pf)
           #print "        ",class_name , " ",pct
           if pct == 0:
               continue
           else:
               first_sum += pct * math.log(pct)
           
           if pct_not == 0:
               continue
           else:
               sec_sum += pct_not * math.log(pct_not)

       return pf * first_sum + (1 - pf) * sec_sum
 
 
   @staticmethod
   def get_IG_features(dataset):
       feat_ig = []
       iter = 1
       print iter
       for feature_name in dataset.get_features_list():
           #print feature_name
           if iter % 10000 == 0:
               print iter
           iter += 1
           feat_ig.append((feature_name, FeatureSelector.compute_information_gain(dataset, feature_name)))
       feat_ig.sort(lambda x, y:-cmp(x[0], y[0]))
       return feat_ig
   @staticmethod
   def __compute_chi2_score(dataset, feature_name, class_name):
       
       #print feature_name, class_name
       # A = dataset.get_joint_count_feature(feature_name, class_name, True, True)
       # B = dataset.get_joint_count_feature(feature_name, class_name, True, False)
       # C = dataset.get_joint_count_feature(feature_name, class_name, False, True)
       # D = dataset.get_joint_count_feature(feature_name, class_name, False, False)
       A, B, C, D = dataset.get_joint_count_feature2(feature_name, class_name)
       N = A + B + C + D
       #print A,B,C,D,N
       chi2 = (N * (A * D - C * B) ** 2) / ((A + B) * (A + C) * (B + D) * (C + D))
       
       return chi2
   
   @staticmethod
   def compute_chi2(dataset, feature_name):
       
       chi2_avg = 0.0
       for class_name in dataset.get_classes_list():
           prob = dataset.get_prob_class(class_name)
           chi2 = FeatureSelector.__compute_chi2_score(dataset, feature_name, class_name)
           chi2_avg += prob * chi2
       return chi2_avg
   @staticmethod
   def get_top_features(feat_tuple, n):
       
       feat_tuple.sort(lambda x, y:-cmp(x[1], y[1]))
       return feat_tuple[0:n]
   @staticmethod
   def get_CHI2_features(dataset):
       feat_chi2 = []
       iter = 1
       for feature_name in dataset.get_features_list():
           if iter % 10000 == 0:
            print iter
           iter += 1
           feat_chi2.append((feature_name, FeatureSelector.compute_chi2(dataset, feature_name)))
       feat_chi2.sort(lambda x, y:-cmp(x[0], y[0]))
       return feat_chi2       
