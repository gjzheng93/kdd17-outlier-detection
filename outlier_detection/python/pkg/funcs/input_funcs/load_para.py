# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 14:16:12 2016

@author: gjz5038
"""

# filename: load_para.py

def get_para(para_name, f):
    
    '''
    get the value for parameter named "para_name" from file object f
    '''
    
    for line in f:
        if line[0] == '#':
            continue
        if line[:len(para_name)] == para_name:
            line = line.replace('\n', '')
            [para_head, para] = line.split('=')
            break
        
    para = para.replace(' ', '')
    
    if para[0] == "'" and para[-1] == "'":
        # this is a string
        para = para[1:-1]
    elif para[0] == '[' and para[-1] == ']':
        # this is a list
        para = para[1:-1].split(',')
        for i in range(len(para)):
            if para[i][0] == "'" and para[i][-1] == "'":
                # each element is a string
                para[i] = para[i][1:-1]
            else:
                # each element is a value
                try:
                    para[i] = float(para[i])
                    if para[i] == int(para[i]):
                        para[i] = int(para[i])
                except:
                    raise TypeError('wrong input type for para')
    else:
        # this is a value
        try:
            para = float(para)
            if para == int(para):
                para = int(para)
        except:
            raise TypeError('wrong input type for para')
    
    return para

def load_para(list_para_name, path_to_para, para_file):
    
    '''
    load the values for each parameter in "list_para_name" 
    from file "para_file"
    '''
    
    dict_para = {}
    
    for para_name in list_para_name:
        f = open(path_to_para+para_file, 'r')
        dict_para[para_name] = get_para(para_name, f)
        f.close()
    
    return dict_para

def write_para(para_s, path_to_para, para_file):
    
    '''
    write the string "para_s" to "para_file"
    '''
    
    f = open(path_to_para+para_file, 'w')
    f.write(para_s)
    f.close()
