# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 15:59:12 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

preMM = np.load('preMM2.npy')
shp = preMM.shape
print shp

blk_sz = 10

ht = np.floor(shp[0]/blk_sz).astype('int32')
print 'ht: %s' %ht
wd = np.floor(shp[1]/blk_sz).astype('int32')
print 'wd: %s' %wd

pixelize = np.zeros([ht-1,wd-1])

# here we take an average over a square (with a side specified by blk_sz)
# and put it into a new cell in pixelize
for h in xrange(1,ht-1):
    if h % 100 == 0:   
        print 'h: %s' %h
    for w in xrange(1,wd-1):
        # ht_lb and wd_lb are the lower bounds of the location of the square
        # which is averaged over in preMM
        # ht_ub and wd_ub are the upper bounds
        ht_lb = h*blk_sz
        ht_ub = ht_lb + blk_sz
        wd_lb = w*blk_sz
        wd_ub = wd_lb + blk_sz
#        print 'ht_lb:%s ht_ub:%s wd_lb:%s wd_ub:%s' %(ht_lb,ht_ub,wd_lb,wd_ub)
        blk = preMM[ht_lb:ht_ub, wd_lb:wd_ub]
#        print blk
        pixelize[h,w] = np.average(blk)

plt.close()

plt.subplot(121)
ax = plt.imshow(pixelize[1:,1:(wd/2)], origin='lower', interpolation='none',
    cmap='binary')
plt.colorbar(ax)

plt.subplot(122)
ax = plt.imshow(pixelize[1:,((wd/2)+1):], origin='lower', interpolation='none',
    cmap='binary')
plt.colorbar(ax)