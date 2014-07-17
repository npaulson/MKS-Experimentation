# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions_ti_alpha_fip_v1 as rr
import numpy as np
import scipy.io as sio
import sys

def vtk_read(sn_ini, ns, set_id):
## ns: the number of sample microstructures for calibration.
## set_id: specify the set designation (string format)

    ## el is the # of elements per side of the cube 
    el = 21
    ## specify the file to write messages to 
#    wrt_file = 'vtk_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 
    
    euler = np.zeros([el**3,ns,3])
    E11 = np.zeros([el,el,el,ns])
    
    for sn in xrange(sn_ini, sn_ini + ns):
        l_sn = str(sn+1).zfill(5)  
        [euler_temp,E11_temp] = rr.read_vtk('Results_Ti64_RandomMicroFZreduced_21x21x21_AbqInp_PowerLaw_%s_data_v2_06.vtk' %l_sn)
        euler[:,sn,:] = euler_temp
        E11[:,:,:,sn] = np.swapaxes(np.reshape
                            (np.flipud(E11_temp), [el,el,el]),1,2)
        
    #np.save('euler_%s%s' %(ns,set_id), euler)
    sio.savemat('euler_%s-%s%s' %(sn_ini,ns,set_id), {'euler':euler})
    np.save('E11_%s-%s%s' %(sn_ini,ns,set_id), E11)
    
    
if __name__ == "__main__":

    sn_ini = sys.argv[1]
    ns = sys.argv[2]
    set_id = sys.argv[3]
    
    vtk_read(sn_ini,ns,set_id)
    
    

    
    
    


