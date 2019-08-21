'''
Created on Dec 16, 2016

@author: guanjie
'''

import numpy as np

from pkg.pipelines.outlier.outlier_pipeline import OutlierPipeline
from ...models.outlier.melody import Melody

class MelodyPipeline(OutlierPipeline):

    def processing(self):
        
        melody_instance = Melody(
            self.data.array_loc_norm, self.data.array_feature_norm, 
            self.data.array_target_norm, self.para.para_set)
        self.results.array_score, self.results.dic_array_debug_info = \
            melody_instance.run()
        
            
    def post_processing(self):
        
        if self.para.para_set.normalization_mode == 'min-max':
            target_range = self.data.target_max-self.data.target_min
            self.results.dic_array_debug_info['pred'] = \
                np.multiply(
                    self.results.dic_array_debug_info['pred'], 
                    target_range[None,:])+ \
                self.data.target_min[None,:]
                        
        array_pred = self.results.dic_array_debug_info[
            'pred']
        array_context = self.results.dic_array_debug_info[
            'array_context']
        array_context_distances = self.results.dic_array_debug_info[
            'array_context_distances']
        array_context_weight = self.results.dic_array_debug_info[
            'array_context_weight']
    
        n_context = len(array_context[0])
          
        array_context_id = np.zeros(np.shape(array_context))
        for i in range(len(array_context)):
            for j in range(len(array_context[i])):
                array_context_id[i][j] = \
                    self.data.array_sample_id[array_context[i][j]]
                
        if __debug__:        
                
            array_result = np.concatenate(
                (self.data.array_sample_id, 
                 np.array([self.results.array_score]).transpose(),
                 array_pred,
                 array_context_id, 
                 array_context_distances, 
                 array_context_weight), axis = 1)
            
        
            self.results.array_results = array_result
            self.results.array_results_head = ['sample_id','oscore', 'pred']+ \
                [str(i)+' th' for i in range(n_context)] + \
                [str(i)+' th dist' for i in range(n_context)] + \
                [str(i)+' th weight' for i in range(n_context)] 
                 
        else:
            
            array_result = np.concatenate(
                (self.data.array_sample_id, 
                 np.array([self.results.array_score]).transpose(),
                 array_pred), axis = 1)
            
        
            self.results.array_results = array_result
            self.results.array_results_head = ['sample_id','oscore', 'pred']
         
            