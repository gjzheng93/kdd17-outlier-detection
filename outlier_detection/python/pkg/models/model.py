'''
Created on Dec 17, 2016

@author: guanjie
'''

import numpy as np

class Model():
    
    def __init__(self, loc, X, Y, para_set):
        
        self.loc = loc
        self.X = X
        self.Y = Y
        self.para_set = para_set
        
        self.d = np.shape(self.X)[1]
        self.n = np.shape(self.Y)[0]
        self.m = np.shape(self.Y)[1]
        
    def run(self):
        
        self.array_score = []
        self.dic_debug_info = {}
        
        return self.array_score, self.dic_debug_info
        
        
