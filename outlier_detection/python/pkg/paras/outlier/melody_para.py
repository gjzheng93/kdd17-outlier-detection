'''
Created on Dec 15, 2016

@author: guanjie
'''

from pkg.paras.outlier.outlier_para import OutlierPara

class MelodyPara(OutlierPara):
    
    method_parameters = ['metric_type', 
                         'data_range', 
                         'kNN',    
                         'with_local_confidence']          
    
#     list_metric_type = ['euclidean', 'metric', 'metricRobust']
    list_metric_type = ['metricRobust']
    list_data_range = ['full']
    list_kNN = [60]
    list_with_local_confidence = [1]
