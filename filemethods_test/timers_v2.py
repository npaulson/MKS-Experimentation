# -*- coding: utf-8 -*-
"""
Created on Fri May 16 08:46:15 2014

@author: nhpnp3
"""

import numpy as np
import time

### generate R

R = np.random.rand(1000,5000)

ns = 1000
H = 5000

### Save each row of R in '.npy' format
start = time.time()
for ii in range(ns):
    R = np.random.rand(1,H) 
    filename = 'R_%s' % ii    
    np.save(filename,R)    
end = time.time()
timeE = np.round((end - start),5)
print "time to save each row in '.npy' format: %s seconds" % timeE


### Save each row of R into 'R_append.npy' by appending each line
start = time.time()
R = np.random.rand(1,H) 
np.save('R_append',R)
for ii in range(1,ns):    
    R_append = np.load('R_append.npy')
    R = np.random.rand(1,H) 
    R_append = np.append(R_append,R,axis = 0)    
    np.save('R_append',R_append)    
end = time.time()
timeE = np.round((end - start),5)
print "time to append each row of R to R_append: %s seconds" % timeE    


### Load each row of R from the individual files
start = time.time()
R_fin = np.load('R_0.npy')
for ii in range(1,ns):
    filename = 'R_%s.npy' % ii    
    R_sub = np.load(filename)
    R_fin = np.append(R_fin,R_sub,axis = 0)    
end = time.time()
timeE = np.round((end - start),5)
print "time to load each row in '.npy' format: %s seconds" % timeE

print R_fin.shape

#### Save each row of R in '.txt' format
#start = time.time()
#for ii in range(ns):
#    filename = 'R_%s' % ii    
#    R = np.random.rand(1,H) 
#    np.savetxt(filename,R)    
#end = time.time()
#timeE = np.round((end - start),5)
#print "time to save each row in '.txt' format: %s seconds" % timeE
