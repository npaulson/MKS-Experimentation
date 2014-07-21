# -*- coding: utf-8 -*-
"""
Created on Fri May 16 08:46:15 2014

@author: nhpnp3
"""

import numpy as np
import time

### generate R

R = np.random.rand(1000,5000)


### save R in '.npy' format
start = time.time()
np.save('R',R)
end = time.time()
timeE = np.round((end - start),5)
print "time to save R in '.npy' format : %s seconds" % timeE


### Load total R array
start = time.time()
R = np.load('R.npy')
end = time.time()
timeE = np.round((end - start),5)
print 'loading total R: %s seconds' % timeE


### Save each row of R in '.npy' format
start = time.time()
for ii in range(len(R[:,0])):
    filename = 'R_%s' % ii    
    np.save(filename,R[ii,:])    
end = time.time()
timeE = np.round((end - start),5)
print "time to save each row in '.npy' format: %s seconds" % timeE


### Save each row of R into 'R_append.npy' by appending each line
start = time.time()
np.save('R_append',R[0,:])
for ii in range(1,len(R[:,0])):    
    R_append = np.load('R_append.npy')
    R_append = np.append(R_append,R[ii,:],axis = 0)    
    np.save('R_append',R_append)    
end = time.time()
timeE = np.round((end - start),5)
print "time to append each row of R to R_append: %s seconds" % timeE    


### Save each row of R in '.txt' format
start = time.time()
for ii in range(len(R[:,0])):
    filename = 'R_%s' % ii    
    np.savetxt(filename,R[ii,:])    
end = time.time()
timeE = np.round((end - start),5)
print "time to save each row in '.txt' format: %s seconds" % timeE

