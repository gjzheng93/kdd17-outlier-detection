# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 14:16:12 2016

@author: gjz5038
"""

# filename: load_data.py

import numpy as np
import csv
      
def clean_table(table):
    '''
    Convert each element of a table to lowercase, remove , and ;
    '''
    for l in range(len(table)):
        for r in range(len(table[l])):
            table[l][r] = table[l][r].lower()
            table[l][r] = table[l][r].replace(',', ' ')
            table[l][r] = table[l][r].replace(';', ' ')
    return table

def load_data(path_to_data, file_name):
    '''
    load a 2d table with headline
    '''
    
    with open(path_to_data+file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        list_data = list(reader)
        list_data = clean_table(list_data)
        
        list_data_head = list_data[0]
        del list_data[0]
        
        array_data = np.array(list_data)
        array_data_head = list_data_head[:]    
        
    return array_data, array_data_head
    
def load_data_without_head(path_to_data, file_name):
    
    '''
    load a 2d table without headline
    '''
    
    with open(path_to_data+file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        list_data = list(reader)
        list_data = clean_table(list_data)
        
        array_data = np.array(list_data)  
        
    return array_data



