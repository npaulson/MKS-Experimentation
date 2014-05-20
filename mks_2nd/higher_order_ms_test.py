# -*- coding: utf-8 -*-
"""
Created on Mon Apr 07 15:19:39 2014

Trying to generate additional terms to represent second order microstructure
descriptors.

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

el = 3
ns = 2

micr = np.round(np.random.rand(el, el, el, ns))


## NEW METHOD ##
# 4/10/14: this method appears to be working perfectly at this point. Yuksel
# showed this algorithm to me.

# Generate the microstructure function
pm = np.zeros([el,el,el,ns,2])
pm[:,:,:,:,0] = (micr == 0)
pm[:,:,:,:,1] = (micr == 1)
pm = pm.astype(int)

hs = np.array([[1,0],[0,1],[0,0],[1,1]])
vec = np.array([[1,0],[1,1],[1,2],[-1,0],[-1,1],[-1,2]])

k = 0 
m = np.zeros([el,el,el,ns, len(hs[:,0]) * len(vec[:,0]) ])
m = m.astype(int)
for hh in xrange(len(hs[:,0])):
    for t in xrange(len(vec[:,0])):
        a1 = pm[:,:,:,:,hs[hh,0]]
        a2 = np.roll(pm[:,:,:,:,hs[hh,1]],vec[t,0],vec[t,1])
        m[:,:,:,:,k] = a1 * a2
        
#        print "phase arrangement: %s" %hs[hh,:]
#        print "roll increment and direction: %s" %vec[t,:] 
#        print a1[0,:,:,0]
#        print a2[0,:,:,0]
#        print m[0,:,:,0,k]        
        
        k = k + 1
                
m = m.astype(int)

## OLD METHOD (WORKING) ##
# 4/9/14: This is functional, but I think I'll switch to the method above for 
# user friendliness and to get help in debugging from Yuksel 
c = 0
PM = np.zeros([el,el,el,2,6])
for hh in range(2):
    for ii in range(3):              
        if hh == 0:
            PM[:,:,:,:,c] = np.roll(micr,1,ii)
            c = c + 1
        if hh == 1:
            PM[:,:,:,:,c] = np.roll(micr,-1,ii)
            c = c + 1

k = 0
M = np.zeros([el,el,el,2,24])
for u in range(len(PM[0,0,0,0,:])):
    for v in range(2):
        for w in range(2):
            M[:,:,:,:,k] = (micr == v) * (PM[:,:,:,:,u] == w)            
            k = k + 1

M = M.astype(int)            


# 4/10/14: I used the following four lines to check that every single 3d array
# from the old second order microstructure function generator matched only 
# one from the new one. This test was successful, so I am completely confident
# in the results.
ReaR = np.zeros([24])
for ii in xrange(24):    
    for jj in xrange(24):
        if np.array_equal(M[:,:,:,:,ii],m[:,:,:,:,jj]) == True:
            ReaR[ii]=jj            
            print "M%s == m%s" %(ii,jj)


lm = np.zeros([el,el,el,ns, len(hs[:,0]) * len(vec[:,0]) ])
lm = lm.astype(int) 
for k in xrange(24):
    lm[:,:,:,:,ReaR[k]] = m[:,:,:,:,k]
    print k
    print lm[2,:,:,0,ReaR[k]]
    print m[2,:,:,0,k]




## VALIDATION ##

#slc = 1
#
##print pm[slc,:,:,0,0]
#rollpm = np.roll(pm[:,:,:,0,0],1,2)
##print rollpm[slc,:,:]
##print m[slc,:,:,0,14]
#
#plt.close()
#
#plt.subplot(131)
#ax = plt.imshow(pm[slc,:,:,0,0], interpolation='none', cmap='binary')
#plt.colorbar(ax)
#plt.title('original')
#
#plt.subplot(132)
#ax = plt.imshow(rollpm[slc,:,:], interpolation='none', cmap='binary')
#plt.colorbar(ax)
#plt.title('shifted')
#
#plt.subplot(133)
#ax = plt.imshow(m[slc,:,:,0,13], interpolation='none', cmap='binary')
#plt.colorbar(ax)
#plt.title('multiplied')

# NOTE: I was initially confused because the roll direction didn't seem to
# match what I was seeing in my roll_test.py script. I asked David B., and 
# he rightly suggested that this inconsistency traced back to the way
# the graphs were being plotted.





