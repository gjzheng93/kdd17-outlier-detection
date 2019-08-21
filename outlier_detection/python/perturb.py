'''
Created on Dec 25, 2016

@author: guanjie

This file is to generate perturbed data

'''

#perturb.py

from pkg.funcs.input_funcs import load_data
from pkg.funcs.output_funcs import output_tools
from pkg.funcs.input_funcs import load_para

import sklearn.preprocessing
import numpy as np
import os
import sys

class Perturb:
    
    def __init__(self, 
                 array_data, array_data_head, 
                 list_x_name, list_y_name, 
                 perturb_ratio, perturb_sample_size):
        
        self.array_data = array_data
        self.array_data_head = array_data_head
        self.list_x_name = list_x_name
        self.list_y_name = list_y_name
        self.perturb_ratio = perturb_ratio
        self.perturb_sample_size = perturb_sample_size
        
        self.n = len(self.array_data)
        self.n_perturb = int(self.perturb_ratio * self.n)
        self.n_perturb_compare = int(self.perturb_sample_size)
        
        self.array_data_after_perturb = np.copy(array_data)
        self.array_data_after_perturb_head = self.array_data_head[:]
        
        self.list_perturb_id = []
        
        
    def perturb(self):
        
        for i in range(self.n_perturb):
            perturb_id = np.random.randint(0, self.n)
            while perturb_id in self.list_perturb_id:
                perturb_id = np.random.randint(0, self.n)
            
            self.perturb_one_record(perturb_id) 
            self.list_perturb_id.append(perturb_id)
            
        self.array_data_after_perturb_head += ['label']
        array_label = np.zeros((self.n, 1))
        array_label[self.list_perturb_id] += 1
        self.array_data_after_perturb = np.concatenate(
            (self.array_data_after_perturb, array_label), axis = 1)
        
        
        return self.array_data_after_perturb, \
            self.array_data_after_perturb_head
    
    def perturb_one_record(self, perturb_id):
 
        # generate a pool of candidates for this sample to perturb with
        
        random_sample_index = list(
            np.random.randint(0, self.n, self.n_perturb_compare))
        while len(np.unique(random_sample_index)) != self.n_perturb_compare:
            random_sample_index = list(
                np.random.randint(0, self.n, self.n_perturb_compare))
        
        # replace the y value with the y' so that (y-y')^2 is maximized
        
        list_index_y = [self.array_data_head.index(y_name) 
                        for y_name in self.list_y_name]
        
        y_this_sample = self.array_data[perturb_id:perturb_id+1, list_index_y]
        array_y_select = self.array_data[random_sample_index][:,list_index_y]
        
        index_to_perturb_with = np.argmax(\
            np.multiply(array_y_select-y_this_sample, 
                        array_y_select-y_this_sample))
        
        self.array_data_after_perturb[perturb_id,list_index_y] = \
            array_y_select[index_to_perturb_with]


def main(data_source, 
        list_perturb_ratio, 
        list_perturb_sample_size, 
        total_run_cnt):
    
    
    PATH_TO_DATA = '../../data/clean_data/'+data_source+'/'
    PATH_TO_PARA = 'pkg/confs/'+data_source+'/'
    DATA_FILE_NAME = data_source+'.csv'
    PARA_FILE_NAME = data_source+'.conf'
    
    # load data
    array_data, array_data_head = load_data.load_data(
        PATH_TO_DATA, DATA_FILE_NAME)
    array_data = array_data.astype(float)
    
    # load attributes name
    list_x_name = \
        load_para.load_para(
            ['list_locs_name'], 
            PATH_TO_PARA, 
            PARA_FILE_NAME)['list_locs_name'] \
        + load_para.load_para(
            ['list_features_name'], 
            PATH_TO_PARA, 
            PARA_FILE_NAME)['list_features_name']
    y_name = \
        load_para.load_para(
            ['target'], PATH_TO_PARA, PARA_FILE_NAME)['target']
    
    # select features and target to keep   
    list_to_keep = ['sample_id']+list_x_name+[y_name]
    list_index_to_keep = [array_data_head.index(name) for name in list_to_keep]    
    array_data = array_data[:,list_index_to_keep]
    array_data_head = list_to_keep[:]
    
    # start perturbing the data
    
    for perturb_ratio in list_perturb_ratio:
        for perturb_sample_size in list_perturb_sample_size:
            
            PATH_TO_OUTPUT = \
                PATH_TO_DATA+ \
                str(perturb_ratio)+'/'+ \
                str(perturb_sample_size)+'/'
            
            if not os.path.exists(PATH_TO_OUTPUT):
                os.makedirs(PATH_TO_OUTPUT)
            else:
                sys.exit('perturb already exist')
    
            for i in range(total_run_cnt):
                perturb_instance = Perturb(
                    array_data, array_data_head, 
                    list_x_name, [y_name], 
                    perturb_ratio, perturb_sample_size)
                
                # perturb
                array_data_after, array_data_after_head = \
                    perturb_instance.perturb()
                
                # output
                output_tools.output_2d_data(
                    array_data_after, array_data_after_head, 
                    PATH_TO_OUTPUT, str(i)+'.'+str(data_source)+'.csv')
                
                # normalize for the sake of metric learning
                array_data_after_rescale = \
                    np.concatenate(
                        (array_data_after[:,0:1], 
                         sklearn.preprocessing.minmax_scale(
                             array_data_after[:,1:-1]), 
                         array_data_after[:,-1:]), 
                                   axis = 1)
                
                #output    
                output_tools.output_2d_data(
                    array_data_after_rescale, array_data_after_head, 
                    PATH_TO_OUTPUT, str(i)+'.'+str(data_source)+'.norm.csv')
    

if __name__ == '__main__':  
    
    path_to_settings = 'settings/'
    settings_file = sys.argv[1]
    print (settings_file)
    dic_para = load_para.load_para(
        ['data_source', 
         'list_perturb_ratio', 
         'list_perturb_sample_size', 
         'total_run_cnt'], 
        path_to_settings, settings_file)  
               
    main(**dic_para)      
    
