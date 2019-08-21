# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 14:59:00 2016

@author: gjz5038
"""


import math
import numpy as np
from scipy.stats import norm
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import minmax_scale
import sys

from .outlier import Outlier

class Melody(Outlier): 
    
    def __init__(self, loc, X, Y, para_set):

        self.X = np.concatenate((loc,X),axis=1)
        self.Y = Y
        self.para_set = para_set
        
        self.d = np.shape(self.X)[1]
        self.n = np.shape(self.Y)[0]
        self.m = np.shape(self.Y)[1]   
    
    def run(self):
        
        self.array_context, self.array_context_distances, self.distance_sigma = \
            self.get_neighbors()
        self.array_context_weight = \
            self.cal_context_weight()
        
        self.Y_hat = self.get_Y_hat()
            
        self.array_score = \
            self.cal_outlying_score()
            
        self.array_score = minmax_scale(self.array_score)
        
        if np.any(np.isnan(self.array_score)):
            sys.exit('error')

        self.dic_debug_info = {
            'pred': self.Y_hat, 
            'array_context': self.array_context, 
            'array_context_distances': self.array_context_distances, 
            'array_context_weight': self.array_context_weight}

        return self.array_score, self.dic_debug_info
    
    def smooth_distance(self, distances_raw, indices):
        min_dist = np.sort(np.unique(distances_raw))[1]
    
        distances = np.copy(distances_raw)
        for i in range(len(distances)):
            for j in range(len(distances[i])):
                if math.isnan(distances[i,j]):
                    distances[i,j] = 0
                if distances[i,j] == 0:
                    distances[i,j] += min_dist
        
        return distances
    
    def get_neighbors(self):
        '''
        calculate the context score for all the nodes
        '''
        
        nbrs = NearestNeighbors(
            n_neighbors = self.para_set.kNN, 
            algorithm = 'ball_tree', 
            metric = 'mahalanobis', 
            metric_params = {'VI': self.para_set.metric}).fit(self.X)
        distances_raw, indices = nbrs.kneighbors()
        
        distances = self.smooth_distance(distances_raw, indices)
        all_dist  =np.reshape(
            np.copy(distances), np.shape(distances)[0]*np.shape(distances)[1])
        sigma = np.std(all_dist)       
      
        return indices, distances, sigma
        
    def cal_context_weight(self):
        '''
        calculate the gaussian weight
        '''
        array_context_weight = norm.pdf(
                self.array_context_distances, scale = self.distance_sigma)
        
        return array_context_weight        
        
    def get_Y_hat(self):
        '''
        estimate Y
        '''
        
        
        Y_hat = np.zeros(np.shape(self.Y))   
        
        for i in range(len(self.Y)):
            context = self.array_context[i]
            context_weight = self.array_context_weight[i]
            
            if np.sum(context_weight[:]) == 0:
                print ("not enough neighbors for sample {0}".format(i))
                list_ind_to_use = [ind for ind in range(len(self.Y)) if ind != i]
                Y_hat[i] = np.average(self.Y[list_ind_to_use], axis = 0)
            else:
                Y_hat[i] = \
                    np.sum(
                        np.multiply(self.Y[context[:]], 
                                    context_weight[:][:,None]), 
                        axis = 0)/ \
                    np.sum(context_weight[:]) 
                    
        return Y_hat
            
    def cal_outlying_score(self):
        '''
        get outlier score
        '''
           
        array_score_tmp = abs((self.Y_hat-self.Y)[:,0])
        array_score = np.zeros(np.shape(array_score_tmp))
        
        if self.para_set.with_local_confidence:
            for i in range(self.n):
                context = self.array_context[i]
                array_score[i] = \
                    self.cal_score_with_local_confidence(
                        array_score_tmp[i], array_score_tmp[context]) 
        
            # in case some points have a very normal neighborhood          
            array_score[array_score == -1] = np.max(array_score)
                
        else:
            array_score = np.copy(array_score_tmp)
     
        return array_score
        
    def cal_score_with_local_confidence(self, oscore, context_oscore):
        
        if np.sum(context_oscore) == 0:
            # this point a very normal neighborhood
            if oscore != 0:
                lc =  -1
            else:
                lc = 0
        else:
            lc = oscore/(np.sum(context_oscore)/len(context_oscore))
                
        if math.isnan(lc):
            print ('error')
        
        return lc
    
        

    