# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

#import vtk_read as vtk
import time
#import euler_to_gsh as gsh
#import microstructure_function as msf
import validation_viz
import results_field
import matplotlib.pyplot as plt

plt.close('all')

ns_cal = 200
set_id_cal = 'cal'

ns_val = 1
set_id_val = 'val25el'

# el: # elements per side of the validation microstructure
el = 25


for step in xrange(1,2):

    wrt_file = 'log_step%s_%s.txt' %(step,time.strftime("%Y-%m-%d_h%Hm%M"))
    
#    vtk_filename = 'Results_Ti64_RandomMicroFZfinal_%sx%sx%s_AbqInp_PowerLaw_%s_data_v2_0%s.vtk' %(el,el,el,'%s',step)
#    
#    ## The tensorID determines the type of tensor data read from the .vtk file
#    ## if tensorID == 0, we read the stress tensor        
#    ## if tensorID == 1, we read the strain tensor        
#    ## if tensorID == 2, we read the plastic strain tensor 
#    
#    tensor_ID = 0
#    
#    if step == 1:
#        
#        ## Gather euler angles from validation vtk files 
#        vtk.read_euler(el,ns_val,set_id_val,vtk_filename, wrt_file)
#        
#        ## Convert the orientations from the validation datasets from bunge euler angles
#        ## to GSH coefficients
#        gsh.euler_to_gsh(el,ns_val,set_id_val,wrt_file)
#        
#        ## Generate the fftn of the validation microstructure function
#        msf.micr_func(el,ns_val,set_id_val,wrt_file)    
#    
#    
#    ## get field of interest from vtk file
#    for comp in xrange(9):
#        vtk.read_meas(el,ns_val,set_id_val,step,comp,vtk_filename, tensor_ID, wrt_file)
#       
#    ## Perform the validation
#    for comp in xrange(9):
#        validation.validation_zero_pad(el,ns_cal,ns_val,set_id_cal,set_id_val,step,comp,wrt_file)

    ## Perform the validation
    
    comp = 0     
    validation_viz.validation_zero_pad(el,ns_cal,ns_val,set_id_cal,set_id_val,step,comp,wrt_file)
    
    results_field.results(el, ns_val,set_id_val,step,comp,'sigma')
        