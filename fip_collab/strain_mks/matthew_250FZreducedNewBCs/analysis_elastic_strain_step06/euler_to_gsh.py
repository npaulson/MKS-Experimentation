# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import GSH_func as gsh
#import scipy.io as sio

ns = 50
el = 21
set_id = 'val'

euler = np.load('euler_%s%s.npy' %(ns,set_id))

euler_GSH = np.zeros([el**3,ns,15], dtype= 'complex128')

for sn in range(ns):
    for k in range(el**3):
        euler_GSH[k,sn,:] = gsh.GSH_Hexagonal_Triclinic(euler[k,sn,:])
    print sn

np.save('euler_GSH_%s%s.npy' %(ns,set_id),euler_GSH)


### Let us compare this result to the matlab result:
#
#euler_GSH_matlab = sio.loadmat('euler_GSH_%s%s.mat' %(ns,set_id))['euler_GSH']
#euler_GSH = np.load('euler_GSH_%s%s.npy' %(ns,set_id))
#
#print np.sum(np.absolute(euler_GSH_matlab - euler_GSH))




#euler = np.load('euler_%s%s.npy' %(ns,set_id))
#
#euler_GSH = np.zeros([el**3,ns,10], dtype= 'complex128')
#
#for sn in range(ns):
#    for k in range(el**3):
#        euler_GSH[k,sn,:] = gsh.GSH_Cubic_Triclinic(euler[k,sn,0],euler[k,sn,1],euler[k,sn,2])
#    print sn
#
#np.save('euler_GSH_%s%s.npy' %(ns,set_id),euler_GSH)
#
#
### Let us compare this result to the matlab result:
#
#euler_GSH_matlab = sio.loadmat('euler_cubic_GSH_%s%s.mat' %(ns,set_id))['euler_GSH']
#euler_GSH = np.load('euler_GSH_%s%s.npy' %(ns,set_id))
#
#print np.sum(np.absolute(euler_GSH_matlab - euler_GSH))
