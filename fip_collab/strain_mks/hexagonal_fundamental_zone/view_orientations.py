# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script evaluates the success of a given MKS calibration and validation
through metrics like MASE and maximum error as well as plotting strain
fields and histograms.

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

set_id = 'Comparo_C2maxStress33'

## specify the file to write messages to 
wrt_file = '%s_%s.txt' %(set_id,time.strftime("%Y-%m-%d_h%Hm%M"))


## el is the # of elements per side of the cube 
el = 21 


### READ DATA FROM TEXT FILE ###

def file_read(filename):
    
    f = open(filename, "r")
    
    linelist = f.readlines()
    
    # line0 is the index of first line of the data
    line0 = 2;      
    
    euler = np.zeros((21**3,3))
    c = -1
    
    ## This reads through all the lines in the file.
     
    for k in xrange(21**3):
        c += 1                        
        euler[k,:] = linelist[line0 + c].split()[1:4]
    
    f.close()    
         
    return euler


filename = 'Ti64_RandomMicro_21x21x21_EulerAngles_FundZoneZeroPhi2_00200.txt'
euler = file_read(filename)

fig = plt.figure()
ax3D = fig.add_subplot(111, projection='3d')
p3d = ax3D.scatter(euler[:500,0],euler[:500,1],euler[:500,2])

