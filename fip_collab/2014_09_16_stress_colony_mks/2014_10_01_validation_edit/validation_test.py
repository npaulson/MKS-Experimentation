# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import time
import validation
import results

wrt_file = 'log_%s.txt' %time.strftime("%Y-%m-%d_h%Hm%M")

ns_cal = 200
set_id_cal = 'cal'

ns_val = 50
set_id_val = 'val'

comp = 0
   
   
## Perform the validation
validation.validation_procedure(ns_cal,ns_val,set_id_cal,set_id_val,comp,wrt_file)
    
results.results_comp(ns_val,set_id_val,comp,'sigma')

