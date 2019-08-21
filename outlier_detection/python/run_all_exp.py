'''
Created on Dec 26, 2016

@author: guanjie

Run all experiments. 
Read the experiment settings and loop the 
    pertrub_ratio, 
    perturb_sample_size, 
    run_cnt


'''

import time
import timeit
import sys
import copy
from multiprocessing import Process

from run_exp import OneRun
from pkg.paras.para import Para
from pkg.funcs.input_funcs import load_para

from pkg.paras.outlier import melody_para


class RunAllExp:
    
    
    PATH_TO_CONF_TEMPLATE = 'pkg/confs/'
    
    dic_analysis_type = {'xgboost': 'regression',
                      'lr': 'regression', 
                      'melody': 'outlier', 
                      'cad': 'outlier', 
                      'rocod': 'outlier', 
                      'lof': 'outlier', 
                      'zs': 'outlier',
                      'sod': 'outlier',
                      'glssod': 'outlier'
                      }
    
    def __init__(
            self, data_source, 
            list_perturb_ratio, list_perturb_sample_size, 
            list_methods, total_run_cnt, run_mode):
        
        self.data_source = data_source
        self.list_perturb_ratio = list_perturb_ratio
        self.list_perturb_sample_size = list_perturb_sample_size
        self.list_methods = list_methods
        self.total_run_cnt = total_run_cnt
        self.run_mode = run_mode
        
    def single_run(self, para_instance, analysis_type, method, run_cnt):
        
        # update parameters by run cnt
                        
        para_instance_this_run = copy.deepcopy(para_instance)
        
        para_instance_this_run.change_para(
            'run_cnt', run_cnt)
        
        para_instance_this_run.change_para(
            'data_file_name',
            str(run_cnt)+'.'+str(self.data_source)+'.csv') 
        
        # start running each test

        this_run = OneRun(
            para_instance_this_run, self.data_source, 
            analysis_type, method, run_cnt)
        
        if self.run_mode == 'one_run':
            this_run.direct_run()
        elif self.run_mode == 'tune_para':
            this_run.tune_para_run()
            
        

    def check_all_workers_working(self, list_cur_p):
        
        for i in range(len(list_cur_p)):
            if not list_cur_p[i].is_alive():
                return i
        
        return -1
        
        
        
    def run(self):
        
        for perturb_ratio in self.list_perturb_ratio:
            for perturb_sample_size in self.list_perturb_sample_size:
                for method in self.list_methods:
                    
                    time1 = timeit.default_timer()
                    
                    # update the parameters in the para file
                    
                    analysis_type = self.dic_analysis_type[method]
                    
                    para_instance = getattr(
                        getattr(sys.modules[__name__], method+'_para'), 
                        method.title()+'Para')(
                            self.PATH_TO_CONF_TEMPLATE+self.data_source+'/', 
                            self.data_source)
                    

                    para_instance.change_para(
                        'perturb_ratio', perturb_ratio)
                    para_instance.change_para(
                        'perturb_sample_size', perturb_sample_size)
                    para_instance.change_para(
                        'analysis_type', analysis_type)
                    para_instance.change_para(
                        'method', method)
                    
#                     # ========================= single process ===============
#                     for run_cnt in range(self.total_run_cnt):
#                         self.single_run(para_instance, 
#                                         analysis_type, 
#                                         method, 
#                                         run_cnt)
                        
                    # ========================== multi process ===============
 
                    list_p = []
                    for run_cnt in range(self.total_run_cnt):
                              
                        p = Process(target = self.single_run, 
                                    args=(para_instance, 
                                          analysis_type, 
                                          method, 
                                          run_cnt))  
                        list_p.append(p)
                    i = 0
                          
                    list_cur_p = []
                    for p in list_p:
                        if len(list_cur_p) < n_workers:
                            print(i)
                            p.start()
                            list_cur_p.append(p)
                            i+=1
                        if len(list_cur_p) < n_workers:
                            continue
                              
                        idle = self.check_all_workers_working(list_cur_p)
                              
                        while idle == -1:
                            time.sleep(1)
                            idle = self.check_all_workers_working(
                                list_cur_p)
                        del list_cur_p[idle]   
                                
                    for p in list_cur_p:
                        p.join()
                        
                    time2 = timeit.default_timer()
                    print (method+'    '+str(time2-time1))
            
            
if __name__ == '__main__':  
    
    PATH_TO_SETTINGS = 'settings/'
    settings_file = sys.argv[1]
    
    print (settings_file)
    
    dic_para = load_para.load_para(
        ['data_source', 
         'list_perturb_ratio', 'list_perturb_sample_size', 
         'list_methods', 'total_run_cnt', 'run_mode'], 
        PATH_TO_SETTINGS, settings_file) 
    
    n_workers = load_para.load_para(
        ['n_workers'], 
        PATH_TO_SETTINGS, settings_file)['n_workers']
             
    run_instance = RunAllExp(**dic_para)
    run_instance.run()       
        
        
