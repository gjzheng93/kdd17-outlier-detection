'''
Created on Dec 25, 2016
 
@author: guanjie

This file is calling the matlab script to generate distance metric
'''
 
 
 
import os
import shutil
import sys
from matlab import engine
from pkg.funcs.input_funcs import load_para
 

def main(data_source, 
         list_perturb_ratio, list_perturb_sample_size, 
         total_run_cnt):
  
    PATH_TO_PARA = 'pkg/confs/'+data_source+'/'
    PARA_FILE = data_source+'.conf' 
     
    list_x_name = \
        load_para.load_para(
            ['list_locs_name'], 
            PATH_TO_PARA, PARA_FILE)['list_locs_name'] + \
        load_para.load_para(
            ['list_features_name'], 
            PATH_TO_PARA, PARA_FILE)['list_features_name']
    y_name = \
        load_para.load_para(
            ['target'], 
            PATH_TO_PARA, PARA_FILE)['target']

    # metric type: euclidean, metric, metricRobust
    # data range: full (including outlier)
    dic_para_M_file = {
        'euclidean.full':''+data_source+'.M.euclidean.full.conf', 
        'metric.full': ''+data_source+'.M.metric.full.conf', 
        'metricRobust.full': ''+data_source+'.M.metricRobust.full.conf'}
    dic_para_L_file = {
        'euclidean.full':''+data_source+'.L.euclidean.full.conf', 
        'metric.full': ''+data_source+'.L.metric.full.conf', 
        'metricRobust.full': ''+data_source+'.L.metricRobust.full.conf'}
       
    for perturb_ratio in list_perturb_ratio:
        for perturb_sample_size in list_perturb_sample_size:
            path_to_data = '../../data/clean_data/'+ \
                data_source+'/'+ \
                str(perturb_ratio)+'/'+str(perturb_sample_size)+'/'
            path_to_output = 'pkg/confs/'+ \
                data_source+'/'+ \
                str(perturb_ratio)+'/'+str(perturb_sample_size)+'/'
            
            for run_cnt in range(total_run_cnt):
                for para_M_file_short in dic_para_M_file:
                    
                    # call matlab to learn metric
                    pwd = os.getcwd()
                    engine.os.chdir('../MLKR1.0')
                    mat = engine.start_matlab()
                    [metric_type, data_range] = para_M_file_short.split('.') 
                    success = mat.demo(
                        data_source, 
                        path_to_data, str(run_cnt)+'.'+data_source+'.norm.csv', 
                        metric_type, data_range, 
                        list_x_name, y_name)
                    if success == 0:
                        print ('failed to generate metric')
                        sys.exit()
                    mat.quit()
                    os.chdir(pwd)
                    
                    if not os.path.exists(path_to_output):
                        os.makedirs(path_to_output)
                    shutil.copy(
                        'pkg/'+str(dic_para_M_file[para_M_file_short]), 
                        path_to_output+str(run_cnt)+'.'+\
                        str(dic_para_M_file[para_M_file_short]))
                    shutil.copy(
                        'pkg/'+str(dic_para_L_file[para_M_file_short]), 
                        path_to_output+str(run_cnt)+'.'+\
                        str(dic_para_L_file[para_M_file_short]))


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
