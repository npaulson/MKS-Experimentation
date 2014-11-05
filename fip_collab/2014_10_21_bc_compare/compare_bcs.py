# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import vtk_read as vtk
import time
import results
import matplotlib.pyplot as plt
import numpy as np
import functions_polycrystal as rr

plt.close('all')

el = 21
ns = 1
set_id_new = 'new'
set_id_old = 'old'
step = 1

wrt_file = 'log_%s.txt' %time.strftime("%Y-%m-%d_h%Hm%M")

vtk_filename_new = 'Results_Ti64_RandomMicroFZfinal_21x21x21_AbqInp_PowerLaw_%s_data_v2_0%s.vtk' %('%s',step)
vtk_filename_old = 'Results_Ti64_RandomMicroFZfinal_21x21x21_AbqInp_PowerLaw_%s_data_v2_0%s_old.vtk' %('%s',step)


## The tensorID determines the type of tensor data read from the .vtk file
## if tensorID == 0, we read the stress tensor        
## if tensorID == 1, we read the strain tensor        
## if tensorID == 2, we read the plastic strain tensor 

tensor_ID = 0  

## get field of interest from vtk file
for comp in xrange(9):
    vtk.read_meas(el,ns,set_id_old,step,comp,vtk_filename_old, tensor_ID, wrt_file)
    vtk.read_meas(el,ns,set_id_new,step,comp,vtk_filename_new, tensor_ID, wrt_file)
    
results.results_all(el,ns,set_id_old,set_id_new,step,'sigma')
    