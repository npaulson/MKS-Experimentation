# -*- coding: utf-8 -*-
"""
Created on Mon Apr 07 15:19:39 2014

Trying to generate additional terms to represent seventh order microstructure
descriptors.

3-D case

@author: nhpnp3
"""

import numpy as np
import itertools as it

## MICROSTRUCTURE GENERATION ##
el = 3
ns = 2
micr = np.round(np.random.rand(el, el, el, ns))

## BASELINE MICROSTRUCTURE FUNCTION GENERATION ##

pm = np.zeros([el,el,el,ns,2])
pm[:,:,:,:,0] = (micr == 0)
pm[:,:,:,:,1] = (micr == 1)
pm = pm.astype(int)

hs = np.array(list(it.product([0,1],repeat=7)))
vec = np.array([[1,0],[1,1],[1,2],[-1,0],[-1,1],[-1,2]])

# H is the # of conformations of location and phase
H = len(hs[:,0])
m = np.zeros([el,el,el,ns,H])

for hh in xrange(H):
    
    a1 = pm[:,:,:,:,hs[hh,0]]    
    pre_m = a1
    
    for t in xrange(len(vec[:,0])):
        
        a_n = np.roll(pm[:,:,:,:,hs[hh,t+1]],vec[t,0],vec[t,1])
        pre_m = pre_m * a_n
    
    m[:,:,:,:,hh] = pre_m

m = m.astype(int)


## VALIDATION ##

# for each index in the microstructure function we output the arrangement
# of local states we are looking for and the locations of those local states
# in the slice
for k in xrange(H):
    print k
    print '\nlocal state and confirmation on middle slice'
    print hs[k,:]
    print m[:,:,:,0,k]
    print '\nmicrostructure'    
    print pm[:,:,:,0,1]
    print '\n\n'

print '\ncheck that every location is associated with a specific local state\n' 
print np.sum(m[:,:,:,0,:],axis = 3)