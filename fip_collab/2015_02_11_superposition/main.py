# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import vtk_read as vtk
import numpy as np
import time
import os
import results_view

ns_val = 50
set_id_val = 'val_equi'

H = 15
el = 21

compl = ['11','22','33','12','23','31']

for step in xrange(1,2):

    wrt_file = 'log_step%s_%s.txt' %(step,time.strftime("%Y-%m-%d_h%Hm%M"))    
        
    ## The tensorID determines the type of tensor data read from the .vtk file
    ## if tensorID == 0, we read the stress tensor        
    ## if tensorID == 1, we read the strain tensor        
    ## if tensorID == 2, we read the plastic strain tensor 
    
    tensor_ID = 1
       
    ## Gather data from validation vtk files 
    
    dir_val = 'val_equi'
        
#    for comp in compl:
#        vtk.read_meas(el,ns_val,set_id_val,step,comp,tensor_ID,dir_val,wrt_file)
#        
#        
#    for comp in compl:    
#
#        comp1dir = 'xload'        
#            
#        nwd = os.getcwd() + '\\' + comp1dir    
#        os.chdir(nwd)
#    
#        c1 = np.load('mksR%s_%s%s_s%s.npy' %(comp,ns_val,set_id_val,step))    
#    
#        os.chdir('..')
#    
#    
#        comp2dir = 'yload'        
#            
#        nwd = os.getcwd() + '\\' + comp2dir    
#        os.chdir(nwd)
#    
#        c2 = np.load('mksR%s_%s%s_s%s.npy' %(comp,ns_val,set_id_val,step))    
#    
#        os.chdir('..')
#
#        np.save('mksR%s_%s%s_s%s.npy' %(comp,ns_val,set_id_val,step), c1+c2)
             
        
    comp_app = 1;
    
    results_view.results(el,ns_val,set_id_val,step,'33','epsilon')

