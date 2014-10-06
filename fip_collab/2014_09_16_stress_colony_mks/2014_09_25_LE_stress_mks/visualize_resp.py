# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 12:42:54 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

resp = np.load('r0_200cal.npy')
real_comp = 11

plt.close('all')

typ = 'sigma'


## pick a slice perpendicular to the x-direction
slc = 13
sn = 12

## Plot slices of the response
plt.figure(num=1,figsize=[12,4])

plt.subplot(122)
ax = plt.imshow(resp[slc,:,:,sn], origin='lower', interpolation='none',
    cmap='jet')
plt.colorbar(ax)
plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
 