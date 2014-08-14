# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:20:36 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

el = 21
# select the desired number of bins in the histogram
bn = 400


field_pr = np.load("E11_fft_5bc_test.npy")
lin_field_pr = np.absolute(np.reshape(field_pr,5*el**3)[100:])/np.mean(np.absolute(field_pr))

field_ya = np.load("FE_results_fft_200cal.npy")
lin_field_ya = np.absolute(np.reshape(field_ya[:,:,:,:5],5*el**3)[100:])/np.mean(np.absolute(field_ya[:,:,:,:5]))

dmin = np.amin([lin_field_pr,lin_field_ya])
dmax = np.amax([lin_field_pr,lin_field_ya])



plt.close()

#plt.subplot(211)
#plt.plot(lin_field_pr[1:],'k.')
#plt.title('Response with unstable BCs: real space')

n, bins, patches = plt.hist(lin_field_pr, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
lin_field_pr, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 0.5)


#plt.subplot(212)
#plt.plot(lin_field_ya[1:],'k.')
#plt.title('Response with stable BCs: real space')

n, bins, patches = plt.hist(lin_field_ya, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
lin_field_ya, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 0.5)

plt.legend([lin_field_pr, lin_field_ya], ["Periodic BCs, GOALI", "Periodic BCs, MINED"])

plt.xlabel("Normalized frequency-space strain amplitude")
plt.ylabel("Frequency of occurrence")
plt.title("Comparison of frequency spectra to identify boundary condition problems")
