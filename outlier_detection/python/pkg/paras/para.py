'''
Created on Dec 15, 2016

@author: guanjie


Define all the parameters used in the experiment.


'''


class ParaSet:
    
    '''
    All parameters of the experiment
    '''
        
    data_name = ['data_source', 
                 'perturb_ratio', 
                 'perturb_sample_size', 
                 'data_file_name']
    analysis_name = ['analysis_type', 
                     'method']
    test_name = ['run_cnt', 
                 'this_run_name']
    features_and_trargets = ['list_locs_name', 
                             'list_locs_type', 
                             'list_features_name', 
                             'list_features_type', 
                             'target', 
                             'target_type']
    preprocess = ['normalization_mode']
    metric_file = ['metric_type', 
                   'data_range']
    
    def __init__(self, s, method_parameters):
        
        self.method_parameters = method_parameters
        
        for item in self.data_name + \
                self.analysis_name + \
                self.test_name + \
                self.features_and_trargets + \
                self.preprocess + \
                self.metric_file+ \
                self.method_parameters:
            
            try:
                setattr(self, item, self.get_para(item, s))
            except:
                ValueError(item+ ' not in parameter list')
            
        
    def get_para(self, para_name, para_s):
        
        ''' 
        get para value from "para_s"
        '''
    
        start = para_s.find('\n'+para_name) + len(para_name)
        for i in range(start, len(para_s)):
            if para_s[i] == '=':
                para_start = i+1
            if para_s[i] == '\n':
                para_end = i
                break
            
        para = para_s[para_start:para_end].replace(' ', '')

        if para[0] == "'" and para[-1] == "'":
            # this is a string
            para = para[1:-1]
        elif para[0] == '[' and para[-1] == ']':
            # this is a list
            para = para[1:-1].split(',')
            for i in range(len(para)):
                if para[i][0] == "'" and para[i][-1] == "'":
                    para[i] = para[i][1:-1]
                else:
                    try:
                        para[i] = float(para[i])
                        if para[i] == int(para[i]):
                            para[i] = int(para[i])
                    except:
                        raise TypeError('wrong input type for para')
        else:
            try:
                # this is a value
                para = float(para)
                if para == int(para):
                    para = int(para)
            except:
                raise TypeError('wrong input type for para')
        
        return para 

class Para:
    
    '''
    store the basic setting of the experiment:
        data_source, path_to_conf
    and para_string, para_set
    '''
    
    method_parameters = []
    
    def __init__(self, path_to_conf, data_source):
        
        self.data_source = data_source
        self.path_to_conf = path_to_conf
        self.para_s = self.load_para()
        self.para_set = ParaSet(self.para_s, self.method_parameters)
        
        
    def load_para(self):
        
        '''
        load para from file to str
        '''
        
        fin = open(self.path_to_conf+str(self.data_source)+'.conf', 'r')
        para_s = fin.read()
        fin.close()
        
        return para_s
        
    def write_para(self, path_to_output):
        
        '''
        write para from str to file
        '''
        
        fout = open(path_to_output+str(self.data_source)+'.conf', 'w')
        fout.write(self.para_s)
        fout.close()
        
    def change_para(self, para_name, para_value):
        
        '''
        change para in the ParaSet class and update it in the str
        '''
            
        setattr(self.para_set, para_name, para_value)
        
        if type(para_value) is str:
            para_value = "'"+para_value+"'"
        elif type(para_value) is int or type(para_value) is float:
            para_value = str(para_value)
        elif type(para_value) is list:
            para_value = str(para_value)
        
        start = self.para_s.find('\n'+para_name) + len(para_name)
        for i in range(start, len(self.para_s)):
            if self.para_s[i] == '=':
                para_start = i+1
            if self.para_s[i] == '\n':
                para_end = i
                break
        self.para_s = \
            self.para_s[:para_start]+' '+para_value+' '+self.para_s[para_end:]
        
    def update_para_with_dic(self, this_run_para):
        
        '''
        update para in ParasSet class and in the str according to a dict
        '''
        
        for para_name in this_run_para:
            self.change_para(para_name, this_run_para[para_name])
        
    def get_tune_list(self, list_tune, dic_this_para, depth):
        
        '''
        recursively list all the possible parameter combinations
        '''
        
        if depth == len(self.method_parameters):
            list_tune.append(dic_this_para.copy())
        else:
            para_name = self.method_parameters[depth]
            para_values = getattr(self,'list_'+para_name)
            
            for value in para_values:
                dic_this_para[para_name] = value
                list_tune = self.get_tune_list(
                    list_tune, dic_this_para, depth + 1)
        return list_tune
    

 