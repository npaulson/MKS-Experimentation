# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:20:36 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

el = 21
# select the desired number of bins in the histogram
bn = 100


mined_fft = np.load("FE_results_fft_1test.npy")
mined_lin = np.absolute(np.reshape(mined_fft,el**3))/np.mean(np.absolute(mined_fft))

goali_fft = np.fft.fftn(np.load("dat2.npy"),axes=[0,1,2])
goali_lin = np.absolute(np.reshape(goali_fft,el**3))/np.mean(np.absolute(goali_fft))


plt.close()

dmin = np.amin([mined_lin,goali_lin])
dmax = 8  #np.amax([mined_lin,goali_lin])

weight = np.ones_like(mined_lin)/(mined_lin.size)

#plt.subplot(211)
#plt.plot(mined_lin[1:],'k.')
#plt.title('MINED FFT Frequencies')

n, bins, patches = plt.hist(mined_lin, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), weights=weight, color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
mined_lin, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 0.5)


#plt.subplot(212)
#plt.plot(goali_lin[1:],'k.')
#plt.title('GOALI FFT Frequencies')

n, bins, patches = plt.hist(goali_lin, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), weights=weight, color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
goali_lin, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 0.5)

plt.legend([mined_lin, goali_lin], ["MINED FFT response, C3D8", "GOALI FFT response, C3D8R"])

plt.xlabel("Normalized frequency-space strain amplitude")
plt.ylabel("Frequency of occurrence")
plt.title("Comparison of FFT frequency spectra")
