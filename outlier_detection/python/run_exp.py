'''
Created on Dec 14, 2016

@author: guanjie
'''

import sys

from pkg.pipelines.outlier import melody_pipeline 
        
class OneRun:
    
    
    def __init__(
            self, para, data_source, 
            analysis_type, method, run_cnt):
        
        self.data_source = data_source
        self.analysis_type = analysis_type
        self.method = method
        
        self.run_cnt = run_cnt
        
        self.para = para
        self.pipeline = None
        
    def direct_run(self):
        
        # determine the name of this run
        this_run_name = str(self.run_cnt)+'/'+str(self.run_cnt)
        
        for para_name in self.para.method_parameters:
            this_run_name = \
                this_run_name + '.' + str(getattr(self.para.para_set, para_name)) 
        self.para.change_para('this_run_name', this_run_name)
        
        print (this_run_name)
        
        # determine the name of the metric file
        metric_file_name = \
            str(self.para.para_set.run_cnt)+'.'+ \
            str(self.para.para_set.data_source+'.M.'+
                self.para.para_set.metric_type+'.'+
                self.para.para_set.data_range+'.conf')
        self.para.change_para('metric_file_name', metric_file_name)
        
        # run this test
        self.pipeline = getattr(
            getattr(sys.modules[__name__], self.method+'_pipeline'), 
            self.method.title()+'Pipeline')(self.para)
        self.pipeline.run_pipeline()
        
    def tune_para_run(self):
        
        self.list_tune = self.para.get_tune_list([], {}, 0)    
        
        for this_run_para in self.list_tune:
            self.para.update_para_with_dic(this_run_para)                         
            self.direct_run()
        

