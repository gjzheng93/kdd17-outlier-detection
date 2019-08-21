'''
Created on Dec 16, 2016

@author: guanjie
'''


import os
import sklearn.preprocessing
import numpy as np
import shutil

from ..funcs.input_funcs import load_data
from ..funcs.output_funcs import output_tools
from ..models.model import Model


class Data:
    
    def __init__(self):
        self.array_data = None
        self.array_data_head = None
        self.array_loc = None
        self.array_loc_norm = None
        self.array_feature = None
        self.array_feature_norm = None
        self.array_target = None
        self.array_target_norm = None
        self.array_sample_id = None
        self.array_label = None
        
        self.target_min = None
        self.target_max = None
        
class Paths:
    
    def __init__(self):
        self.PATH_TO_ROOT = None
        self.PATH_TO_DATA = None
        self.PATH_TO_OUTPUT = None
        self.PATH_TO_CONF = None
        
class Results:
    
    def __init__(self):
        self.array_score = None

class Pipeline:
    
    def __init__(self, para):
        
        self.para = para
        self.data = Data()
        self.paths = Paths()
        self.results = Results()
        
        
    def run_pipeline(self):
        
        # load everything
        
        self.load_everyhing()
        
        # preprocessing
        
        self.pre_processing()
        
        # processing
        
        self.processing()
        
        # postprocessing
        
        self.post_processing()
        
        # output
        
        self.output_everything()
        
    def load_everyhing(self):
        
        '''
        Define the paths and load data, para
        '''
        
        self.paths.PATH_TO_ROOT = '../../'
        self.paths.PATH_TO_DATA = \
            self.paths.PATH_TO_ROOT + 'data/clean_data/'+ \
            self.para.para_set.data_source+'/'+ \
            str(self.para.para_set.perturb_ratio)+'/'+ \
            str(self.para.para_set.perturb_sample_size)+'/'
        self.paths.PATH_TO_OUTPUT = \
            self.paths.PATH_TO_ROOT + 'data/'+ \
            self.para.para_set.data_source+'/'+ \
            str(self.para.para_set.perturb_ratio)+'/'+ \
            str(self.para.para_set.perturb_sample_size)+'/'+ \
            self.para.para_set.method+'/'+ \
            self.para.para_set.this_run_name+'/'    
        self.paths.PATH_TO_CONF = \
            'pkg/confs/'+ \
            self.para.para_set.data_source+'/'+ \
            str(self.para.para_set.perturb_ratio)+'/'+ \
            str(self.para.para_set.perturb_sample_size)+'/'
            
        if os.path.exists(self.paths.PATH_TO_OUTPUT):
            print('already exists')
    #        sys.exit(PATH_TO_OUTPUT+'  exists')
        else:
            os.makedirs(self.paths.PATH_TO_OUTPUT)  
        #=========================================== load data ============
        
        self.data.array_data, self.data.array_data_head = \
            load_data.load_data(
                self.paths.PATH_TO_DATA, 
                self.para.para_set.data_file_name)
        self.data.array_data = self.data.array_data.astype(float)
        
        # load metric
        self.para.para_set.metric = \
            load_data.load_data_without_head(
                self.paths.PATH_TO_CONF, 
                self.para.para_set.metric_file_name
                ).astype(float)
                
        print (self.para.para_set.metric_file_name)
                        
        
    def pre_processing(self):
        
        '''
        load features, target
        normalize
        '''
    
        list_index_loc = [
            self.data.array_data_head.index(
                self.para.para_set.list_locs_name[i]) 
            for i in range(len(self.para.para_set.list_locs_name))]
        list_index_feature = [
            self.data.array_data_head.index(
                self.para.para_set.list_features_name[i]) 
            for i in range(len(self.para.para_set.list_features_name))]
        index_sample_id = self.data.array_data_head.index('sample_id')
        index_label = self.data.array_data_head.index('label')
        index_target = self.data.array_data_head.index(
            self.para.para_set.target)
      
        array_loc = self.data.array_data[:,list_index_loc]
        array_feature = self.data.array_data[:,list_index_feature]
        array_sample_id = \
            self.data.array_data[:,index_sample_id:index_sample_id+1]
        array_label = self.data.array_data[:,index_label:index_label+1]
        array_target = self.data.array_data[:,index_target:index_target+1]
    
            
        if self.para.para_set.normalization_mode == 'min-max':
            
            array_loc_normalized = sklearn.preprocessing.minmax_scale(array_loc)
            array_feature_normalized = sklearn.preprocessing.minmax_scale(array_feature)
            array_target_normalized = sklearn.preprocessing.minmax_scale(array_target)
            
        elif self.para.para_set.normalization_mode == 'no':
            
            array_loc_normalized = np.copy(array_loc)
            array_feature_normalized = np.copy(array_feature)
            array_target_normalized = np.copy(array_target)
    
        self.data.array_loc, self.data.array_loc_norm, \
        self.data.array_feature, self.data.array_feature_norm, \
        self.data.array_target, self.data.array_target_norm, \
        self.data.array_sample_id, self.data.array_label = \
            array_loc, array_loc_normalized, \
            array_feature, array_feature_normalized, \
            array_target, array_target_normalized, \
            array_sample_id, array_label
            
        self.data.target_min = np.min(self.data.array_target, axis=0)
        self.data.target_max = np.max(self.data.array_target, axis=0)
        
        if __debug__:
            
            output_tools.output_2d_data(
                np.concatenate(
                    (array_sample_id, 
                     array_loc_normalized, 
                     array_feature_normalized, 
                     array_target_normalized, 
                     array_label), 
                axis = 1), 
                ['sample_id']+ \
                    self.para.para_set.list_locs_name+ \
                    self.para.para_set.list_features_name+ \
                    [self.para.para_set.target]+['label'], 
                self.paths.PATH_TO_OUTPUT, 
                'normalized_data.csv')    

            
    def processing(self):
        
        '''
        run the algorithms
        '''
        
        instance = Model(
            self.data.array_loc_norm, 
            self.data.array_feature_norm, 
            self.data.array_target_norm, 
            self.para.para_set)
        self.results.array_score, self.results.dic_array_debug_info = \
            instance.run()
            
    def post_processing(self):
        
        '''
        recover the prediction to the original scale
        '''
        
        if self.para.para_set.normalization_mode == 'min-max':
            if 'pred' in self.results.dic_array_debug_info:
                target_range = self.data.target_max-self.data.target_min
                self.results.dic_array_debug_info['pred'] = \
                    np.multiply(
                        self.results.dic_array_debug_info['pred'], 
                        target_range[None,:])+ \
                        self.data.target_min[None,:]
        
        if 'pred' in self.results.dic_array_debug_info:
            
            array_pred = self.results.dic_array_debug_info['pred']
            array_result = np.concatenate(
                (self.data.array_sample_id, 
                    np.array([self.results.array_score]).transpose(), 
                array_pred), axis = 1)
        
            self.results.array_results = array_result
            self.results.array_results_head = ['sample_id','oscore', 'pred']
            
        else: 
            array_result = np.concatenate(
                (self.data.array_sample_id, 
                    np.array([self.results.array_score]).transpose()), 
                axis = 1)
        
            self.results.array_results = array_result
            self.results.array_results_head = ['sample_id','oscore']
            
    def output_everything(self):  
        
        '''
        output parameters and results
        '''
    
        self.output_parameters()
        
        self.output()    
        
    
    def output_parameters(self):
        
        self.para.write_para(self.paths.PATH_TO_OUTPUT)

        return  
        
    def output(self):
        
        index_sample_id_data = \
            self.data.array_data_head.index('sample_id')    
        index_sample_id_results = \
            self.results.array_results_head.index('sample_id')
    
        # sort the results and data according to sample id
        self.data.array_data = \
            self.data.array_data[
                np.argsort(self.data.array_data[:,index_sample_id_data])]
        self.results.array_results = \
            self.results.array_results[
                np.argsort(
                    self.results.array_results[:,index_sample_id_results])] 
            
             
        # check if the results and data are aligned and output results
        if np.array_equal(
            self.results.array_results[:,index_sample_id_results],
            self.data.array_data[:,index_sample_id_data]):
            
            if __debug__:
        
                array_output_results = \
                    np.concatenate(
                        (self.data.array_data, 
                         self.results.array_results[:,
                                                    index_sample_id_results+1:]
                        ), axis = 1)
                array_output_results_head = \
                    self.data.array_data_head + \
                    self.results.array_results_head[index_sample_id_results+1:]
                
            else:
                
                array_output_results = self.results.array_results
                array_output_results_head = self.results.array_results_head
            
            output_tools.output_2d_data(
                array_output_results, 
                array_output_results_head, 
                self.paths.PATH_TO_OUTPUT, 
                self.para.para_set.data_source+ \
                    '.result.'+self.para.para_set.method)    
        
        