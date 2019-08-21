# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 18:07:01 2016

@author: gjz5038
"""


        
import os


def replace(read_s, list_point, point_type):
    
    '''
    fill in the locations of "list_point" in "read_s"
    '''
    
    s = ''
    
    for cnt in range(len(list_point)):
        sample = list_point[cnt]
        point_lat = sample[1]
        point_lon = sample[2]
        
        s+= "{lat: "+str(point_lat)+', lng: '+str(point_lon) +"},\n"
        
    read_s = read_s.replace('replace with '+ point_type, s)
    
    return read_s

def write(dic_points, path_to_output, file_name):
    
    '''
    generate the html file for the map
    '''
    
    path_to_this_script =  os.path.dirname(os.path.realpath(__file__))
    
    # read the template
    f = open(path_to_this_script + '/sample/sample_page.html', 'r')
    read_s = str(f.read())
    f.close()
    
    # fill in the locations of the markers
    read_s = read_s.replace(
        'center_coordinate', 
        str(dic_points['center'][1])+','+str(dic_points['center'][2]))
    
    for point_type in dic_points:
        if point_type != 'center':
            read_s = replace(read_s, dic_points[point_type], point_type)
    
    # locate the markers
    while (read_s.find('"replace with path_to_markers"') > 0):
        read_s = read_s.replace(
            '"replace with path_to_markers"', 
            os.path.relpath(
                path_to_this_script+'/sample/', path_to_output)+'/')
    
    
    f = open(path_to_output+'/'+file_name+'.html', 'w')
    f.write(read_s)
    f.close()
          
