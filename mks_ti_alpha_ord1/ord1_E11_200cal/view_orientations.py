# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np
import time
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


filename1 = 'extremeorientv_hexa.mat'
filename2 = 'orientation2.mat'

el = 21
ns = 50


start = time.time()

## convert the matlab files arrays in python        

micr_flag_BASE = sio.loadmat(filename2)
## micr_flag contains 9261 flags for each sample microsturcture,
## each representing an orientation. The number in these flags
## corresponds with an orientation in ex_ori_fr
micr_flag = micr_flag_BASE['ct']         

ex_ori_BASE = sio.loadmat(filename1)    
## ex_ori_fr contains 522 sets of 15 GSH coefficients, where each 
## set corresponds with an orientation on the surface of the
## hexagonal-triclinic fundamental zone.        
ex_ori = ex_ori_BASE['extremeorienth']  
       
euler = np.zeros((el**3,ns,3))
for k in range(el**3):
    for n in range(ns):
        euler[k,n,:] = ex_ori[micr_flag[k,n]-1,:]

sn=25
max = 500

fig = plt.figure()
ax3D = fig.add_subplot(111, projection='3d')
p3d = ax3D.scatter(euler[:max,sn,0],euler[:max,sn,1],euler[:max,sn,2])
