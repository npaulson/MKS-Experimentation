# -*- coding: utf-8 -*-
"""
1 Dimensional MKS
Yuksel C. Yabansu
Transfered to Python by Noah Paulson

"look git, I changed a file!"
"and I changed it again, look at that..."
"""

import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

from fem1d import fem1d
from find_independent import independent_columns

plt.clf()

# Number of samples
ns = 10
# Number of elements per sample
el = 10
# Number of local states
H = 4


## Generate the microstructure functions for all samples
mf = np.zeros((ns, el, H))
mfi_init = np.ceil(H * np.random.rand(ns, el))
mfi = mfi_init.astype(int)

for ii in range(H):
    mf[:,:,ii] = (mfi[:,:] == (ii+1))
m = mf


## Convert microstructure function to frequency space
M = np.zeros((ns, el, H),dtype = 'complex128')

mtest=m

for ii in range(ns):
    for jj in range(H):
        M[ii, :, jj] = sc.fft(np.squeeze(m[ii,:,jj]))


## FEM response of data points
femresp = np.zeros((ns, el))

for ii in range(ns):
    femresp[ii, :] = fem1d(mfi[ii, :])
    
fftresp =  sc.fft(femresp)


## Perform the calibration itself
calibm = np.zeros((H, H, el)) + 0j*np.zeros((H, H, el));
respfd = np.zeros((H, el)) + 0j*np.zeros((H, el));
specinfc = np.zeros((el, H)) + 0j*np.zeros((el, H));

for ii in range(el):
    for jj in range(ns):
        
        mSQc = np.conjugate(M[jj, ii, :])        
        mSQt = np.mat(M[jj, ii, :]).T  
        
        calibm[:, :, ii] = calibm[:, :, ii] + np.outer(mSQt,mSQc)
        
        respfd[:, ii] = respfd[:, ii] + (fftresp[jj, ii] * mSQc)
    
    if ii < 2:
        p = independent_columns(calibm[:, :, ii], .001)
    
    calred = calibm[0 : p[-1]+1, 0 : p[-1]+1, ii]
    resred = respfd[0 : p[-1]+1, ii].conj().T
    
#    if ii == 0:
#        print calred
#        print resred
#        print np.linalg.solve(calred,resred)
#        print specinfc[ii, 0 : p[-1]+1]
    specinfc[ii, 0 : p[-1]+1] = np.linalg.solve(calred, resred)


## Microstructure functions of comparison data point
mfbar = np.zeros((el, H))
mfibar_init = np.ceil(H * np.random.rand(el))
mfibar = np.array(mfibar_init.astype(int))

for ii in range(H):
    mfbar[:, ii] = (mfibar[:] == (ii+1))
    
## Plotting a comparison figure
barfem = fem1d(mfibar)

mfbar_fft = sc.fft(mfbar, None, 0)

finsum = np.sum(np.conjugate(specinfc) * mfbar_fft , 1)
barmksfo = np.real(sc.ifft(finsum, None, 0))

e = np.arange(.5, el+.5 , 1)
plt.plot(e,barfem.T,'rx',e,barmksfo.T,'bx')
plt.axis([0, 10, 0, .1])
plt.show