# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 09:18:00 2014

@author: nhpnp3
"""

import functions_ti_alpha_fip_v1 as rr
import numpy as np
import time

def strain_freq(Ecomp, ns, set_id):
## ns: the number of sample microstructures for calibration.
## set_id: specify the set designation (string format)

    ## specify the file to write messages to 
    wrt_file = 'Efreq_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 
    
    ## responses in frequency space
    start = time.time()
    E11_fft = np.fft.fftn(Ecomp, axes = [0,1,2]) 
    np.save('E11_fft_%s%s' %(ns,set_id),E11_fft)  
    end = time.time()
    timeE = np.round((end - start),3)
    
    msg = 'Convert calibration FIP results to frequency space: %s seconds' %timeE
    rr.WP(msg,wrt_file)