# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:20:36 2014

@author: nhpnp3
"""

import numpy as np

## el is the # of elements per side of the cube 
el = 21 



### READ DATA FROM TEXT FILE ###
def file_read(filename):
    
    f = open(filename, "r")
    
    linelist = f.readlines()
    
    # line0 is the index of first line of the data
    line0 = 2;      
    
    resp = np.zeros((21**3,6))
    c = -1
    
    ## This reads through all the lines in the file.
     
    for k in xrange(21**3):
        c += 1                        
        resp[k,:] = linelist[line0 + c].split()[1:7]
    
    f.close()    
         
    return resp



filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_AnisoLE_00001_data_strain_max_C1.txt'
resp = file_read(filename)


print np.mean(resp, axis = 0)


field_ya = np.load("FE_results_200cal.npy")

means = np.zeros(6)
for comp in xrange(6):
    means[comp] = np.mean(field_ya[:,:,:,comp,:])

print means


