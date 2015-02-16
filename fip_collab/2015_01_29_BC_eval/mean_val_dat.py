# -*- coding: utf-8 -*-
"""
This script imports an abaqus .dat file containing all strain components, as
well as a file with an orientation matrix for each element in the .dat file,
and then calculates the mean strain for each component over all elements in 
the simulation

Noah Paulson, 2/12/2015
"""

import numpy as np
import scipy.io as sio

el = 21
#sn = 1

ori_mat = sio.loadmat('orientation_test_1.mat')['orientation']

filename = 'test_1.dat'
f = open(filename, "r")

linelist = f.readlines()

# finds a location several lines above the start of the data
# linelist[n] reads the entire line at location n
for ln in xrange(1000):
    if 'THE FOLLOWING TABLE' in linelist[ln]:
        break

# line0 is the index of first line of the data
line0 = ln + 5;      

E = np.zeros((21**3,8,6))
c = -1

# this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
for k in xrange(21**3):
    for jj in xrange(8):
        c += 1                        
        E[k,jj,:] = linelist[line0 + c].split()[3:]

f.close()    

# here we average all 8 integration points in each element cell
E = np.mean(E, axis=1)

Etot = np.zeros([el**3,6])
# here we convert the strain tensor at each location from crystal to 
# sample frame
for k in xrange(21**3):
    # E_ten_cry is the strain tensor at the spatial location of interest
    # in the crystal frame
    E_ten_cry = np.array([[    E[k,0], 0.5*E[k,3], 0.5*E[k,4]],
                          [0.5*E[k,3],     E[k,1], 0.5*E[k,5]],
                          [0.5*E[k,4], 0.5*E[k,5],     E[k,2]]])
    # Here we convert from crystal to sample frame
#    E_ten_samp = np.dot(ori_mat[:,:,k,sn].T ,np.dot(E_ten_cry,ori_mat[:,:,k,sn]))
    E_ten_samp = np.dot(ori_mat[:,:,k].T ,np.dot(E_ten_cry,ori_mat[:,:,k]))
   
         
    Etot[k,:] = [E_ten_samp[0,0],E_ten_samp[1,1],E_ten_samp[2,2],
                 E_ten_samp[0,1],E_ten_samp[1,2],E_ten_samp[1,2]]
      

print np.mean(Etot,axis = 0)
    




