# -*- coding: utf-8 -*-
"""
Created on Tue Oct 07 15:51:43 2014

@author: nhpnp3
"""

import numpy as np

el = 39


filename = 'Results_Ti64_RandomMicroFZfinal_39x39x39_AbqInp_PowerLaw_00002_data_stress_max_C1.txt'



def read_odb_txt(filename,el):

    f = open(filename, "r")

    linelist = f.readlines()
    
    # line0 is the index of first line of the data
    line0 = 2   

    intnum = 9
    pre_resp = np.zeros([el**3,intnum,6])
    c = 0

    # this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
    for k in xrange(el**3):
        for jj in xrange(intnum):                     
            pre_resp[k,jj,:] = linelist[line0].split()[1:]
            line0 += 1 
    
    f.close()    
    
    # here we average all 8 integration points in each element cell
    pre_resp = np.mean(pre_resp, axis=1)
    
    
    # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix       
    resp = np.zeros([el,el,el,7])
    for c in xrange(6):    
        resp[:,:,:,c] = np.swapaxes(np.reshape(np.flipud(pre_resp[:,c]), [el,el,el]),1,2)

    return resp
    
resp = read_odb_txt(filename,el)

resp[:,:,:,6] = np.sqrt(0.5*((resp[:,:,:,0] - resp[:,:,:,1])**2 + (resp[:,:,:,1] - resp[:,:,:,2])**2 + (resp[:,:,:,2] - resp[:,:,:,0])**2 + 6*(resp[:,:,:,3]**2 + resp[:,:,:,4]**2 + resp[:,:,:,5]**2)))


# write to vtk file    

from pyevtk.hl import gridToVTK    

maxx = maxy = maxz = el + 1
x = np.arange(0, maxx, 1, dtype='float64')
y = np.arange(0, maxy, 1, dtype='float64') 
z = np.arange(0, maxz, 1, dtype='float64')

gridToVTK("testvtk2", x, y, z, cellData = {"stress11" : resp[:,:,:,0], "stressVM" : resp[:,:,:,6]})