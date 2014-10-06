# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script performs the MKS calibration given the microstructure function 
and the FIP response, both in frequency space.

@author: nhpnp3
"""

import time
import numpy as np
import functions_polycrystal as rr
from functools import partial


def calibration_procedure(ns_cal,ns,set_id,step,comp,wrt_file):

    ## el is the # of elements per side of the cube 
    el = 21 
    ## specify the number of local states you are using
    H = 15
    
    M = np.load('M_%s%s.npy' %(ns_cal,set_id))
    r_fft = np.load('r%s_fft_%s%s_s%s.npy' %(comp,ns_cal,set_id,step))
    
    start = time.time()
    
    specinfc = np.zeros((el**3,H),dtype = 'complex64')
    
    ## here we perform the calibration for the scalar FIP
    
    specinfc[0,:] = rr.calib(0,M,r_fft,0,H,el,ns)
    [specinfc[1,:],p] = rr.calib(1,M,r_fft,0,H,el,ns)
    
    ## calib_red is simply calib with some default arguments
    calib_red = partial(rr.calib,M=M,r_fft=r_fft,
                        p=p,H=H,el=el,ns=ns)
    specinfc[2:(el**3),:] = np.asarray(map(calib_red,range(2,el**3)))
     
    
    np.save('specinfc%s_%s%s_s%s' %(comp,ns,set_id,step),specinfc)
    
    end = time.time()
    timeE = np.round((end - start),3)
    msg = 'Calibration, component %s, %s samples: %s seconds' %(comp, ns, timeE)
    rr.WP(msg,wrt_file)