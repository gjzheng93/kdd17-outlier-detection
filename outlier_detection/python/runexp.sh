#!/bin/bash

python -O perturb.py settings_elnino.conf
python -O generate_metric.py settings_elnino.conf
python -O run_all_exp.py settings_elnino.conf
