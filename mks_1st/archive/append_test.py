# -*- coding: utf-8 -*-
"""
1 Dimensional MKS
Yuksel C. Yabansu
Transfered to Python by Noah Paulson
"""

import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import sys

filepath = "C:\Users\nhpnp3\Documents\Spyder Workspace\MKS\MKS1D"
if filepath not in sys.path:
    sys.path.append(filepath)
    print "path appended"
else:
    print "path present"
    
from fem1d import fem1d
#from fem1d import fem1d
#from find_independent import independent_columns
#
#plt.close()
#
## Number of data points
#ns = 10
#
## Number of elements in a data point
#el = 10
#
## Number of local states
#H = 4
#
## Microstructure functions of data points
#mf = np.zeros((ns, el, H))
#mfi_init = np.ceil(H * np.random.rand(ns, el))
#mfi = mfi_init.astype(int)
#
#for ii in range(H):
#    mf[:,:,ii] = (mfi[:,:] == (ii+1))
#m = mf
#
## Microstructure function in frequency space
#M = np.zeros((ns, el, H)) + 0j*np.zeros((ns, el, H))
#
#mtest=m
#
#for ii in range(ns):
#    for jj in range(H):
#        M[ii, :, jj] = sc.fft(np.squeeze(m[ii,:,jj]))
#
## FEM response of data points
#femresp = np.zeros((ns, el))
#
#for ii in range(ns):
#    femresp[ii, :] = fem1d(mfi[ii, :])
#    
#fftresp =  sc.fft(femresp)
#
#calibm = np.zeros((H, H, el)) + 0j*np.zeros((H, H, el));
#respfd = np.zeros((H, el)) + 0j*np.zeros((H, el));
#specinfc = np.zeros((el, H)) + 0j*np.zeros((el, H));
#
#for ii in range(el):
#    for jj in range(ns):
#        mSQ = M[jj, ii, :]
#        
#        mSQ_t = np.zeros((H, 1)) + 0j*np.zeros((H, 1))
#        for k in range(H):
#            mSQ_t[k, 0] = M[jj, ii, k]
#        
#        calibm[:, :, ii] = calibm[:, :, ii] + np.conjugate(mSQ) * mSQ_t
#        #calibm[:, :, ii] = calibm[:, :, ii] + np.conjugate(mSQ) * np.mat(mSQ).T
#        
#        respfd[:, ii] = respfd[:, ii] + (fftresp[jj, ii] * np.conjugate(mSQ))
#    
#    if ii < 2:
#        p = independent_columns(calibm[:, :, ii], .001)
#    
#    calred = calibm[0 : p[-1]+1, 0 : p[-1]+1, ii]
#    resred = respfd[0 : p[-1]+1, ii].conj().T
#    specinfc[ii, 0 : p[-1]+1] = np.linalg.solve(calred, resred)
#
## Microstructure functions of comparison data point
#mfbar = np.zeros((el, H))
#mfibar_init = np.ceil(H * np.random.rand(el))
#mfibar = np.array(mfibar_init.astype(int))
#
#for ii in range(H):
#    mfbar[:, ii] = (mfibar[:] == (ii+1))
#    
## Plotting a comparison figure
#barfem = fem1d(mfibar)
#
#mfbar_fft = sc.fft(mfbar, None, 0)
#
#finsum = np.sum(np.conjugate(specinfc) * mfbar_fft , 1)
#barmksfo = np.real(sc.ifft(finsum, None, 0))
#
#e = np.arange(.5, el+.5 , 1)
#plt.plot(e,barfem.T,'rx',e,barmksfo.T,'bx')
#plt.axis([0, 10, 0, .1])
#plt.show

