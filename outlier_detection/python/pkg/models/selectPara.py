#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:19:21 2017

@author: gjz5038
"""

import numpy as np
from sklearn import cross_validation
from sklearn import metrics



class ModelObj:
    def __init__(self, 
                 model_name, model, 
                 list_model_para_name, list_model_para):
        self.model_name = model_name
        self.model = model
        self.list_model_para_name = list_model_para_name
        self.list_model_para = list_model_para
   
        
class SelectPara:
    def __init__(self, 
                 model_name, model, 
                 list_model_para_name, list_model_para, 
                 X, Y):
        
        self.model_obj = ModelObj(
            model_name, model, 
            list_model_para_name, list_model_para)
        self.X = X
        self.Y = Y
        
        self.final_para = {}
        
        
    def run(self):
        
        # count the times that this parameter leads to the best result
        dic_model_para_count = {} 
        for i in range(len(self.model_obj.list_model_para_name)):
            para_name = self.model_obj.list_model_para_name[i]
            dic_model_para_count[para_name] = {}
            for value in self.model_obj.list_model_para[i]:
                dic_model_para_count[para_name][value] = 0
        
        for i in range(10):
            min_para = self.divide()
            for para_name in min_para:
                dic_model_para_count[para_name][min_para[para_name]] += 1
        
        for para_name in dic_model_para_count:
            count = 0
            max_value = None
            for value in dic_model_para_count[para_name]:
                if dic_model_para_count[para_name][value] > count:
                    count = dic_model_para_count[para_name][value]
                    max_value = value
                    
            self.final_para[para_name] = max_value
    
        return self.final_para
        
    
    def divide(self): 
        
        array_XY = np.concatenate((self.X, self.Y), axis = 1)
        kf = cross_validation.KFold(len(array_XY), n_folds = 5, shuffle = True)
    
        dic_para, list_para, list_score = self.tunePara({}, [], [], 0, kf)
    
        arg_min_score = np.argmin(list_score)
        min_para = list_para[arg_min_score]
        
        return min_para
        

    def getScore(self, reg, kf):
        i = 0
        for train, test in kf:
            reg.fit(self.X[train], self.Y[train])
            
            this_pred = reg.predict(self.X[test])
            if len(np.shape(this_pred)) == 1:
                this_pred = np.array([this_pred]).transpose()
            
            if i == 0:
                Y_pred = this_pred
                Y_test = self.Y[test]
            else:
                Y_pred = np.concatenate((Y_pred, this_pred), axis = 0)
                Y_test = np.concatenate((Y_test, self.Y[test]), axis = 0)
                
            i += 1
                
        return metrics.mean_squared_error(Y_test, Y_pred)
        

    def tunePara(self, dic_para, list_para, list_mse, i, kf):
        #recursively list all the possible parameter combinations
        if i == len(self.model_obj.list_model_para_name):
            reg = self.model_obj.model(**dic_para)
            scores = self.getScore(reg, kf)
            list_para.append(dic_para.copy())
            list_mse.append(np.mean(scores))
        else:
            para_name = self.model_obj.list_model_para_name[i]
            para_values = self.model_obj.list_model_para[i]
            for value in para_values:
                dic_para[para_name] = value
                dic_para, list_para, list_mse = self.tunePara(
                    dic_para, list_para, list_mse, i+1, kf)
        return dic_para, list_para, list_mse
        

