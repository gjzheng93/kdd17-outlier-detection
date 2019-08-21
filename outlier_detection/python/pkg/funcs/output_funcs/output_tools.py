# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:58:26 2016

@author: gjz5038
"""

#output_tools.py


import math

def n_float(v, d):
    
    '''
    convert a value to the format of d digit float
    '''
    
    if v < math.pow(10, -d):
        s = '{:.'+str(d)+'e}'
    else:
        s = '{:.'+str(d)+'f}'
    return s.format(v)

def output_2d_data(data, data_head, path_to_output, file_name):
    
    '''
    output a 2d table with headline
    '''
    
    f = open(path_to_output+file_name, 'w')
    
    for i in range(len(data_head)):
        if i == len(data_head) -1:
            f.write(data_head[i]+'\n')
        else:
            f.write(data_head[i]+',')
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j == len(data[i]) -1:
                f.write(str(data[i][j])+'\n')
            else:
                f.write(str(data[i][j])+',')
    
    f.close()
    return

def output_list(l, path_to_output, file_name):
    
    '''
    output an 1d list to one row
    '''
    
    f = open(path_to_output+file_name, 'w')
    for i in range(len(l)):
        if i == len(l)-1:
            f.write(str(l[i])+'\n')
        else:
            f.write(str(l[i])+',')
    f.close()
    return
    
def output_vertical_list(l, path_to_output, file_name):
    
    '''
    output an 1d list to one column
    '''
    
    f = open(path_to_output+file_name, 'w')
    for i in range(len(l)):
        f.write(str(l[i])+'\n')
    f.close()
    return
