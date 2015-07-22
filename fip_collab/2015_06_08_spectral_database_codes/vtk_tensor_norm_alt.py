# -*- coding: utf-8 -*-
"""
@author: nhpnp3
"""

import functions as rr
import numpy as np
import os

el = 21
ns = 101


r_fem = np.zeros([6, ns, el**3])

compl = ['11', '22', '33', ' 12', '13', '23']
compd = {'11': 0, '22': 4, '33': 8, '12': 1, '13': 6, '23': 5}

for comp in xrange(6):

    print comp

    compp = compd[compl[comp]]

    cwd = os.getcwd()

    sn = 0
    for filename in os.listdir(cwd):
        if filename.endswith('.vtk'):
            r_temp = rr.read_vtk_tensor(filename=filename,
                                        tensor_id=1,
                                        comp=compp)
            r_fem[comp, sn, ...] = r_temp
            sn += 1

            print sn

print r_fem.nbytes

r_norm = np.sqrt(r_fem[0, ...]**2 +
                 r_fem[1, ...]**2 +
                 r_fem[2, ...]**2 +
                 2*(r_fem[3, ...]**2) +
                 2*(r_fem[4, ...]**2) +
                 2*(r_fem[5, ...]**2))

print np.mean(r_norm)
print np.min(r_norm)
print np.std(r_norm)
print np.max(r_norm)
