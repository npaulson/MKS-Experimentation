# -*- coding: utf-8 -*-
"""
Created on Thursday, August 14th, 2014


@author: nhpnp3
"""

import numpy as np
import functions_comparison as rr
import matplotlib.pyplot as plt
import time

comp = 'vm' # the strain component to be analyzed
cyc = 3 # the current strain cycle
st_comp = "E%s" %comp
comp_latex = "$\epsilon_{%s}$" %comp


## el is the # of elements per side of the cube 
el = 21 

# the first column of the following is LE vs alpha, the second is LE vs colony
MASE = np.zeros([8,2])
MAX_ERR = np.zeros([8,2])

for ii in xrange(8):
    SA_lvl = (ii + 1)*25 # this is the strain amplitude (SA) multiplied by 100

    for jj in xrange(2):
        
        if jj == 0:
            typ = 'alpha' # the colony type for the CPFEM study
        else:
            typ = 'colony'
    
        ## specify the file to write messages to 
        wrt_file = 'Data_E%s_cyc%s_%s_%s_%s.txt' %(comp,cyc,SA_lvl,typ,time.strftime("%Y-%m-%d_h%Hm%M"))
    
    
        ### READ DATA FROM TEXT FILE ###
        filename = '%s_%s_strain_max_C%s.txt' %(typ,SA_lvl,cyc)
        C_CPFEM = rr.file_read_vm(filename)
        
        filename = 'LE_%s_strain_max_C%s.txt' %(SA_lvl,cyc)
        C_LE = rr.file_read_vm(filename)
    
    
        (MASE[ii,jj],MAX_ERR[ii,jj]) = rr.data_gen(C_CPFEM=C_CPFEM,C_LE=C_LE,cyc=cyc,comp=comp,comp_latex=comp_latex,SA_lvl=SA_lvl,typ=typ,st_comp=st_comp,wrt_file=wrt_file)
      
#np.save('MASE',MASE)
#np.save('MAX_ERR',MAX_ERR)

#MASE = np.load('MASE.npy')
#MAX_ERR = np.load('MAX_ERR.npy')
#
#
#
#plt.close('all')
#
#
#
#plt.figure(num=1,figsize=(14,6))
#
#axis_lab = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00]
#
#alpha, = plt.plot(axis_lab, MASE[:,0], color='k', marker = 's', linestyle = '-', lw = 1.0)
#colony, = plt.plot(axis_lab, MASE[:,1], color='r', marker = 'o', linestyle = '-', lw = 1.0)
#
#plt.legend([alpha, colony], ["alpha grains","colony grains"])
#
#plt.grid(True)
#plt.xlabel("% Strain Amplitude (SA)")
#plt.ylabel("% MASE")
#plt.title("Mean Absolute Strain Error (MASE) between LE simulations and CPFEM simulations on alpha grains")
#plt.xticks([0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00])
##plt.yscale('log')
##plt.axis([0.25, 2, 0, 1000])
#plt.axis([0.25, 2, 0, 22])
#
#
#plt.figure(num=2,figsize=(14,6))
#
#axis_lab = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00]
#
#alpha, = plt.plot(axis_lab, MAX_ERR[:,0], color='k', marker = 's', linestyle = '-', lw = 1.0)
#colony, = plt.plot(axis_lab, MAX_ERR[:,1], color='r', marker = 'o', linestyle = '-', lw = 1.0)
#
#plt.legend([alpha, colony], ["alpha grains","colony grains"])
#
#plt.grid(True)
#plt.xlabel("% Strain Amplitude (SA)")
#plt.ylabel("% Maximum Error")
#plt.title("Maximum Error between LE simulations and CPFEM simulations on alpha grains")
#plt.xticks([0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00])
##plt.yscale('log')
##plt.axis([0.25, 2, 0, 1000])
#plt.axis([0.25, 2, 0, 120])



    







