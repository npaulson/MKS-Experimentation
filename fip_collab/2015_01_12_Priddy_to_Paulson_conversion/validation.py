# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script predicts the FE response of a set of microstructures designated by
a specific set-ID using a previously calibrated MKS

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
#import matplotlib.pyplot as plt



def validation(el,ns_cal,ns_val,H,set_id_cal,set_id_val,wrt_file):

    start = time.time()

    ## perform the prediction procedure    
    specinfc = np.load('specinfc_%s%s.npy' %(ns_cal,set_id_cal)).reshape(H,el,el,el)    
    
    M = np.load('M_%s%s.npy' %(ns_val,set_id_val))
    tmp = np.sum(np.conjugate(specinfc) * M,1)    
    mks_R = np.fft.ifftn(tmp,[el,el,el],[1,2,3]).real
    
    np.save('mksR_%s%s' %(ns_val,set_id_val), mks_R)

    end = time.time()
    timeE = np.round((end - start),3)

    msg = 'validation performed: %s seconds' %timeE
    rr.WP(msg,wrt_file)

