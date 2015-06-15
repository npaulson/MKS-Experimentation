    # -*- coding: utf-8 -*-
"""
@author: nhpnp3
"""

import functions as rr
import numpy as np

el = 21

filename = 'Results_Ti64_Dream3D_XdirLoad_210microns_9261el_AbqInp_PowerLaw_LCF_021_data_v2_05.vtk'
r_fem = np.zeros([6, el**3])

compl = ['11', '22', '33', '12', '13', '23']
compd = {'11': 0, '22': 4, '33': 8, '12': 1, '13': 6, '23': 5}

for comp in xrange(6):

    compp = compd[compl[comp]]

    print comp 
    print compl[comp]
    print compd[compl[comp]] 

    r_temp = rr.read_vtk_tensor(filename=filename,
                                tensor_id=1,
                                comp=compp)

    r_fem[comp, ...] = r_temp

r_norm = np.sqrt(r_fem[0,...]**2 + r_fem[1,...]**2 + r_fem[2,...]**2 + \
                 2*(r_fem[3,...]**2) + 2*(r_fem[4,...]**2) + 2*(r_fem[5,...]**2))

print np.min(r_norm)
print np.max(r_norm) 