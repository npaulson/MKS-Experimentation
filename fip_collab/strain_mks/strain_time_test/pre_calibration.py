# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions_ti_alpha_beta as rr
import GSH_func as gsh
import numpy as np
import sys
import time

## el is the # of elements per side of the cube 
el = 21

def vtk_read(sn_ini, ns, set_id):
## ns: the number of sample microstructures for calibration.
## set_id: specify the set designation (string format)
       
    E11 = np.zeros([el,el,el,ns])
    euler_GSH = np.zeros([el**3,ns,15], dtype= 'complex128') 
    
    for sn in xrange(sn_ini, sn_ini + ns):
        l_sn = str(sn+1).zfill(5)  
        [euler,E11_temp] = rr.read_vtk('Results_Ti64_RandomMicroFZreduced_21x21x21_AbqInp_PowerLaw_%s_data_v2_06.vtk' %l_sn)
        
        for k in range(el**3):
            euler_GSH[k,sn,:] = gsh.GSH_Hexagonal_Triclinic(euler[k,:])
            
        E11[:,:,:,sn] = np.swapaxes(np.reshape
                            (np.flipud(E11_temp), [el,el,el]),1,2)        

    np.save('E11_%s-%s%s' %(sn_ini,ns,set_id), E11)
    np.save('euler_GSH_%s-%s%s' %(sn_ini,ns,set_id),euler_GSH)
         
    
def micr_func(sn_ini, ns, set_id):

    ## specify the number of local states you are using
    H = 15   
    
    ## import microstructures
    micr = np.zeros([el,el,el,ns,H], dtype = 'complex128')
    euler_GSH = np.load('euler_GSH_%s-%s%s.npy' %(sn_ini,ns,set_id))
    for h in xrange(H):
        for sn in xrange(sn_ini, sn_ini + ns):
            micr[:,:,:,sn,h] = np.swapaxes(np.reshape(np.flipud
                                    (euler_GSH[:,sn,h]), [el,el,el]),1,2)
    
#    msg = 'microstructures imported'
#    rr.WP(msg,wrt_file)
    
    ## Microstructure functions in frequency space
    M = np.fft.fftn(micr, axes = [0,1,2])
    np.save('M_%s-%s%s' %(sn_ini,ns,set_id),M)

    
if __name__ == "__main__":
    
    sn_ini = sys.argv[1]
    ns = sys.argv[2]
    set_id = sys.argv[3]

    ## specify the file to write messages to 
    wrt_file = 'vtk_%s-%s_%s_%s.txt' %(sn_ini,ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 

    vtk_read(sn_ini,ns,set_id)
    micr_func(sn_ini,ns,set_id)
    
    
    

    
    
    


