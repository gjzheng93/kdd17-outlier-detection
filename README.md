# Contextual Spatil Outlier Detection with Metric Learning

This code is written by Guanjie Zheng (gjz5038@ist.psu.edu), Penn State University. 
The code is implementing the kdd 2017 paper:

Zheng, Guanjie, Susan L. Brantley, Thomas Lauvaux, and Zhenhui Li. "Contextual spatial outlier detection with metric learning." In Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 2161-2170. ACM, 2017.

(Our code will call the metric learning part. This part (in folder MLKR1.0) is implemented by Kilian Q.Weinberger in 

Weinberger, Kilian Q., and Gerald Tesauro. "Metric Learning for Kernel Regression." AISTATS. 2007.

We modified it to facilitate our input and output. We further add robust metric learning in this program.)

## Some notes

Here are some release notes on the code:

1. The code is written under linux. We are working on to make it compatible to windows and mac os. This should be updated soon.
2. The code is written in Python 3.
3. In order to run the code, we recommend to install anaconda3. The code also requires Matlab and several python packages (xgboost, engine (from matlab)).

## Code implementation

Please go to experiment/outlier_detection/python/ to see the code.

The code has four major steps:
- "perturb.py"                generate perturbed data 
- "generate_metric.py"        call matlab script to calculate distance metric
- "run_all_exp.py"            run all experiments
- "compare.py"                output the results comparison for different methods

The major part of the models are written in the pkg folder:
- "models" folder implements all the methods. 
- "paras" folder can help you tune the parameters.

## Runing the code

Please run "bash runexp.sh" in the experiment/outlier_detection/python folder. You can change the file name in "runexp.sh" to run experiment on other datasets.

Please find the settings you want to change in experiment/outlier_detection/python/settings/. Please keep the "run_mode" as "tune_para". The other mode is only for code testing. 

## Contact us

Any question or concern, please contact Guanjie Zheng at gjz5038@ist.psu.edu.
